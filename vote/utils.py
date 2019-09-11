import random

def generate_mobile_code(length=6):
    """生成手机验证码字符串"""
    select_nums = random.choice('0123456789')
    return ''.join(select_nums)


def generate_captcha_code(length=4):
    """生成图片验证码字符串"""
    selected_chars = random.choice('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz')
    return ''.join(selected_chars)