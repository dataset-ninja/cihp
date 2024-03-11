**CIHP: Crowd Instance-level Human Parsing** is a dataset for instance segmentation, semantic segmentation, and object detection tasks. It is used in the surveillance industry. 

The dataset consists of 38280 images with 768446 labeled objects belonging to 19 different classes including *face*, *hair*, *torso_skin*, and other: *upperclothes*, *right_arm*, *left_arm*, *pants*, *coat*, *left_shoe*, *right_shoe*, *right_leg*, *left_leg*, *hat*, *dress*, *socks*, *sunglasses*, *skirt*, *scarf*, and *glove*.

Images in the CIHP dataset have pixel-level instance segmentation annotations. Due to the nature of the instance segmentation task, it can be automatically transformed into a semantic segmentation (only one mask for every class) or object detection (bounding boxes for every object) tasks. There are 5000 (13% of the total) unlabeled images (i.e. without annotations). There are 3 splits in the dataset: *training* (28280 images), *testing* (5000 images), and *validation* (5000 images). The dataset was released in 2018 by the <span style="font-weight: 600; color: grey; border-bottom: 1px dashed #d3d3d3;">Sun Yat-sen University</span>, <span style="font-weight: 600; color: grey; border-bottom: 1px dashed #d3d3d3;">SenseTime Group (Limited)</span>, and <span style="font-weight: 600; color: grey; border-bottom: 1px dashed #d3d3d3;">CVTE Research</span>.

Here are the visualized examples for the classes:

[Dataset classes](https://github.com/dataset-ninja/cihp/raw/main/visualizations/classes_preview.webm)
