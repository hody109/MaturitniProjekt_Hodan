from moviepy.editor import VideoFileClip
import subprocess
import sys

def play_video(video_path):
    clip = VideoFileClip(video_path)
    clip.preview()
    clip.close()

def run_main_script():
    subprocess.Popen([sys.executable, 'main.py'])
    sys.exit()

if __name__ == "__main__":
    video_path = 'assets/outro.mp4'
    play_video(video_path)
    run_main_script()
