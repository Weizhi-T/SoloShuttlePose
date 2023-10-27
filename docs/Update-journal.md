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

2023/10/22:
 
    Add the "NetDetect.py" for net detection.
    
    Make "FrameSelect.py" select frames faster by selecting from the center. 

    Fix the "CourtDetect.py", "NetDetect.py" and "FrameSelect.py" bugs.

    Delete the court-info-analysis folder.   

2023/10/23:

    Delete the model folder, you can download in https://drive.google.com/drive/folders/16mVjXrul3VaXKfHHYauY0QI-SG-JVLvL?usp=sharing

2023/10/27:

    Adding Terminal Passing Parameters. 

    Modified project file structure. 

    Separate detection from keypoint mapping, split 'main.py' into two files: 'main.py' and 'FrameSelect.py'.
