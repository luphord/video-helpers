from moviepy.editor import *
from moviepy import *
import numpy as np
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from pathlib import Path


def concatenate_reverse_padding(clips, padding=0, bg_color=None):
    timings = np.cumsum([0] + [clip.duration for clip in clips])

    sizes = [clip.size for clip in clips]

    w = max(size[0] for size in sizes)
    h = max(size[1] for size in sizes)

    timings = np.maximum(0, timings + padding * np.arange(len(timings)))
    timings[-1] -= padding  # Last element is the duration of the whole

    result = CompositeVideoClip(
        list(
            reversed(
                [
                    clip.set_start(t).set_position("center")
                    for (clip, t) in zip(clips, timings)
                ]
            )
        ),
        size=(w, h),
        bg_color=bg_color,
        ismask=False,
    )

    result.timings = list(reversed(timings))

    result.start_times = list(reversed(timings[:-1]))
    result.start, result.duration, result.end = 0, timings[-1], timings[-1]

    audio_t = [
        (clip.audio, t) for clip, t in zip(clips, timings) if clip.audio is not None
    ]
    if audio_t:
        result.audio = CompositeAudioClip([a.set_start(t) for a, t in audio_t])

    fpss = [clip.fps for clip in clips if getattr(clip, "fps", None) is not None]
    result.fps = max(fpss) if fpss else None
    return result


parser = ArgumentParser(
    description="Concatenate videos with padding (overlap) and audio fade-in/out",
    formatter_class=ArgumentDefaultsHelpFormatter,
)
parser.add_argument(
    "-o",
    "--output",
    type=Path,
    help="Folder for video output",
    default=Path.cwd() / "out.mp4",
)
parser.add_argument(
    "-p",
    "--padding",
    type=float,
    help="Seconds to pad/overlap between clips",
    default=3,
)
parser.add_argument(
    "-f", "--fade", type=float, help="Seconds to fade video/audio in/out", default=3
)
parser.add_argument("videos", type=Path, nargs="+")


if __name__ == "__main__":
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    if args.output.exists():
        raise FileExistsError(args.output)

    videos = [
        VideoFileClip(str(fname)).audio_fadein(args.padding).audio_fadeout(args.padding)
        for fname in args.videos
    ]
    videos[0] = videos[0].fadein(args.fade)
    videos[-1] = videos[-1].fadeout(args.fade)

    result = concatenate_reverse_padding(videos, padding=-args.padding)
    result.write_videofile(str(args.output))
