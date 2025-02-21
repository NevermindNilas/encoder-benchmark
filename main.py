"""
This is the main file for the project.
Simple validation tool that tells you for a given video file,
what encoding settings give you the best quality.
"""

import argparse
import sys

import os
from src.getFFMPEG import getFFMPEG
from version import __version__

# Some global vars for the project
# I will always download the latest FFMPEG build
# from the official sources
SYSUSED = sys.platform
DOWNLOADDIR = os.path.join(os.path.dirname(__file__), "ffmpeg")


def main():
    parser = argparse.ArgumentParser(description="A simple project.")
    parser.add_argument(
        "--version",
        action="version",
        version=f"{__version__}",
    )

    parser.add_argument(
        "--input",
        type=str,
        help="Input file",
        required=True,
    )

    parser.add_argument(
        "--method",
        type=str,
        help="Method to use",
        choices=["vmaf"],
        default="vmaf",
    )

    parser.add_argument(
        "--encode",
        type=str,
        help="Encode settings you wish to test",
        default="",
        required=True,
    )

    args = parser.parse_args()

    print(args)

    ffmpegPath = getFFMPEG(SYSUSED, DOWNLOADDIR)
    print(ffmpegPath)


if __name__ == "__main__":
    main()
