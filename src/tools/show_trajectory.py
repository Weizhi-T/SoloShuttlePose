import os
import cv2

import argparse
import numpy as np
import pandas as pd
from collections import deque
from PIL import Image, ImageDraw


def show_traj(video_path, loca_dict, traj_len=8):

    video_name = os.path.basename(video_path).split('.')[0]
    video_dir = os.path.dirname(video_path)
    output_video_path = f"{video_dir}/{video_name}_traj.mp4"

    # Read prediction result of the input video
    df_ls = []
    for frame, vxy_dict in loca_dict.items():
        fvxy_ditc = {}
        fvxy_ditc["frame"] = int(frame)
        for key, value in vxy_dict.items():
            fvxy_ditc[key] = value
        df_ls.append(fvxy_ditc)
    label_df = pd.DataFrame(df_ls)
    frame_id = np.array(label_df['frame'])
    x, y, vis = np.array(label_df['x']), np.array(label_df['y']), np.array(
        label_df['visible'])
    print(f'total frames: {len(frame_id)}')

    # For storing trajectory
    queue = deque()

    # Cap configuration
    cap = cv2.VideoCapture(video_path)
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    success = True
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (w, h))

    frame_i = 0
    while success:
        success, frame = cap.read()
        if not success:
            break

        if frame_i not in frame_id:
            continue

        # Push ball coordinates for each frame
        if vis[frame_i]:
            if len(queue) >= traj_len:
                queue.pop()
            queue.appendleft([x[frame_i], y[frame_i]])
        else:
            if len(queue) >= traj_len:
                queue.pop()
            queue.appendleft(None)

        # Convert to PIL image for drawing
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)

        # Draw ball trajectory
        for i in range(len(queue)):
            if queue[i] is not None:
                draw_x = queue[i][0]
                draw_y = queue[i][1]
                bbox = (draw_x - 2, draw_y - 2, draw_x + 2, draw_y + 2)
                draw = ImageDraw.Draw(img)
                draw.ellipse(bbox, outline='yellow')
                del draw

        # Convert back to cv2 image and write to output video
        frame = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        out.write(frame)
        frame_i += 1

    out.release()
    cap.release()
    os.remove(video_path)
    os.rename(output_video_path, video_path)
    print('Done')