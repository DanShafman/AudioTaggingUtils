from moviepy.editor import *

def augment_clip(input_clip_filename, augment_audio_filename, output_filename, sound_level=1):
    # str, str, float, str -> None
    input_clip = VideoFileClip(input_clip_filename)
    audio_clip_orig = input_clip.audio
    audio_clip_new = AudioFileClip(augment_audio_filename)

    # overlay new audio clip on top of original audio clip at specified percent sound level (1 meaning no change)
    # then merge resulting audio clip with original video clip
    audio_clip_aug = CompositeAudioClip([audio_clip_orig, audio_clip_new.volumex(sound_level)])
    input_clip.audio = audio_clip_aug

    input_clip.write_videofile(output_filename)


