# -*- coding: utf-8 -*-
"""
Created on Wed Aug 18 06:00:03 2021

@author: G
"""

import requests
import shutil
import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import imagehash
from PIL import Image
import nekos

#nekos.img("fox_girl")
#nekos.img("kemonomimi")

#img_type = ["neko", "fox_girl", "kemonomimi"]
#img_type = ["erokemo", "eroyuri", "eron", "erok", "erofeet"]
type_selection = 0
token = ''

batch_size = int(input("Enter Batch Size: "))
#batch_size = 49

#file_list = os.listdir("Nekos/A")
#file_list += os.listdir("Nekos/B")

valid_images = []
image_hashes = {}
curr_batch_filenames = []

for file in os.listdir("Nekos/A"):
    with Image.open(os.path.join("Nekos/A", file)) as img:
        image_hashes[imagehash.average_hash(img, 8)] = file
        
for file in os.listdir("Nekos/B"):
    with Image.open(os.path.join("Nekos/B", file)) as img:
        image_hashes[imagehash.average_hash(img, 8)] = file
        
for file in os.listdir("Nekos/U"):
    with Image.open(os.path.join("Nekos/U", file)) as img:
        image_hashes[imagehash.average_hash(img, 8)] = file

my_dpi = 286
loop_max_iterations = batch_size * 4


while token.lower() != 'q':
    token = input("q to quit: ")
    
    if token.lower() == 'q':
        break
    
    batch_counter = 0
    it_counter = 0
    curr_batch_filenames = [] #avoids edge case bug of finding same image in one batch run
    while batch_counter < batch_size and it_counter < loop_max_iterations:
        it_counter += 1
        print(f"{it_counter}/{loop_max_iterations}")
        
        if type_selection == len(img_type):
            type_selection = 0
            
        complete_url = nekos.img(img_type[type_selection])
        
        type_selection += 1
        
        #print(complete_url)
        
        filename = complete_url.split("/")[-1]
        
        #if filename in file_list:
        #    continue          
        
        try:
            r = requests.get(complete_url, stream = True)
        except requests.TimeoutError:
            print(f"URL timed out on url: {complete_url}")
            continue

        if r.status_code == 200:
            #print(f"{filename} opened.")
            r.raw.decode_content = True
            
            with open(filename, 'wb') as f:
                shutil.copyfileobj(r.raw, f)
                
            if filename in curr_batch_filenames:
                #print(f"Duplicate image already in current batch. {complete_url}")
                continue
                
            
            temp_hash = imagehash.average_hash(Image.open(filename), 8)
            if temp_hash in image_hashes: #Duplicate img check
                os.remove(filename)
                #print(f"Duplicate image already in dataset. {complete_url}")
                continue
            
            valid_images.append(filename)
            image_hashes[temp_hash] = filename
            curr_batch_filenames.append(filename)
            batch_counter += 1
            print(f"Image {batch_counter}/{batch_size} found: {complete_url}")
            #input("Enter if added:")
            
        else:
            print(f"{filename} unable to open.")

            
        
    
    if it_counter > batch_size*3:
        print(f"Exited early due to max it_counter ({it_counter} = {loop_max_iterations})")
    
    print(f"Displaying {len(valid_images)} images.")
    
    for v in range(len(valid_images)):
        plt.figure(figsize=(8, 8), dpi=my_dpi)
        plt.axis('off')
        print(f"Displaying image {v}/{len(valid_images)}: {valid_images[v]}")
        img = mpimg.imread(valid_images[v])
        imgplot = plt.imshow(img)
        plt.show()
        token = 'r'
        
        while token.lower() != 'y' and token.lower() != 'n' and token.lower() != 'q' and token.lower() != 's':
            token = input("y, n, or s: ")
            
            if token.lower() == 'y':
                shutil.move(valid_images[v], "Nekos/A")
                print(f"{valid_images[v]} classified as A.")
            elif token.lower() == 'n':
                shutil.move(valid_images[v], "Nekos/B")
                print(f"{valid_images[v]} classified as B.")
            elif token.lower() == 's':
                #os.remove(valid_images[v])
                shutil.move(valid_images[v], "Nekos/U")
                print(f"{valid_images[v]} moved to U.")
            
        #file_list.append(filename)
        #print(f"{valid_images[v]} has been added.")
        
    
    valid_images = []


"""
while token.lower() != 'q':
    for i in range(len(url2)):
        for j in range (2):
            complete_url = f"{url1}{url_[j]}{num:03d}{url2[i]}"
            #print(complete_url)
            
            filename = complete_url.split("/")[-1]
            print(complete_url)
            
            #if filename in file_list:
            #    continue          
            
            r = requests.get(complete_url, stream = True)
    
            if r.status_code == 200:
                r.raw.decode_content = True
                
                with open(filename, 'wb') as f:
                    shutil.copyfileobj(r.raw, f)
                    
                temp_hash = imagehash.average_hash(Image.open(filename), 8)
                if temp_hash in image_hashes:
                    os.remove(filename)
                    continue
                    
                #print("Image successfully Downloaded: ", filename)
                plt.figure(figsize=(8, 8), dpi=my_dpi)
                plt.axis('off')
                img = mpimg.imread(filename)
                imgplot = plt.imshow(img)
                plt.show()
                
                while token.lower() != 'y' and token.lower() != 'n' and token.lower() != 'q':
                    token = input("y or n: ")
                    
                    if token.lower() == 'y':
                        shutil.move(filename, "Nekos/A")
                    elif token.lower() == 'n':
                        shutil.move(filename, "Nekos/B")
                    
                token = 'r'
                #file_list.append(filename)
                image_hashes[temp_hash] = filename
                print(f"{filename} has been added.")
            
    num += 1
    """
