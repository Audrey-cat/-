# -*- coding:utf-8 -*-
'''
author: 文天尧
create: 2020-07-20
update: 2020-07-21
'''
import random

from PIL import Image, ImageFont, ImageDraw, ImageFilter

def get_random_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

def validate_picture(length):
    msg = 'zxcvbnmasdfghjklqwertyuiopQWERTYUIOPASDFGHJKLZMXNCBV1234567890'
    width = 130
    height = 40
    im = Image.new('RGB', (width,height), get_random_color()) # 创建图片
    # 创建字体对象
    font = ImageFont.truetype('../fonts/times.ttf', 38) # 找字体资源
    # 创建ImageDraw对象
    draw = ImageDraw.Draw(im)
    s = ''
    for i in range(length):
        m = random.choice(msg)
        s += m
        draw.text((7 + random.randint(4, 7) + 25 * i, random.randint(2,7)), text=m, fill=get_random_color(), font=font)
    # draw.text((13,5),text=s,fill=get_random_color(),font=font)

    # 绘制干扰线
    for n in range(8):
        x1 = random.randint(0,width/2)
        y1 = random.randint(0,height/2)

        x2 = random.randint(0, width)
        y2 = random.randint(height/2, height)
        draw.line(((x1,y1),(x2,y2)),fill='black',width=1)

    # 添加滤镜
    im = im.filter(ImageFilter.EDGE_ENHANCE)

    # 保存验证码图片到本地
    # with open("validCode.png", "wb") as f:
    #     im.save(f,"png")

    return im,s # 返回图像和字符串

if __name__ == '__main__':
    validate_picture(4)



