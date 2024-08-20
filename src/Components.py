from moviepy.editor import *
import math
from PIL import Image
import numpy
import os

def concatMedias(input_folder, duration_per_image, total_duration, mainTitle, scdTitle):

    global video_clip, image_sequence, audio_clip
    image_clips = []

    # Load
    for filename in sorted(os.listdir(input_folder)):
        file_path = os.path.join(input_folder, filename)

        if filename.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
            # Load Video
            video_clip = VideoFileClip(file_path).subclip(0,total_duration).resize((1920, 540)).set_position(("center", "top")).without_audio()

        elif filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp')):
            # Load Image
            image_clip = ImageClip(file_path).resize((1920, 540)).set_duration(duration_per_image).set_position(("center", "bottom"))
            image_clips.append(image_clip)

        elif filename.lower().endswith(('.mp3', '.wav')):
            #Load Audio
            audio_clip = AudioFileClip(file_path)
            audio_clip = audio_clip.fx(vfx.speedx, 1.1)

    image_sequence = crossfadeLoop(image_clips, total_duration, duration_per_image)
    mainTitleClip = bigTitle(mainTitle, total_duration)
    scdTitleClip = smallTitle(scdTitle, total_duration)

    final_clip = clips_array([[video_clip],[image_sequence]])
    final_clip = final_clip.fx(vfx.resize, (1080, 1920), width=1080)
    final_clip = CompositeVideoClip([final_clip, mainTitleClip, scdTitleClip]).set_duration(total_duration)
    final_clip = final_clip.set_audio(audio_clip)

    return final_clip

def crossfadeLoop(image_clips, total_duration, duration_per_image):
    num_images = len(image_clips)

    if num_images > 0:
        total_clips = int(total_duration // duration_per_image) * 2
        if total_clips % 2 == 0:
            total_clips = total_clips - 1

        image_sequence = []

        for i in range(total_clips):
            clip = image_clips[i % num_images].set_duration(duration_per_image).crossfadein(2)
            clip = zoom_in_effect(clip, 0.04)
            image_sequence.append(clip)

        image_sequence = concatenate_videoclips(image_sequence, method="compose", padding=-2)
        return image_sequence

def zoom_in_effect(clip, zoom_ratio=0.04):
    def effect(get_frame, t):
        img = Image.fromarray(get_frame(t))
        base_size = img.size

        new_size = [
            math.ceil(img.size[0] * (1 + (zoom_ratio * t))),
            math.ceil(img.size[1] * (1 + (zoom_ratio * t)))
        ]

        # The new dimensions must be even.
        new_size[0] = new_size[0] + (new_size[0] % 2)
        new_size[1] = new_size[1] + (new_size[1] % 2)

        img = img.resize(new_size, Image.LANCZOS)

        x = math.ceil((new_size[0] - base_size[0]) / 2)
        y = math.ceil((new_size[1] - base_size[1]) / 2)

        img = img.crop([
            x, y, new_size[0] - x, new_size[1] - y
        ]).resize(base_size, Image.LANCZOS)

        result = numpy.array(img)
        img.close()

        return result

    return clip.fl(effect)

def bigTitle(text, duration):
    txt_clip = TextClip(text, fontsize=100, color='white',bg_color="red")
    txt_clip = txt_clip.set_pos("center").set_duration(duration)

    return txt_clip

def smallTitle(text, duration):
    txt_clip = TextClip(text, fontsize=50, color='white',bg_color="red")
    txt_clip = txt_clip.set_pos("bottom").set_duration(duration)

    return txt_clip