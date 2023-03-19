from generate_images import get_text
from tiktok_tts import tiktok_tts_generation
import os
from dotenv import load_dotenv

def generate_wav_files(text_array, id, output_folder_path):
    session_id = os.getenv("TIKTOK_SESSION_ID")
    for index in range(len(text_array)):
        text = text_array[index]
        output_path = output_folder_path + str(id) + "_" + str(index) + ".mp3"
        tiktok_tts_generation(text, output_path, session_id)
        #audio = AudioSegment.from_file(output_path, format="mp3")
        #audio = audio.speedup(playback_speed=1.1, chunk_size=100, crossfade=25)
        #audio.export(output_path, format="mp3")

if __name__ == "__main__":
    load_dotenv()
    text_csv_path = "data/text.csv"
    prompts_csv_path = "data/prompts.csv"
    output_folder_path = "data/sounds/"
    results_dict = get_text(text_csv_path, prompts_csv_path)
    text_array = results_dict["text_array"]
    id = results_dict["id"]
    generate_wav_files(text_array, id, output_folder_path)

"""
def generate_mp3_files_old_old(text_array, id, output_folder_path):
    for index in range(len(text_array)):
        text = text_array[index]
        language = 'en'
        tts_object = gTTS(text=text, lang=language, slow=False)
        output_path = output_folder_path + str(id) + "_" + str(index) + ".mp3"
        tts_object.save(output_path)
        os.system(output_path)
"""

"""
def generate_mp3_files_old(text_array, id, output_folder_path):
    for index in range(len(text_array)):
        text = text_array[index]
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)
        voices = engine.getProperty('voices')
        for voice in voices:
            print(voice.id)
        engine.setProperty('voice', voices[0].id)
        output_path = output_folder_path + str(id) + "_" + str(index) + ".mp3"
        engine.save_to_file(text, output_path)
        engine.runAndWait()
"""