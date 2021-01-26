import cv2
import sys
import time
from tkinter import *

def start():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Camera open failed!")
        sys.exit()

    start_time = time.time()

    w = round(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = round(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

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

        cv2.imshow('frame', frame)

        if cv2.waitKey(delay) == 27: # esc를 누르면 강제 종료
            break

        if time.time() - start_time >= 5:

            if cnt % 2 == 0:
                out.release()
                out = cv2.VideoWriter('output2.avi', fourcc, fps, (w, h))

            elif cnt % 2 == 1:
                out.release()
                out = cv2.VideoWriter('output.avi', fourcc, fps, (w, h))

            start_time = time.time()

        cnt += 1

    cap.release()
    out.release()
    cv2.destroyAllWindows()

root = Tk() # 객체 생성
root.title("PubQue")

btn1 = Button(root, width=10, height=3, text="시작", command=start)
btn1.pack()

root.mainloop()



