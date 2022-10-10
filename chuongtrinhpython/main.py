import cv2
# import serial
# from threading import Thread
# from time import  sleep
import numpy as np
from tracker import *
print(cv2.__version__)

width = 640
height = 480
flip = 2

flag = 0
rcnt = 0
bcnt = 0
ycnt = 0
# aa = 500
# cv2.namedWindow('Trackbars')
# cv2.moveWindow('Trackbars', 640*2, 0)
# cv2.createTrackbar('aa', 'Trackbars', 500, 5000, nothing)
# cv2.createTrackbar('hueLower', 'Trackbars', 50, 179, nothing)
# cv2.createTrackbar('hueUpper', 'Trackbars', 100, 179, nothing)
#
# cv2.createTrackbar('hue2Lower', 'Trackbars', 50, 179, nothing)
# cv2.createTrackbar('hue2Upper', 'Trackbars', 100, 179, nothing)
#
# cv2.createTrackbar('satLow', 'Trackbars', 100, 255, nothing)
# cv2.createTrackbar('satHigh', 'Trackbars', 255, 255, nothing)
# cv2.createTrackbar('valLow', 'Trackbars', 100, 255, nothing)
# cv2.createTrackbar('valHigh', 'Trackbars', 255, 255, nothing)
cam = cv2.VideoCapture(0)
# Or, if you have a WEB cam, uncomment the next line
# (If it does not work, try setting to '1' instead of '0')
# cam=cv2.VideoCapture(0)
# Create tracker object
tracker = EuclideanDistTracker()
while True:
    ret, frame = cam.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    detection = []
    # hueLow = cv2.getTrackbarPos('hueLower', 'Trackbars')
    # hueUp = cv2.getTrackbarPos('hueUpper', 'Trackbars')
    #
    # hue2Low = cv2.getTrackbarPos('hue2Lower', 'Trackbars')
    # hue2Up = cv2.getTrackbarPos('hue2Upper', 'Trackbars')
    #
    # Ls = cv2.getTrackbarPos('satLow', 'Trackbars')
    # Us = cv2.getTrackbarPos('satHigh', 'Trackbars')
    #
    # Lv = cv2.getTrackbarPos('valLow', 'Trackbars')
    # Uv = cv2.getTrackbarPos('valHigh', 'Trackbars')

    # l_b = np.array([hueLow, Ls, Lv])
    # u_b = np.array([hueUp, Us, Uv])
    #
    # l_b2 = np.array([hue2Low, Ls, Lv])
    # u_b2 = np.array([hue2Up, Us, Uv])
    #
    # FGmask = cv2.inRange(hsv, l_b, u_b)
    # FGmask2 = cv2.inRange(hsv, l_b2, u_b2)
    # FGmaskComp = cv2.add(FGmask, FGmask2)
    # -------------------------red------------------------------
    rl_b = np.array([0, 83, 84])
    ru_b = np.array([14, 197, 233])

    rl_b2 = np.array([127, 83, 84])
    ru_b2 = np.array([179, 197, 233])

    rl_b = np.array([0, 44, 232])
    ru_b = np.array([14, 255, 255])

    rl_b2 = np.array([141, 44, 232])
    ru_b2 = np.array([180, 255, 255])

    RFGmask = cv2.inRange(hsv, rl_b, ru_b)
    RFGmask2 = cv2.inRange(hsv, rl_b2, ru_b2)
    RFGmaskComp = cv2.add(RFGmask, RFGmask2)

    # -------------------------yellow------------------------------
    yl_b = np.array([19, 134, 64])
    yu_b = np.array([43, 255, 255])

    yl_b2 = np.array([19, 134, 64])
    yu_b2 = np.array([43, 255, 255])

    yl_b = np.array([0, 82, 183])
    yu_b = np.array([154, 255, 255])

    yl_b2 = np.array([0, 82, 183])
    yu_b2 = np.array([154, 255, 255])

    YFGmask = cv2.inRange(hsv, yl_b, yu_b)
    YFGmask2 = cv2.inRange(hsv, yl_b2, yu_b2)
    YFGmaskComp = cv2.add(YFGmask, YFGmask2)

    # -------------------------blue------------------------------
    bl_b = np.array([37, 69, 28])
    bu_b = np.array([113, 224, 249])

    bl_b2 = np.array([37, 69, 28])
    bu_b2 = np.array([113, 224, 249])

    bl_b = np.array([0, 108, 228])
    bu_b = np.array([0, 255, 255])

    bl_b2 = np.array([88, 108, 228])
    bu_b2 = np.array([144, 255, 255])

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

    # -------------------------red------------------------------
    Rcontours, _ = cv2.findContours(RFGmaskComp, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    Rcontours = sorted(Rcontours, key=lambda x: cv2.contourArea(x), reverse=True)
    # -------------------------yellow------------------------------
    Ycontours, _ = cv2.findContours(YFGmaskComp, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    Ycontours = sorted(Ycontours, key=lambda x: cv2.contourArea(x), reverse=True)
    # -------------------------blue------------------------------
    Bcontours, _ = cv2.findContours(BFGmaskComp, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    Bcontours = sorted(Bcontours, key=lambda x: cv2.contourArea(x), reverse=True)

    # -------------------------red-------------------------------
    if Rcontours:
        for r in Rcontours:
            rarea = cv2.contourArea(r)
            (rx, ry, rw, rh) = cv2.boundingRect(r)
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

    # -------------------------yellow----------------------------
    if Ycontours:
        for y in Ycontours:
            yarea = cv2.contourArea(y)
            (yx, yy, yw, yh) = cv2.boundingRect(y)
            if yarea >= 3000:
                # cv2.drawContours(frame,[cnt],0,(255,0,0),3)
                if flag == 0:
                    cv2.rectangle(frame, (yx, yy), (yx + yw, yy + yh), (0, 255, 255), 3)
                    cv2.circle(frame, (int(yx + yw / 2), int(yy + yh / 2)), 3, (0, 255, 0), 2, 1)
                    cv2.circle(frame, (int(yx + yw / 2), int(yy + yh / 2)), 1, (0, 255, 0), 2, 1)
                    cv2.circle(frame, (int(yx + yw / 2), int(yy + yh / 2)), 20, (0, 255, 0), 2, 1)
                    cv2.putText(frame, "yellow :" + str(yarea), (int(yx + yw / 2), int(yy + yh / 2)),
                                cv2.FONT_HERSHEY_PLAIN, 1,
                                (0, 0, 255), 1)

                detection.append([yx, yy, yw, yh, 1])
    # -------------------------blue------------------------------
    # if Bcontours:
    #     for b in Bcontours:
    #         barea = cv2.contourArea(b)
    #         (bx, by, bw, bh) = cv2.boundingRect(b)
    #         if barea >= 3000:
    #             # cv2.drawContours(frame,[cnt],0,(255,0,0),3)
    #             if flag == 0:
    #                 cv2.rectangle(frame, (bx, by), (bx + bw, by + bh), (255, 0, 0), 3)
    #                 cv2.circle(frame, (int(bx + bw / 2), int(by + bh / 2)), 3, (0, 255, 0), 2, 1)
    #                 cv2.circle(frame, (int(bx + bw / 2), int(by + bh / 2)), 1, (0, 255, 0), 2, 1)
    #                 cv2.putText(frame, "blue :" + str(barea), (int(bx + bw / 2), int(by + bh / 2)),
    #                             cv2.FONT_HERSHEY_PLAIN, 1,
    #                             (0, 0, 255), 1)
    # detection.append([bx, by, bw, bh])
    boxes_ids = tracker.update(detection)
    for box_id in boxes_ids:
        x, y, w, h, id, colorid = box_id
        cv2.putText(frame, str(id) + " " + str(colorid), (x, y - 15), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
    cv2.imshow('nanoCam', frame)
    cv2.moveWindow('nanoCam', 0, 0)
    if cv2.waitKey(1) == ord('q'):
        break

    # sendData(ser, [1, 255, 152], 3)
cam.release()
cv2.destroyAllWindows()
