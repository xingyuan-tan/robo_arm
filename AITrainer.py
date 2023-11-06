import cv2
import numpy as np
import time
import PoseModule as pm
import socket
from XOR_CheckSum import xor_checksum_string
# from commands import move_arm
# import commands


cap = cv2.VideoCapture(0)

# server_address = ('192.168.250.123', 5890)
# client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# client_socket.connect(server_address)
#
detector = pm.poseDetector()

# count = 0
# dir = 0
pTime = 0
# server_address = ('192.168.250.123', 5890)
# client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# client_socket.connect(server_address)
#
# start_pos = '-100.0,-520.0,550.0,90.0,5.0,0.0,'
# mode = 'PTP'
# r_m = float ()
#
# def move_arm(r_m, mode):
#     output_str_1 = mode + '("JPP",' + r_m + '20,200,0,false)'
#     structure = '1,' + output_str_1
#     datasize = len(structure)
#     checksumstring = 'TMSCT,' + str(datasize) + ',' + structure + ','
#     checksum = hex(xor_checksum_string(checksumstring))[2:]
#     if len(checksum) < 2:
#         checksum = '0' + checksum
#         # print("Checksum: " + checksum)
#         Calibrate = '$TMSCT,' + str(datasize) + ',1,' + output_str_1 + ',*' + checksum + '\r\n'
#         client_socket.send(Calibrate.encode())
#         print("Calibrating arm")
#     # Receive the response from the server listening
# response = client_socket.recv(1024).decode()
# print(response)

while True:
    success, img = cap.read()
    # img = cv2.resize(img, (1280, 720))
    # img = cv2.imread("AiTrainer/test.jpg")
    img = detector.findPose(img, False)
    lmList = detector.findPosition(img, False)

    # print(lmList)
    # angle_initial = 0
    # while (angle_initial == 0):
    if len(lmList) != 0:
        # Right Arm
        angle = detector.findAngle(img, 12, 14, 16)
        angle_round = round(angle)
        print(angle_round)

        # Joint_2 = 0
        # Joint_3 = 90
        # Joint_4 = 0
        # start_pos_1 = '-100.0,0.0,90.0,0.0,90.0,0.0,'
        # r_m = float ()
        # start_pos = ()
        # angle = 120.0
        # start_pos = [90.0, -90.0, (90.0 - angle), 0.0, -90.0, 0.0,]
        start_pos = [90.0, -90.0, 90.0, (angle_round + 0.0), -90.0, 0.0,]
        # start_pos = [90.0, -90.0, (angle_round +0.0), 0.0, -90.0, 0.0, ]
    #     str(start_pos)[1:36]
    #     print(str(start_pos)[:])
    #     X = str(start_pos)[1:36] + ','
    #     # str(start_pos)
    #
    #     # start_pos = -87.535, 90.793,  -95.652, -0.123, 92.637, -6.029
    #
    #     # start_pos = '-87.0, 90.0, -91.0, 0.0, 92.0,-6.0,'
    #     # start_pos_1 = '-120.0,0.0,90.0,0.0,90.0,0.0,'
    #     mode = "PTP"
    #     #
    #     output_str = mode + '("JPP",' + X + '200,200,200,false)'
    #     structure = '1,' + output_str
    #     datasize = len(structure)
    #
    #     checksumstring = 'TMSCT,' + str(datasize) + ',' + structure + ','
    #     checksum = hex(xor_checksum_string(checksumstring))[2:]
    #     if len(checksum) < 2:
    #         checksum = '0' + checksum
    #     # print("Checksum: " + checksum)
    #     Calibrate = '$TMSCT,' + str(datasize) + ',1,' + output_str + ',*' + checksum + '\r\n'
    #
    #     client_socket.send(Calibrate.encode())
    #     print("Calibrating arm")
    #     # Receive the response from the server
    # response = client_socket.recv(1024).decode()
    # print(response)
    # time.sleep(0.10)


    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (50, 100), cv2.FONT_HERSHEY_PLAIN, 5,
                    (255, 0, 0), 5)

    cv2.imshow("Image", img)
    cv2.waitKey(1)
