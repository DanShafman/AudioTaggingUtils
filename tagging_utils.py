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


def merge_audio(input_clip_1_filename, input_clip_2_filename, filepath_to_write="", sound_level_1=1, sound_level_2=1, aud_codec="aac"):
    # str, str[, str, float, float, stf] -> None
    # takes two video clips as input, augments both clips with their respective other (with variable sound levels)
    # sound_level_1 will be the sound level of the audio of input_clip_1, ditto for sound_level_2


    print("\n\n\nfilename: ", input_clip_1_filename, "\n\n\n")
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

    # parse for the filename
    filename_components_1 = input_clip_1_filename.split("/")
    input_clip_1_filename = filename_components_1[len(filename_components_1) - 1]
    filename_components_1 = input_clip_1_filename.split(".")
    input_clip_1_filename = filename_components_1[len(filename_components_1) - 2]

    filename_components_2 = input_clip_2_filename.split("/")
    input_clip_2_filename = filename_components_2[len(filename_components_2) - 1]
    filename_components_2 = input_clip_2_filename.split(".")
    input_clip_2_filename = filename_components_2[len(filename_components_2) - 2]

    # detach audio clips and merge them into a 'merged audio clip'
    audio_clip_1 = input_clip_1.audio
    audio_clip_2 = input_clip_2.audio
    audio_clip_merge = CompositeAudioClip([audio_clip_1.volumex(sound_level_1), audio_clip_2.volumex(sound_level_2)])

    # set audio property of both video clips to merged audio clip and write resulting output
    input_clip_1.audio = audio_clip_merge
    input_clip_1.write_videofile(filepath_to_write + input_clip_1_filename.split("clip.")[0] + "_merge_" + input_clip_2_filename.split("clip.")[0] + ".mp4", audio_codec=aud_codec)

    input_clip_2.audio = audio_clip_merge
    input_clip_2.write_videofile(filepath_to_write + input_clip_2_filename.split("clip.")[0] + "_merge_" + input_clip_1_filename.split("clip.")[0] + ".mp4", audio_codec=aud_codec)


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

def change_resolution_squeeze(input_clip_filename, new_res, filepath_to_write="", aud_codec="aac"):
    # str, tuple(int)[, str, str] -> None
    # takes a video clip, converts it to the desired resolution (squeezes dwon to desired aspect ratio), 
    # and writes that to a filepath which may be specified
    input_clip = VideoFileClip(input_clip_filename)

    # skip clips that are already 1280x720
    if input_clip.w == 1280:
        return

    resize_clip = input_clip.resize(new_res)

    # parse input clip's filename for directory and literal filename
    filename_components = input_clip_filename.split(".")
    input_clip_filename = filename_components[len(filename_components) - 2]

    filename_components = input_clip_filename.split("/")
    input_clip_filename = filename_components[len(filename_components) - 1]

    resize_clip.write_videofile(filepath_to_write + input_clip_filename + "_" + str(new_res[0]) + "p.mp4", audio_codec=aud_codec)

def change_resolution_crop(input_clip_filename, new_res, filepath_to_write="", aud_codec="aac"):
    # str, tuple(int)[, str, str] -> None
    # takes a video clip, converts it to the desired resolution (crops before resizing), and writes 
    # that to a filepath which may be specified
    input_clip = VideoFileClip(input_clip_filename)
    print("\n\n\nwidth: ", input_clip.w, "\n\n\n")
    # crop out equal rectangles from the left and right sides of the clip to bring it down to 1.7:1
    if input_clip.w == 3840:
        crop_clip = input_clip
    elif input_clip.w == 2048:
        crop_clip = input_clip.crop(x1=114, x2=1934)
    elif input_clip.w == 1920:
        crop_clip = input_clip.crop(x1=112, x2=1808)
    elif input_clip.w == 1280:
        return None

    resize_clip = crop_clip.resize(new_res)

    # parse input clip's filename for directory and literal filename
    filename_components = input_clip_filename.split(".")
    input_clip_filename = filename_components[len(filename_components) - 2]

    filename_components = input_clip_filename.split("/")
    input_clip_filename = filename_components[len(filename_components) - 1]

    resize_clip.write_videofile(filepath_to_write + input_clip_filename + "_" + str(new_res[0]) + "p.mp4", audio_codec=aud_codec)



# ========== EXPERIMENT DATA FUNCTIONS ==========

def generate_merged_audio_set():
    # None -> None
    # generates 30 sets of 'merged' primary and secondary clips (as defined later) for use in the experiment

    # a set of merged audio clips is the set of one primary and one secondary clip, where the primary clip has been augmented
    # with the secondary clip and vice versa

    # primary clip: contains construction-related or otherwise loud noises
    # secondary clip: contains 'mundane' everyday noises with no construction or otherwise overbearing sounds

    # 30 primary and secondary clips selected to be used by humans
    primary_clips = [34, 35, 36, 54, 59, 61, 68, 88, 91, 92, 95, 96, 97, 98, 99, 100, 101, 102, 106, 108, 109, 110, 111, 112, 114, 118, 126, 127, 128, 129]
    secondary_clips = [107, 37, 11, 64, 38, 73, 22, 51, 78, 15, 65, 26, 115, 62, 48, 67, 53, 1, 49, 4, 105, 55, 120, 16, 17, 8, 87, 32, 40, 50]

    for i in range(0, 30):
        merge_audio("./equalized_clips/" + str(primary_clips[i]) + "clip_eq.mp4", "./equalized_clips/" + str(secondary_clips[i]) + "clip_eq.mp4", filepath_to_write="./merged_clips/")


def generate_car_horn_siren_augmented_clips():
    # None -> None
    # generates the set of 32 augmented video clips which will be used in the experiment

    # most of the 11 video clips will be augmented with the audio from clip 8, clip 16 (car horn), clip 105 (delayed siren), and clip 106 (10 second siren)
    # the exception is 106clip, which is also being augmented and cannot be used to augment itself
    # to overcome this, 106 will be augmented with 112 (jackhammer) and 119 (reverse beeper)
    detach_audio("./equalized_clips/8clip_eq.mp4", "./car_horn_siren_augmented_clips/")
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
            augment_clip("./equalized_clips/" + str(clip) + "clip_eq.mp4", "./car_horn_siren_augmented_clips/8clip_eq.wav", str(clip) + "_aug_8.mp4", filepath_to_write="./car_horn_siren_augmented_clips/")
            augment_clip("./equalized_clips/" + str(clip) + "clip_eq.mp4", "./car_horn_siren_augmented_clips/16clip_eq.wav", str(clip) + "_aug_16.mp4", filepath_to_write="./car_horn_siren_augmented_clips/")
            augment_clip("./equalized_clips/" + str(clip) + "clip_eq.mp4", "./car_horn_siren_augmented_clips/105clip_eq.wav", str(clip) + "_aug_105.mp4", filepath_to_write="./car_horn_siren_augmented_clips/")
            augment_clip("./equalized_clips/" + str(clip) + "clip_eq.mp4", "./car_horn_siren_augmented_clips/106clip_eq.wav", str(clip) + "_aug_106.mp4", filepath_to_write="./car_horn_siren_augmented_clips/")
            

def equalize_resolutions_squeeze():
    # None -> None
    # takes all the existing standard views and resizes them to 1280x720

    # this is necessary because two cameras were used for recording, a GoPro Fusion and a Ricoh Theta S
    # for Ricoh Theta S, its equirectangular video output is written as 1280x720 a standard view, while for the GoPro it is
    # written as 1920x960 or 2048x1024

    # because of the different aspect ratios, this particular function squeezes the larger resolutions (which are in 2:1)
    # to the smaller resolution (which is 1.7:1)
    standard_view_clips = [34, 35, 36, 54, 59, 61, 68, 88, 91, 92, 95, 96, 97, 98, 99, 100, 101, 102, 106, 108, 109, 110, 111, 112, 114, 118, 126, 127, 128, 129, 107, 37, 11, 64, 38, 73, 22, 51, 78, 15, 65, 26, 115, 62, 48, 67, 53, 1, 49, 4, 105, 55, 120, 16, 17, 8, 87, 32, 40, 50, 56, 25, 27, 79, 4]
    for std_num in standard_view_clips:
        change_resolution_squeeze("./standards/" + str(std_num) + "clip_eq.mp4", (1280, 720), filepath_to_write="./stds_res_equalized/")


def equalize_resolutions_crop():
    # None -> None
    # takes all the existing standard views and resizes them to 1280x720

    # this is necessary because two cameras were used for recording, a GoPro Fusion and a Ricoh Theta S
    # for Ricoh Theta S, its equirectangular video output is written as 1280x720 a standard view, while for the GoPro it is
    # written as 1920x960 or 2048x1024

    # because of the different aspect ratios, this particular function crops the larger resolutions from 2:1 to 1.7:1 before
    # resizing them
    standard_view_clips = [34, 35, 36, 54, 59, 61, 68, 88, 91, 92, 95, 96, 97, 98, 99, 100, 101, 102, 106, 108, 109, 110, 111, 112, 114, 118, 126, 127, 128, 129, 107, 37, 11, 64, 38, 73, 22, 51, 78, 15, 65, 26, 115, 62, 48, 67, 53, 1, 49, 4, 105, 55, 120, 16, 17, 8, 87, 32, 40, 50, 56, 25, 27, 79, 4]
    for std_num in standard_view_clips:
        change_resolution_crop("./standards/" + str(std_num) + "clip_eq.mp4", (1280, 720), filepath_to_write="./stds_res_equalized_crop/")

# generate_car_horn_siren_augmented_clips()
# generate_merged_audio_set();

equalize_resolutions_crop()