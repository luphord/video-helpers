from pathlib import Path
from argparse import ArgumentParser, Namespace, ArgumentDefaultsHelpFormatter

from moviepy.editor import *
from moviepy import *


def sync_fade(in_file: Path, shift: float):
    video = VideoFileClip(str(in_file))
    video = video.subclip(t_start=shift, t_end=video.duration).fadein(3).fadeout(3)
    video.audio = video.audio.audio_fadein(3).audio_fadeout(3)
    return video


parser = ArgumentParser(
    description="Synchronize video and audio and add fade in/out for digitized video8",
    formatter_class=ArgumentDefaultsHelpFormatter,
)
parser.add_argument(
    "-o",
    "--output-folder",
    type=Path,
    help="Folder for video output",
    default=Path.cwd()
)
parser.add_argument(
    "-s",
    "--shift",
    type=float,
    help="Seconds to shift video forward (i.e. cut at beginning)",
    default=0.3
)
parser.add_argument("videos", type=Path, nargs="+")


if __name__=="__main__":
    args = parser.parse_args()
    args.output_folder.mkdir(parents=True, exist_ok=True)
    for in_file in args.videos:
        out_file = args.output_folder / in_file.name
        if out_file.exists():
            raise FileExistsError(out_file)
        video = sync_fade(in_file, args.shift)
        video.write_videofile(str(out_file), bitrate="2M")
