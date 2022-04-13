import cv2

openCvVidCapIds = []

for i in range(100):
    try:
        cap = cv2.VideoCapture(i)
        if cap is not None and cap.isOpened():
            openCvVidCapIds.append(i)
        # end if
    except:
        pass
    # end try
# end for

print(str(openCvVidCapIds))