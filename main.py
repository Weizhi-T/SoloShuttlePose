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
from utils import write_json, clear_file, is_video_detect

import os

folder_path = "video"
video_save_path = "res/video"
force_process = True

for root, dirs, files in os.walk(folder_path):
    for file in files:
        _, ext = os.path.splitext(file)
        if ext.lower() in ['.mp4']:
            video_path = os.path.join(root, file)
            print(video_path)
            video_name = os.path.basename(video_path).split('.')[0]

            if is_video_detect(video_name):
                if force_process:
                    clear_file(video_name)
                else:
                    continue

            full_video_path = os.path.join(video_save_path, video_name)
            if not os.path.exists(full_video_path):
                os.makedirs(full_video_path)

            # Open the video file
            video = cv2.VideoCapture(video_path)
            # Get video properties
            fps = video.get(cv2.CAP_PROP_FPS)
            width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

            # Define the codec for the output video
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            video_writer = cv2.VideoWriter(
                f'{full_video_path}/{video_name}.mp4', fourcc, fps,
                (width, height))

            total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

            rcnn_pose = RCNNPose()
            court_detect = CourtDetect()

            court_detect.pre_process(video_path)

            court_dict = {"court": court_detect.normal_court_info}
            write_json(court_dict, video_name, "res\court")

            video_cilp = VideoClip(video_name, fps, total_frames, height,
                                   width, full_video_path)

            with tqdm(total=total_frames) as pbar:
                while True:
                    # Read a frame from the video
                    ret, frame = video.read()
                    current_frame = int(video.get(cv2.CAP_PROP_POS_FRAMES))
                    # If there are no more frames, break the loop
                    if not ret:
                        break

                    players_dict = {
                        str(current_frame): {
                            "top": None,
                            "bottom": None
                        }
                    }

                    court_frame, human_frame = frame.copy(), frame.copy()
                    court_info, have_court = court_detect.get_court_info(frame)

                    if have_court:
                        original_outputs, human_joints = rcnn_pose.get_human_joints(
                            frame)
                        have_player, players_joints = court_detect.player_detection(
                            original_outputs)

                        if have_player:
                            court_frame = court_detect.draw_court(frame)
                            human_frame = rcnn_pose.draw_key_points(
                                players_joints, frame)
                            players_dict = {
                                str(current_frame): {
                                    "top": players_joints[0],
                                    "bottom": players_joints[1]
                                }
                            }

                    video_cilp.add_frame(have_court, frame, current_frame)

                    alpha = 0.6
                    frame = cv2.addWeighted(human_frame, alpha, court_frame,
                                            1 - alpha, 0)
                    video_writer.write(frame)

                    have_court_dict = {str(current_frame): have_court}

                    write_json(have_court_dict, video_name, "res\court")

                    write_json(players_dict, video_name, "res\joint")
                    pbar.update(1)

            # Release the video capture and writer objects
            video.release()
            video_writer.release()
