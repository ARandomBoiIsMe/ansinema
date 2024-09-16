import argparser

from handlers import image, video

def main():
    parser = argparser.initialize_argparse()
    args = parser.parse_args()

    if not (args.input or args.camera or args.vcall):
        parser.print_help()
        return

if __name__ == '__main__':
    main()