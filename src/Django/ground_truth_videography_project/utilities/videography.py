from moviepy.editor import ColorClip, ImageClip, TextClip, AudioFileClip, concatenate_videoclips, CompositeVideoClip
from django.conf import settings
import cv2
import random
import os

def create_buffer_clip(size, duration, colour=(0, 0, 0)):
    return ColorClip(size, colour, duration=duration)

def create_image_clip(image_path, duration):
    img = cv2.imread(image_path)
    # Convert images to RGB ordering and handle Grayscale images.
    img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB) if len(img.shape) < 3 else cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return ImageClip(img, duration=duration)

def create_text_clip(text, duration):
    return TextClip(text, fontsize=30, color='white').set_position('bottom').set_duration(duration)

def build_video(chunks, clip, audio_path, video_path):
    audio_clip = AudioFileClip(audio_path)
    text_clip = None
    clips = []

    for i, chunk in enumerate(chunks):
        if chunk.image_ids == []:
            print("Performing query...")
            chunk.image_ids = clip.query_prompt(chunk.text)
            chunk.save()
        
        image_path = clip.image_paths[random.choice(chunk.image_ids)]

        buffer_dur = chunk.start_time
        if i > 0:
            buffer_dur -= chunks[i-1].end_time

        buffer_clip = create_buffer_clip((1, 1), buffer_dur)
        image_clip = create_image_clip(os.path.join(settings.IMAGE_DATASET_DIR, image_path), chunk.duration).set_position('top')

        try:
            # ImageMagick must be installed for TextClips to work.
            text_clip = create_text_clip(chunk.text, chunk.duration)
            raise Exception("Test")
        except Exception as ex:
            text_clip = None
            print(f"\u001b[31m{type(ex).__name__}: {ex.args}\u001b[0m")

        if text_clip:
            full_clip = CompositeVideoClip([create_buffer_clip((text_clip.w, image_clip.h + 100), chunk.duration), image_clip, text_clip])
        else:
            full_clip = CompositeVideoClip([create_buffer_clip((image_clip.w, image_clip.h), chunk.duration), image_clip])

        clips.append(concatenate_videoclips([buffer_clip, full_clip], method="compose"))
    
    video = concatenate_videoclips(clips, method='compose')
    video.audio = audio_clip
    video.write_videofile(video_path, fps=24, threads=8)