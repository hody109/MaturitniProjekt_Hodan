from moviepy.editor import VideoFileClip
import subprocess
import sys

def play_video(video_path):
    # Načtení videoklipu
    clip = VideoFileClip(video_path)
    # Přehrávání videa
    clip.preview()
    # Uzavření videoklipu po dokončení
    clip.close()

def run_main_script():
    # Spuštění dalšího skriptu
    subprocess.Popen([sys.executable, 'main.py'])
    sys.exit()

if __name__ == "__main__":
    # Cesta k videu
    video_path = 'assets/outro.mp4'
    # Přehrát video
    play_video(video_path)
    # Po skončení videa spustit main.py
    run_main_script()
