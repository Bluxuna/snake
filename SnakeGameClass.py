import math
import cv2
import random
import cvzone
import numpy as np
import pyttsx4

class SnakeGameClass:
    def __init__(self,pathFood):
        self.initializeData()
        self.gameOver=False
        self.score=0
        # sachmelebi
        self.imgFood=cv2.imread(pathFood,cv2.IMREAD_UNCHANGED)
        self.hFood,self.wFood , _ =self.imgFood.shape #get dim
        
    def randomLocation(self):
        self.foodPoint=random.randint(100,300),random.randint(100,300)
    def initializeData(self):
        self.points=[] #gvelis pointebi
        self.lenghts=[]#distancia
        self.currentLength=0# sruli sigrdze
        self.allowedLength=150
        self.previousHead=0,0
        self.foodPoint=0,0
        self.randomLocation()
        
        
        
    def update(self,imgMain,currentHead):
        
        if self.gameOver:
            cvzone.putTextRect(imgMain,"you lose bidzi",[300//2,400//2],scale=3,thickness=3,
                            offset=20)
            # engine = pyttsx4.init()
            # engine.say('You lose bidzi.')
            # engine.runAndWait()
            cvzone.putTextRect(imgMain,f'amoun of khinkali: {self.score} ',[300//2,550//2],scale=3,thickness=3,
                            offset=20)
            
        else:
            cx,cy=currentHead
            px,py=self.previousHead
            self.points.append((cx,cy))
            distance= math.hypot(cx-px,cy-py)
            self.lenghts.append(distance)
            self.currentLength+=distance
            self.previousHead=cx,cy
            #shemcireba
            self.reduceLength()
            #tu shechama khinkali
            rx,ry=self.foodPoint
            if(rx-self.wFood//2 <cx<rx+self.wFood//2 and ry-self.hFood//2
               <cy<ry+self.hFood//2):
                self.score+=1
                
                self.allowedLength+=50
                self.randomLocation()
            
            #daxatva
            if self.points:
                for i,point in enumerate(self.points):
                    if i!=0:
                        cv2.line(imgMain,self.points[i-1],self.points[i],(0,0,255),15)
                cv2.circle(imgMain,self.points[-1],15,(200,0,200),cv2.FILLED)
            #xinklebi
            cvzone.putTextRect(imgMain,f'eaten khinkali {self.score}',[50,80],scale=3,thickness=2,
                                offset=10)
            imgMain=cvzone.overlayPNG(imgMain,self.imgFood, (rx-self.wFood//2,ry-self.hFood//2))
            #checker
            pts=np.array(self.points[:-2],np.int32)
            pts=pts.reshape((-1,1,2))
            cv2.polylines(imgMain,[pts],False,(0,200,0),2)
            distace=cv2.pointPolygonTest(pts,(cx,cy),True)
            if(-1<=distace<=1):
                self.gameOver=True
                self.initializeData()
               
        return imgMain
                
    def reduceLength(self):
        if self.currentLength>self.allowedLength:
            for i, lenght in enumerate(self.lenghts):
                self.currentLength-=lenght
                self.lenghts.pop(i)
                self.points.pop(i)
                if self.currentLength < self.allowedLength:
                    break