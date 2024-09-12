import os
import subprocess
import io

import cv2

class VideoHandler:
    def __init__(
        self,
        path: str = "",
        camera: bool = False,
        print_char: str = "█"
    ) -> None:
        self.path = path
        self.print_char = print_char
        self.camera = camera

    def display(self):
        parser = self.__get_parser()

        parser.parse()

    def __get_parser(self):
        if self.camera:
            return LiveVideoParser(self.print_char)

        if self.path.strip() == "":
            raise ValueError("Either set the camera flag or provide a video file path.")

        return VideoFileParser(self.path, self.print_char)

class VideoParser:
    def _clear_terminal(self):
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')

    def _print(self, frame):
        f = io.BytesIO(frame)

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

        output = []
        for y in range(height - 1, -1, -1):
            # Move file pointer to the start of the current row
            f.seek(video_start + y * row_size)

            pixel = ""
            for _ in range(width):
                # Little endian means that RGB is now BGR
                blue = int.from_bytes(f.read(1), 'little')
                green = int.from_bytes(f.read(1), 'little')
                red = int.from_bytes(f.read(1), 'little')

                # Double Buffering: Saves all the data to a variable,
                # which is then printed to the screen in one action
                pixel += f"\u001B[38;2;{red};{green};{blue}m"
                pixel += self.print_char
                pixel += "\u001B[0m"

            output.append(pixel)

        # Moves cursor back to top of display buffer, to allow for overwriting of written data
        # instead of clearing the entire terminal
        print('\n'.join(output), end="\033[H", flush=True)

class VideoFileParser(VideoParser):
    def __init__(self, path: str, print_char: str) -> None:
        self.path = path
        self.print_char = print_char

    def __process_video_frames(self):
        cols, rows = os.get_terminal_size()

        command = [
            "ffmpeg",
            "-i", self.path,
            "-f", "image2pipe",
            "-vcodec", "bmp",
            "-vf", f"scale={cols}:{rows}",
            "-"
        ]

        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL
        )

        while True:
            header = process.stdout.read(14)
            if not header or len(header) < 14:
                break

            size = int.from_bytes(header[2:6], 'little')
            frame = header + process.stdout.read(size - 14)

            self._print(frame)

        self._clear_terminal()
        exit()

    def parse(self):
        self.__process_video_frames()

class LiveVideoParser(VideoParser):
    def __init__(self, print_char) -> None:
        self.print_char = print_char

    def parse(self):
        camera = cv2.VideoCapture(0)
        cols, rows = os.get_terminal_size()

        while True:
            result, frame = camera.read()

            frame = cv2.resize(frame, (cols, rows))
            frame = cv2.flip(frame, 1)

            if frame.shape[2] == 3:
                bgr = frame
            else:
                bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

            # Encode the frame as BMP
            _, buffer = cv2.imencode('.bmp', bgr)

            self._print(buffer)