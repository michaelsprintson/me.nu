import os
import io
from collections import defaultdict
import json

"""
This file reads menu OCR results from myfile.txt and dumps json dictionary of menu item to price
"""



#print(os.getcwd())
pref = open("menu_read\pref_sample.txt", "r") #load user preferences txt
pref_lines = pref.readlines()
budget = float(pref_lines[0].strip())
eats_meat = bool(pref_lines[1].strip())
user_likes = (pref_lines[2].strip().split())


menu = io.open("ocr\myfile.txt", "r", encoding="utf-8")
menu_lines = menu.readlines()
#print(len(menu_lines)), 'l'

remove_bad = [] # empty list to hold raw lines of the cleaned up full menu

# get rid of the random numbers from OCR and the menu headings
for lineidx in range(len(menu_lines)):
    # print (lineidx, menu_lines[lineidx])
    item = menu_lines[lineidx]
    if ((len(item) > 4) and not (len(item) > 1 and not item[0].isdigit() and not item[1].isdigit())):
       # print(item, 'added')
        remove_bad.append(menu_lines[lineidx])

#print(len(remove_bad), 'the number of lines in menu ')


# getting the end index for each section of the menu
# each section is a section of the dishes, or the prices of the dishes
for lineidx in range(len(remove_bad)):
    if (remove_bad[lineidx][0]).isdigit():  # if its a price
        sec1item = lineidx
        # print (sec1item, 'sec1item')
        break

for lineidx in range(sec1item, len(remove_bad)):
    if not (remove_bad[lineidx][0]).isdigit():
        sec1price = lineidx
        print (sec1price, 'sec1')
        # print (sec1price, 'sec1price')
        break

for lineidx in range(sec1price, len(remove_bad)):
    if (remove_bad[lineidx][0]).isdigit():
        sec2item = lineidx
        # print (sec2item, 'sec2item')

        break

for lineidx in range(sec2item, len(remove_bad)):
    if not (remove_bad[lineidx][0]).isdigit():
        sec2price = lineidx
        break

for lineidx in range(sec2price, len(remove_bad)):
    if (remove_bad[lineidx][0]).isdigit():
        sec3item = lineidx
        #print(sec3item, 'sec3i')
        break

for lineidx in range(sec3item, len(remove_bad)):
    if not (remove_bad[lineidx][0]).isdigit():
        sec3price = lineidx
        #print (sec3price, 'sec3')
        break

sec1 = remove_bad[0: sec1item]
sec1prices = remove_bad[sec1item: sec1price]
sec2 = remove_bad[sec1price: sec2item]
sec2prices = remove_bad[sec2item: sec2price]
sec3 = remove_bad[sec2price: sec3item]
sec3prices = remove_bad[sec3item: ]

# print(len(sec3))
# print(sec3)
#
# print('------------------')
# print(len(sec3prices))
# print(sec3prices)

menu_dict = defaultdict()

for sec1idx in range(len(sec1)): #add the first sections entries
    menu_dict[sec1[sec1idx].strip()] = float(sec1prices[sec1idx].strip())

for sec2idx in range(len(sec2)): #add the second sections entries
    menu_dict[sec2[sec2idx].strip()] = float(sec2prices[sec2idx].strip())

for sec3idx in range(len(sec3)): #add the third sections entries
    menu_dict[sec3[sec3idx].strip()] = float(sec3prices[sec3idx].strip())


print (menu_dict)

#print(len(menu_dict))
newdict = {}
for dish in menu_dict:
    if menu_dict[dish] <= budget:
        newdict[dish] = menu_dict[dish]

print ("_______________________")
print (newdict)
#print (len(newdict))


# with open('cleaned_menu_dict.json', 'w') as cleaned_menu:
#     json.dump(menu_dict, cleaned_menu)
#
# #
