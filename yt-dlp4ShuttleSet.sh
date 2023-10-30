#!/bin/bash 

# Specify the directory path 
directory="./videos_bd"

source "D://Users//86153//anaconda3//etc//profile.d//conda.sh"
conda activate tracknetv3

# Verify that the yt-dlp command is installed.
if ! command -v yt-dlp &> /dev/null; then
    echo "yt-dlp command not found. Please install yt-dlp to continue."
    exit 1
fi

# Iterates through all subdirectories of the specified directory
for dir in "$directory"/*; do
    # Determine if the subdirectory is a directory, and if so, perform the following actions
    if [ -d "$dir" ]; then
        # Get the name of the subdirectory and replace the underscores with spaces
        dir_name=$(basename "$dir")
        search_name=${dir_name//_/' '}
        # Switch to a subdirectory and perform a search
        cd "$dir"
        yt-dlp --write-link --min-sleep-interval 10 --max-sleep-interval 120 "ytsearch:$search_name" -f 137 --restrict-filenames -o "$dir_name.mp4"
        # Switch back to parent directory
        cd ..
    fi
done


# Wait for the user to press any key and exit 
read -n 1 -s -r -p "按任意键退出"