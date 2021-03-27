from pathlib import Path
from argparse import ArgumentParser, Namespace, ArgumentDefaultsHelpFormatter

from moviepy.editor import *
from moviepy import *


def sync_fade(in_file: Path):
    video = VideoFileClip(str(in_file))
    video = video.subclip(t_start=0.3, t_end=video.duration).fadein(3).fadeout(3)
    video.audio = video.audio.audio_fadein(3).audio_fadeout(3)
    return video


parser = ArgumentParser(
    description="Synchronize video and audio and add fade in/out for digitized video8",
    formatter_class=ArgumentDefaultsHelpFormatter,
)
parser.add_argument("videos", type=Path, nargs="+")


if __name__=="__main__":
    args = parser.parse_args()
    for in_file in args.videos:
        out_file = in_file.parent / f"{in_file.stem}-fade-sync{in_file.suffix}"
        video = sync_fade(in_file)
        video.write_videofile(str(out_file), bitrate="2M")
