import json
import os
import shutil
import json


def is_file_empty(file_path):
    return os.path.getsize(file_path) == 0


def write_json(data, file_name, save_path="./"):
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    full_path = os.path.join(save_path, f"{file_name}.json")

    if not os.path.exists(full_path):
        with open(full_path, 'w') as file:
            pass

    with open(full_path, 'r+') as file:
        for key, value in data.items():
            if is_file_empty(full_path):
                file.write('{}')
                file.seek(0, os.SEEK_END)
                file.seek(file.tell() - 1, os.SEEK_SET)
                file.write('\n')
                file.write(json.dumps(key, indent=4))
                file.write(': ')
                file.write(json.dumps(value, indent=4))
                file.write('\n')
                file.write('}')
                return

            file.seek(0, os.SEEK_END)
            file.seek(file.tell() - 2, os.SEEK_SET)
            file.write(',')
            file.write('\n')
            file.write(json.dumps(key, indent=4))
            file.write(': ')
            file.write(json.dumps(value, indent=4))
            file.write('\n')
            file.write('}')
    return


def is_video_detect(defile_name, save_path="res"):
    if not os.path.exists(save_path):
        print(f"The path {save_path} does not exist!")
        return False

    for root, dirs, files in os.walk(save_path):

        for file in files:
            file_name = file.split('.')[0]

            if defile_name == file_name:
                file_path = os.path.join(root, file)
                print(
                    f"{file_path} has been processed! If you still want to process it, please set force_process as True. "
                )
                return True


def clear_file(defile_name, save_path="res"):
    if not os.path.exists(save_path):
        print(f"The path {save_path} does not exist!")
        return

    for root, dirs, files in os.walk(save_path):
        for dir_name in dirs:
            if dir_name == defile_name:
                dir_path = os.path.join(root, dir_name)
                shutil.rmtree(dir_path)
                print(f"Folder '{defile_name}' has been deleted: {dir_path}")
                continue

        for file in files:
            file_name = file.split('.')[0]
            if defile_name == file_name:
                file_path = os.path.join(root, file)
                os.remove(file_path)
                print(f"{file_path} has been deleted.")


if __name__ == "__main__":
    test = False
    clear_file("test1")
    if not test:
        exit(0)
    data1 = {"0": {"top": None, "bottom": None}}
    data2 = {"1": {"top": None, "bottom": None}}
    data3 = {"2": {"top": None, "bottom": None}}

    write_json(data1, "demo")
    write_json(data2, "demo")
    write_json(data3, "demo")

    import pandas as pd

    data = pd.read_json("demo.json")
    print(data)
