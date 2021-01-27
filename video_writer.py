import cv2
import sys
import time
import queue
from tkinter import *


def start():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Camera open failed!")
        sys.exit()

    camera_start_time = time.time()
    video_start_time = time.time()

    w = round(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = round(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    nseconds = 12
    d = queue.Queue(fps * nseconds)

    fourcc = cv2.VideoWriter_fourcc(*'DIVX')

    delay = round(1000/fps)

    out = cv2.VideoWriter('output.avi', fourcc, fps, (w, h))

    if not out.isOpened():
        print('File open failed!')
        cap.release()
        sys.exit()

    cnt = 0

    while True:                 
        ret, frame = cap.read()

        if not ret:   
            break

        out.write(frame)

        d.put(frame)

        if d.full():

            stream = d.get()
            cv2.namedWindow("stream",cv2.WINDOW_NORMAL)
            cv2.imshow("stream", stream)
            
        # cv2.namedWindow("frame", cv2.WINDOW_NORMAL)
        # cv2.imshow('frame', frame)

        if cv2.waitKey(delay) == 27: # esc를 누르면 강제 종료
            break

        if time.time() - video_start_time >= 20:

            if cnt % 2 == 0:
                out.release()
                out = cv2.VideoWriter('output2.avi', fourcc, fps, (w, h))
                cnt += 1

            elif cnt % 2 == 1:
                out.release()
                out = cv2.VideoWriter('output.avi', fourcc, fps, (w, h))
                cnt += 1

            video_start_time = time.time()

    cap.release()
    out.release()
    cv2.destroyAllWindows()

root = Tk() # 객체 생성
root.title("PubQue")
root.geometry("206x150")

btn1 = Button(root, width=40, height=10, text="시작", command=start)
btn1.pack()

root.mainloop()



