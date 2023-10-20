import cv2
from PIL import Image, ImageTk
import os
import copy
import tkinter as tk
from tkinter import messagebox
from utils import find_reference
from CourtDetect import CourtDetect
from PoseDetect import PoseDetect


def yes_button_click():
    global user_choice
    user_choice = True
    os.remove(reference_path)
    small_window.destroy()


def no_button_click():
    global user_choice
    user_choice = False
    small_window.destroy()


# Image display callback function
def update_image():
    # Read video frames
    global frame
    ret, frame = video.read()

    if not ret:
        # Video readout complete.
        return

    # Resize an image to a specified size
    frame_resized = cv2.resize(frame, (400, 300))
    # Converting OpenCV images to PIL images
    frame_pil = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)
    frame_pil = Image.fromarray(frame_pil)
    # Show unprocessed images in the left-hand tab
    frame_tk1 = ImageTk.PhotoImage(frame_pil)
    image_label1.configure(image=frame_tk1)
    image_label1.image = frame_tk1

    # Display the processed image in the right-hand tab
    # use CourtDetect and PoseDetect to process frame
    frame_copy = frame.copy()
    court_info, have_court = court_detect.get_court_info(frame_copy)
    if have_court:
        original_outputs, human_joints = pose_detect.get_human_joints(frame)
        have_player, players_joints = court_detect.player_detection(
            original_outputs)
        if have_player:
            court_frame = court_detect.draw_court(frame)
            frame_copy = pose_detect.draw_key_points(players_joints,
                                                     court_frame)

    frame_processed = cv2.resize(frame_copy, (400, 300))
    frame_processed_pil = cv2.cvtColor(frame_processed, cv2.COLOR_BGR2RGB)
    frame_processed_pil = Image.fromarray(frame_processed_pil)
    frame_tk2 = ImageTk.PhotoImage(frame_processed_pil)

    image_label2.configure(image=frame_tk2)
    image_label2.image = frame_tk2

    # 更新窗口显示
    window.update()


# 键盘事件回调函数
def key_press(event):
    global frame_counter
    global total_frames
    global frame
    global video_name
    key = event.keysym

    if key == "Return":  # 按下回车键，保存当前帧的图像
        cv2.imwrite(f"references/{video_name}_{frame_counter}.jpg", frame)
        print(f"保存帧 {frame_counter}")
        window.destroy()
        return

    if key == "Escape":  # 按下Esc键，退出程序
        window.destroy()
        return

    if key == "Up":  # 按上键，跳30帧往前
        frame_counter -= 30
        frame_counter = max(0, frame_counter)
        video.set(cv2.CAP_PROP_POS_FRAMES, frame_counter)

    if key == "Down":  # 按下键，跳30帧往后
        frame_counter += 30
        frame_counter = min(frame_counter, total_frames)
        video.set(cv2.CAP_PROP_POS_FRAMES, frame_counter)

    if key == "Left":  # 按左键，往前跳一帧
        frame_counter -= 1
        frame_counter = max(0, frame_counter)
        video.set(cv2.CAP_PROP_POS_FRAMES, frame_counter)

    if key == "Right":  # 按右键，往后跳一帧
        frame_counter += 1
        frame_counter = min(frame_counter, total_frames)
        video.set(cv2.CAP_PROP_POS_FRAMES, frame_counter)

    # 更新图像
    update_image()


folder_path = "videos"
video_name = None
user_choice = True

for root, dirs, files in os.walk(folder_path):
    for file in files:
        _, ext = os.path.splitext(file)
        if ext.lower() in ['.mp4']:

            video_path = os.path.join(root, file)
            video_name = os.path.basename(video_path).split('.')[0]

            user_choice = True
            reference_path = find_reference(video_name)
            while reference_path is not None and user_choice:
                # 创建窗口
                small_window = tk.Tk()
                small_window.title("删除文件")
                small_window.geometry("300x100")

                # 显示文件名称
                label = tk.Label(small_window,
                                 text="file name: " + reference_path)
                label.grid(row=0, column=0, columnspan=2, pady=10)

                # 创建“是”按钮
                yes_button = tk.Button(small_window,
                                       text="是",
                                       command=yes_button_click)
                yes_button.grid(row=1, column=0, padx=10)

                # 创建“否”按钮
                no_button = tk.Button(small_window,
                                      text="否",
                                      command=no_button_click)
                no_button.grid(row=1, column=1, padx=10)

                small_window.mainloop()
                reference_path = find_reference(video_name)

            if not user_choice:
                continue

            # 打开视频文件
            video = cv2.VideoCapture(video_path)

            court_detect = CourtDetect()
            pose_detect = PoseDetect()

            # 创建一个窗口
            window = tk.Tk()
            window.title(f"{video_name}")
            window.geometry("800x600+200+100")

            # 创建左侧图片标签
            image_label1 = tk.Label(window)
            image_label1.pack(side="left")

            # 创建右侧图片标签
            image_label2 = tk.Label(window)
            image_label2.pack(side="right")

            # 保存当前帧计数器
            frame_counter = 0
            total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
            frame = None

            update_image()

            # 绑定键盘事件处理函数
            window.bind("<Key>", key_press)

            # 进入主循环
            window.mainloop()

            # 关闭视频文件
            video.release()
