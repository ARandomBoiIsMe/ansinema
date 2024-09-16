from argparse import Namespace
import os

import argparser
from handlers import image, video

def video_call(args: Namespace):
    pass

def display_camera_view(args: Namespace):
    video.VideoHandler(
        camera=True,
        print_char=args.print_character if args.print_character is not None else "█"
    ).display()

def display_media(args: Namespace):
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp']
    video_extensions = ['.mp4', '.avi', '.mov', '.wmv', '.flv', '.mkv', '.webm']

    _, extension = os.path.splitext(args.input)

    if extension in image_extensions:
        display_image(args)
    elif extension in video_extensions:
        display_video(args)
    else:
        raise ValueError("Unsupported media format. Raise an issue to suggest support for this format.")

def display_image(args: Namespace):
    image.ImageHandler(
        args.input,
        args.print_character if args.print_character is not None else "█"
    ).display()

def display_video(args: Namespace):
    video.VideoHandler(
        path=args.input,
        print_char=args.print_character if args.print_character is not None else "█"
    ).display()

def main() -> None:
    parser = argparser.initialize_argparse()
    args = parser.parse_args()

    if not (args.input or args.camera or args.vcall):
        parser.print_help()
        return

    if args.print_character and len(args.print_character) != 1:
        raise ValueError("print_character must be a single character")

    if args.vcall:
        video_call(args)
    elif args.camera:
        display_camera_view(args)
    elif args.input:
        display_media(args)

if __name__ == '__main__':
    main()