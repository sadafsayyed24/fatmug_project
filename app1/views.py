from django.shortcuts import render,HttpResponse
from django.shortcuts import render, redirect
from .models import videos,subtitles
from .subtitles import extract_subtitles

# Create your views here.
def home(request):
    return render(request,'home.html')

def search_video_page(request):
    return render(request,'search_video_page.html')

def all_videos(request):
    return render(request,'all_videos.html')

def upload_videos_page(request):
    if request.method == 'POST' and request.FILES['video_file']:
        video_file = request.FILES['video_file']
        
        # Create video object in database
        video = videos.objects.create(video_file=video_file)
        
        # Trigger Celery task for subtitle extraction
        extract_subtitles.delay(video.id, language)
        
        # Redirect to the same page or to the list page
        return redirect('upload_videos_page')
    
    return render(request, 'upload_video_page.html')

def video_list(request):
    videos = videos.objects.all()
    return render(request, 'video_list.html', {'videos': videos})

def video_detail(request, video_id):
    video = videos.objects.get(id=video_id)
    subtitles = video.subtitles.all()
    return render(request, 'video_detail.html', {'video': video, 'subtitles': subtitles})

def search_subtitle(request, video_id):
    video = videos.objects.get(id=video_id)
    query = request.GET.get('q', '').lower()
    subtitles = video.subtitles.filter(subtitle_text__icontains=query)
    return render(request, 'search_results.html', {'video': video, 'subtitles': subtitles, 'query': query})
