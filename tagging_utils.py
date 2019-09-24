from moviepy.editor import *
import random


# ========== UTILITY FUNCTIONS ==========

def augment_clip(input_clip_filename, augment_audio_filename, output_filename, filepath_to_write="", sound_level=1, aud_codec="aac"):
    # str, str, str[, str, float, str] -> None
    # 'augment_clip' takes an input video clip and augments it with augment_audio_filename, which can be
    # an audio file or a .mov or .mp4 video file
    input_clip = VideoFileClip(input_clip_filename)
    audio_clip_orig = input_clip.audio

    # check if augment_audio_filename is audio or video, extract audio clip
    augment_audio_file_extension = augment_audio_filename.split(".")[1]
    if (augment_audio_file_extension == '.mp4') or (augment_audio_file_extension == '.mov'):
        video_clip_to_extract = VideoFileClip(augment_audio_filename)
        audio_clip_new = video_clip_to_extract.audio
    else:
        audio_clip_new = AudioFileClip(augment_audio_filename)

    # overlay new audio clip on top of original audio clip at specified percent sound level (1 meaning no change)
    # then merge resulting audio clip with original video clip
    audio_clip_aug = CompositeAudioClip([audio_clip_orig, audio_clip_new.volumex(sound_level)])
    input_clip.audio = audio_clip_aug

    input_clip.write_videofile(filepath_to_write + output_filename, audio_codec=aud_codec)


def detach_audio(input_clip_filename, filepath_to_write="", frequency=44100):
    # str[, str, int] -> None
    # detaches the audio of the input clip and writes it as a .wav file (with a variable sample rate)
    input_clip = VideoFileClip(input_clip_filename)

    # get the name of just the file from the given filepath
    filename_components = input_clip_filename.split(".")
    input_clip_filename = filename_components[len(filename_components) - 2]
    filename_components = input_clip_filename.split("/")
    input_clip_filename = filename_components[len(filename_components) - 1]

    audio_clip = input_clip.audio

    audio_clip.write_audiofile(filepath_to_write + input_clip_filename + ".wav")


def merge_audio(input_clip_1_filename, input_clip_2_filename, sound_level_1=1, sound_level_2=1, aud_codec="aac"):
    # str, str[, float, float, stf] -> None
    # takes two video clips as input, augments both clips with their respective other (with variable sound levels)
    # sound_level_1 will be the sound level of the audio of input_clip_1, ditto for sound_level_2

    # some of the video clips are .mov rather than .mp4, hence this safety
    try:
        input_clip_1 = VideoFileClip(input_clip_1_filename)
    except:
        input_clip_1_filename = input_clip_1_filename.split(".")[0] + ".mov"
        input_clip_1 = VideoFileClip(input_clip_1_filename)
    
    try:
        input_clip_2 = VideoFileClip(input_clip_2_filename)
    except:
        input_clip_2_filename = input_clip_2_filename.split(".")[0] + ".mov"
        input_clip_2 = VideoFileClip(input_clip_2_filename)

    # detach audio clips and merge them into a 'merged audio clip'
    audio_clip_1 = input_clip_1.audio
    audio_clip_2 = input_clip_2.audio
    audio_clip_merge = CompositeAudioClip([audio_clip_1.volumex(sound_level_1), audio_clip_2.volumex(sound_level_2)])

    # set audio property of both video clips to merged audio clip and write resulting output
    input_clip_1.audio = audio_clip_merge
    input_clip_1.write_videofile(input_clip_1_filename.split("clip.")[0] + "_merge_" + input_clip_2_filename.split("clip.")[0] + ".mp4", audio_codec=aud_codec)

    input_clip_2.audio = audio_clip_merge
    input_clip_2.write_videofile(input_clip_2_filename.split("clip.")[0] + "_merge_" + input_clip_1_filename.split("clip.")[0] + ".mp4", audio_codec=aud_codec)


def replace_audio(input_clip_filename, input_audio_filename, filepath_to_write="", aud_codec="aac"):
    # str, str[, str, str] -> None
    # takes an audio clip and a video clip as inputs, and replaces the video clip's audio with the provided clip
    # filepath the result will be written to may optionally be specified
    try:
        input_clip = VideoFileClip(input_clip_filename)
    except: 
        input_clip_filename = input_clip_filename[:len(input_clip_filename) - 4] + ".mov"
        input_clip = VideoFileClip(input_clip_filename)

    input_audio = AudioFileClip(input_audio_filename)
    input_clip.audio = input_audio

    # parse input clip's filename for directory and literal filename
    filename_components = input_clip_filename.split(".")
    input_clip_filename = filename_components[len(filename_components) - 2]

    filename_components = input_clip_filename.split("/")
    input_clip_filename = filename_components[len(filename_components) - 1]

    input_clip.write_videofile(filepath_to_write + input_clip_filename + "_eq.mp4", audio_codec=aud_codec)



# ========== EXPERIMENT DATA FUNCTIONS ==========

def generate_merged_audio_set():
    # None -> None
    # generates 30 sets of 'merged' primary and secondary clips (as defined later) for use in the experiment

    # a set of merged audio clips is the set of one primary and one secondary clip, where the primary clip has been augmented
    # with the secondary clip and vice versa

    # primary clip: contains construction-related or otherwise loud noises
    # secondary clip: contains 'mundane' everyday noises with no construction or otherwise overbearing sounds

    # 30 primary and secondary clips selected to be used by humans
    primary_clips = [34, 35, 36, 54, 59, 61, 68, 88, 91, 92, 95, 96, 97, 98, 99, 100, 101, 102, 106, 108, 109, 110, 111, 112, 114, 118, 126, 127, 128, 129] # 30
    secondary_clips = [1, 4, 8, 11, 16, 17, 22, 26, 37, 38, 40, 48, 49, 50, 51, 53, 55, 64, 65, 67, 87, 105, 107, 115, 120] # 25

    with open("merge_list.txt", "a") as f:
        for p_clip in primary_clips:
            s_clip = secondary_clips[int(random.random() * len(secondary_clips))]
            secondary_clips.remove(s_clip)
            merge_audio(str(p_clip) + "clip.mp4", str(s_clip) + "clip.mp4")
            f.write(str(p_clip) + "  -  " + str(s_clip) + "\n")


def generate_car_horn_siren_augmented_clips():
    # None -> None
    # generates the set of 32 augmented video clips which will be used in the experiment

    # most of the 11 video clips will be augmented with the audio from clip 16 (car horn), clip 105 (delayed siren), and clip 106 (10 second siren)
    # the exception is 106clip, which is also being augmented and cannot be used to augment itself
    # to overcome this, 106 will be augmented with 112 (jackhammer) and 119 (reverse beeper)
    detach_audio("./equalized_clips/16clip_eq.mp4", "./car_horn_siren_augmented_clips/")
    detach_audio("./equalized_clips/105clip_eq.mp4", "./car_horn_siren_augmented_clips/")
    detach_audio("./equalized_clips/106clip_eq.mp4", "./car_horn_siren_augmented_clips/")

    detach_audio("./equalized_clips/112clip_eq.mp4", "./car_horn_siren_augmented_clips/")
    detach_audio("./equalized_clips/119clip_eq.mp4", "./car_horn_siren_augmented_clips/")

    # 11 clips which will be augmented
    clips = [95, 97, 99, 106, 120, 101, 109, 110, 113, 65, 16]

    # loop through each of the 11 clips, augment them with final_audio_v1 except 106clip, which is augmented with final_audio_v2
    for clip in clips:
        if clip == 106:
            augment_clip("./equalized_clips/106clip_eq.mp4", "./car_horn_siren_augmented_clips/112clip_eq.wav", "106_aug_112.mp4", filepath_to_write="./car_horn_siren_augmented_clips/")
            augment_clip("./equalized_clips/106clip_eq.mp4", "./car_horn_siren_augmented_clips/119clip_eq.wav", "106_aug_119.mp4", filepath_to_write="./car_horn_siren_augmented_clips/")
        else:
            augment_clip("./equalized_clips/" + str(clip) + "clip_eq.mp4", "./car_horn_siren_augmented_clips/16clip_eq.wav", str(clip) + "_aug_16.mp4", filepath_to_write="./car_horn_siren_augmented_clips/")
            augment_clip("./equalized_clips/" + str(clip) + "clip_eq.mp4", "./car_horn_siren_augmented_clips/105clip_eq.wav", str(clip) + "_aug_105.mp4", filepath_to_write="./car_horn_siren_augmented_clips/")
            augment_clip("./equalized_clips/" + str(clip) + "clip_eq.mp4", "./car_horn_siren_augmented_clips/106clip_eq.wav", str(clip) + "_aug_106.mp4", filepath_to_write="./car_horn_siren_augmented_clips/")
            

generate_car_horn_siren_augmented_clips()

# ==== TO IMPLEMENT INTO EXPERIMENT FUNCTIONS ====
# for i in range(91, 130):
#     replace_audio("./original_clips/" + str(i) + "clip.mp4", "./equalized_audio/" + str(i) + "clip__eq.wav", filepath_to_write="./equalized_clips/")

