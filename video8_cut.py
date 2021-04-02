from moviepy.editor import *
from moviepy import *
import csv
from pathlib import Path
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter


def sync_fade(video: VideoFileClip, start: float, end: float, shift: float, fade: float):
    audio = video.audio
    video = video.subclip(t_start=start + shift, t_end=end).fadein(fade).fadeout(fade)
    video.audio = audio.subclip(t_start=start, t_end=end - shift).audio_fadein(fade).audio_fadeout(fade)
    return video

parser = ArgumentParser(
    description="Load LosslessCut CSV file, cut into segments, synchronize video and audio and add fade in/out for digitized video8",
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
    default="3M"
)
parser.add_argument("csvs", type=Path, nargs="+")


if __name__=="__main__":
    args = parser.parse_args()
    args.output_folder.mkdir(parents=True, exist_ok=True)
    for csvpath in args.csvs:
        mp4path = csvpath.parent / (csvpath.stem.replace("-llc-edl", "") + ".mp4")
        video = VideoFileClip(str(mp4path))
        with open(csvpath) as csvfile:
            for row in csv.reader(csvfile, delimiter=","):
                assert len(row) == 3, f"Expecting 3 columns, got {len(row)}"
                start = float(row[0]) if row[0] else video.start
                end = float(row[1]) if row[1] else video.duration
                name = row[2]
                if name:
                    subclip = sync_fade(video, start, end, args.shift, args.fade)
                    out_file = args.output_folder / f"{name}.mp4"
                    if out_file.exists():
                        raise FileExistsError(out_file)
                    subclip.write_videofile(str(out_file), bitrate=args.bitrate)