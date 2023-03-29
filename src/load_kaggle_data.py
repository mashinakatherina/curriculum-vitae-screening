import os
import shutil
from pathlib import Path

dataset_name = "eenardeshmukh/curriculum-vitae"

def copy_api_settings():
    src_config_file_path = os.path.abspath(os.path.join(os.path.realpath(__file__), "..", "..", "kaggle.json"))
    dst_config_file_dir = os.path.join(Path.home(), ".kaggle")
    dst_config_file_path = os.path.join(dst_config_file_dir, "kaggle.json")
    if not os.path.isdir(dst_config_file_dir):
        os.makedirs(dst_config_file_dir, exist_ok=True)
    if not os.path.isfile(dst_config_file_path):
        shutil.copy(src_config_file_path, dst_config_file_dir)



if __name__ == "__main__":
    copy_api_settings()
    os.system("cd ~")
    os.system("kaggle datasets download" + " " + dataset_name)

