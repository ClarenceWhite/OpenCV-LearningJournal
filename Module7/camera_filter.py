import cv2  as cv
import sys
import numpy

PREVIEW = 0
BLUR = 1
FEATURES = 2
CANNY = 3

feature_params = dict(
    maxCorners = 500,
    qualityLevel = 0.2,
    minDistance = 15,
    blockSize = 9)

s = 0
if len(sys.argv) > 1:
    s = sys.argv[1]

image_filter = PREVIEW
alive = True

win_name = 'Camera Filters'
cv.namedWindow(win_name, cv.WINDOW_NORMAL)
result = None

source = cv.VideoCapture(s)

while alive:
    has_frame, frame = source.read()  #read the frame from video stream
    if not has_frame:
        break
    
    frame = cv.flip(frame, 1) #flip that frame horizontally

# show different objects according to commands
    if image_filter == PREVIEW:
        result = frame
    elif image_filter == CANNY:
        result = cv.Canny(frame, 145, 150)
    elif image_filter == BLUR:
        result = cv.blur(frame, (13,13))
    elif image_filter == FEATURES:
        result = frame
        frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        corners = cv.goodFeaturesToTrack(frame_gray, **feature_params)
        if corners is not None:
            for x,y in numpy.float32(corners).reshape(-1, 2):
                cv.circle(img=result, center=(int(x), int(y)), radius=10, color=(0,0,255), thickness=2)

    cv.imshow(win_name, result)

#read keys from the user
    key = cv.waitKey(1)
    if key == ord('q'):
        alive = False
    elif key == ord('c'):
        image_filter = CANNY
    elif key == ord('b'):
        image_filter = BLUR
    elif key == ord('f'):
        image_filter = FEATURES
    elif key == ord('p'):
        image_filter = PREVIEW
    

source.release()
cv.destroyWindow(win_name)