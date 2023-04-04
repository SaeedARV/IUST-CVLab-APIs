<a name="readme-top"></a>

<!-- PROJECT LOGO -->
<div align="center">

<h3 align="center">crop_image, csv_xml and video_partition APIs</h3>

  <p align="center">
    Three easy-to-use APIs for IUST CV Lab
    <br />
    <a href="https://github.com/SaeedARV/IUST-CVLab-FastAPI-Projects"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/SaeedARV/IUST-CVLab-FastAPI-Projects/issues">Report Bug</a>
    ·
    <a href="https://github.com/SaeedARV/IUST-CVLab-FastAPI-Projects/issues">Request Feature</a>
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#crop_image">crop_image</a></li>
        <li><a href="#csv_xml">csv_xml</a></li>
        <li><a href="#video_partition">video_partition</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#how-to-use">How to use</a></li>
     <ul>
        <li><a href="#crop_image2">crop_image</a></li>
        <li><a href="#csv_xml2">csv_xml</a></li>
        <li><a href="#video_partition2">video_partition</a></li>
      </ul>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About The Project
This project contains three API: crop_video, csv_xml and video_partition

### crop_image

This one can take a video and a CSV file. It will convert the CSV file to JSON and save an image sequence from the video. It can make gifs out of image sequences as well.

### csv_xml

You can use this API to convert CSV to XML and CSV to XML. (CSV and XML files in specific formats)

### video_partition

This API can split a video into multiple smaller videos.
<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started

### Prerequisites

1. cd to the directory where requirements.txt is located
2. run: pip install -r requirements.txt to install all you need

### Installation

1. cd to the directory where api.py and utils.py are located
2. run: python -m uvicorn api:app --reload to run the live server

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->
## How to use

<div id='crop_image2'>
  
### crop_image
  
1. Go to this URL: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
2. Click the **/crop_image/**
3. Click the **try it out** button
4. Fill in the camera_name field
5. Choose a crop_type
6. Choose if you want gifs or not
7. Upload a video
8. Upload a CSV file
9. Click Execute button
  
JSON file will be saved in the json folder, image sequences will be saved in the frame_sequence folder and gifs will be saved in the gif folder.
  
</div>

<div id='csv_xml2'>

### csv_xml
  
1. Go to this URL: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
2. Click the **/csv_xml/**
3. Click the **try it out** button
4. Upload as many CSV and XML files as you want
5. Click Execute button

Now you can download the zip file.
  
</div>

<div id ='video_partition2'>

### video_partition
  
1. Go to this URL: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
2. Click the **/video_partition/**
3. Click the **try it out** button
4. Fill in the partition_name field
5. Fill in the second_start field (The second of the start of partitioning)
6. Fill in the second_end field (The second of the end of partitioning)
7. Fill in the duration field (Duration of partitioning in seconds)
8. Fill in the overlap_frame field
9. Upload a video
10. Click Execute button

Splitted videos will be saved in the partition_videos folder.

</div>

<p align="right">(<a href="#readme-top">back to top</a>)</p>
