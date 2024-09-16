import os
import subprocess
import tempfile

class ImageHandler:
    def __init__(self, path: str, print_char: str = "█") -> None:
        self.path = path
        self.print_char = print_char

    def display(self) -> None:
        parser = self.__get_parser()

        width, height, pixels = parser.parse()

        for y in range(height):
            for x in range(width):
                # Offsets into current pixel's position to get its colors.
                red, green, blue = pixels[y * width + x]

                print(f"\u001B[38;2;{red};{green};{blue}m", end='')
                print(self.print_char, end='')
                print("\u001B[0m", end='')

            print()

    def __get_parser(self) -> "BMPParser" | None:
        with open(self.path, 'rb') as f:
            data = f.read()

        if data[:2].decode('ascii') == 'BM':
            return BMPParser(self.path, self.print_char)
        else:
            raise ValueError("Unsupported file type.")

class ImageParser:
    def __init__(self, path: str, print_char: str) -> None:
        self.path = path
        self.file_name = self.__get_image_file_name()
        self.print_char = print_char

    def __get_image_file_name(self) -> str:
        return os.path.basename(self.path)

    def _resize_image(self) -> str:
        cols, rows = os.get_terminal_size()
        temp = tempfile.mkdtemp()

        command = [
            'ffmpeg',
            '-i',
            self.path,
            '-vf',
            f'scale={cols}:{rows}',
            os.path.join(temp, f'temp-{self.file_name}')
        ]

        subprocess.run(
            command,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT
        )

        return os.path.join(temp, f'temp-{self.file_name}')

    def _delete_temp_image(self, temp) -> None:
        os.remove(temp)

class BMPParser(ImageParser):
    def parse(self) -> tuple[int, int, list]:
        temp = self._resize_image()

        pixels = []

        with open(temp, 'rb') as f:
            # BMP file header
            f.seek(10)
            image_start = int.from_bytes(f.read(4), 'little')

            # DIB header section
            f.seek(18)
            width = int.from_bytes(f.read(4), 'little')
            height = int.from_bytes(f.read(4), 'little')
            f.seek(28)
            bits_per_pixel = int.from_bytes(f.read(2), 'little')

            # Calculate row size and padding
            row_size = ((bits_per_pixel * width + 31) // 32) * 4

            for y in range(height - 1, -1, -1):
                # Move file pointer to the start of the current row
                f.seek(image_start + y * row_size)

                for _ in range(width):
                    # Little endian means that RGB is now BGR
                    blue = int.from_bytes(f.read(1), 'little')
                    green = int.from_bytes(f.read(1), 'little')
                    red = int.from_bytes(f.read(1), 'little')

                    pixels.append((red, green, blue))

        self._delete_temp_image(temp)

        return width, height, pixels