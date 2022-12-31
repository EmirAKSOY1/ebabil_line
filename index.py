import numpy as np
import cv2
  
webcam = cv2.VideoCapture("kesik.mp4")
while(1):
    _, imageFrame = webcam.read()
    imageFrame = cv2.resize(imageFrame, (640, 480))
    #imageFrame = cv2.flip(imageFrame, 0)
    
    hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV)
    #siyah
    # red_lower = np.array([10, 10, 10], np.uint8)
    # red_upper = np.array([180, 255, 30], np.uint8)
    #beyaz
    red_lower = np.array([0, 0, 200], np.uint8)
    red_upper = np.array([145,60,255], np.uint8)

    red_mask = cv2.inRange(hsvFrame, red_lower, red_upper)
  
    kernal = np.ones((5, 5), "uint8")

    imageFrame=cv2.line(imageFrame, (300,250),(320,250),(0,0,0),1)
    imageFrame=cv2.line(imageFrame, (310,240),(310,260),(0,0,0),1)

    red_mask = cv2.dilate(red_mask, kernal)
    res_red = cv2.bitwise_and(imageFrame, imageFrame, 
                              mask = red_mask)
   
    contours, hierarchy = cv2.findContours(red_mask,
                                           cv2.RETR_TREE,
                                           cv2.CHAIN_APPROX_SIMPLE)
      
    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if(area > 300):
            x, y, w, h = cv2.boundingRect(contour)
            imageFrame = cv2.rectangle(imageFrame, (x, y), 
                                       (x + w, y + h), 
                                       (0, 0, 255), 2)
            imageFrame=cv2.line(imageFrame,(x,y),(x+w,y+h),(0,255,0),1)
            imageFrame=cv2.line(imageFrame,(x+w,y),(x,h+y),(0,255,0),1)

            yariw=w/2
            yarix=int(x+yariw)
            yarih=h/2
            yariy=int(y+yarih)
            cv2.circle(imageFrame,(yarix,yariy),6,(255,255,255),-1)
            imageFrame=cv2.line(imageFrame, (310,250),(yarix,yariy),(255,255,255),1)

            imageFrame = cv2.putText(
            img = imageFrame,
            text = 'X:'+str(yarix-320),
            org = (0, 50),
            fontFace = cv2.FONT_HERSHEY_DUPLEX,
            fontScale = 1.0,
            color = (255, 0, 0),
            thickness = 1
            )

    cv2.imshow("itu-fanuc", imageFrame)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        cv2.release()
        cv2.destroyAllWindows()
        break