from app import db
from app.models import Video
from datetime import datetime
import subprocess
import os, time

BASE_DIR = r"D:\work\tm"
ffprobe = r"D:\work\tm\utilities\ffmpeg\bin\ffprobe.exe"
MEDIADIR = os.path.join(BASE_DIR, 'media')
CATEGORIES = ("1st", "2nd", "videos")
active = True


def get_video_info(video):
    result = subprocess.run([ffprobe, "-v", "error", "-show_entries",
                             "format", "-sexagesimal", "-of",
                             "default=noprint_wrappers=1:nokey=0", video],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT)
    dirty_info = str(result.stdout)[2:].split('\\r\\n')
    info = {}

    for i in dirty_info:
        try:
            temp = i.split("=")
            info[temp[0]] = temp[1]
        except IndexError:
            break
    return info


def get_monitor_folders(directory):
    """Monitor media_root folder and returns, list of pairs (directory_name, directory_full_path)
    if directory_name coincides with video categories names"""
    folders_list = []
    print("Start")
    for folder in os.listdir(directory):
        if folder in CATEGORIES:
            folders_list.append((folder, os.path.join(directory, folder)))
    return folders_list


def check_in_video(name, cat, path):

    if Video.query.filter_by(full_path=path).first() is not None:
        print("Video already in DB.")
        return 1
    else:
        if os.path.isfile(path):
            print("New file found:", path)
            video = Video(name=os.path.splitext(name)[0],
                          category=cat,
                          path=os.path.join(cat, name).replace('\\', '/'),
                          full_path=path,
                          creation_date=datetime.utcnow(),
                          )
            v_info = get_video_info(path)
            video.set_duration(v_info)
            video.set_size(v_info)
            db.session.add(video)
            db.session.commit()
            print("done")
            return 0
        else:
            return 2


def monitor(directory_list):
    """List of monitored directories in format [(directory_name, directory_full_path),]"""
    print('Start monitor...')
    for dir_name, dir_path in directory_list:
        print("Категория:", dir_name)
        for video in os.listdir(dir_path):
            print("Before check in ", video)
            if check_in_video(video, dir_name, os.path.join(dir_path, video))==0:
                continue


def main(directory):
    global active
    monitor_folders = get_monitor_folders(directory)
    while active:
        monitor(monitor_folders)
        time.sleep(20)
    else:
        print("active=False, exit from program")
        return 1



main(MEDIADIR)