#------------------
# Written and Modified by R.Ma, L.He and S.Tu
# Version: v0.9_Demo_5.15
#------------------
import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera
import numpy as np
import time
#from test import avoid
import picar_4wd as fc

color_dict = {'red':[0,4],'orange':[5,18],'yellow':[22,37],'green':[42,100],'blue':[92,110],'purple':[115,165],'red_2':[150,180]}  #Here is the range of H in the HSV color space represented by the color

kernel_5 = np.ones((5,5),np.uint8) #Define a 5×5 convolution kernel with element values of all 1.

def back(width):
    time.sleep(2)
    fc.turn_right(1)
    time.sleep(2.5) # This should be changed accordingly with the actual ground material that the robot interacts with.
    fc.stop()
    time.sleep(1)
    fc.backward(1)
    
    

def color_detect(img,color_name):

    # The blue range will be different under different lighting conditions and can be adjusted flexibly.  H: chroma, S: saturation v: lightness
    resize_img = cv2.resize(img, (160,120), interpolation=cv2.INTER_LINEAR)  # In order to reduce the amount of calculation, the size of the picture is reduced to (160,120)
    hsv = cv2.cvtColor(resize_img, cv2.COLOR_BGR2HSV)              # Convert from BGR to HSV
    color_type = color_name

    mask = cv2.inRange(hsv,np.array([min(color_dict[color_type]), 60, 60]), np.array([max(color_dict[color_type]), 255, 255]) )           # inRange()：Make the ones between lower/upper white, and the rest black
    if color_type == 'red':
            mask_2 = cv2.inRange(hsv, (color_dict['red_2'][0],0,0), (color_dict['red_2'][1],255,255))
            mask = cv2.bitwise_or(mask, mask_2)

    morphologyEx_img = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel_5,iterations=1) # Perform an open operation on the image

    # Find the contour in morphologyEx_img, and the contours are arranged according to the area from small to large.
    _tuple = cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    # compatible with opencv3.x and openc4.x
    if len(_tuple) == 3:
        _, contours, hierarchy = _tuple
    else:
        contours, hierarchy = _tuple

    color_area_num = len(contours) # Count the number of contours

    if color_area_num > 0:
        detected = True
        distance_list = []
        x_list = []
        y_list = []
        w_list = []
        h_list = []
        for i in contours:    # Traverse all contours
            x,y,w,h = cv2.boundingRect(i)
            x_list.append(x)
            y_list.append(y)
            w_list.append(w)
            h_list.append(h)
            # calculate distance
            height = h
            object_size = 1.5
            focal_length = 3.04  # Focal length of camera lens in mm
            distance = 1/21 * object_size * 1000 * focal_length / (height * 1.12)
            distance_list.append(distance)
            # distance is in the format of cm
        # return the minimum distance and its corrsponding x,y,w,h
        distance = min(distance_list)
        index = distance_list.index(distance)
        x = x_list[index]
        y = y_list[index]
        w = w_list[index]
        h = h_list[index]

            # Draw a rectangle on the image (picture, upper left corner coordinate, lower right corner coordinate, color, line width)
        if w >= 8 and h >= 8: # Because the picture is reduced to a quarter of the original size, if you want to draw a rectangle on the original picture to circle the target, you have to multiply x, y, w, h by 4.
            x = x * 4
            y = y * 4
            w = w * 4
            h = h * 4
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)  # Draw a rectangular frame
        #cv2.putText(img,color_type,(x,y), cv2.FONT_HERSHEY_SIMPLEX, 1,(0,0,255),2)# Add character description
        cv2.putText(img,str(round(distance,2)) + 'cm',(x,y), cv2.FONT_HERSHEY_SIMPLEX, 1,(0,0,255),2)
    else:
        distance = 0
        height = 100
        w = 100
        detected = False
    return img,mask,morphologyEx_img,distance,detected,height,w

with PiCamera() as camera:
    object_color = "orange"
    object_color = input("Please enter the color of the object you want to track: (Orange set by default) ")
    task_type = "4"
    task_type = input("Please enter the task number: (4 by default, do not change)")
    threshold = "10"
    threshold = input("Please enter the threshold: (10 by default, do not change) ")
    threshold = float(threshold)
    print("start distance detection and calculation based on the color of the object: " + object_color)
    camera.resolution = (640,480)
    camera.framerate = 60
    rawCapture = PiRGBArray(camera, size=camera.resolution)
    #time.sleep(2)
    flag = 0

    for frame in camera.capture_continuous(rawCapture, format="bgr",use_video_port=True):# use_video_port=True
        img = frame.array
        img,img_2,img_3,distance,detected, height, width=  color_detect(img,object_color)  # Color detection function

        cv2.imshow("video", img)    # OpenCV image show
        cv2.imshow("mask", img_2)    # OpenCV image show
        cv2.imshow("morphologyEx_img", img_3)    # OpenCV image show
        rawCapture.truncate(0)   # Release cache
        if task_type == '0':
            _ = 1
        if task_type == '1':
            if distance > threshold and detected:
                fc.forward(10)
            elif distance < threshold and detected:
                fc.stop()
                break
        if task_type == '2':
            if distance > threshold and detected:
                fc.forward(10)
            elif distance < threshold and detected:
                avoid()
                break

        if task_type == '3':
            if distance != 0:
                fc.forward(10)
                if distance < threshold:
                    fc.stop()
                    break
            else:
                fc.turn_right(3)
                time.sleep(0.5)
        if task_type == '4':
            ratio = width/height
            print(ratio,width)
            if flag == 0:
                if 12 <= ratio <100 and width>400:
                    print("detected!")
                    fc.stop()
                    flag = 1
                else:
                    fc.turn_left(1)
            elif flag == 1:
                back(width)
                flag =2
            else:
                if width > 300:
                    fc.stop()
                    break
            
        k = cv2.waitKey(1) & 0xFF
        # 27 is the ESC key, which means that if you press the ESC key to exit
        if k == 27:
            break
    

    print('quit ...')
    
    cv2.destroyAllWindows()
    camera.close()


