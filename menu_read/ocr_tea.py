import os
import io
from collections import defaultdict
import json
import re
from google.cloud import vision

# set environment variable for google api credential
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] =  "apikey.json


"""
This file reads menu OCR results from myfile.txt and dumps json dictionary of menu item to price
"""




def load_words(filename):
    with open(filename) as word_file:
        valid_words = set(word_file.read().split())
    return valid_words


def detect_text(path, savepath):
    """Detects text in the file."""

    d = load_words('ocr/wa.txt')

    file1 = io.open("ocr/menu_tests/" + savepath +
                    ".txt", "w", encoding="utf-8")
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)
    response = client.text_detection(image=image)
    texts = response.text_annotations

    for text in texts[0].description.split('\n'):
        text_lst = re.sub("([^\x82\x00-\x7F])+", " ", text).split()

        first_word = text_lst[0] if text_lst else ''
        # if first_word and not first_word[-1].isdigit():
        #     first_word = first_word[:-1]
        
        if first_word:
            if first_word[0] in {"(", "0", "."}:
                continue

        file1.writelines(first_word + ' ' + ' '.join(
            [word for word in text_lst[1:] if (len(word) > 2 and word.lower() in d)]) + '\n')

    file1.close()

# os.chdir("/Users/shjan/Coding/me.nu/menu_read/")
#
# # create dictionary
# d = load_words()
#
# pic_loc = 'ocr/menupictures/shareteanocolor.jpg'
# test_file_name = 'shareteanocolor'
# detect_text(pic_loc, test_file_name)
