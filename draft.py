import cv2

video_path = "res/videos/test2/test2_0-526.mp4"
video = cv2.VideoCapture(video_path)
# Get video properties
fps = video.get(cv2.CAP_PROP_FPS)
total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
video.set(cv2.CAP_PROP_POS_FRAMES, total_frames - 1)
ret, frame = video.read()
if not ret:
    print("yes")
else:
    print("not")
    print(frame)

print(f"fps: {fps}")
print(f"total_frames: {total_frames}")
