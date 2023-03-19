from generate_images import get_text
#from gtts import gTTS
import pyttsx3

"""
def generate_mp3_files_old(text_array, id, output_folder_path):
    for index in range(len(text_array)):
        text = text_array[index]
        language = 'en'
        tts_object = gTTS(text=text, lang=language, slow=False)
        output_path = output_folder_path + str(id) + "_" + str(index) + ".mp3"
        tts_object.save(output_path)
        os.system(output_path)
"""

def generate_mp3_files(text_array, id, output_folder_path):
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

if __name__ == "__main__":
    text_csv_path = "data/text.csv"
    prompts_csv_path = "data/prompts.csv"
    output_folder_path = "data/sounds/"
    results_dict = get_text(text_csv_path, prompts_csv_path)
    text_array = results_dict["text_array"]
    id = results_dict["id"]
    generate_mp3_files(text_array, id, output_folder_path)