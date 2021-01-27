import cv2
import sys
import time
import queue
from tkinter import *


def start():
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

    if not cap.isOpened():
        print("Camera open failed!")
        sys.exit()

    start_time = time.time()

    w = round(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = round(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    nseconds = 9
    d = queue.Queue(fps * nseconds)

    fourcc = cv2.VideoWriter_fourcc(*'DIVX')

    delay = round(1000/fps)

    out = cv2.VideoWriter('output.avi', fourcc, 20., (w, h))

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

        if cv2.waitKey(delay) == 27: # esc를 누르면 강제 종료
            break

        if time.time() - start_time >= 600:

            if cnt % 2 == 0:
                out.release()
                out = cv2.VideoWriter('output2.avi', fourcc, 20., (w, h))
                cnt += 1

            elif cnt % 2 == 1:
                out.release()
                out = cv2.VideoWriter('output.avi', fourcc, 20., (w, h))
                cnt += 1

            start_time = time.time()

    cap.release()
    out.release()
    cv2.destroyAllWindows()

root = Tk() # 객체 생성
root.title("PubQue")
root.geometry("206x150")

btn1 = Button(root, width=40, height=10, text="시작", command=start)
btn1.pack()

root.mainloop()



