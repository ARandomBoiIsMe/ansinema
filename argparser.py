import argparse

def initialize_argparse():
    parser = argparse.ArgumentParser(
        prog='python main.py',
        description='Renders images and videos to the terminal. Supports video calls too, yay.'
    )

    parser.add_argument(
        '-i',
        '--input',
        help='Input media path'
    )

    parser.add_argument(
        '-c',
        '--camera',
        help='Display view from webcam',
        action='store_true'
    )

    parser.add_argument(
        '-v',
        '--vcall',
        help='Initiate a video call',
        action='store_true'
    )

    parser.add_argument(
        '-p',
        '--print_character',
        help='Character to be used as pixel on terminal'
    )

    return parser