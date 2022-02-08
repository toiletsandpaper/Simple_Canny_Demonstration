import cv2
import numpy as np
from sqlalchemy import false

# rtsp_server = "rtsp://admin:!Samsung1@83.220.61.11/H.264/media.smp"
# rtsp_server = "rtsp://admin:d0m0gA_r0v@85.21.63.215:554/H.264/media.smp"
cap = cv2.VideoCapture(0)

DEFAULT_LINE = 640 + 1
CANNY_A, CANNY_B = 100, 150
L2_INDICATOR = False


def on_change(x):
    global DEFAULT_LINE
    DEFAULT_LINE = max(min(x * 10 + 1, 1200), 80)
    return True

def change_canny_a(x):
    global CANNY_A
    CANNY_A = x

def change_canny_b(x):
    global CANNY_B
    CANNY_B = x
    
def change_l2(x):
    global L2_INDICATOR
    L2_INDICATOR = True if x < 100 else False
    
def l2_swith_control(pos):
    if pos < 100 and not pos == 0:
        cv2.setTrackbarPos('L2', 'frame', 0)
    if pos >= 100 and not pos == 200:
        cv2.setTrackbarPos('L2', 'frame', 200) 


cv2.imshow('frame', np.zeros((1280, 720, 3), np.uint8))
cv2.createTrackbar('X', 'frame', 0, 1280 // 10, on_change)
cv2.createTrackbar('Canny A (t1)', 'frame', 0, 400, change_canny_a)
cv2.createTrackbar('Canny B (t2)', 'frame', 0, 400, change_canny_b)
cv2.createTrackbar('L2', 'frame', 0, 200, change_l2)

cv2.setTrackbarPos('X', 'frame', DEFAULT_LINE)
cv2.setTrackbarPos('Canny A (t1)', 'frame', CANNY_A)
cv2.setTrackbarPos('Canny B (t2)', 'frame', CANNY_B)
cv2.setTrackbarPos('L2', 'frame', 100*L2_INDICATOR)

while(cap.isOpened()):
    ret, frame = cap.read()
    output = cv2.resize(frame, (1280, 720))

    out1 = output[0:721, 0:DEFAULT_LINE]
    out2 = output[0:721, DEFAULT_LINE:1281]

    out2 = cv2.Canny(out2, CANNY_A, CANNY_B, L2gradient=L2_INDICATOR)
    out2 = cv2.cvtColor(out2, cv2.COLOR_GRAY2RGB)

    output_all = np.zeros((720, 1280, 3), np.uint8)
    output_all[:721, :DEFAULT_LINE, :3] = out1
    output_all[:721, DEFAULT_LINE:1281] = out2
    
    l2_swith_control(cv2.getTrackbarPos('L2','frame'))
    cv2.imshow('frame', output_all)
    
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()
