import argparse

def initialize_argparse() -> argparse.ArgumentParser:
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

    parser.add_argument(
        '--target_ip',
        help='IP address of destination computer. Provide this along with --target_port and --out_port to act \
              as the connecting device.'
    )

    parser.add_argument(
        '--target_port',
        help='Port number of destination computer. Provide this along with --target_ip and --out_port to act \
              as the connecting device.',
        type=int
    )

    return parser