Dataset **CIHP** can be downloaded in [Supervisely format](https://developer.supervisely.com/api-references/supervisely-annotation-json-format):

 [Download](https://assets.supervisely.com/remote/eyJsaW5rIjogInMzOi8vc3VwZXJ2aXNlbHktZGF0YXNldHMvMjMwM19DSUhQL2NpaHAtRGF0YXNldE5pbmphLnRhciIsICJzaWciOiAiTERPVEc5NExnc3ZwbTZPQVU2TG8vVDBXL2ZGeUFrc1pwc3VVejBJVm0ydz0ifQ==?response-content-disposition=attachment%3B%20filename%3D%22cihp-DatasetNinja.tar%22)

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