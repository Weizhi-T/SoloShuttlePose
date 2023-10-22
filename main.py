import cv2
import copy
from tqdm import tqdm
import numpy as np
import matplotlib.pyplot as plt
from torchvision.transforms import transforms
from torchvision.transforms import functional as F
import os
from utils import write_json, clear_file, is_video_detect, find_next, find_reference, blend_images
from VideoClip import VideoClip
from PoseDetect import PoseDetect
from CourtDetect import CourtDetect
from NetDetect import NetDetect

folder_path = "videos"
video_save_path = "res/videos"
force_process = False
skip_frac = 2

# you can clear some precessed video's file and then process video
clear_file("test5")
clear_file("test6")

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
            video = cv2.VideoCapture(video_path, cv2.CAP_FFMPEG)
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
            pose_detect = PoseDetect()
            court_detect = CourtDetect()
            net_detect = NetDetect()
            video_cilp = VideoClip(video_name, fps, skip_frac, total_frames,
                                   height, width, full_video_path)

            reference_path = find_reference(video_name)
            if reference_path is None:
                print(
                    "There is not reference frame! Now try to find it automatically. "
                )
            else:
                print(f"The reference frame is {reference_path}. ")

            # begin_frame is a rough estimate of valid frames
            begin_frame = court_detect.pre_process(video_path, reference_path)
            _ = net_detect.pre_process(video_path, reference_path)

            # next_frame is a more accurate estimate of the effective frame using bisection search
            next_frame = find_next(video_path, court_detect, begin_frame)
            first_frame = next_frame

            normal_court_info = court_detect.normal_court_info
            normal_net_info = net_detect.normal_net_info

            court_dict = {
                "game_first_frame": first_frame,
                "game_next_frame": next_frame,
                "court": normal_court_info,
                "net": normal_net_info,
            }

            write_json(court_dict, video_name, "res\courts\court_kp", "w")

            # release memory
            net_detect.del_RCNN()

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

                    final_frame = frame.copy()

                    if current_frame < next_frame:
                        write_json(have_court_dict, video_name,
                                   "res\courts\have_court")
                        write_json(players_dict, video_name, "res\joints")
                        court_mse_dict = {str(current_frame): court_detect.mse}
                        write_json(court_mse_dict, video_name,
                                   "res\courts\court_mse")

                        video_made = video_cilp.add_frame(
                            have_court, frame, current_frame)

                        video_writer.write(frame)
                        pbar.update(1)
                        continue

                    # player detect and court detect
                    court_info, have_court = court_detect.get_court_info(frame)
                    if have_court:

                        pose_detect.setup_RCNN()
                        original_outputs, human_joints = pose_detect.get_human_joints(
                            frame)
                        pose_detect.del_RCNN()

                        have_player, players_joints = court_detect.player_detection(
                            original_outputs)

                        if have_player:
                            # draw human, court, players
                            final_frame = court_detect.draw_court(final_frame)

                            final_frame = net_detect.draw_net(final_frame)

                            final_frame = pose_detect.draw_key_points(
                                players_joints, final_frame)

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
                        court_dict = {
                            "game_first_frame": first_frame,
                            "game_next_frame": next_frame,
                            "court": normal_court_info,
                            "net": normal_net_info,
                        }
                        write_json(court_dict, video_name,
                                   "res\courts\court_kp", "w")

                    video_writer.write(final_frame)

                    have_court_dict = {str(current_frame): True}
                    court_mse_dict = {str(current_frame): court_detect.mse}
                    write_json(court_mse_dict, video_name,
                               "res\courts\court_mse")
                    write_json(have_court_dict, video_name,
                               "res\courts\have_court")
                    write_json(players_dict, video_name, "res\joints")

                    pbar.update(1)

            # Release the video capture and writer objects
            video.release()
            video_writer.release()
