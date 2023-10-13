import cv2
import copy
from tqdm import tqdm
import numpy as np
import matplotlib.pyplot as plt
from torchvision.transforms import transforms
from torchvision.transforms import functional as F
from VideoClip import VideoClip
from kpRCNNPose import RCNNPose
from CourtDetect import CourtDetect
import os
from utils import write_json, clear_file, is_video_detect, find_next

import os

folder_path = "videos"
video_save_path = "res/videos"
force_process = True

# skip_frac means skip int(fps)//skip_frac, always set 1 or 2
# the only control class VideoClip
skip_frac = 2

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

            # compute skip_frames
            skip_frames = int(fps) // skip_frac

            # example class
            rcnn_pose = RCNNPose()
            court_detect = CourtDetect()
            video_cilp = VideoClip(video_name, fps, skip_frac, total_frames,
                                   height, width, full_video_path)

            begin_frame = court_detect.pre_process(video_path)
            next_frame = find_next(video_path, court_detect, begin_frame)
            court_dict = {"court": court_detect.normal_court_info}
            write_json(court_dict, video_name, "res\courts")

            with tqdm(total=total_frames) as pbar:

                while True:
                    # Read a frame from the video
                    current_frame = int(video.get(cv2.CAP_PROP_POS_FRAMES))
                    ret, frame = video.read()
                    # If there are no more frames, break the loop
                    if not ret:
                        break
                    # assume it don't detect anything
                    have_court = False
                    players_dict = {
                        str(current_frame): {
                            "top": None,
                            "bottom": None
                        }
                    }
                    have_court_dict = {str(current_frame): have_court}

                    court_frame, human_frame = frame.copy(), frame.copy()

                    if current_frame < next_frame:
                        write_json(have_court_dict, video_name, "res\courts")
                        write_json(players_dict, video_name, "res\joints")
                        video_made = video_cilp.add_frame(
                            have_court, frame, current_frame)

                        video_writer.write(frame)
                        pbar.update(1)
                        continue

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

                    video_made = video_cilp.add_frame(have_court, frame,
                                                      current_frame)
                    if video_made:
                        next_frame = find_next(video_path, court_detect,
                                               current_frame)

                    alpha = 0.6
                    frame = cv2.addWeighted(human_frame, alpha, court_frame,
                                            1 - alpha, 0)
                    video_writer.write(frame)
                    have_court_dict = {str(current_frame): True}

                    write_json(have_court_dict, video_name, "res\courts")

                    write_json(players_dict, video_name, "res\joints")

                    pbar.update(1)

            # Release the video capture and writer objects
            video.release()
            video_writer.release()
