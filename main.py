from argparse import Namespace
import os
import threading

import argparser
from handlers import image, video
import connection

def print_server_welcome_message(ip: str, port: int):
    message = "\nTerminal Video Call\n"
    message += "===================\n\n"

    message += "Hey!\n"
    message += f"Another device in your network can connect to you at this address - {ip}:{port}\n\n"

    message += "===================\n"

    print(message)

def print_client_welcome_message(args: Namespace):
    message = "\nTerminal Video Call\n"
    message += "===================\n\n"

    message += f"Hey! You'll be connected to {args.target_ip}:{args.target_port} soon.\n\n"

    message += "===================\n"

    print(message)

def video_call(args: Namespace):
    ip = connection.get_ip_address()
    port = connection.get_port()

    if not args.target_ip and not args.target_port:
        print_server_welcome_message(ip, port)
    else:
        print_client_welcome_message(args)

    sock = connection.setup_connection(port, args)

    vid_handle = video.VideoHandler(
        color=args.color if args.color is not None else False,
        camera=True,
        print_char=args.print_character if args.print_character is not None else "█"
    ).stream()

    threading.Thread(target=connection.send_video_data, args=(sock,)).start()
    threading.Thread(target=connection.receive_video_data, args=(sock, vid_handle)).start()

def display_camera_view(args: Namespace):
    print("Starting webcam...")

    video.VideoHandler(
        color=args.color if args.color is not None else False,
        camera=True,
        print_char=args.print_character if args.print_character is not None else "█"
    ).display()

def display_media(args: Namespace):
    if not os.path.exists(args.input):
        raise ValueError("File not found.")

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
        color=args.color if args.color is not None else False,
        path=args.input,
        print_char=args.print_character if args.print_character is not None else "█"
    ).display()

def display_video(args: Namespace):
    video.VideoHandler(
        color=args.color if args.color is not None else False,
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