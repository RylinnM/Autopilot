import socket
from picamera2 import Picamera2
import picar_4wd as fc
import cv2
import time

host_ip = 'xxxx'
port = 6666
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Connect to the PC
client_socket.connect((host_ip, port))

picam2 = Picamera2()
picam2.preview_configuration.main.size = (240*3,180*3)
picam2.preview_configuration.main.format = "RGB888"
picam2.preview_configuration.align()
picam2.configure("preview")
picam2.start()



while True:
	im= picam2.capture_array()
	img1 = cv2.resize(im, dsize=None, fx=1.0, fy=1.0)
	cv2.imshow("Image", img1)
	cv2.waitKey(1)
	data = client_socket.recv(1024)

	data = data.decode()
	if data == "0":
		print("stop")
		fc.stop()
	if data == "1":
		print("left")
		fc.turn_left(1)
	if data == "2":
		print("right")
		fc.turn_right(1)
	if data == "3":
		fc.forward(1)
		print("straight")