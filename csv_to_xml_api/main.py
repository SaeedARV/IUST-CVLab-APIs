import csv
import codecs
import xml.etree.ElementTree as ElementTree
from fastapi import FastAPI, UploadFile
from fastapi.responses import FileResponse

app = FastAPI()

def csv_to_xml(file):

    # create xml file
    annotations = ElementTree.Element("annotations")

    version = ElementTree.Element("version")
    version.text = "1.1"
    annotations.append(version)

    meta = ElementTree.Element("meta")
    annotations.append(meta)

    task = ElementTree.Element("task")
    meta.append(task)

    # read data from csv of bytetrack
    csv_file = file.file
    reader = csv.reader(codecs.iterdecode(csv_file, 'utf-8'))
    rows = list(reader)[1:]

    # finding targets
    target_ids = set()
    for r in rows:
        target_id = r[1]
        target_ids.add(target_id)


    def append_box_to_track(input_track, input_frame, keyframe='0', outside='0'):
        frame_id = input_frame[0]
        mask = input_frame[2]
        xtl = input_frame[3]
        ytl = input_frame[4]
        xbr = str(float(xtl) + float(input_frame[5]))
        ybr = str(float(ytl) + float(input_frame[6]))

        box = ElementTree.Element("box", attrib={
            "frame": frame_id,
            "outside": outside,
            "occluded": '0',
            "keyframe": keyframe,
            "xtl": xtl,
            "ytl": ytl,
            "xbr": xbr,
            "ybr": ybr,
            "z_order": '0'
        })
        input_track.append(box)

        attribute1 = ElementTree.Element("attribute", attrib={
            "name": "Mask"
        })
        attribute1.text = str(False) if "no mask" in mask.lower() else str(True)
        box.append(attribute1)

        attribute2 = ElementTree.Element("attribute", attrib={
            "name": "Gender"
        })
        attribute2.text = "Male"
        box.append(attribute2)


    # filling xml file
    biggest_frame_id = max(rows, key=lambda r: int(r[0]))[0]
    interval = 50

    for target_id in target_ids:
        track = ElementTree.Element("track", attrib={
            "id": target_id,
            "label": "Human",
            "source": "manual"
        })
        annotations.append(track)

        person_frames = list(filter(lambda row: row[1] == target_id, rows))

        for idx, frame in enumerate(person_frames):
            append_box_to_track(
                track,
                frame,
                keyframe=str(int(idx % interval == 0))
            )

        last_frame = person_frames[-1]
        last_frame_id = last_frame[0]
        if last_frame_id != biggest_frame_id:
            last_frame[0] = str(int(last_frame_id) + 1)  # next frame
            append_box_to_track(track, last_frame, keyframe='1', outside='1')

    tree = ElementTree.ElementTree(annotations)

    # save the file's name
    basename = file.filename.split('.')[0]

    # save the xml file
    tree.write(f"{basename}.xml", method="xml", xml_declaration=True, encoding="utf-8")

    return basename


# upload the csv file
@app.post("/uploadfile/")
async def upload_file(file: UploadFile):

    basename = csv_to_xml(file)

    # return a link to download the xml file
    return FileResponse(path=f"{basename}.xml", media_type='application/xml', filename=basename)
