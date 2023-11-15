from animator import animator
from converter import convert
from spliter import vid_spliter, gif_spliter
from asciichars import getSetAscii
import os
import shutil 
import argparse
import tkinter as tk
from tkinter import filedialog
import requests
import re

URL_REGEX = re.compile(
        r'^(?:http|ftp)s?://'
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
        r'(?::\d+)?'
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

FRAME_RESULT_FOLDER = "data/vidframes"
CONVERTED_FRAME_PATH = "data/frames"
TEMP_IMPORTED_MEDIA = "data/temp"

def convert_video(width, delay, generate, vid_path, asscii_set, is_reversed = True):
    if generate : 
        if os.path.isdir(FRAME_RESULT_FOLDER) :
            shutil.rmtree(FRAME_RESULT_FOLDER)
            
        if os.path.isdir(CONVERTED_FRAME_PATH) :
            shutil.rmtree(CONVERTED_FRAME_PATH)
            
        os.mkdir(FRAME_RESULT_FOLDER)
        os.mkdir(CONVERTED_FRAME_PATH)
        
        vid_spliter(vid_path,FRAME_RESULT_FOLDER)
        ascii_char = getSetAscii(asscii_set)
        
        if is_reversed :
            ascii_char.reverse()
        
        print("Converting ...")
        for i, filename in enumerate(os.listdir(FRAME_RESULT_FOLDER)):
            convert(f"{FRAME_RESULT_FOLDER}/{filename}", str(i), CONVERTED_FRAME_PATH, width, ascii_char)  
    animator(CONVERTED_FRAME_PATH, delay)


def convert_image(width, delay, generate, vid_path,asscii_set, is_reversed = True) :
    if generate : 
        if os.path.isdir(FRAME_RESULT_FOLDER) :
            shutil.rmtree(FRAME_RESULT_FOLDER)
            
        if os.path.isdir(CONVERTED_FRAME_PATH) :
            shutil.rmtree(CONVERTED_FRAME_PATH)
            
        os.mkdir(CONVERTED_FRAME_PATH)
        
        ascii_char = getSetAscii(asscii_set)
        
        if is_reversed :
            ascii_char.reverse()
        
        print("Converting ...")
        convert(vid_path, "1", CONVERTED_FRAME_PATH, width, ascii_char)  
    animator(CONVERTED_FRAME_PATH, delay)

def convert_gif(width, delay, generate, vid_path,asscii_set, is_reversed = True) :
    if generate : 
        if os.path.isdir(FRAME_RESULT_FOLDER) :
            shutil.rmtree(FRAME_RESULT_FOLDER)
            
        if os.path.isdir(CONVERTED_FRAME_PATH) :
            shutil.rmtree(CONVERTED_FRAME_PATH)
            
        os.mkdir(FRAME_RESULT_FOLDER)
        os.mkdir(CONVERTED_FRAME_PATH)
        
        gif_spliter(vid_path, FRAME_RESULT_FOLDER)
        ascii_char = getSetAscii(asscii_set)
        
        if is_reversed :
            ascii_char.reverse()
        
        print("Converting ...")
        for i, filename in enumerate(os.listdir(FRAME_RESULT_FOLDER)):
            convert(f"{FRAME_RESULT_FOLDER}/{filename}", str(i), CONVERTED_FRAME_PATH, width, ascii_char)  
    animator(CONVERTED_FRAME_PATH, delay)

def open_file_dialog() -> str :
    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename(filetypes=[("MP4 files", "*.mp4"), ("Image files", "*.png;*.jpg;*.jpeg;*.gif"),])
        
    if file_path:
        return file_path
    else:
        return ""

def import_data(url):
    file_Type = ".png"
    if url.endswith((".mp4", ".avi")) :
        file_Type = ".mp4"
    if url.endswith((".gif")) :
        file_Type = ".gif"
        
    img_data = requests.get(url).content
    
    with open(f"{TEMP_IMPORTED_MEDIA}/tmp{file_Type}", 'wb') as handler:
        handler.write(img_data)
        
    return file_Type

def args_parse() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='A converter to make image and video use ascii, do whatever you want with it :), by Weg895')
    parser.add_argument('-c', '--convert', metavar='vid_path', dest='vid_path', help='the path of the media you want to convert (if not set and the load parameter is not passed, a window will appeard to select a file)', default=None, type=str)
    parser.add_argument('-a', '--ascii', metavar='ascii_set', dest='ascii_set', help='Select the acsii charater set used to convert the image', choices=[1, 2, 3], default=3, type=int)
    parser.add_argument('-w', '--width',  metavar='width', dest='width', help="set the width of the converted media", default=100, type=int)
    parser.add_argument('-d', '--d',  metavar='delay', dest='delay', help="Set the delay of between each redered image only affect animated gif and video", default=0.05, type=float)
    parser.add_argument('-r', '--reversed', dest='reversed', action='store_false', help="If you want to revese the grayscale of the image (white becomes black, etc.)", default=True)
    parser.add_argument('-l', '--load', dest='load', action='store_true', help="Load a previously converted media")
    parser.add_argument('-s', '--cls', dest='enable_cls', action='store_true', help="if the media is a video or animated gif, enable clearing the console after redering the frames (not recommended, it causes a lot of flickering)")
    return parser.parse_args()

def main():
    args = args_parse()
    vid_path = args.vid_path
    width = args.width
    delay = args.delay
    generate = not args.load
    asscii_set = args.ascii_set
    is_reversed = args.reversed
    
    if not vid_path :
        vid_path = open_file_dialog()
    
    if os.path.isdir(TEMP_IMPORTED_MEDIA) :
        shutil.rmtree(TEMP_IMPORTED_MEDIA)
         
    os.mkdir(TEMP_IMPORTED_MEDIA)
    if re.match(URL_REGEX, vid_path) is not None :
        vid_path = f"{TEMP_IMPORTED_MEDIA}/tmp{import_data(vid_path)}"
    
    if vid_path.endswith((".mp4", ".avi")) :
        convert_video(width, delay, generate, vid_path, asscii_set, is_reversed)
    elif vid_path.endswith(('.png', '.jpg', '.jpeg')) :
        convert_image(width, delay, generate, vid_path, asscii_set, is_reversed)
    elif vid_path.endswith(".gif") :
        convert_gif(width, delay, generate, vid_path, asscii_set, is_reversed)
    else :
        print("The selected file is not valid. The accepted extentions are :\n.gif .png .jpg .jpeg .mp4")
        
if __name__ == "__main__":
    main()
