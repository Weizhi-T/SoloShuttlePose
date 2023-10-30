
You can download weights in https://drive.google.com/drive/folders/16mVjXrul3VaXKfHHYauY0QI-SG-JVLvL?usp=sharing

add the weight folder to the "src/model"

# Creating a Environment

```
conda create --name SoloShuttlePose python=3.9
```

# Install the required packages

```
pip install 'docs/requirements.txt'
```


# If you want to manually select the valid frames, you can run the following code.

```
python FrameSelect.py --folder_path "videos"
```

# Run the following code for player, court ,net detect.

Process only unprocessed video.

```
python main.py --folder_path "videos" --result_path "res" 
```

Force processing of all videos, including those that have already been processed.

```
python main.py --folder_path "videos" --result_path "res" --force
```

# Draw the court,  net, and players

Process only unprocessed video.

```
python VideoDraw.py --folder_path "videos" --result_path "res" --court --net --players --ball
```

Force processing of all videos, including those that have already been processed.

```
python VideoDraw.py --folder_path "videos" --result_path "res" --force --court --net --players --ball --trajectory
```

