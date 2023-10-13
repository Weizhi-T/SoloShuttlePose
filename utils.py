import json
import os
import shutil
import json
import cv2
from CourtDetect import CourtDetect


def is_file_empty(file_path):
    return os.path.getsize(file_path) == 0


def write_json(data, file_name, save_path="./"):
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    full_path = os.path.join(save_path, f"{file_name}.json")

    if not os.path.exists(full_path):
        with open(full_path, 'w') as file:
            pass

    with open(full_path, 'r+') as file:
        for key, value in data.items():
            if is_file_empty(full_path):
                file.write('{}')
                file.seek(0, os.SEEK_END)
                file.seek(file.tell() - 1, os.SEEK_SET)
                file.write('\n')
                file.write(json.dumps(key, indent=4))
                file.write(': ')
                file.write(json.dumps(value, indent=4))
                file.write('\n')
                file.write('}')
                return

            file.seek(0, os.SEEK_END)
            file.seek(file.tell() - 2, os.SEEK_SET)
            file.write(',')
            file.write('\n')
            file.write(json.dumps(key, indent=4))
            file.write(': ')
            file.write(json.dumps(value, indent=4))
            file.write('\n')
            file.write('}')
    return


def is_video_detect(defile_name, save_path="res"):
    if not os.path.exists(save_path):
        print(f"The path {save_path} does not exist!")
        return False

    for root, dirs, files in os.walk(save_path):

        for file in files:
            file_name = file.split('.')[0]

            if defile_name == file_name:
                file_path = os.path.join(root, file)
                print(
                    f"{file_path} has been processed! If you still want to process it, please set force_process as True. "
                )
                return True


def find_next(video_path, court_detect, begin_frame):
    # Open the video file
    video = cv2.VideoCapture(video_path)
    # Get video properties
    fps = video.get(cv2.CAP_PROP_FPS)

    # Number of consecutively detected pitch frames
    last_count = 0
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    court_info_list = []
    # the number of skip frams per time
    skip_frames = int(fps)

    def pre_process():
        nonlocal video, fps, total_frames, skip_frames, court_detect, begin_frame, last_count, court_info_list
        video.set(cv2.CAP_PROP_POS_FRAMES, begin_frame)
        while True:
            # Read a frame from the video
            current_frame = int(video.get(cv2.CAP_PROP_POS_FRAMES))
            ret, frame = video.read()

            # If there are no more frames, break the loop
            if not ret or last_count >= skip_frames:
                return current_frame - skip_frames

            court_info, have_court = court_detect.get_court_info(frame)
            if have_court:
                last_count += 1
                court_info_list.append(court_info)
            else:
                if current_frame + skip_frames >= total_frames:
                    return total_frames
                video.set(cv2.CAP_PROP_POS_FRAMES, current_frame + skip_frames)
                last_count = 0
                court_info_list = []

    def find_frame(end_frame):
        nonlocal video, court_detect, begin_frame
        while begin_frame + 1 < end_frame:

            middle_frame = (begin_frame + end_frame) // 2
            video.set(cv2.CAP_PROP_POS_FRAMES, middle_frame)

            ret, frame = video.read()
            court_info, have_court = court_detect.get_court_info(frame)
            if have_court:
                end_frame = middle_frame
            else:
                begin_frame = middle_frame
        return begin_frame

    end_frame = pre_process()
    next_frame = find_frame(end_frame)
    video.release()
    return next_frame


def clear_file(defile_name, save_path="res"):
    if not os.path.exists(save_path):
        print(f"The path {save_path} does not exist!")
        return

    for root, dirs, files in os.walk(save_path):
        for dir_name in dirs:
            if dir_name == defile_name:
                dir_path = os.path.join(root, dir_name)
                shutil.rmtree(dir_path)
                print(f"Folder '{defile_name}' has been deleted: {dir_path}")
                continue

        for file in files:
            file_name = file.split('.')[0]
            if defile_name == file_name:
                file_path = os.path.join(root, file)
                os.remove(file_path)
                print(f"{file_path} has been deleted.")


if __name__ == "__main__":
    test = False
    clear_file("test1")
    if not test:
        exit(0)
    data1 = {"0": {"top": None, "bottom": None}}
    data2 = {"1": {"top": None, "bottom": None}}
    data3 = {"2": {"top": None, "bottom": None}}

    write_json(data1, "demo")
    write_json(data2, "demo")
    write_json(data3, "demo")

    import pandas as pd

    data = pd.read_json("demo.json")
    print(data)