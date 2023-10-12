import cv2
import os


class VideoClip(object):
    def __init__(self,
                 video_name,
                 fps,
                 total_frames,
                 frame_height,
                 frame_wight,
                 save_path="./") -> None:
        self.video_name = video_name
        self.save_path = save_path
        self.fps = int(fps)
        self.total_frames = total_frames
        self.frame_height = frame_height
        self.frame_wight = frame_wight
        self.frame_list = []
        self.begin = 0
        self.end = 0
        self.no_court_cnt = 0

    def __setup(self):
        self.frame_list = []

    def add_frame(self, have_court, frame, frame_count):
        if frame_count == self.total_frames:
            if len(self.frame_list) < self.fps:
                self.frame_list.clear()
                self.begin = 0
                self.end = 0
                return
            self.end = frame_count
            self.frame_list.append(frame)
            self.__make_video()
            self.__setup()
            self.no_court_cnt = 0
            return

        if have_court:
            if self.begin == 0:
                self.begin = frame_count
            self.frame_list.append(frame)
        elif not have_court:
            if len(self.frame_list) < self.fps:
                self.frame_list.clear()
                self.begin = 0
                self.end = 0
            elif len(self.frame_list) >= self.fps and len(
                    self.frame_list) > self.fps * 3:
                # for test.mp4, the 988 and 989 results are weird
                # the 5 frames after have_court=false will also be recorded
                if self.no_court_cnt >= (self.fps // 2):
                    self.end = frame_count
                    self.__make_video()
                    self.__setup()
                    self.no_court_cnt = 0
                else:
                    self.frame_list.append(frame)
                    self.no_court_cnt += 1
        return

    def __make_video(self):

        # 设置输出视频的名称、编解码器、帧率和视频分辨率
        video_name = f"{self.video_name}_{self.begin}-{self.end}.mp4"
        full_path = os.path.join(self.save_path, video_name)

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        fps = self.fps
        output_video_format = (self.frame_wight, self.frame_height)

        video_writer = cv2.VideoWriter(full_path, fourcc, fps,
                                       output_video_format)

        # 遍历列表中的每个元素，将元素绘制到图像上，并将图像写入到视频中
        for frame in self.frame_list:
            video_writer.write(frame)

        # 释放资源
        video_writer.release()