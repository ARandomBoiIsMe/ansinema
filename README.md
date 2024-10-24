# Render images and videos in your terminal

I was curious about how image/video viewers worked, and if I could make one in my terminal. So, I decided to kill two
birds with one poorly-named stone.

# Dependencies

- [FFmpeg](https://ffmpeg.org/)

# Supported file types

- Video: Most likely all. FFmpeg is quite robust.
- Image: `.bmp` (more image formats coming soon...)

# Usage

Install all needed dependencies

```
pip install -r requirements.txt
```

```
usage: python main.py [-h] [-i INPUT] [-c] [-p PRINT_CHARACTER] [--color] [-v] [--target_ip TARGET_IP]
                      [--target_port TARGET_PORT]

Renders images and videos to the terminal. Supports video calls too, yay.

options:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        Input media path
  -c, --camera          Display view from webcam
  -p PRINT_CHARACTER, --print_character PRINT_CHARACTER
                        Character to be used as pixel on terminal
  --color               Sets the output to be colored
  -v, --vcall           Initiate a video call. Only provide this argument to act as the listening device.
  --target_ip TARGET_IP
                        IP address of destination computer. Provide this along with --target_port to act as the
                        connecting device.
  --target_port TARGET_PORT
                        Port number of destination computer. Provide this along with --target_ip to act as the
                        connecting device.
```

# Related blog post(s)

- [Printing images out to the terminal](https://arandomboiisme.github.io/blog/printing-images-out-to-the-terminal/)
- [Playing videos in the terminal](https://arandomboiisme.github.io/blog/playing-videos-in-the-terminal/)
- Video calls in the terminal (Coming soon...)

# Planned Updates

- Playing sound alongside videos
- Matching video playback to the file's framerate
- Support for more image formats

**Have fun!**