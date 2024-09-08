import os
import subprocess
import time
import threading

class VideoHandler:
    def __init__(self, path: str, print_char: str = "█") -> None:
        self.path = path
        self.print_char = print_char

    def display(self):
        parser = VideoParser(self.path, self.print_char)

        parser.parse()

class VideoParser:
    def __init__(self, path: str, print_char: str) -> None:
        self.path = path
        self.print_char = print_char
        self.file_name = self.__get_video_file_name()
        self.dirname = os.path.splitext(self.file_name)[0]

    def __get_video_file_name(self):
        return os.path.basename(self.path)

    def __create_video_frames_dir(self):
        try:
            os.mkdir(self.dirname)
        except FileExistsError:
            pass

    def __generate_video_frames(self):
        cols, rows = os.get_terminal_size()
        self.__create_video_frames_dir()

        subprocess.run(
            [
                "ffmpeg",
                "-i", self.path,
                "-f", "image2pipe",
                "-vcodec", "bmp",
                "-",
                "|",
                "ffmpeg",
                "-y",
                "-f", "image2pipe",
                "-vcodec", "bmp",
                "-i", "-",
                "-vf", f"scale={cols}:{rows}",
                os.path.join(self.dirname, "frame%04d.bmp")
            ],
            shell=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT
        )

    def __delete_video_frame(self, frame):
        frame_path = os.path.join(self.dirname, frame)
        os.remove(frame_path)

    def __delete_frames_dir(self):
        os.rmdir(self.dirname)

    def __clear_terminal(self):
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')

    def __print(self, frame):
        frame_path = os.path.join(self.dirname, frame)
        with open(frame_path, 'rb') as f:
            # BMP file header
            f.seek(10)
            video_start = int.from_bytes(f.read(4), 'little')

            # DIB header section
            f.seek(18)
            width = int.from_bytes(f.read(4), 'little')
            height = int.from_bytes(f.read(4), 'little')
            f.seek(28)
            bits_per_pixel = int.from_bytes(f.read(2), 'little')

            # Calculate row size and padding
            row_size = ((bits_per_pixel * width + 31) // 32) * 4

            output = ""
            for y in range(height - 1, -1, -1):
                # Move file pointer to the start of the current row
                f.seek(video_start + y * row_size)

                for _ in range(width):
                    # Little endian means that RGB is now BGR
                    blue = int.from_bytes(f.read(1), 'little')
                    green = int.from_bytes(f.read(1), 'little')
                    red = int.from_bytes(f.read(1), 'little')

                    # Double Buffering: Saves all the data to a variable,
                    # which is then printed to the screen in one action
                    output += f"\u001B[38;2;{red};{green};{blue}m"
                    output += self.print_char
                    output += "\u001B[0m"

                output += "\n"

            print(output)

        # Moves cursor back to top of display buffer, to allow for overwriting of written data
        # instead of clearing the entire terminal
        print("\033[H", end="")

    def __print_frames(self):
        retries = 0

        while True:
            frames = os.listdir(self.dirname)

            # If no new frames are being generated, end the program
            if len(frames) == 0:
                time.sleep(1)

                retries += 1
                if retries == 3:
                    self.__delete_frames_dir()
                    exit()

                continue

            # Prints all available frames before fetching more
            while len(frames) != 0:
                self.__print(frames[0])
                self.__delete_video_frame(frames[0])
                frames.pop(0)

    def parse(self):
        frame_generation = threading.Thread(target=self.__generate_video_frames)
        frame_display = threading.Thread(target=self.__print_frames)

        frame_generation.start()
        time.sleep(1) # Giving it some time to generate a few images (I'm so kind)
        frame_display.start()

        self.__clear_terminal()