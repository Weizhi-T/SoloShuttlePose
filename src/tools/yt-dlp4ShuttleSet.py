import os

# Specify the directory path
directory_1 = "ShuttleSet/ShuttleSet"
directory_2 = "ShuttleSet/ShuttleSet22"
directory = "./video_bd"

print("directory_1 = ShuttleSet/ShuttleSet",
      "directory_2 = ShuttleSet/ShuttleSet22",
      sep="\n")

choice = int(input("Please input number to choose directory: "))

if choice == 1:
    directory = directory_1
elif choice == 2:
    directory == directory_2
else:
    print("Please input 1 or 2!")
    exit(0)

# # Activate the relevant conda environment
# os.system("D://Users//86153//anaconda3//Scripts//activate.bat SoloShuttlePose")

# Iterates through all subdirectories of the specified directory
for dir in os.listdir(directory):
    # Determine if the subdirectory is a directory, and if so, perform the following actions
    if os.path.isdir(os.path.join(directory, dir)):
        # Get the name of the subdirectory and replace the underscores with spaces
        dir_name = os.path.basename(dir)
        search_name = dir_name.replace("_", " ")
        # Switch to a subdirectory and perform a search
        os.chdir(os.path.join(directory, dir))
        os.system(
            'yt-dlp --write-link --min-sleep-interval 10 --max-sleep-interval 120 "ytsearch:'
            + search_name + '" -f 137 --restrict-filenames -o "' + dir_name +
            '.mp4"')
        # Switch back to parent directory
        os.chdir("..")
