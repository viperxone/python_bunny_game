# https://www.raywenderlich.com/2795-beginning-game-programming-for-teens-with-python
# 1 - Import library
import pygame
from pygame.locals import *
import math
import random

# 2 - Initialize the game
pygame.init()
pygame.mixer.init() # for sounds and music
width, height = 640, 480
screen=pygame.display.set_mode((width, height))
keys = [False, False, False, False]
playerpos=[100,100]
acc=[0,0] #keeps track of players accuracy
arrows=[] #keeps track of arrows

gametime = 90000

# badgers.
# 1) Add bad guys to a list an array.
# 2) Update the bad guy array each frame and check if they are off screen.
# 3) Show the bad guys.

# sets up a timer (as well as a few other values) so that the game adds
# a new badger after some time has elapsed. You decrease the badtimer 
# every frame until it is zero and then you spawn a new badger.
badtimer=100
badtimer1=0
badguys=[[640,100]]
healthvalue=194


# 3 - Load images
player = pygame.image.load("resources/images/dude.png")
grass = pygame.image.load("resources/images/grass.png")
castle = pygame.image.load("resources/images/castle.png")
arrow = pygame.image.load("resources/images/bullet.png")
badguyimg1 = pygame.image.load("resources/images/badguy.png")
# sets up a copy of the image so that you can animate the bad guy much more easily
badguyimg=badguyimg1

healthbar = pygame.image.load("resources/images/healthbar.png")
health = pygame.image.load("resources/images/health.png")

gameover = pygame.image.load("resources/images/gameover.png")
youwin = pygame.image.load("resources/images/youwin.png")

# MY OWN - trying to get the arrow/carrot to start at the mouth of the rabbit
# 
player_width = player.get_width()/2
#player_height = player.get_height()

# 3.1 - Load audio and volume
hit = pygame.mixer.Sound("resources/audio/explode.wav")
enemy = pygame.mixer.Sound("resources/audio/enemy.wav")
shoot = pygame.mixer.Sound("resources/audio/shoot.wav")
hit.set_volume(0.05)
enemy.set_volume(0.05)
shoot.set_volume(0.05)
pygame.mixer.music.load('resources/audio/moonlight.wav') # bg music
pygame.mixer.music.play(-1, 0.0)
pygame.mixer.music.set_volume(0.25)


# 4 - keep looping through
running = 1
exitcode = 0
while running:
    # to decrement the value of badtimer for each frame
    badtimer-=1
    # 5 - clear the screen before drawing it again
    screen.fill(0)
    # 6 - draw the screen elements
    #------------------------------------------
    # <module> for x in range(width/grass.get_width()+1):
    #    TypeError: 'float' object cannot be interpreted as an integer
    #------------------------------------------
    # when i first ran the code, it gave me the above issue. This is because there the "/" was used
    # should be "//"
    for x in range(width//grass.get_width()+1):
        for y in range(height//grass.get_height()+1):
            screen.blit(grass,(x*100,y*100))

    screen.blit(castle,(0,30))
    screen.blit(castle,(0,135))
    screen.blit(castle,(0,240))
    screen.blit(castle,(0,345 ))

    # screen.blit(player, playerpos)
    # 6.1 - Set player position and rotation
    # First you get the mouse and player positions.
    # Then you feed those into the atan2 function. After that, you
    # convert the angle received from the atan2 function from
    # radians to degrees (multiply radians by approximately 57.29 or 360/2π).
    # Since the bunny will be rotated, its position will change.
    # So now you calculate the new bunny position and display the bunny
    # on screen.
    position = pygame.mouse.get_pos()
    angle = math.atan2(position[1]-(playerpos[1]+32),position[0]-(playerpos[0]+26))
    playerrot = pygame.transform.rotate(player, 360-angle*57.29)
    playerpos1 = (playerpos[0]-playerrot.get_rect().width/2, playerpos[1]-playerrot.get_rect().height/2)
    screen.blit(playerrot, playerpos1) 

    # 6.2 - Draw arrows
    # vely and velx values are calculated using basic trigonometry.
    # 10 is the speed of the arrows. The if statement just checks if the
    # bullet is out of bounds and if it is, it deletes the arrow.
    # The second for statement loops through the arrows and draws them with
    # the correct rotation.
    for bullet in arrows:
        index=0
        velx=math.cos(bullet[0])*10
        vely=math.sin(bullet[0])*10
        bullet[1]+=velx
        bullet[2]+=vely
        if bullet[1]<-64 or bullet[1]>640 or bullet[2]<-64 or bullet[2]>480:
            arrows.pop(index)
        index+=1
        for projectile in arrows:
            arrow1 = pygame.transform.rotate(arrow, 360-projectile[0]*57.29)
            screen.blit(arrow1, (projectile[1], projectile[2]))

    # 6.3 - Draw badgers
    # if badtimer is zero and if it is, creates a badger and 
    # sets badtimer up again based on how many times badtimer has run so far. 
    if badtimer==0:
        badguys.append([width, random.randint(50,(height-50))])
        badtimer=100-(badtimer1*2)
        if badtimer1>=35:
            badtimer1=35
        else:
            badtimer1+=5
    index=0
    
    # The first for loop updates the x position of the badger, 
    # checks if the badger is off the screen, and removes the badger 
    # if it is offscreen. The second for loop draws all of the badgers.
    for badguy in badguys:
        if badguy[0]<-64:
            badguys.pop(index)
        badguy[0]-=7

        # 6.3.1 - Attack castle
        badrect=pygame.Rect(badguyimg.get_rect())
        badrect.top=badguy[1]
        badrect.left=badguy[0]
        if badrect.left<64: # badger hit castle
            hit.play() 
            healthvalue -= random.randint(5,20)
            badguys.pop(index)
        
        # 6.3.2 - Check for collisions
        # have to loop through all of the bad guys and inside each 
        # of those loops, you have to loop through all of the arrows 
        # and check if they collide. If they do, then delete the badger, 
        # delete the arrow, and add one to your accuracy ratio.
        index1=0
        for bullet in arrows:
            bullrect=pygame.Rect(arrow.get_rect())
            bullrect.left=bullet[1]
            bullrect.top=bullet[2]
            if badrect.colliderect(bullrect): #is a built-in PyGame function that checks if two rectangles intersect.
                enemy.play() # arrow hit badger
                acc[0]+=1
                badguys.pop(index)
                arrows.pop(index1)
            index1+=1
       
        # 6.3.3 - Next bad guy
        index+=1

    for badguy in badguys:
        screen.blit(badguyimg, badguy)

    # 6.4 - Draw clock
    # HUD (Heads Up Display) that shows the current health level of the castle.
    # You can also add a clock to show how long the castle has survived.
    font = pygame.font.Font(None, 24)
    # original code will have long float timer. so need to put "//" instead of "/".
    survivedtext = font.render(str((gametime-pygame.time.get_ticks())//60000) + ":" + str((gametime-pygame.time.get_ticks())//1000%60).zfill(2), True, (0,0,0))
    textRect = survivedtext.get_rect()
    textRect.topright=[(width-5),5]
    screen.blit(survivedtext, textRect)

     # 6.5 - Draw health bar
     # The code first draws the all-red health bar. 
     # Then it draws a certain amount of green over the bar, 
     # according to how much life the castle has remaining.
    screen.blit(healthbar, (5,5))
    for health1 in range(healthvalue):
        screen.blit(health, (health1+8,8))

    # 7 - update the screen
    pygame.display.flip()
    # 8 - loop through the events
    for event in pygame.event.get():
        # check if the event is the X button 
        if event.type==pygame.QUIT:
            # if it is quit the game
            pygame.quit() 
            exit(0)

        if event.type == pygame.KEYDOWN:
            if event.key==K_w:
                keys[0]=True
            elif event.key==K_a:
                keys[1]=True
            elif event.key==K_s:
                keys[2]=True
            elif event.key==K_d:
                keys[3]=True
        if event.type == pygame.KEYUP:
            if event.key==pygame.K_w:
                keys[0]=False
            elif event.key==pygame.K_a:
                keys[1]=False
            elif event.key==pygame.K_s:
                keys[2]=False
            elif event.key==pygame.K_d:
                keys[3]=False

    # 9 - Move player
    if keys[0]:
        playerpos[1]-=5
        #print("up??")
    elif keys[2]:
        playerpos[1]+=5
        #print("down??")
    if keys[1]:
        playerpos[0]-=5
        #print("left??")
    elif keys[3]:
        playerpos[0]+=5
        #print("right??")

    # checks if the mouse was clicked and if it was, it gets the
    # mouse position and calculates the arrow rotation based on the
    # rotated player position and the cursor position. This rotation
    # value is stored in the arrows array.
    if event.type==pygame.MOUSEBUTTONDOWN:
        shoot.play()
        position=pygame.mouse.get_pos()
        acc[1]+=1
        arrows.append([math.atan2(position[1]-(playerpos1[1]+32),position[0]-(playerpos1[0]+26)),playerpos1[0]+32,playerpos1[1]+32])
        #print(arrows)
        
    #10 - Win/Lose check
    # win
    if pygame.time.get_ticks()>=gametime:
        running=0 #exit while loop
        exitcode=1
    # lose
    if healthvalue<=0:
        running=0 #exit while loop
        exitcode=0
    if acc[1]!=0:
        accuracy=acc[0]*1.0/acc[1]*100
    else:
        accuracy=0

# 11 - Win/lose display        
if exitcode==0:
    pygame.font.init()
    font = pygame.font.Font(None, 24)
    text = font.render("Accuracy: "+str(accuracy)+"%", True, (255,0,0))
    textRect = text.get_rect()
    textRect.centerx = screen.get_rect().centerx
    textRect.centery = screen.get_rect().centery+24
    screen.blit(gameover, (0,0))
    screen.blit(text, textRect)
else:
    pygame.font.init()
    font = pygame.font.Font(None, 24)
    text = font.render("Accuracy: "+str(accuracy)+"%", True, (0,255,0))
    textRect = text.get_rect()
    textRect.centerx = screen.get_rect().centerx
    textRect.centery = screen.get_rect().centery+24
    screen.blit(youwin, (0,0))
    screen.blit(text, textRect)
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
    pygame.display.flip()
