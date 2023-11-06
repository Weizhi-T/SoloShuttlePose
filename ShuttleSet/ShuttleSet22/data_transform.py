import pandas as pd
import os

def split_data_by_match_and_rally(shot_path,match_dict):
    # 读取 CSV 文件
    shot_df = pd.read_csv(shot_path)

    # 根据 match_id 划分数据
    matches = shot_df.groupby('match_id')

    for match_id, match_data in matches:
        video=match_dict[str(match_id)]
        # 创建文件夹
        folder_path = f'ShuttleSet/ShuttleSet22/set/match/{video}'
        os.makedirs(folder_path, exist_ok=True)

        # 根据 rally_id 划分数据
        rallies = match_data.groupby('rally')
        for rally_id, rally_data in rallies:
            # 构建新的文件名
            rally_filename = f'rally_{rally_id}.csv'
            
            # 保存为 CSV 文件
            rally_data.to_csv(os.path.join(folder_path, rally_filename), index=False)

# 使用示例
shot_path = 'ShuttleSet\ShuttleSet22\set\shot_metadata.csv'  # 替换为你的 CSV 文件路径
match_path= 'ShuttleSet\ShuttleSet22\set\match.csv'

match_dict={}
df=pd.read_csv(match_path)
for index, row in df.iterrows():
    # the transfrom is to avoid int68 which leads to json something wrong
    match_id = str(int(row["id"]))
    video=row['video']
    match_dict[match_id]=video

split_data_by_match_and_rally(shot_path,match_dict)