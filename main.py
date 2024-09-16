from argparse import Namespace

import argparser
from handlers import image, video

def video_call(args: Namespace):
    pass

def display_camera_view(args: Namespace):
    pass

def display_media(args: Namespace):
    pass

def main() -> None:
    parser = argparser.initialize_argparse()
    args = parser.parse_args()

    if not (args.input or args.camera or args.vcall):
        parser.print_help()
        return

    if args.vcall:
        video_call(args)
    elif args.camera:
        display_camera_view(args)
    elif args.input:
        display_media(args)

if __name__ == '__main__':
    main()