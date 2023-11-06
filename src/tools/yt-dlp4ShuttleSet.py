import os
import shutil

source_directory = "ShuttleSet/ShuttleSet22/match"
target_directory = "ShuttleSet/ShuttleSet22/match_db"

# 确保要删除的文件夹存在
if os.path.exists(target_directory):
    pass
else:
   shutil.copytree(source_directory, target_directory)
   print(f"create {target_directory}")
   
# limit_num为30时表示遍历的前30个不下载，只下载以后的
limit_num=0#30
video_cnt=0

# 遍历目录下的子目录
for dir in os.listdir(target_directory):
    if os.path.isdir(os.path.join(target_directory, dir)):
        dir_name = os.path.basename(dir)
        search_name = dir_name.replace(".", "_")
        search_name = search_name.replace("-", "_")
        os.rename(os.path.join(target_directory, dir),
                  os.path.join(target_directory, search_name))

# download video
for dir in os.listdir(target_directory):
    if os.path.isdir(os.path.join(target_directory, dir)):
        dir_name = os.path.basename(dir)
        print(dir_name)
        video_cnt+=1
        if video_cnt<=limit_num:
            continue
        search_name = dir.replace("_", " ")
        # 切换到子目录并执行搜索
        os.chdir(os.path.join(target_directory, dir))
        os.system(
            'yt-dlp --write-link --min-sleep-interval 10 --max-sleep-interval 120 "ytsearch:'
            + search_name + '" -f 137 --restrict-filenames -o "' + dir_name +
            '.mp4"')
        # 切换回父目录
        os.chdir("..")
