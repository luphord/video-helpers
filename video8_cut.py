from moviepy.editor import *
from moviepy import *
import csv
from pathlib import Path
from sys import argv

csvpath = Path(argv[1])
mp4path = csvpath.parent / (csvpath.stem.replace("-llc-edl", "") + ".mp4")
output_folder = Path.cwd()
video = VideoFileClip(str(mp4path))
fade = 3
shift = 0.3
bitrate = "3M"

def sync_fade(video: VideoFileClip, start: float, end: float, shift: float, fade: float):
    audio = video.audio
    video = video.subclip(t_start=start + shift, t_end=end).fadein(fade).fadeout(fade)
    video.audio = audio.subclip(t_start=start, t_end=end - shift).audio_fadein(fade).audio_fadeout(fade)
    return video

with open(csvpath) as csvfile:
    for row in csv.reader(csvfile, delimiter=","):
        assert len(row) == 3, f"Expecting 3 columns, got {len(row)}"
        start = float(row[0]) if row[0] else video.start
        end = float(row[1]) if row[1] else video.duration
        name = row[2]
        if name:
            subclip = sync_fade(video, start, end, shift, fade)
            outfile = output_folder / f"{name}.mp4"
            subclip.write_videofile(str(outfile), bitrate=bitrate)