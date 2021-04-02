from pathlib import Path
from argparse import ArgumentParser, Namespace, ArgumentDefaultsHelpFormatter

from moviepy.editor import *
from moviepy import *


def sync_fade(in_file: Path, shift: float, fade: float):
    video = VideoFileClip(str(in_file))
    audio = video.audio
    video = video.subclip(t_start=shift, t_end=video.duration).fadein(fade).fadeout(fade)
    video.audio = audio.subclip(t_start=0, t_end=audio.duration - shift).audio_fadein(fade).audio_fadeout(fade)
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
parser.add_argument(
    "-f",
    "--fade",
    type=float,
    help="Seconds to fade video/audio in/out",
    default=3
)
parser.add_argument(
    "-b",
    "--bitrate",
    type=str,
    help="Seconds to fade video/audio in/out",
    default="2M"
)
parser.add_argument("videos", type=Path, nargs="+")


if __name__=="__main__":
    args = parser.parse_args()
    args.output_folder.mkdir(parents=True, exist_ok=True)
    for in_file in args.videos:
        out_file = args.output_folder / in_file.name
        if out_file.exists():
            raise FileExistsError(out_file)
        video = sync_fade(in_file, args.shift, args.fade)
        video.write_videofile(str(out_file), bitrate=args.bitrate)
