import os
import cv2
# import Imagehash
from PIL import Image, ImageSequence


def vid_spliter(vid_path, result_folder) :
    print(f"Spliting {vid_path}")
    vid_cap = cv2.VideoCapture(vid_path)
    count = 0
    while True:
        success,image = vid_cap.read()
        if not success:
            break
        cv2.imwrite(os.path.join(result_folder,"{:d}.jpg".format(count)), image)
        count += 1 
        
def gif_spliter(gif_path, result_folder) :
    im = Image.open(gif_path)
    for i,frame in enumerate(ImageSequence.Iterator(im)):
        i += 1
        frame.save(f"{result_folder}/{i}.png")