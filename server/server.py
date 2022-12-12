import cv2 as cv
from math import ceil
import numpy as np
from socket import *

MAX_BUFFER = 2**16
serverAddress = ('140.118.145.249', 5000)
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(serverAddress)

# Read from camera
video = cv.VideoCapture(0)

while True:
    message, clientAddress = serverSocket.recvfrom(MAX_BUFFER)
    # Read until video is completed
    while video.isOpened():
        ret, frame = video.read()  # Capture frame-by-frame
        if ret:
            cv.imshow('SERVER', frame)  # Display the resulting frame
            encoded_frame = cv.imencode('.jpg', frame, [int(cv.IMWRITE_JPEG_QUALITY), 80])[1]  # np array

            data = encoded_frame.tobytes()
            data_size = len(data)

            chunk = ceil(data_size / MAX_BUFFER)
            start = 0
            while chunk:
                end = min(data_size, MAX_BUFFER)
                serverSocket.sendto(data[start:end], clientAddress)
                star = end
                chunk -= 1
            cv.waitKey(25)
        else:
            break

    print("Video has ended")
    video.release()
    cv.destroyAllWindows()
