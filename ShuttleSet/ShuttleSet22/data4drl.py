import os
import glob
import sys
import pandas as pd

sys.path.append("src/tools")
from utils import read_json, write_json

import math

def edist(x1, y1, x2, y2):
    dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return dist

loca4match="E:/res/ball/loca_info"
player4match="E:/res/players/player_kp"
action4match="ShuttleSet/ShuttleSet22/match"
court4match="E:/res/courts/court_kp"

result_path="res"
        
for dir in os.listdir(action4match):
    if os.path.isdir(os.path.join(action4match, dir)):
        dir_name = os.path.basename(dir)
        print(dir_name)
        loca_path=os.path.join(loca4match,dir_name)
        if not os.path.exists(loca_path):
            continue
        loca_dict={}
        for json_path in glob.glob(os.path.join(loca_path, "*.json")):
            loca_dict.update(read_json(json_path))
        
        court_dict=read_json(os.path.join(court4match,f"{dir_name}.json"))
        
        player_dict=read_json(os.path.join(player4match,f"{dir_name}.json"))
        action_path=os.path.join(action4match,dir_name)


        for csv_path in glob.glob(os.path.join(action_path, "*.csv")):
            df = pd.read_csv(csv_path)
            # 创建一个新的DataFrame存储修改后的数据
            new_df = []
            hit_list=[]
            for index, row in df.iterrows():
                frame_num = row['frame_num']
                
                fn=frame_num
                while str(fn) in loca_dict.keys() and\
                    (loca_dict[str(fn)]['visible']==0 or\
                        loca_dict[str(fn)]['x']==0):
                        fn-=1
                
                court_info=court_dict['court_info']
                top_l=abs(court_info[0][1]-court_info[2][1])
                bottom_l=abs(court_info[2][1]-court_info[4][1])

                row['x'] = loca_dict[str(fn)]['x']
                row['y'] = loca_dict[str(fn)]['y']
                
                while player_dict[str(frame_num)]['top'] is None and\
                player_dict[str(frame_num)]['bottom'] is None:
                    frame_num-=1

                row['top'] = player_dict[str(frame_num)]['top']
                row['bottom'] = player_dict[str(frame_num)]['bottom']
                ball=(loca_dict[str(frame_num)]['x'],loca_dict[str(frame_num)]['y'])
                
                top_kp9,top_kp10=player_dict[str(frame_num)]['top'][9],player_dict[str(frame_num)]['top'][10]
                top_kp15,top_kp16=player_dict[str(frame_num)]['top'][11],player_dict[str(frame_num)]['top'][16]
                top_kp17=[(top_kp15[0]+top_kp16[0])/2,(top_kp15[1]+top_kp16[1])/2]
                row['top'].append(top_kp17)

                bottom_kp9,bottom_kp10=player_dict[str(frame_num)]['bottom'][9],player_dict[str(frame_num)]['bottom'][10]
                bottom_kp15,bottom_kp16=player_dict[str(frame_num)]['bottom'][15],player_dict[str(frame_num)]['bottom'][16]
                bottom_kp17=[(bottom_kp15[0]+bottom_kp16[0])/2,(bottom_kp15[1]+bottom_kp16[1])/2]
                row['bottom'].append(bottom_kp17)

                ball2top=abs(ball[1]-top_kp17[1])#edist(ball[0],ball[1],top_kp17[0],top_kp17[1])
                ball2bottom=abs(ball[1]-bottom_kp17[1])#edist(ball[0],ball[1],bottom_kp17[0],bottom_kp17[1])
                # print(top_l,bottom_l)
                # print(ball2top,ball2bottom)
                # print(ball2top/bottom_l,ball2bottom/top_l)
                
                print(ball[1],court_dict['net_info'][0][1])
                ball2net=(ball[1]-court_dict['net_info'][0][1])
                print(ball2net)
                if ball2net<0:
                    row['player']='top'
                else:
                    row['player']='bottom'


                # 将修改后的row添加到新的DataFrame中
                new_df.append(row)

            new_df = pd.DataFrame(new_df)
            # 将修改后的数据保存到新文件中
            new_df.to_csv("new_file.csv", index=False, encoding="utf-8")
            
            exit()
