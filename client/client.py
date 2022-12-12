import cv2 as cv
import numpy as np
from socket import *

BUFFER = 2**16
serverAddress = ('140.118.145.249', 5000)
clientSocket = socket(AF_INET, SOCK_DGRAM)
message = "Hi, server"
clientSocket.sendto(bytes(message, encoding='utf8'), serverAddress)

MAX_BUFFER = 2**16

chunk, serverAddress = clientSocket.recvfrom(MAX_BUFFER)  # recv chunk bytes
while chunk:
    # print(type(chunk))

    # from buffer returns the 1d-array version of the buffer
    data = np.frombuffer(chunk, dtype=np.uint8)
    frame = cv.imdecode(data, cv.IMREAD_COLOR)
    cv.imshow("CLIENT", frame)

    if cv.waitKey(25) & 0xFF == 32:  # Space key to screenshot
        # cv.imwrite("Screenshot.jpg", frame)
        cv.imshow('SCREENSHOT', frame)

    if cv.waitKey(25) & 0xFF == ord('q'):  # 'q' key to quit
        break

    chunk, serverAddress = clientSocket.recvfrom(MAX_BUFFER)  # recv chunk bytes
    if not chunk:
        print("Live has ended")
        break

clientSocket.close()
cv.destroyAllWindows()
