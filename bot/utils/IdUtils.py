import random
import string
import time


def generate_unique_numeric(digits=20):
    digits = digits - 13
    if digits <= 0:
        raise ValueError("位数长度必须大于0")

    # 获取当前时间戳
    current_timestamp = int(time.time() * 1000)

    # 生成随机数，并确保在指定位数内
    max_random = 10 ** digits - 1
    random_part = random.randint(0, max_random)
    # 将时间戳和随机数组合成唯一数字
    unique_numeric = int(f"{current_timestamp}{random_part:0{digits}}")

    return unique_numeric


def generate_random_string(length):
    # 定义包含大小写字母和数字的字符集
    characters = string.ascii_letters + string.digits

    # 使用 random.choice 随机选择字符，拼接成指定长度的字符串
    random_string = ''.join(random.choice(characters) for _ in range(length))

    return random_string


def generate_custom_random_string(prefix, length):
    # 确保前缀部分不超过指定长度
    if len(prefix) >= length:
        raise ValueError("前缀长度不能大于或等于总长度")

    # 计算剩余部分的长度
    remaining_length = generate_random_string(length - len(prefix))

    return prefix + remaining_length
