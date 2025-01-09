import cv2
import time
import numpy as np

#To save the output in a file output.aviq
fourcc = cv2.VideoWriter_fourcc(*'XVID')
output_file = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))

#Starting the webcam
cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
time.sleep(2)
bg = 0
#Capturing background for 60 frames
for i in range(60):
    ret, bg = cap.read()
#Flipping the background
bg = np.flip(bg, axis=1)

while cap.isOpened():
    ret, img = cap.read()

    if not ret:
        break
    
    # flipping the image for consistency
    img = np.flip(img, axis=1)

    # converting from BGR to HSV color space
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # creating mask to detect red color
    lower_red = np.array([0, 120, 50])
    upper_red = np.array([10, 255, 255])
    mask_1 = cv2.inRange(hsv, lower_red, upper_red)
    
    lower_red = np.array([170, 120, 70])
    upper_red = np.array([180, 255, 255])
    mask_2 = cv2.inRange(hsv, lower_red, upper_red)

    mask_1 = mask_1 + mask_2

    # refining the mask
    mask_1 = cv2.morphologyEx(mask_1, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    mask_1 = cv2.morphologyEx(mask_1, cv2.MORPH_DILATE, np.ones((3, 3), np.uint8))
    mask_2 = cv2.bitwise_not(mask_1)

    # creating the result images
    res_1 = cv2.bitwise_and(img, img, mask=mask_2)
    res_2 = cv2.bitwise_and(bg, bg, mask=mask_1)
    final_output = cv2.addWeighted(res_1, 1, res_2, 1, 0)
    
    # writing to output file
    output_file.write(final_output)

    # displaying the output to the user
    cv2.imshow("MAGIC", final_output)

    # check if the ESC key is pressed
    key = cv2.waitKey(1)
    if key == 27:  # ASCII for ESC key
        break

# releasing the webcam
cap.release()
cv2.destroyAllWindows()