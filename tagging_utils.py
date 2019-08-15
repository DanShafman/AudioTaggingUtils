from moviepy.editor import *

def augment_clip(input_clip_filename, augment_audio_filename, output_filename, sound_level=1, aud_codec="aac"):
    # str, str, str[, float, str] -> None
    input_clip = VideoFileClip(input_clip_filename)
    audio_clip_orig = input_clip.audio
    audio_clip_new = AudioFileClip(augment_audio_filename)

    # overlay new audio clip on top of original audio clip at specified percent sound level (1 meaning no change)
    # then merge resulting audio clip with original video clip
    audio_clip_aug = CompositeAudioClip([audio_clip_orig, audio_clip_new.volumex(sound_level)])
    input_clip.audio = audio_clip_aug

    input_clip.write_videofile(output_filename, audio_codec=aud_codec)

def detach_audio(input_clip_filename):
    filename_raw = input_clip_filename.split('.')[0]
    input_clip = VideoFileClip(input_clip_filename)
    audio_clip = input_clip.audio

    audio_clip.write_audiofile(filename_raw + ".wav", 44100)

detach_audio("58clip.mp4")