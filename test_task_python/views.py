# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.conf import settings
import cv2
import numpy as np
import os

from test_task_python.RequestLog import RequestLog

from urllib.parse import unquote


def generate_running_text_video(request, text):
    width = 100
    height = 100
    fps = 30
    duration = 3

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_path = os.path.join(settings.BASE_DIR, 'running_text.mp4')
    video = cv2.VideoWriter(video_path, fourcc, fps, (width, height))

    font = cv2.FONT_HERSHEY_COMPLEX
    font_scale = 1
    font_color = (255, 255, 255)
    line_type = 2

    num_frames = duration * fps
    text_width, text_height = cv2.getTextSize(text, font, font_scale, line_type)[0]
    initial_text_x = width

    for frame_count in range(num_frames):
        frame = np.zeros((height, width, 3), dtype=np.uint8)
        text_x = int(initial_text_x - (frame_count / num_frames) * (text_width + width))
        text_y = int((height + text_height) / 2)
        cv2.putText(frame, text, (text_x, text_y), font, font_scale, font_color, line_type)

        video.write(frame)

    video.release()


def video_view(request):
    text = request.GET.get('text', '')
    decoded_text = unquote(text)

    if text:
        generate_running_text_video(request, decoded_text)
        RequestLog.objects.get_or_create(text=decoded_text)

    video_path = os.path.join(settings.BASE_DIR, 'running_text.mp4')
    video_file = open(video_path, 'rb')
    response = HttpResponse(video_file, content_type='video/mp4')
    response['Content-Disposition'] = 'inline; filename="running_text.mp4"'

    return response
