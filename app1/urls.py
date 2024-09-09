from django.urls import path,include
from .import views 

urlpatterns = [
    path('',views.home,name='home'),
    path('upload_videos_page/',views.upload_videos_page,name="upload_videos_page"),
    path('search_video_page/',views.search_video_page,name="search_video_page"),
    path('all_videos/',views.all_videos,name="all_videos"),
]