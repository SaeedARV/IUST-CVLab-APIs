from fastapi import FastAPI, File, UploadFile, HTTPException, Form, Query
from fastapi.responses import Response
from typing import Annotated, List
from utils import *
from zipfile import ZipFile
import io

app = FastAPI()

# Crop image API
@app.post("/crop_image/")
async def crop_image(camera_name: Annotated[str, Form()],
                     crop_type: str = Query(enum=['normal','padding',"smaller"]),
                     gif_flag: bool = Query(enum=[True, False]),
                     video_file: UploadFile = File(description="Upload a video."), 
                     csv_file: UploadFile = File(description="Upload a CSV file."),
                     ):
    
    if (video_file.content_type != 'video/mp4' and video_file.content_type != 'video/mpeg' and 
        video_file.content_type != 'video/webm') or csv_file.content_type != 'text/csv':
        raise HTTPException(400, detail="Invalid document type! please only upload a video and a csv file.")
    

    path = csv_to_json(csv_file)

    df = pd.read_json(path)
    df.columns = df.iloc[0]
    df = df.drop([0])

    if crop_type == "normal" :
        fps = crop_normal(df, video_file, camera_name)
    elif crop_type == "smaller" :
        fps = crop_frame_smaller(df, video_file, camera_name)
    elif crop_type == "padding" :
        fps = crop_frame(df, csv_file, video_file, camera_name)

    if gif_flag:
        make_gif(camera_name, fps=fps) 
    

# CSV to XML & XML to CSV API
@app.post("/csv_xml/")
async def csv_xml(files: List[UploadFile] = File(description="Upload CSV or XML files.")):
    zip_filename = "archive.zip"
    s = io.BytesIO()
    # create a ZipFile object
    zipObj = ZipFile(s, 'w')

    for file in files:
        if file.content_type == 'text/csv':
            path = csv_to_xml(file)

            # add the xml file to the zip
            zipObj.write(path)
        
        elif file.content_type == 'text/xml':
            path = xml_to_csv(file)
            
            # add the csv file to the zip
            zipObj.write(path)
        
        else:
            raise HTTPException(400, detail="Invalid document type! please only upload CSV and XML files.")
        
    # close the zip file
    zipObj.close()

    # return a link to download the zip file
    return Response(s.getvalue(), media_type="application/x-zip-compressed", headers={
        'Content-Disposition': f'attachment; filename={zip_filename}'
    })

# Video partition API
@app.post("/video_partition/")
async def video_partition(partition_name: Annotated[str, Form()],
                          second_start: Annotated[int, Form()],
                          second_end: Annotated[int, Form()],
                          duration: Annotated[int, Form()],
                          overlap_frame: Annotated[int, Form()],
                          video_file: UploadFile = File(description="Upload a video."),
                          ):
    
    if (video_file.content_type != 'video/mp4' and video_file.content_type != 'video/mpeg' and 
    video_file.content_type != 'video/webm'):
        raise HTTPException(400, detail="Invalid document type! please only upload a video.")
    
    Partition(video_file, partition_name, second_start, second_end, duration, overlap_frame)