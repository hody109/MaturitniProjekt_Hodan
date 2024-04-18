from moviepy.editor import VideoFileClip
import subprocess
import sys
import os

os.environ['SDL_VIDEO_CENTERED'] = '1'  # Center the pygame window on the screen

def play_video(video_path):
    clip = VideoFileClip(video_path)
    clip.preview()
    clip.close()

def run_main_script():
    subprocess.Popen([sys.executable, 'level0.py'])
    sys.exit()

if __name__ == "__main__":
    video_path = 'assets/intro.mp4'
    play_video(video_path)
    run_main_script()
