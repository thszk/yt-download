#! /usr/bin/env python3

import os, re, platform
from pytube import YouTube
from moviepy.editor import AudioFileClip

# configurations
if platform.system() == 'Linux':
    os.environ['IMAGEIO_FFMPEG_EXE'] = '/usr/bin/ffmpeg'

current_dir = os.path.dirname(__file__)
output_dir = os.path.join(current_dir, 'output')
input_file_path = os.path.join(current_dir, 'input.txt')
log_file_path = os.path.join(current_dir, 'log.txt')

print('>>>> yt-download.py')
print('>>>> output directory: ', current_dir)
print('>>>> input file: ', input_file_path)

# open files
input_file = open(input_file_path, 'r', encoding='utf-8')
log_file = open(log_file_path, 'w', encoding='utf-8')

# download videos
for url in input_file:
    try:
        print('... Downloading', url)
        youtube = YouTube(url)

        if youtube.author.endswith(' - Topic'):
            name = youtube.author[:8] + ' - ' + youtube.title
        else:
            name = youtube.author + ' - ' + youtube.title

        youtube.streams.get_audio_only().download(output_dir, name)
    except Exception as e:
        print('xxxx Download error', url, e)
        log_file.write('xxxx Download error' + url)

# convert to .mp3 and remove .mp4
for mp4_file in os.listdir(output_dir):
    try: 
        if re.search('mp4', mp4_file):
            mp4_file_path = os.path.join(output_dir, mp4_file)
            mp3_file_path = os.path.join(output_dir, os.path.splitext(mp4_file)[0] + '.mp3')

            mp3_file = AudioFileClip(mp4_file_path)
            mp3_file.write_audiofile(mp3_file_path)

            os.remove(mp4_file_path)
    except Exception as e:
        filepath = os.path.join(output_dir, mp4_file)
        print('xxxx Convertion error', filepath, e)
        log_file.write('xxxx Convertion error' + filepath + '\n')

# close files
input_file.close()
log_file.close()