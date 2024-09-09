from django.db import models

class videos(models.Model):
    video_file = models.FileField(upload_to='videos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # return str(self.id)  # Corrected __str__ method to return string representation of ID
        return f"{self.id} at {self.uploaded_at}"


class subtitles(models.Model):
    video = models.ForeignKey(videos, on_delete=models.CASCADE, related_name='subtitles')
    language = models.CharField(max_length=10, default='en')
    subtitle_text = models.TextField()  # Store subtitles as plain text
    timestamp = models.FloatField()  # Store timestamp in seconds

    def __str__(self):
        return f"Subtitle for {self.video.id} at {self.timestamp}"

