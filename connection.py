import os
import socket
import cv2
import pickle
import struct
from argparse import Namespace

from handlers import video

def get_ip_address():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        sock.connect(("8.8.8.8", 80)) # Try to connect to Google's public DNS
        ip = sock.getsockname()[0] # Get IP that would have made that connection from your laptop
    except:
        ip = '127.0.0.1'
    finally:
        sock.close()

    return ip

def get_port():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    port = 1024

    while True:
        try:
            sock.bind(('0.0.0.0', port))
            return port
        except socket.error as e:
            port += 1
            continue
        except Exception as err:
            raise err
        finally:
            sock.close()

# This is some shitty code lol
def setup_connection(port: int, args: Namespace):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        if not args.target_ip and not args.target_port:
            # Listening mode | Server
            print(f"Listening on port {port}...")
            sock.bind(('0.0.0.0', port))
            sock.listen(5)

            print("Awaiting incoming connection...")
            conn, _ = sock.accept()
            print("Accepted connection")

            sock.close()
            return conn
        else:
            # Connecting mode | Client
            print(f"Connecting to {args.target_ip}:{args.target_port}...")
            sock.connect((args.target_ip, args.target_port))

            print("Connected")

            return sock
    except socket.error as err:
        sock.close()

        raise err

def send_video_data(sock: socket.socket):
    camera = cv2.VideoCapture(0)
    print("Camera started...")

    while True:
        # Capture frame from camera
        ret, frame = camera.read()
        if not ret:
            print("Failed to capture frame")
            camera.release()
            exit()

        # Send the captured frame
        data = pickle.dumps(frame)
        message_size = struct.pack("L", len(data))

        sock.sendall(message_size + data)

def receive_video_data(sock: socket.socket, video_handler: video.LiveVideoParser):
    cols, rows = os.get_terminal_size()

    while True:
        # Receive the size of the incoming data
        data_size = struct.unpack("L", sock.recv(struct.calcsize("L")))[0]

        # Receive the data
        received_data = b""
        while len(received_data) < data_size:
            received_data += sock.recv(4096)

        # Deserialize the data back into an image
        frame = pickle.loads(received_data)
        video_handler.stream(frame, cols, rows)