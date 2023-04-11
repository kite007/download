import os
import csv
import pathlib
from pytube import YouTube
from moviepy.editor import *
from pytube.exceptions import VideoUnavailable
import concurrent.futures
import ssl
import certifi

ssl.create_default_context = ssl.create_default_context(cafile=certifi.where())


def download_youtube_video(url, output_path):
    try:
        yt = YouTube(url)
        stream = yt.streams.filter(only_audio=True).first()
        return stream.download(output_path)
    except Exception as e:
        print(f"Error downloading video {url}: {e}")
        return None


def convert_to_mp3(input_path, output_path):
    try:
        video = VideoFileClip(input_path)
        video.audio.write_audiofile(output_path)
        video.close()
    except Exception as e:
        print(f"Error converting video {input_path} to mp3: {e}")


def process_row(row, target_folder):
    if len(row) < 3:
        return

    youtube_link = row[1]
    mp3_filename = row[2]
    mp4_filepath = os.path.join(
        target_folder, os.path.splitext(mp3_filename)[0] + '.mp4')
    mp3_filepath = os.path.join(target_folder, mp3_filename)

    print("youtube_link = "+youtube_link)
    print("mp3_filename = "+mp3_filename)
    print("mp3_filepath = "+mp3_filepath)
    print("target_folder = "+target_folder)

    if not os.path.exists(target_folder+'/'+mp3_filename):
        try:
            # video = YouTube(youtube_link)
            # audio_stream = video.streams.filter(only_audio=True).first()

            # audio_stream.download(output_path=target_folder,
            #                       filename=mp3_filename)
            download_youtube_video(youtube_link, target_folder)
            #convert_to_mp3(target_folder,)

        except VideoUnavailable:
            print("VideoUnavailable!!! ", target_folder, mp3_filename)
            # continue
        except Exception as e:
            print(f"Error downloading video {youtube_link}: {e}")
    else:
        print("이미 다운로드 받았음!! ", target_folder, mp3_filename)


source_folder = "audioset"

subfolders = [os.path.join(source_folder, f) for f in os.listdir(
    source_folder) if os.path.isdir(os.path.join(source_folder, f))]

for subfolder in subfolders:
    csv_files = [f for f in os.listdir(subfolder) if f.endswith('.csv')]

    for file in csv_files:
        folder_name = os.path.splitext(file)[0]
        target_folder = os.path.join(subfolder, folder_name)

        with open(os.path.join(subfolder, file), 'r', encoding='utf-8') as csvfile:
            csvreader = csv.reader(csvfile)
            with concurrent.futures.ThreadPoolExecutor() as executor:
                executor.map(lambda row: 
                             process_row(row, target_folder), 
                             csvreader)
            # for row in csvreader:
            #     process_row(row, target_folder)
