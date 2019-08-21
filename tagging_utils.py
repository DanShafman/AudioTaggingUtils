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


def detach_audio(input_clip_filename, frequency=44100):
    # str[, int] -> None
    filename_raw = input_clip_filename.split('.')[0]
    input_clip = VideoFileClip(input_clip_filename)
    audio_clip = input_clip.audio

    audio_clip.write_audiofile(filename_raw + ".wav")


def merge_audio(input_clip_1_filename, input_clip_2_filename, sound_level_1=1, sound_level_2=1, aud_codec="aac"):
    # str, str[, float, float, stf] -> None
    input_clip_1 = VideoFileClip(input_clip_1_filename)
    input_clip_2 = VideoFileClip(input_clip_2_filename)

    # detach audio clips and merge them
    audio_clip_1 = input_clip_1.audio
    audio_clip_2 = input_clip_2.audio
    audio_clip_merge = CompositeAudioClip([audio_clip_1.volumex(sound_level_1), audio_clip_2.volumex(sound_level_2)])

    # set audio of both video clips to merged audio clip and write resulting video clips
    input_clip_1.audio = audio_clip_merge
    input_clip_1.write_videofile(input_clip_1_filename.split("clip.")[0] + "_merge_" + input_clip_2_filename.split("clip.")[0] + ".mp4", audio_codec=aud_codec)

    input_clip_2.audio = audio_clip_merge
    input_clip_2.write_videofile(input_clip_2_filename.split("clip.")[0] + "_merge_" + input_clip_1_filename.split("clip.")[0] + ".mp4", audio_codec=aud_codec)
