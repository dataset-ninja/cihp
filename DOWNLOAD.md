Dataset **CIHP** can be downloaded in [Supervisely format](https://developer.supervisely.com/api-references/supervisely-annotation-json-format):

 [Download](https://assets.supervisely.com/supervisely-supervisely-assets-public/teams_storage/u/t/7z/wDViVqiefgQ3hW6MdC32iKcEt4hdiZyon4EOgbmmyFUUJkPG009f4pRd4e0Zxlvgjo1VvFcwKr7lFmEeSzoXnWP0xLffBmS7krCx070ZQ0l2zYaqc6RPzv4kEKrG.tar)

As an alternative, it can be downloaded with *dataset-tools* package:
``` bash
pip install --upgrade dataset-tools
```

... using following python code:
``` python
import dataset_tools as dtools

dtools.download(dataset='CIHP', dst_dir='~/dataset-ninja/')
```
Make sure not to overlook the [python code example](https://developer.supervisely.com/getting-started/python-sdk-tutorials/iterate-over-a-local-project) available on the Supervisely Developer Portal. It will give you a clear idea of how to effortlessly work with the downloaded dataset.

The data in original format can be [downloaded here](http://pan.baidu.com/s/1nvqmZBN).