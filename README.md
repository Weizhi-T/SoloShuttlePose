# Introduction

Lightweight singles badminton player posture, court detection tool. The framework has a small amount of code and is easy to modify. You can use this tool to get the shuttle player's pose data in competition easily! It means you'll be able to analyze player play more easily using AI methods . 

# Functions implemented

1. court detect

2. multi-human detect

3. players detect

4. Automatically edits out videos from normal camera viewpoints

 # Upcoming Features

please look forward to...

# Update journal

2023/10/13: 
    
    Add "README.md" in the court-info-analysis.
    
    Fix the skipping frames bugs.

    Accelerate process by skipping some valid frames in the video.
    
    Finding valid frame using bisection so that the tool can process video faster.    

    Fix the frame count bug. (ori-version start from frame 1). 

    Fix the clipvideo fps which is different from the ori-video bug. 

2023/10/14:

    Fix the utils.write_json bug. 

    Add more information record about court and add new directory in courts.

    Add 3 test videos.

2023/10/15:

    Delete check_top_bot_court hyper-parameters. 

    Fix the bug about bisection algorithm because cv2 will Incorrectly estimated total number of frames. 

    Add more constraint in pre-process function to avoid detect wrong court for one seconds.

2023/10/18:

    Support manual selection of valid frames, you can use run "FrameSelect.py" and save the valid frame in references folder. 

2023/10/19:

    Modified the content of 'res/court/court_kp' form. 

