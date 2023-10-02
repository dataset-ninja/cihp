import supervisely as sly
import os
import numpy as np
from dataset_tools.convert import unpack_if_archive
import src.settings as s
from urllib.parse import unquote, urlparse
from supervisely.io.fs import get_file_name, dir_exists

from tqdm import tqdm


def download_dataset(teamfiles_dir: str) -> str:
    """Use it for large datasets to convert them on the instance"""
    api = sly.Api.from_env()
    team_id = sly.env.team_id()
    storage_dir = sly.app.get_data_dir()

    if isinstance(s.DOWNLOAD_ORIGINAL_URL, str):
        parsed_url = urlparse(s.DOWNLOAD_ORIGINAL_URL)
        file_name_with_ext = os.path.basename(parsed_url.path)
        file_name_with_ext = unquote(file_name_with_ext)

        sly.logger.info(f"Start unpacking archive '{file_name_with_ext}'...")
        local_path = os.path.join(storage_dir, file_name_with_ext)
        teamfiles_path = os.path.join(teamfiles_dir, file_name_with_ext)

        fsize = api.file.get_directory_size(team_id, teamfiles_dir)
        with tqdm(
            desc=f"Downloading '{file_name_with_ext}' to buffer...",
            total=fsize,
            unit="B",
            unit_scale=True,
        ) as pbar:
            api.file.download(team_id, teamfiles_path, local_path, progress_cb=pbar)
        dataset_path = unpack_if_archive(local_path)

    if isinstance(s.DOWNLOAD_ORIGINAL_URL, dict):
        for file_name_with_ext, url in s.DOWNLOAD_ORIGINAL_URL.items():
            local_path = os.path.join(storage_dir, file_name_with_ext)
            teamfiles_path = os.path.join(teamfiles_dir, file_name_with_ext)

            if not os.path.exists(get_file_name(local_path)):
                fsize = api.file.get_directory_size(team_id, teamfiles_dir)
                with tqdm(
                    desc=f"Downloading '{file_name_with_ext}' to buffer...",
                    total=fsize,
                    unit="B",
                    unit_scale=True,
                ) as pbar:
                    api.file.download(
                        team_id, teamfiles_path, local_path, progress_cb=pbar
                    )

                sly.logger.info(f"Start unpacking archive '{file_name_with_ext}'...")
                unpack_if_archive(local_path)
            else:
                sly.logger.info(
                    f"Archive '{file_name_with_ext}' was already unpacked to '{os.path.join(storage_dir, get_file_name(file_name_with_ext))}'. Skipping..."
                )

        dataset_path = storage_dir
    return dataset_path


def count_files(path, extension):
    count = 0
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(extension):
                count += 1
    return count


def convert_and_upload_supervisely_project(
    api: sly.Api, workspace_id: int, project_name: str
) -> sly.ProjectInfo:
    ### Function should read local dataset and upload it to Supervisely project, then return project info.###
    dataset_path = (
        "CCIHP_icip\instance-level_human_parsing\instance-level_human_parsing"
    )

    images_folder = "Images"
    humans_folder = "Human_ids"
    instances_folder = "Instances"
    categories_folder = "Category_ids"
    batch_size = 50
    masks_ext = ".png"

    def get_unique_colors(img):
        unique_colors = []
        img = img.astype(np.int32)
        h, w = img.shape[:2]
        colhash = img[:, :, 0] * 256 * 256 + img[:, :, 1] * 256 + img[:, :, 2]
        unq, unq_inv, unq_cnt = np.unique(
            colhash, return_inverse=True, return_counts=True
        )
        indxs = np.split(np.argsort(unq_inv), np.cumsum(unq_cnt[:-1]))
        col2indx = {unq[i]: indxs[i][0] for i in range(len(unq))}
        for col, indx in col2indx.items():
            if col != 0:
                unique_colors.append((col // (256**2), (col // 256) % 256, col % 256))
        return unique_colors

    def create_ann(image_path):
        labels = []
        img_np = sly.imaging.image.read(image_path)[:, :, 0]
        img_height = img_np.shape[0]
        img_wight = img_np.shape[1]
        image_name = get_file_name(image_path)
        categories_mask_path = os.path.join(categories_path, image_name + masks_ext)
        categories_mask_np = sly.imaging.image.read(categories_mask_path)[:, :, 0]
        instances_mask_path = os.path.join(instances_path, image_name + masks_ext)
        instances_mask_np = sly.imaging.image.read(instances_mask_path)
        unique_pixels_inst = get_unique_colors(instances_mask_np)
        for color in unique_pixels_inst:
            mask = np.all(instances_mask_np == color, axis=2)
            true_index_list = list(zip(*np.where(mask == 1)))
            for true_index in true_index_list:
                cat = categories_mask_np[true_index[0]][true_index[1]]
                if (
                    cat == 0 and image_name == "0035374" and true_index == (158, 314)
                ):  # bad mask case
                    cat = 10
                else:
                    break
            obj_class = pixel_to_class[cat]
            curr_bitmap = sly.Bitmap(mask)
            curr_label = sly.Label(curr_bitmap, obj_class)
            labels.append(curr_label)
        return sly.Annotation(img_size=(img_height, img_wight), labels=labels)

    hat = sly.ObjClass("hat", sly.Bitmap)
    hair = sly.ObjClass("hair", sly.Bitmap)
    glove = sly.ObjClass("glove", sly.Bitmap)
    sunglasses = sly.ObjClass("sunglasses", sly.Bitmap)
    upperclothes = sly.ObjClass("upperclothes", sly.Bitmap)
    dress = sly.ObjClass("dress", sly.Bitmap)
    coat = sly.ObjClass("coat", sly.Bitmap)
    socks = sly.ObjClass("socks", sly.Bitmap)
    pants = sly.ObjClass("pants", sly.Bitmap)
    torso_skin = sly.ObjClass("torso_skin", sly.Bitmap)
    scarf = sly.ObjClass("scarf", sly.Bitmap)
    skirt = sly.ObjClass("skirt", sly.Bitmap)
    face = sly.ObjClass("face", sly.Bitmap)
    left_arm = sly.ObjClass("left_arm", sly.Bitmap)
    right_arm = sly.ObjClass("right_arm", sly.Bitmap)
    left_leg = sly.ObjClass("left_leg", sly.Bitmap)
    right_leg = sly.ObjClass("right_leg", sly.Bitmap)
    left_shoe = sly.ObjClass("left_shoe", sly.Bitmap)
    right_shoe = sly.ObjClass("right_shoe", sly.Bitmap)

    pixel_to_class = {
        1: hat,
        2: hair,
        3: glove,
        4: sunglasses,
        5: upperclothes,
        6: dress,
        7: coat,
        8: socks,
        9: pants,
        10: torso_skin,
        11: scarf,
        12: skirt,
        13: face,
        14: left_arm,
        15: right_arm,
        16: left_leg,
        17: right_leg,
        18: left_shoe,
        19: right_shoe,
    }

    project = api.project.create(
        workspace_id, project_name, change_name_if_conflict=True
    )
    meta = sly.ProjectMeta(
        obj_classes=[
            hat,
            hair,
            glove,
            sunglasses,
            upperclothes,
            dress,
            coat,
            socks,
            pants,
            torso_skin,
            scarf,
            skirt,
            face,
            left_arm,
            right_arm,
            left_leg,
            right_leg,
            left_shoe,
            right_shoe,
        ]
    )
    api.project.update_meta(project.id, meta.to_json())

    for ds_name in os.listdir(dataset_path):
        ds_path = os.path.join(dataset_path, ds_name)
        if dir_exists(ds_path):
            images_path = os.path.join(ds_path, images_folder)
            humans_path = os.path.join(ds_path, humans_folder)
            categories_path = os.path.join(ds_path, categories_folder)
            instances_path = os.path.join(ds_path, instances_folder)

            dataset = api.dataset.create(
                project.id, ds_name.lower(), change_name_if_conflict=True
            )

            images_names = os.listdir(images_path)

            progress = sly.Progress(
                "Create dataset {}".format(ds_name), len(images_names)
            )

            for img_names_batch in sly.batched(images_names, batch_size=batch_size):
                images_pathes_batch = [
                    os.path.join(images_path, image_name)
                    for image_name in img_names_batch
                ]

                img_infos = api.image.upload_paths(
                    dataset.id, img_names_batch, images_pathes_batch
                )
                img_ids = [im_info.id for im_info in img_infos]

                if ds_name != "Testing":
                    anns_batch = [
                        create_ann(image_path) for image_path in images_pathes_batch
                    ]
                    api.annotation.upload_anns(img_ids, anns_batch)

                progress.iters_done_report(len(img_names_batch))

    return project
