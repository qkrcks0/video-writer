import cv2
import sys
import time
import queue

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

nseconds = 6
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
    
    now = time.localtime()
    current_time = "%04d/%02d/%02d %02d:%02d:%02d"%(now.tm_year, \
                    now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
    cv2.putText(frame, current_time, (0, h-1), cv2.FONT_HERSHEY_SIMPLEX, \
                1.5, (255,255,255), 2, cv2.LINE_AA)

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



