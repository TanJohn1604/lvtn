import cv2
import serial
# from threading import Thread
# from time import  sleep
import time
import numpy as np
from tracker import *

# ----------------serial--------------
# spilitdata[0] kieu str
spilitdata = [0, 0, 0]
flag = 1
cnt = 0
# dictionary luu thong tin vat tren bang tai, moi vat can servo nao gat
data = {}
red = 0
yellow = 0
blue = 0
data_serial = []
rsen = [0, 0, 0]
bsen = [0, 0, 0]
ysen = [0, 0, 0]
indexsen = 0
state_red = 0
state_yellow = 0
state_blue = 0
pre_state_red = 0
pre_state_yellow = 0
pre_state_blue = 0

blue_edge = 0
dtav = 0
startTime = time.time()

def initConnection(port,baud):
    try:
        ser=serial.Serial(port,baud)
        print("Device connected")
        return ser
    except:
        print("Errorrrrrrr")


def sendData(se,data,digits):
    global flag
    myString="$"
    for d in data:
        myString+= str(d).zfill(digits)
    try:
        se.write(myString.encode())
        flag=1
        print(myString)
    except:
        print("send fail")

# ---------------------------------------------serial------------------------------------------


# width = 640
# height = 480
print(cv2.__version__)
cam = cv2.VideoCapture(0)
# Or, if you have a WEB cam, uncomment the next line
# (If it does not work, try setting to '1' instead of '0')
# cam=cv2.VideoCapture(0)
# Create tracker object
tracker = EuclideanDistTracker()
# ---------------------------------------------serial------------------------------------------
ser=initConnection("COM4",9600)
# ---------------------------------------------serial------------------------------------------
while True:
    # ---------------------------------------------serial------------------------------------------
    if flag == 0:
        sendData(ser, [spilitdata[0], spilitdata[1], spilitdata[2]], 3)
    if flag == 1:
        while ser.inWaiting() != 0:
            data_serial = ser.readline()
            data_serial = str(data_serial, 'utf-8')
            data_serial = data_serial.strip('\r\n')
            spilitdata = data_serial.split(",")
            flag = 0
    # ---------------------------------------------serial------------------------------------------
    # ---------------------------------------------khoi camera-------------------------------------------------
    ret, frame = cam.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    detection = []
    # -----------------------------------------------------red----------------------------------------------

    rl_b = np.array([0, 81, 193])
    ru_b = np.array([7, 255, 255])

    rl_b2 = np.array([173, 81, 193])
    ru_b2 = np.array([180, 255, 255])

    RFGmask = cv2.inRange(hsv, rl_b, ru_b)
    RFGmask2 = cv2.inRange(hsv, rl_b2, ru_b2)
    RFGmaskComp = cv2.add(RFGmask, RFGmask2)

    # -----------------------------------------------------yellow----------------------------------------------

    yl_b = np.array([0, 82, 183])
    yu_b = np.array([154, 255, 255])

    yl_b2 = np.array([0, 82, 183])
    yu_b2 = np.array([154, 255, 255])

    YFGmask = cv2.inRange(hsv, yl_b, yu_b)
    YFGmask2 = cv2.inRange(hsv, yl_b2, yu_b2)
    YFGmaskComp = cv2.add(YFGmask, YFGmask2)

    # -----------------------------------------------------blue----------------------------------------------

    bl_b = np.array([79, 47, 190])
    bu_b = np.array([113, 146, 255])

    bl_b2 = np.array([79, 47, 190])
    bu_b2 = np.array([113, 146, 255])

    BFGmask = cv2.inRange(hsv, bl_b, bu_b)
    BFGmask2 = cv2.inRange(hsv, bl_b2, bu_b2)
    BFGmaskComp = cv2.add(BFGmask, BFGmask2)
    # cv2.imshow('RFGmaskComp', RFGmaskComp)
    # cv2.moveWindow('RFGmaskComp', 640, 0)

    # FG = cv2.bitwise_and(frame, frame, mask=FGmaskComp)
    # # cv2.imshow('FG', FG)
    # # cv2.moveWindow('FG', 700, 0)
    # #
    # bgMask = cv2.bitwise_not(FGmaskComp)
    # # cv2.imshow('bgMask', bgMask)
    # # cv2.moveWindow('bgMask', 700, 530)
    # #
    # BG = cv2.cvtColor(bgMask, cv2.COLOR_GRAY2BGR)
    # final = cv2.add(FG, BG)

    # -----------------------------------------------------red----------------------------------------------
    Rcontours, _ = cv2.findContours(RFGmaskComp, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    Rcontours = sorted(Rcontours, key=lambda x: cv2.contourArea(x), reverse=True)
    # -----------------------------------------------------yellow--------------------------------------------
    Ycontours, _ = cv2.findContours(YFGmaskComp, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    Ycontours = sorted(Ycontours, key=lambda x: cv2.contourArea(x), reverse=True)
    # -----------------------------------------------------blue----------------------------------------------
    Bcontours, _ = cv2.findContours(BFGmaskComp, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    Bcontours = sorted(Bcontours, key=lambda x: cv2.contourArea(x), reverse=True)

    # -----------------------------------------------------red----------------------------------------------
    if Rcontours:

        rarea = cv2.contourArea(Rcontours[0])
        (rx, ry, rw, rh) = cv2.boundingRect(Rcontours[0])
        if rarea >= 2500:
            # cv2.drawContours(frame,[cnt],0,(255,0,0),3)

            cv2.rectangle(frame, (rx, ry), (rx + rw, ry + rh), (0, 0, 255), 3)
            cv2.circle(frame, (int(rx + rw / 2), int(ry + rh / 2)), 3, (0, 255, 0), 2, 1)
            cv2.circle(frame, (int(rx + rw / 2), int(ry + rh / 2)), 1, (0, 255, 0), 2, 1)
            cv2.circle(frame, (int(rx + rw / 2), int(ry + rh / 2)), 20, (0, 255, 0), 2, 1)
            cv2.putText(frame, "red :" + str(rarea), (int(rx + rw / 2), int(ry + rh / 2)),
                        cv2.FONT_HERSHEY_PLAIN, 1,
                        (0, 0, 255), 1)
            detection.append([rx, ry, rw, rh, 0])

    # -----------------------------------------------------yellow--------------------------------------------
    # if Ycontours:
    #
    #     yarea = cv2.contourArea(Ycontours[0])
    #     (yx, yy, yw, yh) = cv2.boundingRect(Ycontours[0])
    #     if yarea >= 3000:
    #         # cv2.drawContours(frame,[cnt],0,(255,0,0),3)
    #
    #         cv2.rectangle(frame, (yx, yy), (yx + yw, yy + yh), (0, 255, 255), 3)
    #         cv2.circle(frame, (int(yx + yw / 2), int(yy + yh / 2)), 3, (0, 255, 0), 2, 1)
    #         cv2.circle(frame, (int(yx + yw / 2), int(yy + yh / 2)), 1, (0, 255, 0), 2, 1)
    #         cv2.circle(frame, (int(yx + yw / 2), int(yy + yh / 2)), 20, (0, 255, 0), 2, 1)
    #         cv2.putText(frame, "yellow :" + str(yarea), (int(yx + yw / 2), int(yy + yh / 2)),
    #                     cv2.FONT_HERSHEY_PLAIN, 1,
    #                     (0, 0, 255), 1)
    #
    #         detection.append([yx, yy, yw, yh, 1])
    # -----------------------------------------------------blue----------------------------------------------
    if Bcontours:
        barea = cv2.contourArea(Bcontours[0])
        (bx, by, bw, bh) = cv2.boundingRect(Bcontours[0])
        if barea >= 3000:
            # cv2.drawContours(frame,[cnt],0,(255,0,0),3)

            cv2.rectangle(frame, (bx, by), (bx + bw, by + bh), (255, 0, 0), 3)
            cv2.circle(frame, (int(bx + bw / 2), int(by + bh / 2)), 3, (0, 255, 0), 2, 1)
            cv2.circle(frame, (int(bx + bw / 2), int(by + bh / 2)), 1, (0, 255, 0), 2, 1)
            cv2.putText(frame, "blue :" + str(barea), (int(bx + bw / 2), int(by + bh / 2)),
                        cv2.FONT_HERSHEY_PLAIN, 1,
                        (0, 0, 255), 1)
            detection.append([bx, by, bw, bh, 2])
    boxes_ids = tracker.update(detection)
    for box_id in boxes_ids:
        x, y, w, h, id, colorid = box_id
        cv2.putText(frame, str(id) + " " + str(colorid), (x, y - 15), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
        if colorid == 0:
            if id not in data:
                red = red + 1
                yellow = yellow + 1
                blue = blue + 1
                data[id] = [red, yellow, blue]
        if colorid == 1:
            if id not in data:
                yellow = yellow + 1
                blue = blue + 1
                data[id] = [red, yellow, blue]
        if colorid == 2:
            if id not in data:
                blue = blue + 1
                data[id] = [red, yellow, blue]
    # -------------------------------------xac dinh trang thai cam bien --------------------------------------------
    indexsen = indexsen + 1
    indexsen = indexsen % 3

    rsen[indexsen] = int(spilitdata[0])
    ysen[indexsen] = int(spilitdata[1])
    bsen[indexsen] = int(spilitdata[2])

    if 1 not in rsen:
        state_red = 0
    if 0 not in rsen:
        state_red = 1

    if 1 not in ysen:
        state_yellow = 0
    if 0 not in ysen:
        state_yellow = 1

    if 1 not in bsen:
        state_blue = 0
    if 0 not in bsen:
        state_blue = 1


    # -------------------------------------kiem tra nhieu cam bien --------------------------------------------
    # if int(spilitdata[1]) == 1 and blue > 0:
    #     blue = blue - 1
    #     for key, da in data.items():
    #         da[2] = da[2] - 1
    #         if da[2] < 0:
    #             da[2] = 0
    # print(data)

    if pre_state_blue == 0 and state_blue == 1:
        print(" rising edge ")
        blue_edge = 1
    if pre_state_blue == 1 and state_blue == 0:
        print(" falling edge ")
        blue_edge = 0
    if blue_edge == 1 and state_blue == 1:
        spilitdata[0] = str(1)
    if blue_edge == 0 and state_blue == 0:
        spilitdata[0] = str(0)
    # -------------------------------------cap nhat trang thai cam bien --------------------------------------------
    pre_state_red = state_red
    pre_state_yellow = state_yellow
    pre_state_blue = state_blue
    # ----------------------------------------------fps--------------------------------------------------------

    dt = time.time() - startTime
    startTime = time.time()
    dtav = 0.9 * dtav + 0.1 * dt
    fps = 1 / dtav
    cv2.putText(frame, str(round(fps, 1)) + ' fps', (0, 30), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 1)
    cv2.imshow('nanoCam', frame)
    cv2.moveWindow('nanoCam', 0, 0)
    if cv2.waitKey(1) == ord('q'):
        break
cam.release()
cv2.destroyAllWindows()
