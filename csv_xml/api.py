from fastapi import FastAPI, File, UploadFile
from fastapi.responses import Response
from typing import List
from utils import csv_to_xml, xml_to_csv
from zipfile import ZipFile
import io

app = FastAPI()

# upload the csv file
@app.post("/uploadfile/")
async def upload_file(files: List[UploadFile] = File(...)):
    zip_filename = "archive.zip"
    s = io.BytesIO()
    # create a ZipFile object
    zipObj = ZipFile(s, 'w')

    for file in files:
        if file.content_type == 'text/csv':
            basename = csv_to_xml(file)

            # add the xml file to the zip
            zipObj.write(f"{basename}.xml")
        
        elif file.content_type == 'text/xml':
            basename = xml_to_csv(file)
            
            # add the csv file to the zip
            zipObj.write(f"{basename}.csv")
        
        else:
            raise Exception("Invalid file")
        
    # close the zip file
    zipObj.close()

    # return a link to download the zip file
    return Response(s.getvalue(), media_type="application/x-zip-compressed", headers={
        'Content-Disposition': f'attachment; filename={zip_filename}'
    })
    
