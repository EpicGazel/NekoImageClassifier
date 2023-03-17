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
import numpy as np
import imagehash
from PIL import Image
import nekos

url1 = "https://cdn.nekos.life/neko/neko"
num = 388
#num = 476
url2 = [".png", ".jpg", ".jpeg"]
url_ = ["", "_"]
token = ''
valid_images = []

#batch_size = int(input("Enter Batch Size: "))
batch_size = 49

#file_list = os.listdir("Nekos/A")
#file_list += os.listdir("Nekos/B")

image_hashes = {}
for file in os.listdir("Nekos/A"):
    with Image.open(os.path.join("Nekos/A", file)) as img:
        image_hashes[imagehash.average_hash(img, 8)] = file
        
for file in os.listdir("Nekos/B"):
    with Image.open(os.path.join("Nekos/B", file)) as img:
        image_hashes[imagehash.average_hash(img, 8)] = file

my_dpi = 286



while token.lower() != 'q':
    token = input("q to quit: ")
    
    if token.lower() == 'q':
        print(f"Last num value for links was {num}, this may be off by 1.")
        break
    
    batch_counter = 0
    while batch_counter < batch_size:
        for i in range(len(url2)):
            for j in range (2):
                complete_url = f"{url1}{url_[j]}{num:03d}{url2[i]}"
                #print(complete_url)
                
                filename = complete_url.split("/")[-1]
                #print(complete_url)
                
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
                        print("Duplicate Image Skipped.")
                        continue
                        
                    valid_images.append(filename)
                    image_hashes[temp_hash] = filename
                    batch_counter += 1
                    print(f"Image {batch_counter}/{batch_size} found: {complete_url}")
        print(f"Num {num} completed.")
        num += 1
    
    
    for v in range(batch_size):
        plt.figure(figsize=(8, 8), dpi=my_dpi)
        plt.axis('off')
        img = mpimg.imread(valid_images[v])
        imgplot = plt.imshow(img)
        plt.show()
        token = 'r'
        
        while token.lower() != 'y' and token.lower() != 'n' and token.lower() != 'q':
            token = input("y or n: ")
            
            if token.lower() == 'y':
                shutil.move(valid_images[v], "Nekos/A")
            elif token.lower() == 'n':
                shutil.move(valid_images[v], "Nekos/B")
            
        #file_list.append(filename)
        print(f"{valid_images[v]} has been added.")
        
    
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
