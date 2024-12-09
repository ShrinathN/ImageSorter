#!/bin/python
'''
This scripts reads a list of files (newline separated in images_list.txt) and uses a LLaVA model running on koboldcpp to tag the images according to their contents
The tags are stored in a sqlite3 database
'''

from image_sort_helper import *
import sqlite3
import sys

#getting a list of all images
f = open("images_list.txt", "r")
raw_file_list = f.read()
f.close()
file_list = raw_file_list.split("\n")

#creating database if not already present
db = sqlite3.connect("data.sqlite3")

try:
    db.execute("CREATE TABLE data(file VARCHAR, tags VARCHAR);")
    db.commit()
except sqlite3.OperationalError:
    pass


#looping for all files
for current_file_path in file_list:
    #printing current file
    print(f'Processing {current_file_path[len(current_file_path)-current_file_path[::-1].find("/"):len(current_file_path)]}', end='...')
    sys.stdout.flush()
    
    #getting all the tags
    tags = simple_get_response(current_file_path, "List all the keywords which can be used to search for this image. Output only comma separated keywords.", "You are an image inspecting service, study the image thoroughly and respond describing its contents. Include information if the image is a screenshot, photograph, computer generated image etc.")
    tags = tags.replace('"',"")
    print(tags)
    
    #inserting into database
    try:
        db.execute(f'INSERT INTO data VALUES("{current_file_path}", "{tags}");')
        db.commit()
    except:
        db.commit()
        db.close()
        exit()
    exit()
