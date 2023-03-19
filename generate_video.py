from moviepy.editor import VideoFileClip, AudioFileClip, ImageClip, CompositeVideoClip, concatenate_videoclips
from generate_images import get_text
import os
from pydub import AudioSegment
from mutagen.mp3 import MP3

def combine_sounds(sound_paths):
    # Create an empty audio segment to append to
    combined_audio = AudioSegment.empty()

    # List of audio files to combine
    audio_files = sound_paths

    final_underscore_string = audio_files[0].split("_")[-1]
    main_audio_file_path = audio_files[0].replace("_" + final_underscore_string, ".wav")

    length_dict = {}
    # Loop through the list of audio files and append each one to the combined audio
    for audio_file in audio_files:
        audio = AudioSegment.from_file(audio_file)
        combined_audio = combined_audio + audio
        length_dict[audio_file] = MP3(audio_file).info.length

    # Export the combined audio as an mp3 file
    combined_audio.export(main_audio_file_path, format="mp3")
    return length_dict, main_audio_file_path

def generate_video(input_video_path, sound_path, image_paths, length_dict, output_path):
    # Load the input video and the image
    video_clip = VideoFileClip(input_video_path)
    audio_clip = AudioFileClip(sound_path)
    video_clip = video_clip.set_audio(audio_clip)
    composite_clip = concatenate_videoclips([video_clip])
    current_point = 0
    for index in range(len(image_paths)):
        image_path = image_paths[index]
        image_clip = ImageClip(image_path)
        sound_path = image_path.replace(".jpg", ".mp3").replace("images", "sounds")
        sound_duration = length_dict[sound_path]

        # Set the duration of the image clip to be the same as the duration of the video clip
        image_clip = image_clip.set_duration(sound_duration)

        # Position the image clip in the center of the video clip
        image_clip = image_clip.set_position(("center", "center"))

        # Composite image and video.
        composite_clip = CompositeVideoClip([composite_clip, image_clip.set_start(current_point)], size=video_clip.size)
        # Set up the output file path and write the composite clip to the output file

        current_point = current_point + sound_duration
    
    composite_clip.write_videofile(output_path)

    # Cleanup by closing the clips
    video_clip.close()
    image_clip.close()
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
    input_video_path = "data/videos/videoplayback.webm"
    output_video_path = "data/videos/output.mp4"
    generate_video(input_video_path, main_audio_file_path, image_paths, length_dict, output_video_path)