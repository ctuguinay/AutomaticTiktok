import os
from dotenv import load_dotenv
import datetime
import csv
import openai

def openai_request():

    # Prompt the user for text input
    prompt = input("Enter your prompt: ")
    keyword = input("Enter your keyword: ")

    openai.api_key = os.getenv("OPENAI_API_KEY")

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
                {"role": "system", "content": "You are a whimsical storyteller."},
                {"role": "user", "content": prompt}
        ],
        max_tokens=200
    )

    # Print the API response
    text = response['choices'][0]['message']['content'].strip().replace("\"", "")
    return [prompt, keyword, text]

def data_to_files(text_path, prompts_path, data):
    current_date = datetime.datetime.now().strftime("%m_%d_%y")
    prompt = data[0]
    keyword = data[1]
    text = data[2]
    text_row_data = [text, "true"]
    prompt_row_data = [current_date + "_" + keyword, prompt]

    # Open the CSV file in append mode
    with open(text_path, mode="a", newline="\n") as text_file:

        # Create a CSV writer object
        csv_writer = csv.writer(text_file)

        # Write the new row to the CSV file
        csv_writer.writerow(text_row_data)

    # Cleanup by closing the CSV file
    text_file.close()

    # Open the CSV file in append mode
    with open(prompts_path, mode="a", newline="\n") as prompts_file:

        # Create a CSV writer object
        csv_writer = csv.writer(prompts_file)

        # Write the new row to the CSV file
        csv_writer.writerow(prompt_row_data)

    # Cleanup by closing the CSV file
    prompts_file.close()

if __name__ == "__main__":
    load_dotenv()
    data = openai_request()
    text_path = "data/text.csv"
    prompts_path = "data/prompts.csv"
    data_to_files(text_path, prompts_path, data)