from celery import shared_task
import subprocess
from .models import *
import os

@shared_task
def extract_subtitles(video_id):
    video = videos.objects.get(id=video_id)
    output_srt = f"media/subtitles/{video.id}.srt"
    
    # Run ccextractor to extract subtitles
    subprocess.run(['ccextractor', video.video_file.path, '-o', output_srt])
    
    # Read the .srt file and save to database
    with open(output_srt, 'r') as f:
        subtitles_data = f.read()

    # Process the subtitle file to extract text and timestamps
    # This example assumes the subtitle format is simple, so adapt as needed
    for subtitle_line in parse_srt(subtitles_data):  # Assumes a parse_srt function
        subtitle = subtitles(video=video, subtitle_text=subtitle_line['text'], timestamp=subtitle_line['timestamp'])
        subtitle.save()

def parse_srt(srt_data):
    # Simplified SRT parser - adjust based on your subtitle format
    import re
    pattern = re.compile(r"(\d+)\n(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})\n(.+)")
    subtitles = []
    for match in re.finditer(pattern, srt_data):
        start_time = match.group(2)  # start time
        text = match.group(4)        # subtitle text
        # Convert start_time (HH:MM:SS,ms) to seconds for easy timestamping
        h, m, s = map(float, start_time.replace(',', '.').split(':'))
        timestamp = h * 3600 + m * 60 + s
        subtitles.append({'text': text, 'timestamp': timestamp})
    return subtitles
