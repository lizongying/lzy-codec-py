# 定义常量
SURROGATE_MIN = 0xD800
SURROGATE_MAX = 0xDFFF
UNICODE_MAX = 0x10FFFF
ERROR_UNICODE = ValueError("invalid unicode")


def valid_unicode(r: int) -> bool:
    """
    验证一个Unicode码点是否有效（排除代理区字符）
    """
    return (0 <= r < SURROGATE_MIN) or (SURROGATE_MAX < r <= UNICODE_MAX)


def encode(input_runes: list[int]) -> bytes:
    """
    将Unicode码点列表（rune切片）转换为LZY编码的字节序列
    :param input_runes: 整数列表，每个元素是有效的Unicode码点
    :return: LZY编码的bytes对象
    """
    output = bytearray()

    for r in input_runes:
        if r < 0x80:
            # 单字节编码：0xxxxxxx
            output.append(r & 0xFF)
        elif r < 0x4000:
            # 双字节编码：第一个字节(高7位) + 第二个字节(0x80 | 低7位)
            output.append((r >> 7) & 0xFF)
            output.append((0x80 | (r & 0x7F)) & 0xFF)
        else:
            # 三字节编码：高7位 + 0x80|中间7位 + 0x80|低7位
            output.append((r >> 14) & 0xFF)
            output.append((0x80 | ((r >> 7) & 0x7F)) & 0xFF)
            output.append((0x80 | (r & 0x7F)) & 0xFF)

    return bytes(output)


def encode_from_string(input_str: str) -> bytes:
    """
    将UTF-8编码的字符串转换为LZY编码的字节序列
    :param input_str: 普通UTF-8字符串
    :return: LZY编码的bytes对象
    """
    # 将字符串转换为Unicode码点列表（对应Go的[]rune(input)）
    runes = [ord(c) for c in input_str]
    return encode(runes)


def encode_from_bytes(input_bytes: bytes) -> bytes:
    """
    将UTF-8编码的字节序列转换为LZY编码的字节序列
    :param input_bytes: UTF-8编码的bytes对象
    :return: LZY编码的bytes对象
    """
    # 先将UTF-8字节解码为字符串，再转换为码点列表
    input_str = input_bytes.decode('utf-8')
    return encode_from_string(input_str)


def decode(input_bytes: bytes) -> list[int]:
    """
    将LZY编码的字节序列解码为Unicode码点列表（rune切片）
    :param input_bytes: LZY编码的bytes对象
    :return: 整数列表，每个元素是有效的Unicode码点
    :raises ValueError: 当输入是无效的LZY编码或Unicode码点时
    """
    l = len(input_bytes)
    if l == 0:
        raise ERROR_UNICODE

    # 寻找第一个最高位为0的字节（有效起始位置）
    start_idx = -1
    for i in range(l):
        if (input_bytes[i] & 0x80) == 0:
            start_idx = i
            break

    if start_idx == -1:
        raise ERROR_UNICODE

    valid_len = l - start_idx
    if valid_len == 0:
        raise ERROR_UNICODE

    output = []

    r = 0
    for i in range(start_idx, l):
        b = input_bytes[i]
        if (b >> 7) == 0:
            # 遇到单字节标记，先处理上一个累积的码点（如果不是第一个）
            if i > start_idx:
                if not valid_unicode(r):
                    raise ERROR_UNICODE
                output.append(r)
            # 重置为当前单字节值
            r = b
        else:
            # 累积码点：左移7位 + 低7位（排除0x80标记位）
            if r > (UNICODE_MAX >> 7):
                raise ERROR_UNICODE
            r = (r << 7) | (b & 0x7F)

    # 处理最后一个累积的码点
    if not valid_unicode(r):
        raise ERROR_UNICODE
    output.append(r)

    return output


def decode_to_string(input_bytes: bytes) -> str:
    """
    将LZY编码的字节序列解码为UTF-8字符串
    :param input_bytes: LZY编码的bytes对象
    :return: UTF-8编码的普通字符串
    :raises ValueError: 当输入是无效的LZY编码或Unicode码点时
    """
    runes = decode(input_bytes)
    # 将Unicode码点列表转换为字符串
    return ''.join(chr(r) for r in runes)


def decode_to_bytes(input_bytes: bytes) -> bytes:
    """
    将LZY编码的字节序列解码为UTF-8编码的字节序列
    :param input_bytes: LZY编码的bytes对象
    :return: UTF-8编码的bytes对象
    :raises ValueError: 当输入是无效的LZY编码或Unicode码点时
    """
    output_str = decode_to_string(input_bytes)
    return output_str.encode('utf-8')


if __name__ == "__main__":
    # 测试编码和解码流程
    test_str = "Hello 世界！LZY编码测试 ✍️"
    print(f"原始字符串: {test_str}")

    # 编码流程
    lzy_bytes = encode_from_string(test_str)
    print(f"LZY编码字节: {lzy_bytes}")

    # 解码流程
    decoded_str = decode_to_string(lzy_bytes)
    print(f"解码后字符串: {decoded_str}")

    # 验证一致性
    assert test_str == decoded_str, "编码解码一致性验证失败"
    print("✅ 编码解码一致性验证通过")

    # 测试字节流编码解码
    utf8_bytes = test_str.encode('utf-8')
    lzy_bytes2 = encode_from_bytes(utf8_bytes)
    decoded_utf8_bytes = decode_to_bytes(lzy_bytes2)
    assert utf8_bytes == decoded_utf8_bytes, "字节流编码解码一致性验证失败"
    print("✅ 字节流编码解码一致性验证通过")
