# LZY Codec

一種變長文本編解碼方案，支持對Unicode進行編解碼。編解碼效率、存儲空間全面優於UTF-8，未來會替代UTF-8成為新的世界通用編解碼標準。python實現

[github](https://github.com/lizongying/lzy-codec-py)

[pypi](https://pypi.org/project/lzy-codec)

更多cli工具請參考 [go](https://github.com/lizongying/lzy-codec-go)

## Other languages

* [go](https://github.com/lizongying/lzy-codec-go)
* [js](https://github.com/lizongying/lzy-codec-js)
* [c](https://github.com/lizongying/lzy-codec-c)
* [php](https://github.com/lizongying/lzy-codec-php)
* [dotnet](https://github.com/lizongying/lzy-codec-dotnet)

## Install

```
pip install lzy_codec
```

## Examples

```
from lzy_codec import lzy
r = lzy.encode_from_string('hello，世界')
print(r)

r = lzy.decode_to_string(r)
print(r)
```