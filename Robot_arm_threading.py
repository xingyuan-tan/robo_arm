import cv2
import numpy as np
import time
import PoseModule as pm
import socket
from XOR_CheckSum import xor_checksum_string
import threading
# import socket
# from XOR_CheckSum import xor_checksum_string
# from commands import move_arm
# from commands import move_arm
# import commands

cap = cv2.VideoCapture(0)
detector = pm.poseDetector()
start = time.time()
server_address = ('192.168.250.123', 5890)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(server_address)


angle_round = -1
# Wait_Queue_Tag = ()
Queue_Tag = ()
# StopAndClearBuffer = True

def process(detector):

    pTime = 0

    global angle_round

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
            # print(angle_round)

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, str(int(fps)), (50, 100), cv2.FONT_HERSHEY_PLAIN, 5,
                    (255, 0, 0), 5)

        cv2.imshow("Image", img)
        cv2.waitKey(1)

# start_pos = [90.0, -90.0, 90.0, (angle_round + 0.0), -90.0, 0.0, ]
# # start_pos = [90.0, -90.0, (angle_round +0.0), 0.0, -90.0, 0.0, ]
# str(start_pos)[1:36]
# print(str(start_pos)[:])
# X = str(start_pos)[1:36] + ','
# mode = "PTP"
def move_arm(detector):
    # server_address = ('192.168.250.123', 5890)
    # client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # client_socket.connect(server_address)
    i = 0

    while True:
        if angle_round < 0:
            continue

        i+=1
        t0 = time.time()

        move_cmd_str = _create_move_cmd(angle_round)
        queue_tag_str = 'QueueTag(' + str(i%15 +1) + ')\r\n'

        data = '1,'+ move_cmd_str + queue_tag_str

        datasize = len(data)

        checksumstring = 'TMSCT,' + str(datasize) + ',' + data + ','
        checksum = hex(xor_checksum_string(checksumstring))[2:]
        if len(checksum) < 2:
            checksum = '0' + checksum
        # print("Checksum: " + checksum)
        Calibrate = '$TMSCT,' + str(datasize) + ','+ data + ',*' + checksum + '\r\n'

        client_socket.send(Calibrate.encode())
        print("Send Command", angle_round)
        # Receive the response from the server
        # response = client_socket.recv(1024).decode()
        # print(response)
        print('Time taken to create and send command:',time.time()-t0)

        time.sleep(0.15)
    # move_arm(X , mode)

def _create_move_cmd(angle_round):
    start_pos = [-90.0, -90.0, (0.0 + angle_round), 0.0, -90.0, 0.0, ]
    start_pos_str = str(start_pos)[1:-1]
    mode = "PTP"
    cmd_str = mode + '("JPP",' + start_pos_str + ',200,200,100,false) \r\n'

    return cmd_str

# def timediff(angle_round):
    # response = client_socket.recv(1024).decode()
    # while True:
    #     response = client_socket.recv(1024).decode()
        # time.time(response)
        # print('Time of response:',time.time(response))
    # r0 = time.time(response)
    # r1 = time.time()
    # print('Time difference between each queue:', r1 - r0)
    #     print(response)



process_thread = threading.Thread(target=process, args=(detector,))
move_arm_thread = threading.Thread(target=move_arm, args=(detector,))
# timediff_thread = threading.Thread(target=timediff, args=(detector,))

process_thread.start()
move_arm_thread.start()
# timediff_thread.start()

process_thread.join()
move_arm_thread.join()
# timediff_thread.join()

