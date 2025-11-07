import cv2
import numpy as np
import pandas as pd
import os
from utils import *
import json




def paint_image(image_path,filename,prompt:str):
    '''
    Takes image path and prompt, spawns GUI window, then saves paint mask and uses JSON file to link masks to dataset images
    
    
    
    '''
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(image_path)

    draw_img = img.copy()
    mask = np.zeros(img.shape[:2], dtype=np.uint8)

    drawing = False       # True while mouse pressed
    erasing = False        # True when erasing
    brush_size = 10

    def draw(event, x, y, flags, param):
        nonlocal drawing, erasing, draw_img, mask

        if event == cv2.EVENT_LBUTTONDOWN:
            drawing = True
            erasing = False
        elif event == cv2.EVENT_RBUTTONDOWN:
            drawing = True
            erasing = True
        elif event == cv2.EVENT_MOUSEMOVE:
            if drawing:
                color = (0, 255, 0) if not erasing else (0, 0, 255)
                cv2.circle(draw_img, (x, y), brush_size, color, -1)
                cv2.circle(mask, (x, y), brush_size, 255 if not erasing else 0, -1)
        elif event == cv2.EVENT_LBUTTONUP or event == cv2.EVENT_RBUTTONUP:
            drawing = False

    cv2.namedWindow("Annotator")
    cv2.setMouseCallback("Annotator", draw)

    print("PROMPT: " , prompt)

    print("[Controls]")
    print(" Left click + drag  = paint mask")
    print(" Right click + drag = erase")
    print(" +/- = change brush size")
    print(" s = save mask.png, r = reset, ESC = Save and Next Image")

    while True:
        cv2.imshow("Annotator", draw_img) 
        key = cv2.waitKey(1) & 0xFF

        if key == ord('s'):
            cv2.imwrite(f'masks/{filename.removesuffix(".png")}' + "_human_mask" + '.png', mask)
            print('Saved: masks/{filename}.png')
            #add to json linking file
            json_path = "img_masks_link.json"
            if os.path.exists(json_path):
                with open(json_path, "r") as f:
                    results = json.load(f)
            results[filename] = f'masks/{filename.removesuffix(".png")}' + "_human_mask" + '.png'
            with open(json_path, "w") as f:
                json.dump(results, f, indent=4)
            
        elif key == ord('r'):
            draw_img = img.copy()
            mask[:] = 0
            print("🔄 reset")
        elif key == ord('+') or key == ord('='):
            brush_size = min(brush_size + 2, 100)
            print(f"Brush size: {brush_size}")
        elif key == ord('-') and brush_size > 2:
            brush_size -= 2
            print(f"Brush size: {brush_size}")
        elif key == 27:  # ESC
            cv2.imwrite(f'masks/{filename.removesuffix(".png")}' + "_human_mask" + '.png', mask)
            print('Saved: masks/{filename}.png')
            #add to json linking file
            json_path = "img_masks_link.json"
            if os.path.exists(json_path):
                with open(json_path, "r") as f:
                    results = json.load(f)
            results[filename] = f'masks/{filename.removesuffix(".png")}' + "_human_mask" + '.png'
            with open(json_path, "w") as f:
                json.dump(results, f, indent=4)
            break

    cv2.destroyAllWindows()

#---------------------------

#Put path to excel file of your dataset
df = pd.read_excel("/home/phroog/Documents/columbia/dl/project/annotation_tool/data/Fourth Set (Summer 2025)/fourth_dataset.xlsx")

# === Setup ===
#set root path of the dataset
root_path = 'data/Fourth Set (Summer 2025)'

#load excel



#load existing masks  
json_path = "img_masks_link.json"
if os.path.exists(json_path):
    with open(json_path, "r") as f:
        links = json.load(f)
        existing_masks = [i for i in links.keys()]

#iterate through dataset, grab the identifier and the prompt to print out during image annotation
for im_filename in os.listdir(root_path):
    #if the mask already exists, skip it
    
    if im_filename in existing_masks:
        continue

    if im_filename.endswith(".png"):
        im_path = root_path + "/" + im_filename
        #print(im_path)
        iden = iden_from_filename(im_filename)
        view = view_from_filename(im_filename) #either 1 or 0 , equivalent to promp in excel file
        #grab the prompt from the excel
        row = df[df['identifier'] == iden]
        prompt = df[df['identifier'] == iden][f'prompt_{view}'].to_string()
        
        paint_image(im_path,im_filename,prompt)


#add pickup where left off tech

