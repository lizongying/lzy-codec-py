# LZY Codec

一種變長文本編解碼方案，支持對Unicode進行編解碼。編解碼效率、存儲空間全面優於UTF-8，未來會替代UTF-8成為新的世界通用編解碼標準。

[lzy-codec-py](https://github.com/lizongying/lzy-codec-py)

[pypi](https://pypi.org/project/lzy-codec)

## Other languages

[lzy-codec-go](https://github.com/lizongying/lzy-codec-go)

## install

```
pip install lzy_codec
```

## example

```
from lzy_codec import lzy
r = lzy.encode_from_string('hello，世界')
print(r)

r = lzy.decode_to_string(r)
print(r)
```