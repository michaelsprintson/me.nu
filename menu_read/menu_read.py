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
#budget = float(pref_lines[0].strip())
budget = 100.0
eats_meat = bool(pref_lines[1].strip())
user_likes = (pref_lines[2].strip().split())


#menu = io.open("ocr\myfile.txt", "r", encoding="utf-8")
#menu = io.open("ocr\menu_tests\soups.txt", "r", encoding="utf-8")
#menu = io.open("ocr\menu_tests\weirdapps.txt", "r", encoding="utf-8")
menu = io.open("ocr\menu_tests\pic5test.txt", "r", encoding="utf-8")
#menu = io.open("ocr\menu_tests\pic7test.txt", "r", encoding="utf-8")



menu_lines = menu.readlines()
print( menu_lines, '_____________________________')
# print(len(menu_lines)), 'l'

remove_bad = [] # empty list to hold raw lines of the cleaned up full menu

# get rid of the random numbers from OCR and the menu headings
for lineidx in range(len(menu_lines)):
    # print (lineidx, menu_lines[lineidx])
    item = menu_lines[lineidx].strip()
    if (len(item) >= 4) and (item[3].isdigit() or ((not item[0].isdigit() and item[1].isdigit()))):
        #((len(item) > 4) and not (len(item) > 1 and not item[0].isdigit() and not item[1].isdigit())):
        #print(item, 'added')
        remove_bad.append(menu_lines[lineidx])

# print(len(remove_bad), 'the number of lines in menu ')
# print (remove_bad)

# getting the end index for each section of the menu
# each section is a section of the dishes, or the prices of the dishes

def findidx(usemenu, findprice):
    for lineidx in range(len(usemenu)):
        if findprice:
            if (usemenu[lineidx][0]).isdigit():  # if its a price
                sectionidx = lineidx
                break
        else:  # if its a food item
            if not (usemenu[lineidx][0]).isdigit():
                sectionidx = lineidx
                break
        if lineidx == len(usemenu)- 1:
            return len(usemenu)- 1
    return sectionidx


sec1item = findidx(remove_bad, True)
sec1price = findidx(remove_bad[sec1item :], False) + sec1item

sec2item = findidx(remove_bad[sec1price :], True) + sec1price
sec2price = findidx(remove_bad[sec2item :], False) + sec2item

sec3item = findidx(remove_bad[sec2price :], True) + sec2price
sec3price = findidx(remove_bad[sec3item :], False) + sec3item


# for lineidx in range(len(remove_bad)):
#     if (remove_bad[lineidx][0]).isdigit():  # if its a price
#         sec1item = lineidx
#         print (sec1item, 'sec1item')
#         break
#
# for lineidx in range(sec1item, len(remove_bad)):
#     if not (remove_bad[lineidx][0]).isdigit():
#         sec1price = lineidx
#         print (sec1price, 'sec1price')
#         break
#
# for lineidx in range(sec1price, len(remove_bad)):
#     if (remove_bad[lineidx][0]).isdigit():
#         sec2item = lineidx
#         print (sec2item, 'sec2item')
#         break
#
# for lineidx in range(sec2item, len(remove_bad)):
#     if not (remove_bad[lineidx][0]).isdigit():
#         sec2price = lineidx
#         print (sec2price, 'sec2price')
#         break
#
# for lineidx in range(sec2price, len(remove_bad)):
#     if (remove_bad[lineidx][0]).isdigit():
#         sec3item = lineidx
#         print(sec3item, 'sec3i')
#         break
#
# for lineidx in range(sec3item, len(remove_bad)):
#     if not (remove_bad[lineidx][0]).isdigit():
#         sec3price = lineidx
#         print (sec3price, 'sec3')
#         break

sec1 = remove_bad[0: sec1item]
print (sec1,'sec1')
print ("_______________")
sec1prices = remove_bad[sec1item: sec1price]
print (sec1prices, '1prices')

sec2 = remove_bad[sec1price: sec2item]
print (sec2,'sec2')
sec2prices = remove_bad[sec2item: sec2price]
print ("_______________")


sec3 = remove_bad[sec2price: sec3item]
print (sec3,'sec3')
print ("_______________")

sec3prices = remove_bad[sec3item: ]

# print(len(sec3))
# print(sec3)
#
# print('------------------')
# print(len(sec3prices))
# print(sec3prices)

menu_dict = defaultdict()

for sec1idx in range(len(sec1)): # add the first sections entries
    menu_dict[sec1[sec1idx].strip()] = float(sec1prices[sec1idx].strip())

for sec2idx in range(len(sec2)): # add the second sections entries
    menu_dict[sec2[sec2idx].strip()] = float(sec2prices[sec2idx].strip())

for sec3idx in range(len(sec3)): # add the third sections entries
    menu_dict[sec3[sec3idx].strip()] = float(sec3prices[sec3idx].strip())

print (len(menu_dict))
print (menu_dict)


# print(len(menu_dict))
meats = {"Beef", "Pork", "Duck", "Chicken", "Lamb", "Blood", "Lung", "Meat", "Fish", "Clam", "Tripe", "Prawn", "Rib", "Tilapia"}


# filters out dishes for vegetarians or if over budget
newdict = {}
for dish in menu_dict:
    item = menu_dict[dish]
    if menu_dict[dish] <= budget:
        if not eats_meat:
            for meat in meats:
                if meat in dish:
                    nomeat = False
            if nomeat:
                 newdict[dish] = menu_dict[dish]
        else:
            newdict[dish] = menu_dict[dish]

#
# print (newdict)

# print ("_______________________")
# print (newdict)
# print (len(newdict))

#
# with open('cleaned_menu_dict.json', 'w') as cleaned_menu:
#     json.dump(newdict, cleaned_menu)
#
# #
