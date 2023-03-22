
import numpy as np
import os
import cv2
import pandas as pd
def csv_to_json(csvFilePath, jsonFilePath):
    import csv 
    import json 
    jsonArray = []
      
    #read csv file
    with open(csvFilePath, encoding='utf-8') as csvf: 
        #load csv file data using csv library's dictionary reader
        csvReader = csv.DictReader(csvf) 

        #convert each csv row into python dict
        for row in csvReader: 
            #add this python dict to json array
            jsonArray.append(row)
  
    #convert python jsonArray to JSON String and write to file
    with open(jsonFilePath, 'w', encoding='utf-8') as jsonf: 
        jsonString = json.dumps(jsonArray, indent=4)
        jsonf.write(jsonString)
# list_df[i][0] --> id
# list_df[i][1] --> label
# list_df[i][2] --> frame
# list_df[i][3] --> outside
# list_df[i][4] --> occluded
# list_df[i][5] --> xtl
# list_df[i][6] --> ytl
# list_df[i][7] --> w
# list_df[i][8] --> h

def min_max_wh(csvFilePath,df):  
    df1 = pd.read_csv(csvFilePath,index_col="id")
    print(df1)
    m = [[df1.loc[i]['w'].max() , df1.loc[i]['h'].max(),i] for i in np.unique(df['id'])]
    print("min_max_wh:",m)
    return m

def convert_DataFramToDict(df):  
  new_dict ={}
  for index,i in enumerate(np.unique(df['frame'])):
    top_level_key = i
    new_dict[top_level_key] = {}
    for idx,j in enumerate(df['frame']):
      if i==j:
        # print("index,i:",index,i,"idx,j:",idx,j)
        # print(df['target_id'][idx] , df['x'][idx],df['y'][idx],df['w'][idx],df['h'][idx])
        new_dict[top_level_key].update({df['id'][idx] : (df['x'][idx],df['y'][idx],df['w'][idx],df['h'][idx])})
  return new_dict

def prepare_category(category_crop_image_path ,current_frame ,idx ,image_crop1,name_camera ):
  #category_crop_image_path = "./frame_sequence"
  name = name_camera+"_F"+str(current_frame)+"_T"+str(idx)+ ".webP"
  name1= name[0:-5]
  #print(name1)
  ID  = name1.split('_')
  #new folder for each video
  each_video_path = category_crop_image_path + '/' + ID[0] 
  if not os.path.isdir(each_video_path):
      os.mkdir(each_video_path)
  #new folder for each label
  dst_path = each_video_path + '/' + ID[2] 
  if not os.path.isdir(dst_path):
      os.mkdir(dst_path)
  cv2.imwrite(dst_path + "/" + name , image_crop1)     # save current_frame as JPEG file

def crop_frame(df,csvFilePath='2.csv' ,category_crop_image_path="./frame_sequence",video_path='./sync_30_D2.mp4',name_camera="D3"):
  import cv2
  m= min_max_wh(csvFilePath,df)
  list_df = df.values.tolist()
#   new_dict = convert_DataFramToDict(df=df)
  vidcap = cv2.VideoCapture(video_path)
  fps = vidcap.get(cv2.CAP_PROP_FPS)
  print('fps:',fps)
  success,image = vidcap.read()
  frame = 0
  success = True
  cap = cv2.VideoCapture(video_path)
  current_frame = 0
  while True:
        if current_frame > int(df[['frame']].max()):
            break
        ret, image = cap.read()
        if ret:
            z = list(np.where(np.array(list(zip(*list_df))[3])==current_frame))[0]
            for ind , i in enumerate(z):
        
                if list_df[i][5]==1 or list_df[i][4] ==1 :
                        pass
                        # print('frame:',list_df[i][3],' id:',list_df[i][1],' outside:',list_df[i][4],' occluded:',list_df[i][5])
                else:    
                    
                    # print('z:',z)
                
                    print('star/ ind , i:' , ind , i , 'z:',z,'id:',list_df[i][1],'frame:',list_df[i][3])
                    l = np.where(np.array(list(zip(*m))[2])==list_df[i][1])[0]
                    
                    max_w_int = int(m[l[0]][0])
                    # max_w_int = int(m[list_df[i][1]==m[]][0]) 
                    max_h_int = int(m[l[0]][1])
                    print('ind , i:' , ind , i , 'max_h_int,max_w_int:',max_h_int,max_w_int,'list_df[i][1]:',list_df[i][1])
                    # print('frame , id, max_h_int, max_w_int:',list_df[i][3],list_df[i][1],max_h_int, max_w_int)   
                    x = int(list_df[i][6]) 
                    y = int(list_df[i][7]) 
                    w = int(list_df[i][8]) 
                    h = int(list_df[i][9])
                    # print('x,y,w,h:',x,y,w,h)
                    print('id:',list_df[i][1],'frame:',list_df[i][3],'m',m[l[0]],'x,y,w,h:',x,y,w,h)
                    if image is not None:
            
                        
                        #image_crop= image[int((y-(max_h_int/2))):int(y+(max_h_int/2)), int((x-(max_w_int/2))):int(x+(max_w_int/2))]
                        
                        if (y-((max_h_int-h)/2))<0 and (x-((max_w_int-w)/2))<0:
            

                            image_crop1= image[0:int(y+(max_h_int/2)), 0:int(x+(max_w_int/2))]
                            print('if/step0/image_crop.shape:',image_crop1.shape)
                            #image_crop1 = cv2.copyMakeBorder(src= image_crop,top=int(np.absolute((max_h_int-image_crop.shape[0])/2)),bottom= 0,left= int(np.absolute((max_w_int-image_crop.shape[1])/2)),right= 0, borderType=cv2.BORDER_CONSTANT, value = 0)
                            if max_h_int != image_crop1.shape[0] :
                                image_crop1 = cv2.copyMakeBorder(src= image_crop1,top=int(np.absolute((max_h_int-image_crop1.shape[0])/2)),bottom= int(np.absolute((max_h_int-image_crop1.shape[0])/2)),left=0,right= 0, borderType=cv2.BORDER_CONSTANT, value = 0)                     
                                print('if/step1/image_crop.shape/max_h_int != image_crop1.shape[0]:',image_crop1.shape)
                            if max_w_int != image_crop1.shape[1] :
                                image_crop1 = cv2.copyMakeBorder(src= image_crop1,top=0,bottom= 0,left=int(np.absolute((max_w_int-image_crop1.shape[1])/2)),right= int(np.absolute((max_w_int-image_crop1.shape[1])/2)), borderType=cv2.BORDER_CONSTANT, value = 0)
                                print('if/step2/image_crop.shape/max_w_int != image_crop1.shape[1]:',image_crop1.shape)

                        elif (y-((max_h_int-h)/2))<0:
                        
                            # print('elif1/x,y,w,h,max_h_int,y-((max_h_int-h)/2):',x,y,w,h,max_h_int,y-((max_h_int-h)/2))
                                image_crop1= image[0:int(y+h+((max_h_int-h)/2)), int((x-((max_w_int-w)/2))):int(x+w+((max_w_int-w)/2))]
                                print('elif1/step0/image_crop.shape:',image_crop1.shape)
                            #image_crop1 = cv2.copyMakeBorder(src= image_crop,top=int(np.absolute((max_h_int-image_crop.shape[0])/2)),bottom= 0,left= int(np.absolute((max_w_int-image_crop.shape[1])/2)),right= 0, borderType=cv2.BORDER_CONSTANT, value = 0)
                            
                            # print('elif1/image_crop1.shape:',image_crop1.shape)
                                if max_h_int != image_crop1.shape[0] :
                                    image_crop1 = cv2.copyMakeBorder(src= image_crop1,top=int(np.absolute((max_h_int-image_crop1.shape[0])/2)),bottom= int(np.absolute((max_h_int-image_crop1.shape[0])/2)),left=0,right= 0, borderType=cv2.BORDER_CONSTANT, value = 0)
                                    print('elif1/step1/image_crop.shape/max_h_int != image_crop1.shape[0]:',image_crop1.shape)
                                if max_w_int != image_crop1.shape[1] :
                                    image_crop1 = cv2.copyMakeBorder(src= image_crop1,top=0,bottom= 0,left=int(np.absolute((max_w_int-image_crop1.shape[1])/2)),right= int(np.absolute((max_w_int-image_crop1.shape[1])/2)), borderType=cv2.BORDER_CONSTANT, value = 0)
                                    print('elif1/step2/image_crop.shape/max_w_int != image_crop1.shape[1]:',image_crop1.shape)

                        elif (x-((max_w_int-w)/2))<0:
                            
                            image_crop1= image[int((y-((max_h_int-h)/2))):int(y+h+((max_h_int-h)/2)), 0:int(x+w+((max_w_int-w)/2))]
                            print('elif2/step0/image_crop.shape:',image_crop1.shape)
                            #image_crop1 = cv2.copyMakeBorder(src= image_crop,top=int(np.absolute((max_h_int-image_crop.shape[0])/2)),bottom= 0,left= int(np.absolute((max_w_int-image_crop.shape[1])/2)),right= 0, borderType=cv2.BORDER_CONSTANT, value = 0)
                            if max_h_int != image_crop1.shape[0] :
                                image_crop1 = cv2.copyMakeBorder(src= image_crop1,top=int(np.absolute((max_h_int-image_crop1.shape[0])/2)),bottom= int(np.absolute((max_h_int-image_crop1.shape[0])/2)),left=0,right= 0, borderType=cv2.BORDER_CONSTANT, value = 0)
                                print('elif2/step1/image_crop.shape/max_h_int != image_crop1.shape[0]:',image_crop1.shape)
                            if max_w_int != image_crop1.shape[1] :
                                image_crop1 = cv2.copyMakeBorder(src= image_crop1,top=0,bottom= 0,left=int(np.absolute((max_w_int-image_crop1.shape[1])/2)),right= int(np.absolute((max_w_int-image_crop1.shape[1])/2)), borderType=cv2.BORDER_CONSTANT, value = 0)
                                print('elif2/step2/image_crop.shape/max_w_int != image_crop1.shape[1]:',image_crop1.shape)

                        else:

                            image_crop1= image[int((y-((max_h_int-h)/2))):int(y+h+((max_h_int-h)/2)), int((x-((max_w_int-w)/2))):int(x+w+((max_w_int-w)/2))]
                            print('else/step0/image_crop.shape:',image_crop1.shape)
                            if max_h_int != image_crop1.shape[0] :
                                image_crop1 = cv2.copyMakeBorder(src= image_crop1,top=int(np.absolute((max_h_int-image_crop1.shape[0])/2)),bottom= int(np.absolute((max_h_int-image_crop1.shape[0])/2)),left=0,right= 0, borderType=cv2.BORDER_CONSTANT, value = 0)
                                print('else/step1/image_crop.shape/max_h_int != image_crop1.shape[0]:',image_crop1.shape)
                            if max_w_int != image_crop1.shape[1] :
                                image_crop1 = cv2.copyMakeBorder(src= image_crop1,top=0,bottom= 0,left=int(np.absolute((max_w_int-image_crop1.shape[1])/2)),right= int(np.absolute((max_w_int-image_crop1.shape[1])/2)), borderType=cv2.BORDER_CONSTANT, value = 0)
                                print('else/step2/image_crop.shape/max_w_int != image_crop1.shape[1]:',image_crop1.shape)
                    if image_crop1 is not None:
                        #pass
                        prepare_category(category_crop_image_path = category_crop_image_path,current_frame = list_df[i][3],idx = list_df[i][1],image_crop1 = image_crop1,name_camera=name_camera)
        current_frame += 1
  print('done!')
  return fps
         
def crop_normal(df,csvFilePath='2.csv' ,category_crop_image_path="./frame_sequence",video_path='./sync_30_D2.mp4',name_camera="D3"):

  import cv2
  list_df = df.values.tolist()
  vidcap = cv2.VideoCapture(video_path)
  fps = vidcap.get(cv2.CAP_PROP_FPS)
  print('fps:',fps)
  cap = cv2.VideoCapture(video_path)
  current_frame = 0
  while True:
        if current_frame >  int(df[['frame']].max()):
            break
        ret, image = cap.read()
        if ret:
            z = list(np.where(np.array(list(zip(*list_df))[3])==current_frame))[0]
            for ind , i in enumerate(z):
        
                if list_df[i][5]==1 or list_df[i][4] ==1 :
                        print('frame:',list_df[i][3],'id:',list_df[i][1],'occluded:',list_df[i][5],'outside:',list_df[i][4])
                        # pass
                else:    
 
                    x = int(list_df[i][6]) 
                    y = int(list_df[i][7]) 
                    w = int(list_df[i][8]) 
                    h = int(list_df[i][9])
                    if y<0 :
                        image_crop1= image[0:y+h, x:x+w]
                    elif x<0:
                        image_crop1= image[y:y+h, 0:x+w]
                    else :
                        
                        image_crop1= image[y:y+h, x:x+w]
                    if image_crop1 is not None:
                        prepare_category(category_crop_image_path = category_crop_image_path,current_frame = list_df[i][3],idx = list_df[i][1],image_crop1 = image_crop1,name_camera=name_camera)
        current_frame += 1
  print('done!')
  return fps

def crop_frame_smaller_size(df,csvFilePath='2.csv' ,category_crop_image_path="./frame_sequence",video_path='./sync_30_D2.mp4',name_camera="D3"):

  import cv2
  list_df = df.values.tolist()
  vidcap = cv2.VideoCapture(video_path)
  fps = vidcap.get(cv2.CAP_PROP_FPS)
  print('fps:',fps)
  cap = cv2.VideoCapture(video_path)
  current_frame = 0
  while True:
        if current_frame >  int(df[['frame']].max()):
            break
        ret, image = cap.read()
        if ret:
            z = list(np.where(np.array(list(zip(*list_df))[3])==current_frame))[0]
            for ind , i in enumerate(z):
        
                if list_df[i][5]==1 or list_df[i][4] ==1 :
                        print('frame:',list_df[i][3],'id:',list_df[i][1],'occluded:',list_df[i][5],'outside:',list_df[i][4])
                        # pass
                else:    
 
                    x = int(list_df[i][6]) 
                    y = int(list_df[i][7]) 
                    w = int(list_df[i][8]) 
                    h = int(list_df[i][9])
                    if y<0 :
                        image_crop1= image[0:y+h, x:x+w]
                        image_crop1_R = cv2.resize(image_crop1, (int(image_crop1.shape[1] * 0.33),int(image_crop1.shape[0] * 0.33)), interpolation = cv2.INTER_AREA)
                    elif x<0:
                        image_crop1= image[y:y+h, 0:x+w]
                        image_crop1_R = cv2.resize(image_crop1, (int(image_crop1.shape[1] * 0.33),int(image_crop1.shape[0] * 0.33)), interpolation = cv2.INTER_AREA)
                    else :
                        
                        image_crop1= image[y:y+h, x:x+w]
                        image_crop1_R = cv2.resize(image_crop1, (int(image_crop1.shape[1] * 0.33),int(image_crop1.shape[0] * 0.33)), interpolation = cv2.INTER_AREA)
                    if image_crop1 is not None:
                        prepare_category(category_crop_image_path = category_crop_image_path,current_frame = list_df[i][3],idx = list_df[i][1],image_crop1 = image_crop1_R,name_camera=name_camera)
        current_frame += 1
  print('done!')
  return fps

def make_gif(frame_folder,save_gif,name_camera,fps):
    import os
    import glob
    from PIL import Image
    import moviepy.editor as mp
    print('frame_folder:',frame_folder)
    for sub_path in glob.glob(f"{frame_folder}/*"):
            print('sub_path:',sub_path)
            frames = [Image.open(image) for image in glob.glob(f"{sub_path}/*")]
            frame_one = frames[0]
            print('len(frames):',len(frames))
            print(" os.path.basename(sub_path):", os.path.basename(sub_path))
            # if len(frames) < 100:
            #     frame_one.save("./gif_frame/"+ os.path.basename(sub_path)  +".gif", format="GIF", append_images=frames[0:101:5],
            #             save_all=True, duration=fps, loop=1)
            # else:
            print('int(len(frames)/fps):',int(len(frames)/fps))
            path = save_gif+ "/"+ name_camera + "/"+ os.path.basename(sub_path)
            try:
                frame_one.save(path +".gif", format="GIF", append_images=frames[0:len(frames):int(len(frames)/fps)],
                            save_all=True, duration=(fps*10), loop=1)
            except:
                frame_one.save(path +".gif", format="GIF", append_images=frames[0:len(frames)],
                            save_all=True, duration=(fps*10), loop=1)




            clip = mp.VideoFileClip(path +".gif")
            clip.write_videofile(path + ".webM")