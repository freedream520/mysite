#coding=utf-8
from VideoCapture import Device
from PIL import ImageDraw
import sys, pygame, time
from pygame.locals import *
from PIL import ImageEnhance
class websee:
     #   设置窗口、摄像头分辨率
    res = (640,480)
 
    #   初始化窗口
    pygame.init()
    pygame.display.set_caption('Webcam')
    pygame.font.init()
 
    screen = pygame.display.set_mode((640,480))
    font   = pygame.font.SysFont("Courier",11)
 
 #   取得摄像头设备，设置分辨率
    cam = Device()
    cam.setResolution(res[0],res[1])
 
 
    #   亮度,对比度
    brightness = 1.0
    contrast = 1.0
    #   截图计数器
    shots = 0
    while 1:
        camshot = ImageEnhance.Brightness(cam.getImage()).enhance(brightness)
        camshot = ImageEnhance.Contrast(camshot).enhance(contrast)
        for event in pygame.event.get():
         if event.type == pygame.QUIT: sys.exit()
       
      #   截图保存,shots为计数器
        
        if(shots==31):
            shots=0
        filename="C:/Users/Canon/Desktop/PollSystem/static/polls/images/"+str(shots)+".jpg"
        cam.saveSnapshot(filename, quality=80, timestamp=0)
        shots =shots+1
        camshot = pygame.image.frombuffer(camshot.tostring(), res, "RGB")
        screen.blit(camshot, (0,0))
        #   填充图像
        pygame.display.flip()
        
