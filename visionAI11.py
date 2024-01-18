import cv2

cap= cv2.VideoCapture(0)

print("=" * 50)
print("Look at the webcam and strike a pretty pose. And press any key")

if cap.isOpened():
    while True:
        ret,frame = cap.read()
        
        if ret:
            cv2.imshow('camera', frame)

            if cv2.waitKey(1) != -1:
                cv2.imwrite('./files/webcam1.jpg', frame)
                break
            
        else:
            print('no frame')
            break
else:
    print('no camera!')

cap.release()
cv2.destroyAllWindows()

print("\n\n--> Check the captured files : ./files/webcam1.jpg")

