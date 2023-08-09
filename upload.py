# Import the necessary moviepy modules
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from moviepy.video.io.VideoFileClip import VideoFileClip
import os
import sys
import random
from tqdm import tqdm
from pyrogram import Client
import time
import mimetypes

api_id = 
api_hash = ''

username = sys.argv[1]
video_path = sys.argv[2]
caption = sys.argv[3]

mime_type = mimetypes.guess_type(video_path)[0]
if mime_type is None:
    print("Error: Unable to determine MIME type of the file.")
    sys.exit(1)

# Create a progress bar
progress_bar = tqdm(total=os.path.getsize(video_path), unit='B', unit_scale=True, ncols=80)

# Define the progress callback function
def progress_callback(current, total):
    progress_bar.update(current - progress_bar.n)

if mime_type.startswith('video'):
    # Generate the thumbnail using moviepy
    thumbnail_path = 'thumb.jpg'
    clip = VideoFileClip(video_path)
    duration = clip.duration

    # Set thumbnail time to a random position in the middle of the video
    thumbnail_time = random.uniform(duration / 4, duration * 3 / 4)
    thumbnail = clip.save_frame(thumbnail_path, t=thumbnail_time)

# Retry settings
max_attempts = 3
retry_delay = 5  # seconds

attempts = 0
if username.isdigit():
    username = int(username)
while attempts < max_attempts:
    try:
        # Authenticate and send the media
        with Client('name', api_id, api_hash) as client:
            if mime_type.startswith('video'):                
                client.send_video(chat_id=username, video=video_path, caption=caption, progress=progress_callback, thumb=thumbnail_path, duration=int(duration), supports_streaming=True)
                # Delete the generated thumbnail file
                os.remove(thumbnail_path)

            elif mime_type.startswith('audio'):                
                client.send_audio(chat_id=username, audio=video_path, caption=caption, progress=progress_callback)

            elif mime_type.startswith('image'):                
                client.send_photo(chat_id=username, photo=video_path, caption=caption, progress=progress_callback)            
            # FALLBACK DEFAULT
            else:                
                client.send_document(chat_id=username, document=video_path, caption=caption, progress=progress_callback)
        
        # Content sent successfully, break the loop
        break
    except Exception as e:
        attempts += 1
        print(f"Attempt {attempts} failed: {e}")
        if attempts < max_attempts:
            print("Retrying...")
            time.sleep(retry_delay)
        else:
            print("Max attempts reached. Upload failed.")
            break
