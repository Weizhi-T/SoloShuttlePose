import json
import os


def write_json(data, file_name, save_path="./"):
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    full_path = os.path.join(save_path, f"{file_name}.json")
    with open(full_path, "a") as file:
        json.dump(data, file, indent=4)
        file.write(",")  # 写入逗号
    return


import os


def clear_file(defile_name, save_path="res"):
    if not os.path.exists(save_path):
        print(f"The path {save_path} does not exist!")
        return

    for root, dirs, files in os.walk(save_path):
        for file in files:
            file_name = file.split('.')[0]

            if defile_name == file_name:

                # print(file)
                file_path = os.path.join(root, file)
                os.remove(file_path)
                print(f"{file_path} has been deleted.")


if __name__ == "__main__":

    # 调用函数并传入参数
    file_name = "a"
    save_path = "res"

    clear_file(file_name, save_path)
