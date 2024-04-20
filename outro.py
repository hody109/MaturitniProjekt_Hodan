from moviepy.editor import VideoFileClip
import subprocess
import sys

def play_video(video_path):
    """
    Plays a video file from the specified path using MoviePy.

    :param video_path: The file path of the video to be played.
    :type video_path: str
    """
    clip = VideoFileClip(video_path)
    clip.preview()
    clip.close()

def run_main_script():
    """
    Runs the main game script (`main.py`) and exits the current script.
    """
    subprocess.Popen([sys.executable, 'main.py'])
    sys.exit()

if __name__ == "__main__":
    video_path = 'assets/outro.mp4'
    play_video(video_path)
    run_main_script()
