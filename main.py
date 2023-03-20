import os
from dotenv import load_dotenv
import datetime
import csv
import openai
from openai_api import openai_request, data_to_files
from generate_images import get_text, generate_images
from speech_creation import generate_wav_files
from generate_video import combine_sounds, generate_video
from tiktok_formatting import format_video

if __name__ == "__main__":
    """
    load_dotenv()
    data = openai_request()
    text_path = "data/text.csv"
    prompts_path = "data/prompts.csv"
    data_to_files(text_path, prompts_path, data)
    output_folder_path = "data/images/"
    results_dict = get_text(text_path, prompts_path)
    text_array = results_dict["text_array"]
    id = results_dict["id"]
    prompt = results_dict["prompt"]
    output_caption_path = output_folder_path + str(id) + "_caption" + ".jpg"
    prompt_text = ["GPT 3.5 STORY", "Prompt: " + prompt]
    generate_images(text_array, id, output_folder_path, prompt_text, output_caption_path)
    output_folder_path = "data/sounds/"
    generate_wav_files(text_array, id, output_folder_path)
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
    input_video_path = output_video_path
    output_video_path = input_video_path.replace(".mp4", "_final.mp4")
    format_video(input_video_path, output_video_path)
    """
    chatgpt_tags = "#chatgpt #chatgpttutorial #whatischatgpt #chatgptexplained #chatgpt4 #chatgptai #openaichatgpt #chatgptexamples #howtousechatgpt"
    reddit_video_tags = "#reddit #videosifoundfromreddit #funnyvideos #redditvideos #funnyredditvideos #videosifoundonreddit #video #redditcompilation #askreddit"
    caption = "CHAT GPT 3.5 STORIES \n" + chatgpt_tags + " " + reddit_video_tags
    print(caption)