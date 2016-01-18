# -*- coding: utf-8 -*-
import uuid
import os.path
import json
import math
from PIL import Image, ImageDraw, ImageFont

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.base import View
from django.conf import settings


class ImageCutDeme(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'fm_common/test.html')

    def post(self, request, *args, **kwargs):
        top = int(request.POST.get('top', None))
        left = int(request.POST.get('left', None))
        width = int(request.POST.get('width', None))
        height = int(request.POST.get('height', None))
        img_path = request.POST.get('img_path', None)
        pic_width = int(request.POST.get('pic_width', None))
        pic_height = int(request.POST.get('pic_height', None))

        real_img_path = os.path.join(
            settings.MEDIA_ROOT, 'test', os.path.basename(img_path))
        crop_img_path = os.path.join(
            settings.MEDIA_ROOT, 'test',
            '%s%s' % ('c', os.path.basename(img_path)))
        image = Image.open(real_img_path)
        image.resize((pic_width, pic_height), Image.ANTIALIAS).save(
            crop_img_path, 'jpeg', quality=100)
        # import pdb; pdb.set_trace()
        image_crop = Image.open(crop_img_path)
        file_name = '%s.%s' % (
            str(uuid.uuid1()), crop_img_path.split('.')[-1])
        final_path = os.path.join(settings.MEDIA_ROOT, 'test', file_name)
        box = (top, left, top + width, left + height)
        image_crop.crop(box).save(final_path, 'jpeg', quality=100)
        result = {
            'status': 0,
            'message': 'seccess',
            'data': os.path.join(
                '/uploads/test', os.path.basename(final_path)),
        }

        return HttpResponse(
            json.dumps(result), content_type="application/json")


image_path = ''


def image_up(request):
    result = {
        'status': 1,
        'message': 'failed',
        'data': None,
    }
    if request.method == 'POST':
        if request.FILES:
            file_path_dir = os.path.join(settings.MEDIA_ROOT, 'test')
            format = request.FILES['image'].name.split('.')[-1]
            file_name = '%s%s%s' % (str(uuid.uuid1()), '.', format)
            src = '/uploads/test/%s' % file_name
            file_path = os.path.join(file_path_dir, file_name)
            # import pdb; pdb.set_trace()
            image = open(file_path, 'wb')
            image.write(request.FILES['image'].read())
            image.close()
            result['status'] = 0
            result['message'] = 'success'
            result['data'] = src
    return HttpResponse(
        json.dumps(result), content_type='application/json')


class ImageWatermark(View):

    text = 'Thecover.cn'

    def get(self, request, *args, **kwargs):
        return render(request, 'fm_common/image_watermark.html')

    def post(self, request, *args, **kwargs):
        if request.FILES:
            image_file = request.FILES['image']

            image_name = '%s.%s' % (
                uuid.uuid1(), image_file.name.split('.')[-1])
            image_path = os.path.join(
                settings.MEDIA_ROOT, 'test', image_name)
            save_image = open(image_path, 'wb')
            save_image.write(image_file.read())
            save_image.close()

            image = Image.open(image_file)
            image_w, image_h = image.size
            text_image_w = image_w
            text_image_h = image_h
            blank = Image.new("RGB", (text_image_w, text_image_h), 'white')
            d = ImageDraw.Draw(image)

            if image_w < 400:
                k = 32
            elif image_w < 600:
                k = 48
            elif image_w < 800:
                k = 64
            elif image_w < 1000:
                k = 80
            elif image_w < 1200:
                k = 100
            elif image_w < 1400:
                k = 128
            elif image_w < 1800:
                k = 156
            elif image_w < 2200:
                k = 192
            elif image_w < 2600:
                k = 256
            elif image_w < 3100:
                k = 300
            else:
                k = 350

            font = ImageFont.truetype(
                os.path.join(settings.PROJECT_ROOT,
                    'static',
                    'AlexBrush-Regular.ttf'
                ), k)
            text_w, text_h = font.getsize(self.text)
            d.ink = 0 + 0 * 256 + 0 * 256 * 256
            d.text(
                [(text_image_w - text_w) / 2, (text_image_h - text_h) / 2],
                self.text,
                font=font
            )
            # text_rotate = blank.rotate(30)
            # r_len = math.sqrt((text_w / 2) ** 2 + (text_h / 2) ** 2)
            # ori_angle = math.atan(text_h / text_w)
            # crop_w = r_len * math.cos(ori_angle + math.pi / 6) * 2
            # crop_h = r_len * math.sin(ori_angle + math.pi / 6) * 2
            # box = [
            #     int((text_image_w - crop_w) / 2 - 1),
            #     int((text_image_h - crop_h) / 2) - 50,
            #     int((text_image_w + crop_w) / 2 + 1),
            #     int((text_image_h + crop_h) / 2 + 1)
            # ]
            # text_image = text_rotate.crop(box)

            # paste_w, paste_h = text_image.size
            # text_blank = Image.new('RGB', (image_w, image_h), 'white')
            # paste_box = (
            #     int((image_w - paste_w) / 2 - 1),
            #     int((image_h - paste_h) / 2 - 1)
            # )
            # text_blank.paste(text_image, paste_box)
            # water_image = Image.blend(image, blank, 0.1)
            file_name = '%s.%s' % (
                uuid.uuid1(), image_file.name.split('.')[-1])
            image.save(
                os.path.join(settings.MEDIA_ROOT, 'test', file_name))
            result = {
                'status': 0,
                'message': 'success',
                'data': [
                    os.path.join('/uploads', 'test', image_name),
                    os.path.join('/uploads', 'test', file_name)
                ]
            }

            return HttpResponse(
                json.dumps(result), content_type='application/json')
