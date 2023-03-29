from utils import *
import pandas as pd
import numpy as np
import os

import argparse
import argument
args = argument.get_args()

csvFilePath = args.csvFilePath
jsonFilePath = args.jsonFilePath #
video_path = args.video_path
crop_image_path = args.crop_image_path #
name_camera = args.name_camera
gif_flag = args.gif_flag
save_gif = args.save_gif #
type_crop = args.type_crop


# csvFilePath = r'C:\\Users\\Mavara\\Desktop\\person_reid\\Implementation\\annotaion_video\\darb1_D3_1_1part.csv'
# jsonFilePath = r'C:\\Users\\Mavara\\Desktop\\person_reid\\Implementation\\annotaion_video\\darb1_D3_1_1part.json'
# video_path=r'C:\\Users\\Mavara\\Desktop\\person_reid\\Implementation\\annotaion_video\\video\\D3_1_1part.mp4'
csv_to_json(csvFilePath=csvFilePath, jsonFilePath=jsonFilePath)

df = pd.read_json(jsonFilePath)
# print(df[['frame']].max)
# print(df)

if args.type_crop == "normal" :
    fps = crop_normal(df, csvFilePath=csvFilePath, name_camera=name_camera, category_crop_image_path=crop_image_path, video_path=video_path)
elif args.type_crop == "smaller" :
    fps = crop_frame_smaller_size(df, csvFilePath=csvFilePath, category_crop_image_path=crop_image_path, video_path=video_path, name_camera=name_camera)
elif args.type_crop == "padding" :
    fps = crop_frame(df, name_camera=name_camera, csvFilePath =csvFilePath, category_crop_image_path=crop_image_path, video_path=video_path)

if gif_flag:
    make_gif(frame_folder=crop_image_path, name_camera=name_camera, save_gif=save_gif, fps=fps)       

  
