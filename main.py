import cv2
import copy
from tqdm import tqdm
import numpy as np
import matplotlib.pyplot as plt
from torchvision.transforms import transforms
from torchvision.transforms import functional as F
from VideoClip import VideoClip
from RCNNPose import RCNNPose
from CourtDetect import CourtDetect
import os
import pandas as pd
from ultils import write_json

video_path = 'video/a.mp4'
video_name = os.path.basename(video_path).split('.')[0]

# Open the video file
video = cv2.VideoCapture(video_path)
# Get video properties
fps = video.get(cv2.CAP_PROP_FPS)
width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Define the codec for the output video
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
video_writer = cv2.VideoWriter('output_video.mp4', fourcc, fps,
                               (width, height))

total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

rcnn_pose = RCNNPose()
court_detect = CourtDetect()

court_detect.pre_process(video_path)

write_json(court_detect.normal_court_info, video_name, "res\court")

video_cilp = VideoClip(video_name, fps, height, width)

with tqdm(total=total_frames) as pbar:
    while True:
        # Read a frame from the video
        ret, frame = video.read()
        current_frame = int(video.get(cv2.CAP_PROP_POS_FRAMES))
        # If there are no more frames, break the loop
        if not ret:
            break

        players_info = {"frame": current_frame, "top": None, "bottom": None}

        court_frame, human_frame = frame.copy(), frame.copy()
        court_info, have_court = court_detect.get_court_info(frame)

        if have_court:
            original_outputs, human_joints = rcnn_pose.get_human_joints(frame)
            have_player, players_joints = court_detect.player_detection(
                original_outputs)

            if have_player:
                court_frame = court_detect.draw_court(frame)
                human_frame = rcnn_pose.draw_key_points(players_joints, frame)
                players_info = {
                    "frame": current_frame,
                    "top": players_joints[0],
                    "bottom": players_joints[1]
                }

        video_cilp.add_frame(have_court, frame, current_frame)

        alpha = 0.6
        frame = cv2.addWeighted(human_frame, alpha, court_frame, 1 - alpha, 0)
        video_writer.write(frame)
        # print(f"{current_frame}:{have_court}")
        # pbar.set_postfix({'Frame': count})  # 更新进度条上显示的帧数信息

        write_json(players_info, video_name, "res\joint")
        pbar.update(1)

# Release the video capture and writer objects
video.release()
video_writer.release()
