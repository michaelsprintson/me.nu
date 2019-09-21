import io
import os
import re
import json

# This is 
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:\Users\User\Documents\me.nu\ocr\ocrtest1-824f812b3427.json"



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




def detect_text(path):
    """Detects text in the file."""
    from google.cloud import vision
    import io

    file1 = io.open("ocr\myfile.txt","w", encoding="utf-8")


    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations
    #print('Texts:')

    #print(type(texts[0].description))
    new_texts = texts[0].description.split('\n')
    #print(new_texts)

    for text in new_texts:
        text_no_chinese = re.sub("([^\x82\x00-\x7F])+","", text)
        file1.writelines(text_no_chinese + '\n')

    file1.close()


    # for count_text_index, text in enumerate(texts):

    #     print('\n{} {}"'.format(count_text_index, text.description))
    #     file1.writelines(text.description)

    #     vertices = (['({},{})'.format(vertex.x, vertex.y)
    #                 for vertex in text.bounding_poly.vertices])

    #     #print('bounds: {}'.format(','.join(vertices)))



# run test with a picture
#detect_text('ocr\menupictures\pic3.jpg')
detect_text('ocr\menupictures\pic7.jpg')