import io
import os
import re
import json
from google.cloud import vision

# Set path to key 
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\shjan\Downloads\ocrtest1-bf8fefb197a6.json"

# # Imports the Google Cloud client library
# from google.cloud import vision
# from google.cloud.vision import types

# # Instantiates a client
# client = vision.ImageAnnotatorClient()

# # The name of the image file to annotate
# file_name = os.path.abspath('pic1.png')

# # Loads the image into memory
# with io.open(file_name, 'rb') as image_file:
#     content = image_file.read()

# image = types.Image(content=content)
# # Performs label detection on the image file
# response = client.label_detection(image=image)
# labels = response.label_annotations

# print('Labels:')
# for label in labels:
#     print(label.description)


def load_words():
    with open(r"ocr\words_alpha.txt") as word_file:
        valid_words = set(word_file.read().split())
    return valid_words


def detect_text(path, savepath):
    """Detects text in the file."""

    file1 = io.open("ocr\\menu_tests\\" + savepath + ".txt","w", encoding="utf-8")
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)
    response = client.text_detection(image=image)
    texts = response.text_annotations

    for text in texts[0].description.split('\n'):
        text_lst = re.sub("([^\x82\x00-\x7F])+"," ", text).split()
        
        first_word = text_lst[0] if text_lst else ''
        if first_word and not first_word[-1].isdigit():
            first_word = first_word[:-1]
        
        file1.writelines(first_word + ' ' + ' '.join([word for word in text_lst[1:] if (len(word) > 2 and word.lower() in d)]) + '\n')

    file1.close()




# create dictionary
d = load_words()

# run test with normal pictures

# detect_text('ocr\menupictures\pic6.jpg', 'pic6test')


# run test with weird pictures

for i in range(1, 20):
    pic_loc = 'ocr\menupictures\weirdpic\wpic' + str(i) + '.jpg'
    weird_file_name = 'weirdfiletest' + str(i)
    detect_text(pic_loc, weird_file_name)