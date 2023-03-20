from moviepy.editor import VideoFileClip, AudioFileClip, ImageClip, CompositeVideoClip, concatenate_videoclips
from moviepy.editor import *
from generate_images import get_text
from pydub import AudioSegment
from mutagen.mp3 import MP3
import math

def combine_sounds(sound_paths):
    # Create an empty audio segment to append to
    combined_audio = AudioSegment.empty()

    # List of audio files to combine
    audio_files = sound_paths

    final_underscore_string = audio_files[0].split("_")[-1]
    main_audio_file_path = audio_files[0].replace("_" + final_underscore_string, ".mp3")

    length_dict = {}
    # Loop through the list of audio files and append each one to the combined audio
    for audio_file in audio_files:
        audio = AudioSegment.from_file(audio_file)
        combined_audio = combined_audio + audio
        length_dict[audio_file] = MP3(audio_file).info.length

    # Export the combined audio as an mp3 file
    combined_audio.export(main_audio_file_path, format="mp3")
    return length_dict, main_audio_file_path

def generate_video(input_video_path, sound_path, image_paths, length_dict, 
                   output_caption_path, output_path):
    # Load the input video and the image
    video_clip = VideoFileClip(input_video_path)
    video_clip_length = video_clip.duration
    audio_clip = AudioFileClip(sound_path)
    total_audio_length = audio_clip.duration
    scaling_factor = math.ceil(total_audio_length / video_clip_length)
    caption_clip = ImageClip(output_caption_path)
    caption_clip = caption_clip.set_duration(8)
    caption_clip = caption_clip.set_position(("center", "center"))
    video_clips = [video_clip]
    if scaling_factor > 1:
        for _ in range(scaling_factor):
            video_clips.append(video_clip)
    composite_clip = concatenate_videoclips(video_clips)
    composite_clip = composite_clip.set_audio(audio_clip)
    current_point = 0
    image_clips = []
    for index in range(len(image_paths)):
        image_path = image_paths[index]
        image_clip = ImageClip(image_path)
        sound_path = image_path.replace(".jpg", ".mp3").replace("images", "sounds")
        sound_duration = length_dict[sound_path]

        # Set the duration of the image clip to be the same as the duration of the video clip
        image_clip = image_clip.set_duration(sound_duration)

        # Position the image clip in the center of the video clip
        image_clip = image_clip.set_position(("center", "center"))

        image_clip.set_duration(sound_duration)
        image_clips.append(image_clip)
        current_point = current_point + sound_duration
    
    concat_clip = concatenate_videoclips(image_clips, method="compose").set_position(("center", "top"))
    composite_clip = CompositeVideoClip([composite_clip, concat_clip, caption_clip], size=video_clip.size)
    #composite_clip = CompositeVideoClip([composite_clip, caption_clip], size=video_clip.size)
    composite_clip = composite_clip.subclip(0, current_point)
    composite_clip.write_videofile(output_path)

    # Cleanup by closing the clips
    for video_clip in video_clips:
        video_clip.close()
    
    for image_clip in image_clips:
        image_clip.close()

    audio_clip.close()
    concat_clip.close()
    composite_clip.close()

if __name__ == "__main__":
    # Set up the input video file path and image file path
    text_csv_path = "data/text.csv"
    prompts_csv_path = "data/prompts.csv"
    output_folder_path = "data/sounds/"
    results_dict = get_text(text_csv_path, prompts_csv_path)
    text_array = results_dict["text_array"]
    id = results_dict["id"]
    sound_paths = []
    image_paths = []
    for index in range(len(text_array)):
        text = text_array[index]
        output_sound_path = output_folder_path + str(id) + "_" + str(index) + ".mp3"
        sound_paths.append(output_sound_path)
        output_image_path = output_sound_path.replace("mp3", "jpg").replace("sounds", "images")
        image_paths.append(output_image_path)
    length_dict, main_audio_file_path = combine_sounds(sound_paths)
    #input_video_path = "data/videos/background_1_short.mp4"
    input_video_path = "data/videos/background_1.mp4"
    output_video_path = main_audio_file_path.replace(".mp3", ".mp4").replace("sounds", "videos")
    output_caption_path = output_folder_path.replace("sounds", "images") + str(id) + "_caption" + ".jpg"
    generate_video(input_video_path, main_audio_file_path, image_paths, length_dict, 
                   output_caption_path, output_video_path)