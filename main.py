'''
@Author Aritra Ghosh
Version 2.0
Abstract: A Virtual Mouse based on hand gestures using OpenCV Mediapipe
'''


import cv2
import mediapipe as mp
import pyautogui
import math
import time


def meansquaredistance(x1,y1,x2,y2):
    dist=math.sqrt((x1-x2)**2+(y1-y2)**2)
    return dist

def isTouching(x1,y1,x2,y2,threshold):
    dist=meansquaredistance(x1,y1,x2,y2)
    if dist<threshold:
        return True
    else:
        return False

cap=cv2.VideoCapture(0) #Captures video from the first source from the available list of devices
hand_detector=mp.solutions.hands.Hands() #Hand Detector module from Mediapipe
drawing_utils=mp.solutions.drawing_utils

screen_width,screen_height=pyautogui.size()

index_x=0
index_y=0
index_base_x=0
index_base_y=0
index_second=0
middle_y=0
thumb_x=0
thumb_y=0

while True:
    _,frame=cap.read()  
    frame=cv2.flip(frame,1)  #Flip Feed
    frame_height,frame_width,_=frame.shape
    '''
    Ignoring the first result of the read function, cap.read() returns ret,frame
    ret is a boolean variable that returns if the frame is available, we dont need it right now
    ''' 
    rgb_frame=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)

    '''
    Shooting is done in BGR color channels for quality. But for image detection, RGB mode is preferred.
    So, we change the color channels from BGR to RGB
    '''

    output=hand_detector.process(rgb_frame) 
    '''Processes the image feed with hand_detector module'''
    hands=output.multi_hand_landmarks  
    '''Stores the position of the hands processed'''
   #print(hands)


    if hands:
        for hand in hands:
            drawing_utils.draw_landmarks(frame,hand)
            '''Draw the hand landmarks on the frame'''
            landmarks=hand.landmark
            for id,landmark in enumerate(landmarks):
                x=int(landmark.x*frame_width)    
                y=int(landmark.y*frame_height)
                #print(x,y)
                if id==8:  
                    '''Index of Index Finger Tip'''
                    cv2.circle(img=frame,center=(x,y),radius=10,color=(0,255,255))
                    index_x=screen_width/frame_width*x
                    index_y=screen_height/frame_height*y
                    pyautogui.moveTo(index_x,index_y) #Moves cursor
                
                '''Converting the coordinates of index finger tip to frame coordinates and drawing a yellow circle on it'''
                if id==4:  
                    '''Index of Thumb Tip'''
                    cv2.circle(img=frame,center=(x,y),radius=10,color=(255,0,255))
                    thumb_x=screen_width/frame_width*x
                    thumb_y=screen_height/frame_height*y
                   # print("Current mean squared distance:",meansquaredistance(thumb_x,thumb_y,index_x,index_y))
                    
                        
                
                if id==5:
                    cv2.circle(img=frame,center=(x,y),radius=10,color=(255,0,0))
                    index_base_x=screen_width/frame_width*x
                    index_base_y=screen_height/frame_height*y
                    
                    if isTouching(thumb_x,thumb_y,index_base_x,index_base_y,55):
                        print('Click')
                        #print(meansquaredistance(thumb_x,thumb_y,index_base_x,index_base_y))
                        pyautogui.click()
                        time.sleep(0.7)
                        
                        

                if id==6:
                    cv2.circle(img=frame,center=(x,y),radius=10,color=(0,255,0))
                    index_second=screen_width/frame_width*x
                    middle_y=screen_height/frame_height*y
                    middle_y=screen_height/frame_height*y
                    if isTouching(thumb_x,thumb_y,index_second,middle_y,65):
                        print('Right Click')
                #        print(meansquaredistance(thumb_x,thumb_y,index_second,middle_y))
                        pyautogui.rightClick()
                        time.sleep(0.7)
                        
                

                    
            

            




    cv2.imshow('Virtual Mouse',frame) 
    '''
    Running in an infinite loop gives the feel of showing a video.
    CV2.imshow actually shows an image only, which is the current frame captured in the loop iteration.
    '''
    cv2.waitKey(1)
