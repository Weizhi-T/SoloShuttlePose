import pandas as pd
import os

def split_data_by_match_and_rally(shot_path,match_dict):
    shot_df = pd.read_csv(shot_path)
    matches = shot_df.groupby('match_id')

    for match_id, match_data in matches:
        video=match_dict[str(match_id)]
        folder_path = f'ShuttleSet/ShuttleSet22/match/{video}'
        os.makedirs(folder_path, exist_ok=True)

        rallies = match_data.groupby('rally_id')
        rid=1
        for rally_id, rally_data in rallies:
            rally_filename = f'rally_{rid}.csv'
            rid+=1 
            rally_data.to_csv(os.path.join(folder_path, rally_filename), index=False)

shot_path = 'ShuttleSet\ShuttleSet22\set\shot_metadata.csv'  
match_path= 'ShuttleSet\ShuttleSet22\set\match.csv'

match_dict={}
df=pd.read_csv(match_path)
for index, row in df.iterrows():
    match_id = str(int(row["id"]))
    video=row['video']
    match_dict[match_id]=video

split_data_by_match_and_rally(shot_path,match_dict)