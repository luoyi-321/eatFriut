import cv2
import mediapipe as mp
import os
import math
import random
import cvzone
from object import Object


gameOver = False

# object 
Eat_DIR = "eatFruitGame\object\eatable"
eatable = os.listdir(Eat_DIR)
Fruits = []
objPos = [300,0]
speed = 5
global isEatable
isEatable = True
for object in eatable:
    img = cv2.imread(f'{Eat_DIR}\{object}',cv2.IMREAD_UNCHANGED)
    img = cv2.resize(img,(72,128))
    Fruits.append(img)
    
noEat_DIR = "eatFruitGame\object\\noneatable"
noeatable = os.listdir(noEat_DIR)
noFruits = []
for object in noeatable:
    img = cv2.imread(f'{noEat_DIR}\{object}',cv2.IMREAD_UNCHANGED)
    img = cv2.resize(img,(72,128))
    noFruits.append(img)  

curentObject  = Fruits[0]
    # print(object)
def objectReset():
    objPos[0] = random.randint(10,540)
    objPos[1] = random.randint(-10,0)
    objNo = random.randint(0,1)
    if objNo == 0:
        curentObject = Fruits[random.randint(0,4)]
        isEatable = True
    else :
        curentObject = noFruits[random.randint(0,2)]
        isEatable = False
    print(objNo)
    return curentObject,isEatable
# camara
cap = cv2.VideoCapture(0)
# face Mesh 
mp_face = mp.solutions.face_mesh
idList = [0,16,76,292]
count = 0

mp_face_mesh = mp_face.FaceMesh()
def distance(pointOne:list,pointTwo:list):
    return math.dist(pointOne,pointTwo)

while True:
    ret,frame = cap.read(0)
    height,width,_ = frame.shape
    frame   = cv2.cvtColor(cv2.flip(frame,1),cv2.COLOR_BGR2RGB)
    result = mp_face_mesh.process(frame)
    frame = cv2.cvtColor(frame,cv2.COLOR_RGB2BGR)
    
    if result.multi_face_landmarks and not gameOver:
        for facial_landmark in result.multi_face_landmarks:
            pos = []
            for idx in idList:
                pt1 = facial_landmark.landmark[idx]
                x   = int(pt1.x * width)
                y   = int(pt1.y * height)
                cv2.circle(frame,(x,y),2,(255,0,100),-1) 
                cv2.putText(frame,str(idx),(x,y),cv2.FONT_HERSHEY_COMPLEX,0.4,(0,0,255))
                pos.append((x,y))
            
            cv2.line(frame,pos[0],pos[2],(0,255,0),3)
            cv2.line(frame,pos[0],pos[3],(0,255,0),3)
            
            cv2.line(frame,pos[1],pos[2],(0,255,0),3)
            cv2.line(frame,pos[1],pos[3],(0,255,0),3)
            
            upDown    = distance(pos[0],pos[1])
            leftRight = distance(pos[2],pos[3])
            ratio = int((upDown/leftRight)*100)
            cx,cy = (pos[0][0]+pos[1][0])//2,(pos[0][1]+pos[1][1])//2
            cv2.circle(frame,(cx,cy),1,(0,255,255),-1)
            cv2.line(frame,(cx,cy),(objPos[0]+36,objPos[1]+64),(0,255,0),3)
            distMouseObject = distance((cx,cy),(objPos[0]+36,objPos[1]+64))
            
            
            mouseState = ""
            ColorState = []
            if ratio < 55 :
                mouseState = "Close"
                ColorState = [0,0,255]
            else:
                mouseState = "Open"
                ColorState = [0,255,0]
            if distMouseObject < 20 and mouseState == "Open":
                if isEatable:
                    curentObject , isEatable = objectReset()
                    count += 1
                else:
                    gameOver = True
            cv2.putText(frame,"Your score: {}".format(count),(50,50),cv2.FONT_HERSHEY_COMPLEX,2,ColorState,2)
            
        
        objPos[1] += speed
        if objPos[1] > 370:
            curentObject , isEatable = objectReset()
        frame = cvzone.overlayPNG(frame,curentObject,objPos)
    else :
        cv2.putText(frame,"Game Over Yourscore:{}".format(count),(0,200),cv2.FONT_HERSHEY_PLAIN,3,[0,0,255],3)
    cv2.imshow("frame",frame)
    cv2.waitKey(1)

