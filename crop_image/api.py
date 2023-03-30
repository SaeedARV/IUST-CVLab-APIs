from fastapi import FastAPI, File, UploadFile, HTTPException, Form, Query
from fastapi.responses import Response
from typing import Annotated
from utils import *
from zipfile import ZipFile
import io

app = FastAPI()

# upload the csv file
@app.post("/uploadfile/")
async def upload_file(camera_name: Annotated[str, Form()],
                      crop_type: str = Query(enum=['normal','padding',"smaller"]),
                      gif_flag: bool = Query(enum=[True, False]),
                      video_file: UploadFile = File(description="Upload a video."), 
                      csv_file: UploadFile = File(description="Upload a CSV file."),
                      ):
    zip_filename = "archive.zip"
    s = io.BytesIO()
    # create a ZipFile object
    zipObj = ZipFile(s, 'w')
    
    if (video_file.content_type != 'video/mp4' and video_file.content_type != 'video/mpeg' and 
        video_file.content_type != 'video/webm') or csv_file.content_type != 'text/csv':
        raise HTTPException(400, detail="Invalid document type! please only upload a video and a csv file.")
    

    basename = csv_to_json(csv_file)

    df = pd.read_json(f"{basename}.json")
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


    # # close the zip file
    zipObj.close()

    # # return a link to download the zip file
    # return Response(s.getvalue(), media_type="application/x-zip-compressed", headers={
    #     'Content-Disposition': f'attachment; filename={zip_filename}'
    # })
    
