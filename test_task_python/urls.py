from django.urls import path
from test_task_python.views import video_view

urlpatterns = [
    path('video', video_view, name='video'),
    path('video/<str:text>/', video_view, name='video_with_text'),
]