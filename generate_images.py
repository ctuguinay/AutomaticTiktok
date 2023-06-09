from PIL import Image, ImageDraw, ImageFont
import csv
import textwrap

def get_text(text_csv_path, prompts_csv_path, word_count=18):

    text = None
    with open(text_csv_path, mode="r") as text_file:
        csv_reader = csv.reader(text_file)
        latest_row = None
        for row in csv_reader:
            latest_row = row
            text = latest_row[0]
    
    text = text.replace('"', "")
    split_text = text.split()
    text_array = []
    current_string = ""
    count = 0
    for index in range(len(split_text)):
        count = count + 1
        word = split_text[index]
        current_string = current_string + " " + word
        if count == word_count:
            text_array.append(current_string)
            current_string = ""
            count = 0
    text_array.append(current_string)

    id = None
    prompt = None
    with open(prompts_csv_path, mode="r") as prompt_file:
        csv_reader = csv.reader(prompt_file)
        latest_row = None
        for row in csv_reader:
            latest_row = row
            id = latest_row[0]
            prompt = latest_row[1]

    return {"text_array": text_array, "id": id, "prompt": prompt}
        
def generate_images(text_array, id, output_folder_path, prompt_text, output_caption_path):
    for index in range(len(text_array)):
        # Set up the parameters for the image
        image_width = 600
        image_height = 180
        background_color = (0, 0, 0)
        text_color = (255, 255, 255)
        text_size = 20
        text = text_array[index]

        # Create a new image with the specified width and height, and fill it with the background color
        image = Image.new("RGB", (image_width, image_height), background_color)

        # Get a font object for the specified font and size
        font = ImageFont.truetype("CENTURY.TTF", text_size)

        # Get a draw object for the image
        draw = ImageDraw.Draw(image)

        lines = textwrap.wrap(text, width=50)
        number_of_lines = len(lines)
        _, top, _, bottom = font.getbbox(lines[0])
        y_text = (image_height * (2/3)) + (((number_of_lines / 2) - 1)*((top - bottom)*2/3))
        for line_index in range(len(lines)):
            line = lines[line_index]
            left, top, right, bottom = font.getbbox(line)
            width = right - left
            height = top - bottom
            draw.text(((image_width - width) / 2, y_text ), line, font=font, fill=text_color)
            y_text -= height

        # Save the image to a file
        image.save(output_folder_path + str(id) + "_" + str(index) + ".jpg")

        # Cleanup by closing the image and draw objects
        image.close()
        #draw.close()
    
    # Set up the parameters for the image
    image_width = 600
    image_height = 180
    background_color = (0, 0, 0)
    text_color = (255, 255, 255)
    text_size = 25

    # Create a new image with the specified width and height, and fill it with the background color
    image = Image.new("RGB", (image_width, image_height), background_color)

    # Get a font object for the specified font and size
    font = ImageFont.truetype("CENTURY.TTF", text_size)

    # Get a draw object for the image
    draw = ImageDraw.Draw(image)

    lines = textwrap.wrap(prompt_text[1], width=30)
    lines.insert(0, prompt_text[0])
    number_of_lines = len(lines)
    _, top, _, bottom = font.getbbox(lines[0])
    y_text = (image_height / 2) + (((number_of_lines - 1) / 2)*((top - bottom) * 1.2) + (top - bottom) * 1.5)
    for line_index in range(len(lines)):
        line = lines[line_index]
        left, top, right, bottom = font.getbbox(line)
        width = right - left
        height = top - bottom
        draw.text(((image_width - width) / 2, y_text ), line, font=font, fill=text_color)
        if line_index == 0:
            y_text -= (height * 2)
        else:
            y_text -= (height * 1.2)

    # Save the image to a file
    image.save(output_caption_path)

    # Cleanup by closing
    image.close()


if __name__ == "__main__":
    text_csv_path = "data/text.csv"
    prompts_csv_path = "data/prompts.csv"
    output_folder_path = "data/images/"
    results_dict = get_text(text_csv_path, prompts_csv_path)
    text_array = results_dict["text_array"]
    id = results_dict["id"]
    prompt = results_dict["prompt"]
    output_caption_path = output_folder_path + str(id) + "_caption" + ".jpg"
    prompt_text = ["GPT 3.5 STORY", "Prompt: " + prompt]
    generate_images(text_array, id, output_folder_path, prompt_text, output_caption_path)