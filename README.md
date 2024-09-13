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

Make sure to uncomment the appropriate code blocks in the `main.py` file before running the command
```
python main.py
```

# Related blog post(s)

- [Printing images out to the terminal](https://arandomboiisme.github.io/blog/printing-images-out-to-the-terminal/)
- [Playing videos in the terminal](https://arandomboiisme.github.io/blog/playing-videos-in-the-terminal/)

# Planned Updates

- Playing sound alongside videos
- Matching video playback to the file's framerate
- Support for more image formats

**Have fun!**