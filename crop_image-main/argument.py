import argparse
def get_args():
    parser = argparse.ArgumentParser(description='Test')
    parser.add_argument('--csvFilePath',default='/content/drive/MyDrive/test_shop/cam_csv/cam1', type=str, help='path of csv file')
    parser.add_argument('--jsonFilePath',default='/content/drive/MyDrive/test_shop/cam_csv/cam3', type=str, help="Json's output path")
    parser.add_argument('--video_path',default='/content/drive/MyDrive/test_shop/cam_csv/cam3', type=str, help='video path')
    parser.add_argument('--crop_image_path',default='/content/drive/MyDrive/test_shop/cam_csv/cam3', type=str, help='crop_image_path')
    parser.add_argument('--save_gif',default='/content/drive/MyDrive/test_shop/cam_csv/cam3', type=str, help='save_gif_path')
    parser.add_argument('--name_camera',default='D2', type=str, help='The name of the camera whose video images are crop')
    parser.add_argument('--type_crop', default='', type=str, required=True, choices=['normal','padding',"smaller"])
    parser.add_argument('--gif_flag',default=False, type=str, help='gif_flag: 0:False  1:True ')
    args=parser.parse_args()
    return args

