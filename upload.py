# Import the necessary moviepy modules
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from moviepy.video.io.VideoFileClip import VideoFileClip
import os
import sys
from tqdm import tqdm
from pyrogram import Client

api_id = 
api_hash = ''

username = sys.argv[1]
video_path = sys.argv[2]
caption = sys.argv[3]

# Get the total size of the file
total_size = os.path.getsize(video_path)
  
# Generate the thumbnail using moviepy
thumbnail_path = 'thumb.jpg'
clip = VideoFileClip(video_path)
duration = clip.duration
thumbnail_time = duration / 2  # Set thumbnail time to middle of the video
thumbnail = clip.save_frame(thumbnail_path, t=thumbnail_time)

# Create a progress bar
progress_bar = tqdm(total=os.path.getsize(video_path), unit='B', unit_scale=True, ncols=80)

# Define the progress callback function
def progress_callback(current, total):
    progress_bar.update(current - progress_bar.n)


with Client('name3', api_id, api_hash) as client:
  client.send_video(username, video_path, caption=caption, progress=progress_callback, thumb=thumbnail_path, duration=int(duration), supports_streaming=True)
  
# Delete the generated thumbnail file
os.remove(thumbnail_path)
