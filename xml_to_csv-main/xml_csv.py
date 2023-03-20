import pandas as pd
import xml.etree.ElementTree as et 
import csv
import os
import argparse
temp=[]
# xtl & ytl is string
parser = argparse.ArgumentParser(description='xml_csv')
parser.add_argument('--input_xml_path',default="C:\\Users\\Mavara\\Desktop\\person_reid\\annotaion_video\\xml\\darb1_D2_1_1part.xml", type=str, help='.path of xml for video')
parser.add_argument('--output_csv_path',default='C:\\Users\\Mavara\\Desktop\\person_reid\\annotaion_video\\hello.csv', type=str, help='.path of xml for video')

arg = parser.parse_args()
input_xml_path = arg.input_xml_path
output_csv_path = arg.output_csv_path
root = et.parse(input_xml_path).getroot()
# root = et.parse('./annotations.xml').getroot()
for image_tag in root:
        image = {}
        for key, value in image_tag.items():
            image[key] = value
        for box_tag in image_tag.iter('box'):

            
            #box = {'type': 'box'}
            box = {}
            for key, value in box_tag.items():
                box[key] = value
            # print('box:',box)
            z = {**image, **box}
            temp.append(z)
        # print('image:',image)
import numpy as np
print('temp:',temp)
field_names = ['id','label','source','frame','outside','occluded','keyframe','xtl','ytl','xbr','ybr','rotation','z_order']
df = pd.DataFrame(temp, columns =field_names)
print(df)
df['w'] = df['xbr'].astype(float) - df['xtl'].astype(float) 
df['h'] = df['ybr'].astype(float)  - df['ytl'].astype(float) 
df = df[['id','label','frame','outside','occluded','xtl','ytl','w','h']]
df['frame'] = df['frame'].astype(int)
df['id'] = df['id'].astype(int)
df = df.sort_values(by = 'frame')
df.to_csv(output_csv_path)
