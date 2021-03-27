from sys import argv
from pathlib import Path
from moviepy.editor import *
from moviepy import *

if len(argv) < 2:
    print(f"Usage: {argv[0]} /path/to/video.mp4")
    sys.exit(1)

in_file = Path(argv[1])
out_file = in_file.parent / f"{in_file.stem}-fade-sync{in_file.suffix}"

video = VideoFileClip(str(in_file)).fadein(3).fadeout(3)
video.audio = video.audio.subclip(t_start=0.3, t_end=video.duration).audio_fadein(3).audio_fadeout(3)
video.write_videofile(str(out_file), bitrate="2M")