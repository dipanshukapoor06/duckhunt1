import pygame
import time
import serial
import math
from random import randint

PORT=10; #COM Port No(Change it according to your PC)

PORT="COM"+str(PORT);
ser=serial.Serial(PORT,9600);

ch='n';
while(ch!='y'):
    ch=input("Press y after connecting \n");

x=0;
y=0;
print("Program Started");
background=pygame.image.load('final_back.jpg');
BOOM=pygame.image.load('boom.png');
BOOM=pygame.transform.scale(BOOM,(150,80));

pygame.init();
size=700,500; #screen size
screen=pygame.display.set_mode(size);
pygame.display.set_caption("DUCK HUNT"); #Title of the screen
done=False;
clock=pygame.time.Clock();

birds=[1,1,1,1];
#initial random locations of birds and their directions
# Directions ,  1:North 2:North-East 3:East 4:South-East and so on to 8:North West
print("Initial Random Locations :"); 
location=[ [randint(100,600),75] , [randint(100,600),150] , [randint(100,600),250] , [randint(100,600),360] ];
print(location);
directions=[0,0,0,0];
for i in range(4):
    directions[i]=randint(1,8);
print("Initial Random Directions :");
print(directions);
print("After Boundry Conditions  :");

location2=[ [0,0],[0,0],[0,0],[0,0] ];
t0=time.time(); #Note initial time
SCORE_CARD=0;
BULLETS_FIRED=0;

while not done:

        for i in range(7):
            img = pygame.image.load('tmp-'+str(i)+'.gif')
            seconds=math.floor(time.time()-t0);
            if(seconds==151): #time limit to kill birds is 2.5 minutes
                done=True
            if(birds[0]==0 and birds[1]==0 and birds[2]==0 and birds[3]==0): #end if all birds die
                done=True
            for event in pygame.event.get():
                if event.type==pygame.QUIT: #exit program by turning it off
                    done=True
            
            screen.fill([255,255,255])
            
            font=pygame.font.SysFont(None,40);
            screen.blit(background,(0,0));

            #show x-y coordinates
            text=font.render("X :"+str(x),True,[255,0,0]);
            screen.blit(text,[10,20]);
            text=font.render("Y :"+str(y),True,[255,0,0]);
            screen.blit(text,[10,80]);

            #draw the pointers
            pygame.draw.circle(screen,[0,0,0],[int((size[0]/2)+(x*-20)),int((size[1]/2)+(y*20))],20);
            pygame.draw.circle(screen,[0,0,255],[int((size[0]/2)),int((size[1]/2))],210,3);

            #draw the lines near the cursor (uses parametric eq of the circle)
            pygame.draw.line(screen,[0,0,0],[int((size[0]/2)+(x*-20)),int((size[1]/2)+(y*20))],[int(size[0]/2)+(x*-20),int(size[1]/2)-(210*math.sin(math.acos((x*-20)/210)))],5);
            pygame.draw.line(screen,[0,0,0],[int((size[0]/2)+(x*-20)),int((size[1]/2)+(y*20))],[int(size[0]/2)+(x*-20),int(size[1]/2)+(210*math.sin(math.acos((x*-20)/210)))],5);
            pygame.draw.line(screen,[0,0,0],[int((size[0]/2)+(x*-20)),int((size[1]/2)+(y*20))],[int(size[0]/2)-(210*math.cos(math.asin((y*20)/210))),int(size[1]/2)+(y*20)],5);
            pygame.draw.line(screen,[0,0,0],[int((size[0]/2)+(x*-20)),int((size[1]/2)+(y*20))],[int(size[0]/2)+(210*math.cos(math.asin((y*20)/210))),int(size[1]/2)+(y*20)],5);

                    
            time.sleep(0.07);
            #check for Serial data
            if(ser.inWaiting()>0):         
                ch=b'/';
                while(ch.decode('UTF-8')!='*' and ser.inWaiting()>0):
                    ch=ser.read(1);
                    #print(ch);
                if(ser.inWaiting()>0):
                    ch=ser.read(3);
                    #print(ch);
                    #print("X"+str(ch[0])+",Y"+str(ch[1]));
                    x=int(str(ch[0]));
                    x=x-10;
                    y=int(str(ch[1]));
                    y=y-11;
                    if(ch[2]==49):
                        print("Gun Fired");
                        pygame.draw.circle(screen,[255,255,0],[int((size[0]/2)+(x*-20)),int((size[1]/2)+(y*20))],10);
                        ser.write('#'.encode('utf-8'));
                        loop=1;
                        X=int((size[0]/2)+(x*-20));
                        Y=int((size[1]/2)+(y*20));
                        BULLETS_FIRED=BULLETS_FIRED+1; #increment no. of bullets  
                        for j in range(4):
                            if(birds[j]==1):
                                x1=location2[j][0];
                                y1=location2[j][1];
                                if(X>x1-50 and X<x1+50 and Y>y1-50 and Y<y1+50): #check if bullet was fired at the birds location
                                    birds[j]=0;
                                    SCORE_CARD=SCORE_CARD+(500*loop);
                                    loop=loop+1;
                                    print("Bird"+str(j+1)+" is fired");
                                    screen.blit(BOOM,(x1,y1));
                                    
                if(x<-10):
                    x=-10;
                if(x>10):
                    x=10;
                if(y<-10):
                    y=-10;
                if(y>10):
                    y=10;
            

            ser.flushInput();
            #draw the images of birds and move according to their direction
            for j in range(4):
                img = pygame.image.load('tmp-'+str(i)+'.gif')
                if(birds[j]==1):         
                    x1=location[j][0];
                    y1=location[j][1];
                    
                    if(directions[j]==1):
                        new=pygame.transform.rotate(img,-90);
                        x1=x1;
                        y1=y1-5;
                    elif(directions[j]==8):
                        new=pygame.transform.rotate(img,-45);
                        x1=x1-5;
                        y1=y1-5;     
                    elif(directions[j]==6):
                        new=pygame.transform.rotate(img,45);
                        x1=x1-5;
                        y1=y1+5;     
                    elif(directions[j]==5):
                        new=pygame.transform.rotate(img,90);
                        x1=x1;
                        y1=y1+5;     
                    elif(directions[j]==2):
                        new=pygame.transform.rotate(img,-45);
                        new=pygame.transform.flip(new,1,0);
                        x1=x1+5;
                        y1=y1-5;     
                    elif(directions[j]==3):
                        new=pygame.transform.flip(img,1,0);
                        x1=x1+5;
                        y1=y1;     
                    elif(directions[j]==4):
                        new=pygame.transform.rotate(img,45);
                        new=pygame.transform.flip(new,1,0);
                        x1=x1+5;
                        y1=y1+5;     
                    elif(directions[j]==7):
                        new=img;    
                        x1=x1-5;
                        y1=y1;
            
                    location[j][0]=x1;
                    location[j][1]=y1;
                    #checking for boundry location and reflecting the bird accordingly
                    if(y1-20<0):
                        directions[j]=randint(4,6);
                        print(directions);
                    elif(y1+20>400):
                        directions[j]=randint(8,10);
                        if(directions[j]>8):
                            directions[j]=directions[j]-8;
                        print(directions);
                    elif(x1+20>600):
                        directions[j]=randint(6,8);
                        print(directions);
                    elif(x1-20<0):
                        directions[j]=randint(2,4);
                        print(directions);
                    w,h=new.get_size();    
                    screen.blit(new,(location[j][0],location[j][1]));
                    location2[j][0]=int(x1+w/2);
                    location2[j][1]=int(y1+h/2);
                    #draw circles around the bird to show the area you need to shoot at to kill it
                    #uncomment the next line if you need to see it
                    #pygame.draw.circle(screen,[0,255,255],[location2[j][0],location2[j][1]],50,3);
    
                
            pygame.display.flip()

#show stats of your play
print("\n\n###################");            
if(seconds==151):
    print("Time Complete");
print("SCORE :"+str(SCORE_CARD));
print("Time Taken(seconds) :"+str(time.time()-t0));
print("Bullets Fired :"+str(BULLETS_FIRED));
if(BULLETS_FIRED!=0):
    print("Accuracy :"+str( ((4-birds[0]-birds[1]-birds[2]-birds[3])/BULLETS_FIRED)*100)+"%");
print("Program Terminated");
print("###################");            
pygame.quit();
