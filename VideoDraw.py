import cv2
import copy
from tqdm import tqdm
import numpy as np
import matplotlib.pyplot as plt
from torchvision.transforms import transforms
from torchvision.transforms import functional as F
import os
from src.tools.utils import write_json, clear_file, is_video_detect, find_next, find_reference, read_json
from src.tools.VideoClip import VideoClip
from src.models.PoseDetect import PoseDetect
from src.models.CourtDetect import CourtDetect
from src.models.NetDetect import NetDetect
import argparse

parser = argparse.ArgumentParser(description='para transfer')
parser.add_argument('--folder_path',
                    type=str,
                    default="videos",
                    help='folder_path -> str type.')
parser.add_argument('--result_path',
                    type=str,
                    default="res",
                    help='result_path -> str type.')
parser.add_argument('--force_process',
                    action='store_true',
                    default=False,
                    help='force_process -> bool type.')

args = parser.parse_args()
print(args)

folder_path = args.folder_path
force_process = args.force_process
result_path = args.result_path

for root, dirs, files in os.walk(folder_path):
    for file in files:
        _, ext = os.path.splitext(file)
        if ext.lower() in ['.mp4']:
            video_path = os.path.join(root, file)
            print(video_path)
            video_name = os.path.basename(video_path).split('.')[0]

            if is_video_detect(video_name, f"{result_path}/videos"):
                if force_process:
                    clear_file(video_name, f"{result_path}/videos")
                else:
                    continue

            full_video_path = os.path.join(f"{result_path}/videos", video_name)
            if not os.path.exists(full_video_path):
                os.makedirs(full_video_path)

            # Open the video file
            video = cv2.VideoCapture(video_path, cv2.CAP_FFMPEG)
            # Get video properties
            fps = video.get(cv2.CAP_PROP_FPS)
            height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
            width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))

            # Define the codec for the output video
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            video_writer = cv2.VideoWriter(
                f'{full_video_path}/{video_name}.mp4', fourcc, fps,
                (width, height))

            total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

            reference_path = find_reference(video_name, "res/courts/court_kp")
            pose_detect = PoseDetect()
            court_detect = CourtDetect()
            net_detect = NetDetect()

            _ = court_detect.pre_process(video_path, reference_path)
            _ = net_detect.pre_process(video_path, reference_path)

            reference_path = find_reference(video_name,
                                            "res/players/player_kp")
            players_dict = read_json(reference_path)

            with tqdm(total=total_frames) as pbar:
                while True:
                    # Read a frame from the video
                    current_frame = int(video.get(cv2.CAP_PROP_POS_FRAMES))
                    ret, frame = video.read()
                    # If there are no more frames, break the loop
                    if not ret:
                        break

                    joints = players_dict[f"{current_frame}"]
                    players_joints = [joints['top'], joints['bottom']]

                    draw = True
                    if players_joints[0] is None or players_joints[1] is None:
                        draw = False

                    if draw:
                        # draw human, court, players
                        frame = court_detect.draw_court(frame)
                        frame = net_detect.draw_net(frame)
                        frame = pose_detect.draw_key_points(
                            players_joints, frame)

                    video_writer.write(frame)
                    pbar.update(1)

            # Release the video capture and writer objects
            video.release()
