
import pygame
import random
import os
import json
import time
import sys
from mixer_bufferproxy import *

WIDTH, HEIGHT = 900, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

gameIcon = pygame.image.load('assets/nitro_rush.ico')
pygame.display.set_icon(gameIcon)
pygame.display.set_caption("Nitro Rush")
clock = pygame.time.Clock()
fps = 60
ability_level_list = database_update("ability_level","view")
grav = True
nitro = 70  
nitro_fill_status = False
aqua = (79, 255, 232) 
#orange = (253, 77, 12)
grey = (49,49,49)
sap_green = (13, 38, 13)
#terquois = (68, 141, 118)
#aqua_marine = (20, 184, 132)
#mint = (244, 218, 209)
#dark_cyan = (9, 52, 38)
dark_orange = (77, 31, 0)
color0 = [(244, 218, 209),(247, 212, 227),(249, 244, 223)]
color1 = [(253, 77, 12),(194, 20, 96),(252, 205, 37)]
color2 = [(20, 184, 132),(178, 215, 50),(72, 39, 218)]
color3 = [(68, 141, 118),(148, 184, 20),(52, 21, 189)]
color4 = [(9, 52, 38),(43, 52, 9),(18, 9, 54)]
theme = database_update("color","view")
if theme == "cyan":
    color_index = 0
if theme == "green":
    color_index = 1
if theme == "blue":
    color_index = 2

terquois = color3[color_index]
aqua_marine = color2[color_index]
mint = color0[color_index]
dark_cyan = color4[color_index]
orange = color1[color_index]
mdet = False  
global platform_handler
platform_handler = []
kill_rect = []
player = pygame.Rect(150,50,30,50)
collision = False
nitro_amt = 70
global bottom_collision
bottom_collision = False
score = 0
if_clicked = False
toggle = False
syncing_event = pygame.USEREVENT + 1
cooldown = False
mouse_pos = None
global rope_rectcollision
rope_rectcollision = False
hook_hitbox = None
movement = True
counter = 8
case_below = False
case_above = False
rectcollision = False
if ability_level_list[0] == 1:
    grapplecd_const = 14
if ability_level_list[0] == 2:
    grapplecd_const = 12
if ability_level_list[0] == 3:
    grapplecd_const = 10
if ability_level_list[0] == 4:
    grapplecd_const = 8

if ability_level_list[1] == 1:
    time_freezeconst = 15 * 60
    timer_tfconst = 5 * 30
if ability_level_list[1] == 2:
    time_freezeconst = 14 * 60
    timer_tfconst = 6 * 30
if ability_level_list[1] == 3:
    time_freezeconst = 12 * 60
    timer_tfconst = 7 * 30
if ability_level_list[1] == 4:
    time_freezeconst = 10 * 60
    timer_tfconst = 9 * 30

if ability_level_list[2] == 1:
    spawn_rectcdconst = 10
    spr_w = 225
if ability_level_list[2] == 2:
    spawn_rectcdconst = 9
    spr_w = 250
if ability_level_list[2] == 3:
    spawn_rectcdconst = 8
    spr_w = 275
if ability_level_list[2] == 4:
    spawn_rectcdconst = 7
    spr_w = 300


grapple_cd = grapplecd_const
fullscreen = False
cd_visiablity = True
tolerance = 40
rect_speed = 4
kill_rectdensity = 0
data_json = []
ability = 0
spawn_rect_status = False
spawn_rectcd = spawn_rectcdconst
timefreezecd = time_freezeconst
timer_tf = timer_tfconst
tf_status = False
pause = False
upgrade_hover = False
mbackx = 0
mbackdx = 1000
midx = 0
middx = 1000
middx2, midx2 = 1000, 0
sound_unlooper = True
clicksound_unlooper = True
time_freeze_unlooper = True
pygame.font.init()
pygame.mixer.init()
pygame.time.set_timer(syncing_event, 5)


grapple_i = pygame.image.load(os.path.join('assets', 'rope.png'))
grapple_img = pygame.transform.scale(grapple_i,(50, 50))

spawn_recti = pygame.image.load(os.path.join('assets', 'spawn_rect.png'))
spawn_rect_img = pygame.transform.scale(spawn_recti,(50, 50))

coini = pygame.image.load(os.path.join('assets', 'coin.png'))
coins_img = pygame.transform.scale(coini,(50, 50))

time_freezei = pygame.image.load(os.path.join('assets', 'time_freeze.png'))
time_freeze_img = pygame.transform.scale(time_freezei,(50, 50))

time_freezeshopi = pygame.image.load(os.path.join('assets', 'time_freeze_shop.png'))
time_freezeshop_img = pygame.transform.scale(time_freezeshopi,(90, 90))

rope_shopi = pygame.image.load(os.path.join('assets', 'rope_shop.png'))
rope_shop_img = pygame.transform.scale(rope_shopi,(80, 80))

skin_umberala = pygame.image.load(os.path.join('assets/Skins', 'skin_umberala.png'))
skin_umberala_img = pygame.transform.scale(skin_umberala,(60, 60))

bg = pygame.image.load(os.path.join('assets', 'bg.png'))
bg_img = pygame.transform.scale(bg,(WIDTH, HEIGHT))

time_freezelens = pygame.image.load(os.path.join('assets', 'time_freeze_lensfx.png'))
time_freezelensfx = pygame.transform.scale(time_freezelens,(WIDTH + 2, HEIGHT))

spawn_rect_shop = pygame.image.load(os.path.join('assets', 'spawn_rect_shop.png'))
spawn_rect_shop_img = pygame.transform.scale(spawn_rect_shop,(100,100))

main_bg_back = pygame.image.load(os.path.join('assets/Game_background', 'mountains-back.png')).convert_alpha()
main_bg_back_img = pygame.transform.scale(main_bg_back,(1000,800))

main_bg_mid1 = pygame.image.load(os.path.join('assets/Game_background', 'mountains-mid1.png')).convert_alpha()
main_bg_mid1_img = pygame.transform.scale(main_bg_mid1,(1000,800))

main_bg_mid2 = pygame.image.load(os.path.join('assets/Game_background', 'mountains-mid2.png')).convert_alpha()
main_bg_mid2_img = pygame.transform.scale(main_bg_mid2,(1000,800))

def text_objects(text, font):
    textSurface = font.render(text, True, mint)
    return textSurface, textSurface.get_rect()

def text_objects1(text, font):
    textSurface = font.render(text, True, aqua_marine)
    return textSurface, textSurface.get_rect()

def text_objects2(text, font):
    textSurface = font.render(text, True, terquois)
    return textSurface, textSurface.get_rect()

def text_objects3(text, font):
    textSurface = font.render(text, True, dark_cyan)
    return textSurface, textSurface.get_rect()

def button(msg, x, y, w, h, ic, ac, action=None):
    global upgrade_hover 
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(WIN, ac, (x, y, w, h))
        upgrade_hover = False

        if click[0] == 1 and action != None:
            buttonClick = pygame.mixer.Sound('sound/button_click.wav')
            buttonClick.play()
            action()
            
    else:
        if w == 251 and x == 550:
            upgrade_hover = True
        pygame.draw.rect(WIN, ic, (x, y, w, h)) 

    smallText = pygame.font.Font("fonts/bendy.ttf", 30)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ((x+(w/2)), (y+(h/2)))
    WIN.blit(textSurf, textRect)

def button1(msg, x, y, w, h, ic, ac, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(WIN, ac, (x, y, w, h))

        if click[0] == 1 and action != None:
            buttonClick = pygame.mixer.Sound('sound/button_click.wav')
            buttonClick.play()
            action()
    else:
        pygame.draw.rect(WIN, ic, (x, y, w, h))


    smallText = pygame.font.SysFont("calibri", 40)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ((x+(w/2)), (y+(h/2)))
    WIN.blit(textSurf, textRect)

def button2(msg, x, y, w, h, ic, ac, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(WIN, ac, (x, y, w, h))

        if click[0] == 1 and action != None:
            buttonClick = pygame.mixer.Sound('sound/button_click.wav')
            buttonClick.play()
            action()
          
    else:
        pygame.draw.rect(WIN, ic, (x, y, w, h))


    smallText = pygame.font.Font("fonts/bendy.ttf", 26)
    textSurf, textRect = text_objects1(msg, smallText)
    textRect.center = ((x+(w/2)), (y+(h/2)))
    WIN.blit(textSurf, textRect)


def draw_window(keys_pressed):
    global nitro_bar, nitro_amt, bottom_collision, platform_handler, score, toggle, if_clicked, mouse_pos
    global mpos_x, mpos_y, rope_rectcollision, hook_hitbox, grav, movement, counter, mdet, case_below, grapple_cd
    global case_above, rectcollision, nitro_fill_status, cd_visiablity, kill_rect, spawn_rect_status, spawn_rectcd
    global timefreezecd,timer_tf,tf_status, fps, grapplecd_const, time_freezeconst, timer_tfconst,mbackx,mbackdx
    global midx, middx, middx2, midx2, clicksound_unlooper, time_freeze_unlooper
    ability = database_update("ability","view")
    WIN.fill((117, 189, 166))
    
    WIN.blit(main_bg_back_img, (mbackx,0))
    WIN.blit(main_bg_back_img, (mbackdx,0))
    mbackx -= 0.5
    mbackdx -= 0.5
    if mbackx < -999:
        mbackx = 0
    if mbackdx < 0:
        mbackdx = 999
    WIN.blit(main_bg_mid2_img, (midx,0))
    WIN.blit(main_bg_mid2_img, (middx,0))
    midx -= 1
    middx -= 1
    if midx < -999:
        midx = 0
    if middx < 0:
        middx = 999
    WIN.blit(main_bg_mid1_img,(midx2,0))
    WIN.blit(main_bg_mid1_img, (middx2,0))
    midx2 -= 2
    middx2 -= 2
    if midx2 < -999:
        midx2 = 0
    if middx2 < 0:
        middx2 = 997
    
    score += 0.069 
    largeText = pygame.font.Font("fonts/bendy.ttf",40)
    TextSurf, TextRect = text_objects3(f"Score: {round(score)}", largeText)
    TextRect.center = ((WIDTH - 105),(HEIGHT/15))
    WIN.blit(TextSurf, TextRect)
    
    
    if ability == "grapple":
        WIN.blit(grapple_img,(30,HEIGHT - 60))
    if ability == "spawn rect":
        WIN.blit(spawn_rect_img,(30,HEIGHT - 60))
    if ability == "time freeze":
        WIN.blit(time_freeze_img,(30,HEIGHT - 60))

    for i in platform_handler:
        i.build()
        if i.x + i.w < 0:
            platform_handler.remove(i)
    
    for i in kill_rect:
        i.summon()
        if i.x + i.w < 0:
            kill_rect.remove(i)
    
    
    if ability == "grapple":
        if (pygame.mouse.get_pressed())[0] == True:
            mouse_pos = get_mouse_location() 
            mpos_x = mouse_pos[0]
            mpos_y = mouse_pos[1]
            clicksound_unlooper = True
            hook_hitbox = pygame.Rect(mpos_x, mpos_y, 10, 10)
            if hook_hitbox != None:
                if hook_hitbox.y > player.y:
                    mouse_pos = None
            pygame.draw.rect(WIN, orange, hook_hitbox)
            rope_rectcollision = False
            nitro_fill_status = True
        if mouse_pos != None and grapple_cd == grapplecd_const:
            if rope_rectcollision == True:
                clickSound = pygame.mixer.Sound('sound/b.mp3')
                if clicksound_unlooper == True:
                    clickSound.play()
                    clicksound_unlooper = False
                hook_hitbox = pygame.Rect(mpos_x, mpos_y, 10, 10)
                pygame.draw.rect(WIN, orange, hook_hitbox)
                pygame.draw.aaline(WIN, orange, (player.x, player.y), (mpos_x, mpos_y), 1)
                movement = False
                grav = False
                if counter > -4 and player.y > 1:
                    cd_visiablity = False
                    pygame.draw.arc(WIN, orange, (30,HEIGHT - 60,50,50), 0, (counter + 4), 5)
                    if hook_hitbox.y < player.y:
                        case_below = True
                    if case_below == True:
                        player.y -= counter
                

                if counter < -4:
                
                    grav = True
                    movement = True
                    counter = 8
                    mdet = True
                    case_below = False
                    grapple_cd = 0
                    cd_visiablity = True
                    mouse_pos = None
                    nitro_fill_status = False
                counter -= 0.2
            mpos_x -= 4 
        if cd_visiablity == True:
            pygame.draw.arc(WIN, mint, (30,HEIGHT - 60,50,50), -grapple_cd/(grapplecd_const/6.3), 0, 3)

        if grapple_cd <= grapplecd_const:
            grapple_cd += 1/60
            if grapple_cd > grapplecd_const:
                grapple_cd = grapplecd_const

    if ability == "spawn rect":
        global spr_w, spawn_rectcdconst
        if keys_pressed[pygame.K_a] and spawn_rect_status == False:
            spawn_rect_status = True
            spawn_rectcd = 0
            
            spr_x = player.x - spr_w / 6
            spr_y = player.y + player.h + 15
            spawn_rect = Platform(spr_x,spr_y,spr_w,35)
            platform_handler.append(spawn_rect)
            cd_visiablity = True
                    
        if spawn_rect_status == True and spawn_rectcd <= spawn_rectcdconst:
            spawn_rectcd += 1 / 60
        if spawn_rectcd >= spawn_rectcdconst:
            spawn_rect_status = False
        pygame.draw.arc(WIN, mint, (30,HEIGHT - 60,50,50), 0, spawn_rectcd / (spawn_rectcdconst / 6.3), 4)


    if ability == "time freeze":
        if keys_pressed[pygame.K_a]:
            
            
            if tf_status == False and timefreezecd >= time_freezeconst:
                tf_status = True
                timer_tf = 0
        if tf_status == True and timer_tf <= timer_tfconst:
            WIN.blit(time_freezelensfx,(-2,0))
            timer_tf += 1
            fps = 30
            time_freezesound = pygame.mixer.Sound('sound/time_freezesound.mp3')
            time_freezesound.play()
            cd_visiablity = False
            if tf_status == True and timer_tf >= timer_tfconst:
                timefreezecd = 0
                tf_status = False
                fps = 60
                cd_visiablity = True

        if tf_status == False and timefreezecd <= time_freezeconst:
            timefreezecd += 1
        if cd_visiablity == False:
            pygame.draw.arc(WIN, orange, (30,HEIGHT - 60,50,50), timer_tf / (timer_tfconst / 6.3), 0, 5)
        if cd_visiablity == True:
            pygame.draw.arc(WIN, mint, (30,HEIGHT - 60,50,50), 0, timefreezecd / (time_freezeconst / 6.3), 3)




    nitro_bar = pygame.Rect(player.x - 35,player.y - 30,nitro_amt * 1.50,15)
    nitro_bar1 = pygame.Rect(player.x - 35,player.y - 30,nitro * 1.50,15)
    largeText = pygame.font.SysFont("verdana",40)
    TextSurf, TextRect = text_objects("!", largeText)
    TextRect.center = ((nitro_bar.x - 15),(nitro_bar.y + 2))
    if nitro < 2: 
        WIN.blit(TextSurf, TextRect)
    
    pygame.draw.rect(WIN, mint, player)
    pygame.draw.rect(WIN, orange, nitro_bar)
    pygame.draw.rect(WIN, mint, nitro_bar1)
    

fallsp = 1
def gravity():
    global fallsp, grav
    if grav == True:
        tv = 15
        player.y += fallsp
        if fallsp < tv:
            fallsp += 0.15


def nitro_fill():
    global nitro, nitro_fill_status
    if nitro_fill_status == True:
        if nitro < nitro_amt:
            nitro += 0.35


def movementum():
    global mdet, fallsp
    if mdet == True and player.y > 1:
        fallsp = -1
        mdet = False

def kill():
    death = pygame.mixer.Sound('sound/death.mp3')
    death.play()
    death_screen()

def restart():
    ability_level_list = database_update("ability_level","view")
    global player, grav, nitro, nitro_fill_status, platform_handler, rope_rectcollision, bottom_collision, mdet
    global collision, nitro_amt, score, if_clicked, toggle, syncing_event, cooldown, mouse_pos, hook_hitbox
    global movement, counter, case_above, case_below, rectcollision, grapple_cd, fullscreen, plat, kill_rect
    global cd_visiablity, spawn_rectcd, spawn_rect_status, color0, color1, color2, color3, color4,timefreezecd,timer_tf,tf_status, fps
    global grapplecd_const, pause, upgrade_hover, time_freezeconst, timer_tfconst, spawn_rectcdconst, spr_w
    global sound_unlooper, clicksound_unlooper, time_freeze_unlooper
    theme = database_update("color","view")
    if theme == "cyan":
        color_index = 0
    if theme == "green":
        color_index = 1
    if theme == "blue":
        color_index = 2
    
    cd_visiablity = True
    grav = True
    time_freeze_unlooper = True
    sound_unlooper = True
    clicksound_unlooper = True
    tf_status = False
    fps = 60
    pause = False
    upgrade_hover = False
    nitro = 70
    nitro_fill_status = False
    mdet = False 
    aqua = (79, 255, 232) 
    orange = color1[color_index]
    grey = (49,49,49)
    sap_green = (13, 38, 13)
    terquois = color3[color_index]
    aqua_marine = color2[color_index]
    mint = color0[color_index]
    dark_cyan = color4[color_index]
    dark_orange = (77, 31, 0) 

    platform_handler = []
    kill_rect = []
    player = pygame.Rect(150,50,30,50)
    collision = False
    nitro_amt = 70
    bottom_collision = False
    score = 0
    if_clicked = False
    toggle = False
    syncing_event = pygame.USEREVENT + 1
    cooldown = False
    mouse_pos = None
    rope_rectcollision = False
    hook_hitbox = None
    movement = True
    counter = 8
    case_below = False
    case_above = False
    rectcollision = False

    
    if ability_level_list[0] == 1:
        grapplecd_const = 14
    if ability_level_list[0] == 2:
        grapplecd_const = 12
    if ability_level_list[0] == 3:
        grapplecd_const = 10
    if ability_level_list[0] == 4:
        grapplecd_const = 8

    if ability_level_list[1] == 1:
        time_freezeconst = 15 * 60
        timer_tfconst = 5 * 30
    if ability_level_list[1] == 2:
        time_freezeconst = 14 * 60
        timer_tfconst = 6 * 30
    if ability_level_list[1] == 3:
        time_freezeconst = 12 * 60
        timer_tfconst = 7 * 30
    if ability_level_list[1] == 4:
        time_freezeconst = 10 * 60
        timer_tfconst = 9 * 30
    
    if ability_level_list[2] == 1:
        spawn_rectcdconst = 10
        spr_w = 225
    if ability_level_list[2] == 2:
        spawn_rectcdconst = 9
        spr_w = 250
    if ability_level_list[2] == 3:
        spawn_rectcdconst = 8
        spr_w = 275
    if ability_level_list[2] == 4:
        spawn_rectcdconst = 7
        spr_w = 300

    
    timefreezecd = time_freezeconst
    timer_tf = timer_tfconst
    grapple_cd = grapplecd_const
    fullscreen = False
    player.y = 100
    spawn_rect_status = False
    spawn_rectcd = spawn_rectcdconst
    plat = Platform(100,400,800,50)
    platform_handler.append(plat)
    kill_plat = Killing_plat(-5,-5,1,1)
    kill_rect.append(kill_plat)
    if player.y < 600:
        main()

def player_fly(keys_pressed):
    global nitro_fill_status, grav, collision, nitro, fallsp, mdet, bottom_collision, movement, sound_unlooper
    if keys_pressed[pygame.K_SPACE] and movement == True:
        boost = pygame.mixer.Sound('sound/jump.wav')
        if sound_unlooper == True:
            boost.play()
            sound_unlooper = False
        if player.y > 1 and nitro > 0:
            player.y -= 4
            nitro -= 0.75
        nitro_fill_status = False
        grav = False
        if nitro > 7:
            mdet = True
        if nitro < 0:
                grav = True
                sound_unlooper = True
        collision = False
    else:
        if collision == False:
            grav = True
            sound_unlooper = True
            movementum()

 
def player_glide(keys_pressed):
    global nitro_fill_status, grav, collision, nitro, fallsp, mdet, movement
    if keys_pressed[pygame.K_g] and movement == True:
        if player.y > 1 and nitro > 0:
            player.y += 1.5
            nitro -= 0.1369
        nitro_fill_status = False
        grav = False
        if nitro > 5:
            mdet = False
        if nitro < 0:
            grav = True
        collision = False
    else:
        if collision == False:
            grav = True
            movementum()


class Platform():
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w 
        self.h = h
    def build(self):
        global grav, nitro_fill_status, collision, mdet, fallsp, bottom_collision, hook_hitbox, rope_rectcollision
        global rect_speed
        recta = pygame.Rect(self.x,self.y,self.w,self.h)
        pygame.draw.rect(WIN, dark_cyan, recta)
        self.x -= rect_speed
        if nitro_fill_status == True:
            grav = True
        if player.colliderect(recta):
            if recta.bottom - player.top > 15:
                bottom_collision = True
                grav = False
                fallsp = 2
                nitro_fill_status = True
                collision = True
            if recta.bottom - player.top > 15:
                player.y = recta.y - 49
        if hook_hitbox != None:
            if recta.colliderect(hook_hitbox):
                rope_rectcollision = True
                
class Killing_plat():
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w 
        self.h = h
    def summon(self):
        global player, hook_hitbox, rope_rectcollision, rect_speed
        killua = pygame.Rect(self.x,self.y,self.w,self.h)
        pygame.draw.rect(WIN, dark_orange, killua)
        self.x -= rect_speed
        if player.colliderect(killua):
            kill()
        if hook_hitbox != None:
            if killua.colliderect(hook_hitbox):
                rope_rectcollision = True

plat = Platform(100,400,800,50)
platform_handler.append(plat)

kill_plat = Killing_plat(-5,-5,1,1)
kill_rect.append(kill_plat)

def get_mouse_location():
    mouse_pos = pygame.mouse.get_pos()
    return mouse_pos

def click_check():
    global if_clicked, cooldown, syncing_event
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if_clicked = True  
        else:
            if_clicked = False
             
def toggle_check():
    global toggle, if_clicked, cooldown, syncing_event
    for event in pygame.event.get():
        if event.type == syncing_event:
            cooldown = False
    if if_clicked == True:
        if cooldown == False:
            if toggle == False:
                toggle = True
                return True
            if toggle == True:
                toggle = False
                return False
            cooldown = True

            

def platform_generator(): 
    global plat, platform_handler, score, kill_rect, Py, Px, Pw, kill_plat, tolerance, kill_rectdensity, rect_speed
    run = True
    if score > 500:
        kill_rectdensity = 2
        rect_speed = 5
    if score > 1000:
        kill_rectdensity = 3
        rect_speed = 6
    if score > 4000:
        kill_rectdensity = 4
        rect_speed = 7
    if score > 8000:
        rect_speed = 8
    if score > 16000:
        kill_rectdensity = 5
        rect_speed = 10

    if len(platform_handler) < 6:
        Py = random.randint(100,450)
        Pw = random.randint(100,480)
        Px = plat.x + plat.w + random.randint(250,300)
        plat = Platform(Px,Py,Pw,30) 
        platform_handler.append(plat)
    if len(kill_rect) < kill_rectdensity and score > 650:
        Ky = random.randint(100,450)
        Kw = random.randint(25,100)
        Kx = kill_plat.x + kill_plat.w + random.randint(550,770)
        if Py - Ky < tolerance or Py - Ky > tolerance and Px - Kx < tolerance or (Px + Pw) - Kx > tolerance:
            kill_plat = Killing_plat(Kx,Ky,Kw,30) 
            kill_rect.append(kill_plat)




def death_screen():
    pygame.mixer.music.stop()
    coins = database_update("coins","view")
    earned_coins = score / 3
    earned_coins = round(earned_coins)
    total_coins = earned_coins + coins
    database_update("coins","equals",total_coins)
    run = True
    while run:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()
        
        WIN.fill(grey)
        largeText = pygame.font.Font("fonts/bendy.ttf",23)
        TextSurf, TextRect = text_objects(f"You earned {earned_coins}       , Now you have {total_coins}", largeText)
        TextRect.center = ((WIDTH/2),(HEIGHT - 115)) 
        WIN.blit(TextSurf, TextRect)
        WIN.blit(coins_img,((WIDTH/2.3),(HEIGHT/1.3)))
        WIN.blit(coins_img,((WIDTH/1.440),(HEIGHT/1.3)))
        
        
        Highscore = database_update("highscore", "view")
        if score > Highscore:
            Highscore = round(score)
            database_update("highscore", "equals", Highscore)
        largeText = pygame.font.Font("fonts/bendy.ttf",35)
        TextSurf, TextRect = text_objects(f"highscore {Highscore}", largeText)
        TextRect.center = ((WIDTH/2),(HEIGHT - 370)) 
        WIN.blit(TextSurf, TextRect)
        largeText = pygame.font.Font("fonts/bendy.ttf",35)
        TextSurf, TextRect = text_objects(f"score {round(score)}", largeText)
        TextRect.center = ((WIDTH/2),(HEIGHT - 300))
        WIN.blit(TextSurf, TextRect)
        largeText = pygame.font.Font("fonts/bendy.ttf",60)
        TextSurf, TextRect = text_objects("You Died", largeText)
        TextRect.center = ((WIDTH/2),(HEIGHT/4))
        WIN.blit(TextSurf, TextRect)
        button("Restart", 600,400,120,50,terquois,dark_cyan,restart) 
        button("Menu", 400,400,120,50,terquois,dark_cyan, game_intro) 
        button("Exit", 200,400,120,50,terquois,dark_cyan,quit_game)
        pygame.display.update()
        clock.tick(15)

def quit_game():
    pygame.quit()
    sys.exit()

def unpause():
    global pause
    pygame.mixer.music.unpause()
    pause = False


def paused():
    global pause
    pygame.mixer.music.pause()
    WIN.fill(grey)
    largeText = pygame.font.Font("fonts/Dash.otf", 115)
    TextSurf, TextRect = text_objects("Paused", largeText)
    TextRect.center = ((WIDTH/2.0), (HEIGHT/3))
    WIN.blit(TextSurf, TextRect)

    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause = False
                    unpause()

        button("Continue", 150, 450, 150, 50, terquois, dark_cyan, unpause)
        button("Menu", 550, 450, 150, 50, terquois, dark_cyan, game_intro)
        button("Restart", 350, 450, 150, 50,terquois, dark_cyan, restart)

        pygame.display.update()
        clock.tick(15)

current_page = "Skills"
def shop_section_sorter(section):
    global current_page
    current_page = section

def img_zoomer(path, h, w,x,y):
    imgi = pygame.image.load((path))
    img = pygame.transform.scale(imgi,(h,w))
    WIN.blit(img,(x,y))

def text_bliter(text,Font,color,size,x,y):
    largeText = pygame.font.Font(Font,size,bold=True)
    textSurface = largeText.render(text, True, color)
    TextSurf, TextRect = textSurface, textSurface.get_rect()
    TextRect.center = ((x),(y))
    WIN.blit(TextSurf, TextRect)

def text_bliter_acc(text,Font,color,size,x,y):
    largeText = pygame.font.Font(Font,size,bold=True)
    textSurface = largeText.render(text, True, color)
    TextSurf, TextRect = textSurface, textSurface.get_rect()
    TextRect.x,TextRect.y = x,y
    WIN.blit(TextSurf, TextRect)

price_level_list = [
            0,
            969,
            2000,
            4000,
            "Max"
        ]

def shop_buy(obj,price):
    coins = database_update("coins","view")
    skill_level_list = database_update("ability_level", "view")
    if coins >= price:
        Owned_item_list = database_update("Owned_Skills","view")
        Owned_item_list[obj] = 1
        coins -= price
        database_update("coins","equals",coins)
        database_update("Owned_Skills","equals",Owned_item_list)
        skill_level_list[obj] = 1
        database_update("ability_level","equals",skill_level_list)


def skill_equip(obj):
    Owned_items_list = database_update("Owned_Skills","view")
    x = 0
    for i in Owned_items_list:
        if Owned_items_list[x] == 2:
            Owned_items_list[x] = 1
        x += 1
        
    if Owned_items_list[obj] == 1:
       Owned_items_list[obj] = 2
    if Owned_items_list[obj] == 2:
        ability = ["grapple","time freeze","spawn rect"]
        database_update("ability","equals",ability[obj])
        database_update("Owned_Skills","equals",Owned_items_list)


def time_equip():
    skill_equip(1)

def hkm():
    shop_buy(0,1499)

def time_hkm():
    shop_buy(1,2499)

def rect_hkm():
    shop_buy(2,1199)

def rect_eqiup():
    skill_equip(2)



def hkm1():
    skill_equip(0)

def hkm_gupgrade():
    global price_level_list
    level_list = database_update("ability_level","view")
    ability_upgrade(0,price_level_list[level_list[0]])

def time_gupgrade():
    global price_level_list
    level_list = database_update("ability_level","view")
    ability_upgrade(1,price_level_list[level_list[1]])

def rect_gupgrade():
    global price_level_list
    level_list = database_update("ability_level","view")
    ability_upgrade(2,price_level_list[level_list[2]])

def ability_upgrade(ability,price):
    skillability = database_update("ability_level","view")
    coins = database_update("coins","view")
    if price_level_list[skillability[ability]] != "Max":
        if coins >= price:
            coins -= price
            skillability[ability] += 1
            database_update("coins","equals",coins)
            database_update("ability_level","equals",skillability)



def shop():
    global current_page, if_clicked, grapplecd_const, price_level_list,ability_level_list, upgrade_hover,timer_tfconst,time_freezeconst
    global spawn_rectcdconst, spr_w
    rope_shop_click = False
    tf_shop_click = False
    SR_click = False

    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        Owned_items_list = database_update("Owned_Skills","view")
        skill_level_list = database_update("ability_level","view")
        coins = database_update("coins","view")
        if skill_level_list[0] == 1:
            grapplecd_const = 14
        if skill_level_list[0] == 2:
            grapplecd_const = 12
        if skill_level_list[0] == 3:
            grapplecd_const = 10
        if skill_level_list[0] == 4:
            grapplecd_const = 8
        
        if ability_level_list[1] == 1:
            time_freezeconst = 15 * 60
            timer_tfconst = 5 * 30
        if ability_level_list[1] == 2:
            time_freezeconst = 14 * 60
            timer_tfconst = 6 * 30
        if ability_level_list[1] == 3:
            time_freezeconst = 12 * 60
            timer_tfconst = 7 * 30
        if ability_level_list[1] == 4:
            time_freezeconst = 10 * 60
            timer_tfconst = 9 * 30

        if ability_level_list[2] == 1:
            spawn_rectcdconst = 10
            spr_w = 225
        if ability_level_list[2] == 2:
            spawn_rectcdconst = 9
            spr_w = 250
        if ability_level_list[2] == 3:
            spawn_rectcdconst = 8
            spr_w = 275
        if ability_level_list[2] == 4:
            spawn_rectcdconst = 7
            spr_w = 300

        
        WIN.fill(terquois)
        nav_bar = pygame.Rect(0,0,900,55)
        pygame.draw.rect(WIN, dark_cyan, nav_bar)

        button1("<", 0, 0, 55, 55, dark_cyan, aqua_marine, game_intro)
        button2("More tabs coming soon..", 350, 0, 95, 55, dark_cyan, dark_cyan, shop)
        if current_page == "Skills":
            button2("Skills", 95, 0, 95, 55, dark_cyan, dark_cyan, shop)
        else:
            button("Skills", 95, 0, 95, 55, dark_cyan, aqua_marine, shop)
        if current_page == "Skills":
            skill_nav_tab = pygame.Rect(50,300,800,250)
            coin_display = pygame.Rect(0,200,120,32)
            rope_click_hitbox = pygame.Rect(60,320,80,80)
            time_click_hitbox = pygame.Rect(160,320,80,80)
            rect_click_hitbox = pygame.Rect(255,320,80,80)
            
            mupos = get_mouse_location()
            muposx = mupos[0]
            muposy = mupos[1]
            pygame.draw.rect(WIN, orange, rope_click_hitbox)
            pygame.draw.rect(WIN, orange, time_click_hitbox)
            pygame.draw.rect(WIN, orange, rect_click_hitbox)
            pygame.draw.rect(WIN, dark_cyan, coin_display)
            img_zoomer("assets/coin.png",40,40,2,196)
            text_bliter_acc(f"{coins}","fonts/Dash.otf",mint,20,37,208)
            pygame.draw.rect(WIN, dark_cyan, skill_nav_tab)
            WIN.blit(rope_shop_img,(60,320))
            WIN.blit(time_freezeshop_img, (155,315))
            WIN.blit(spawn_rect_shop_img, (245,310))
            
    
            if rope_click_hitbox.x < muposx and rope_click_hitbox.x + 80 > muposx and rope_click_hitbox.y < muposy and rope_click_hitbox.y + 80 > muposy and (pygame.mouse.get_pressed())[0] == True:
                rope_shop_click = True
                tf_shop_click = False
                SR_click = False
            if time_click_hitbox.x < muposx and time_click_hitbox.x + 80 > muposx and time_click_hitbox.y < muposy and time_click_hitbox.y + 80 > muposy and (pygame.mouse.get_pressed())[0] == True:
                rope_shop_click = False
                tf_shop_click = True
                SR_click = False
            if rect_click_hitbox.x < muposx and rect_click_hitbox.x + 80 > muposx and rect_click_hitbox.y < muposy and rect_click_hitbox.y + 80 > muposy and (pygame.mouse.get_pressed())[0] == True:
                rope_shop_click = False
                tf_shop_click = False
                SR_click = True
            

            if rope_shop_click == True:
                img_zoomer("assets/rope_shop.png",180,180,150,87)
                text_bliter("Grappling Hook","fonts/Dash.otf",mint,45,500,85)
                text_bliter("Swing to the platforms above you, using Grappling Hook.","fonts/bendy.ttf",dark_cyan,20,600,130)
                text_bliter("Left mouse click on the platform, you wanna grapple on.","fonts/bendy.ttf",dark_cyan,20,600,160)
                text_bliter(f"You cannot grapple on platforms below you. cooldown:               ","fonts/bendy.ttf",dark_cyan,18,600,190)
                
            
                
                if upgrade_hover == False and grapplecd_const != 8:
                    text_bliter(f"{grapplecd_const - 2} sec","fonts/bendy.ttf",mint,18,818,190)
                else:
                    text_bliter(f"{grapplecd_const} sec","fonts/bendy.ttf",dark_cyan,18,818,190)
                if Owned_items_list[0] == 0: 
                    button("Buy 1499",350,225,150,50,dark_cyan, terquois,hkm)

                if Owned_items_list[0] == 1:
                    button("Equip",350,225,150,50,dark_cyan, terquois,hkm1)
                    button(f"Upgrade        {price_level_list[skill_level_list[0]]}",550,225,251,50,dark_cyan, terquois, hkm_gupgrade)
                    img_zoomer("assets/coin.png",55,55,680,222)
                    text_bliter("-","fonts/sign_font.ttf",mint,28,630,90)
                    text_bliter(f"Level. {skill_level_list[0]}","fonts/Dash.otf",mint,28,680,90)
                if Owned_items_list[0] == 2:
                    button("Equipped",350,225,150,50,dark_cyan, terquois)
                    button(f"Upgrade        {price_level_list[skill_level_list[0]]}",550,225,251,50,dark_cyan, terquois,hkm_gupgrade)
                    img_zoomer("assets/coin.png",55,55,680,222)
                    text_bliter("-","fonts/sign_font.ttf",mint,28,630,90)
                    text_bliter(f"Level. {skill_level_list[0]}","fonts/Dash.otf",mint,28,680,90)
                
            if tf_shop_click == True:
                img_zoomer("assets/time_freeze_shop.png",180,180,150,87)
                text_bliter("Time Freeze","fonts/Dash.otf",mint,45,500,85)
                text_bliter("Press a to slow the time around you. Great for clutches.","fonts/bendy.ttf",dark_cyan,20,600,130)
                text_bliter(f"time goes 50 percent slower for {round(timer_tfconst / 30)} sec","fonts/bendy.ttf",dark_cyan,20,520,160)
                text_bliter(f"cooldown ","fonts/bendy.ttf",dark_cyan,18,410,190)
            
                if upgrade_hover == False and time_freezeconst != 10 * 60:
                    text_bliter_acc(f"{round((time_freezeconst/60) - 1)} sec","fonts/bendy.ttf",mint,18,460,178)
                else:
                    text_bliter_acc(f"{round(time_freezeconst / 60)} sec","fonts/bendy.ttf",dark_cyan,18,460,178)
                if Owned_items_list[1] == 0:
                    button("Buy 2499",350,225,150,50,dark_cyan, terquois,time_hkm)

                if Owned_items_list[1] == 1:
                    button("Equip",350,225,150,50,dark_cyan, terquois,time_equip)
                    button(f"Upgrade       {price_level_list[skill_level_list[1]]}",550,225,251,50,dark_cyan, terquois,time_gupgrade)
                    img_zoomer("assets/coin.png",55,55,680,222)
                    text_bliter("-","fonts/sign_font.ttf",mint,28,630,90)
                    text_bliter(f"Level. {skill_level_list[1]}","fonts/Dash.otf",mint,28,680,90)
                if Owned_items_list[1] == 2:
                    button("Equipped",350,225,150,50,dark_cyan, terquois)
                    button(f"Upgrade       {price_level_list[skill_level_list[1]]}",550,225,251,50,dark_cyan, terquois,time_gupgrade)
                    img_zoomer("assets/coin.png",55,55,680,222)
                    text_bliter("-","fonts/sign_font.ttf",mint,28,630,90)
                    text_bliter(f"Level. {skill_level_list[1]}","fonts/Dash.otf",mint,28,680,90)

            if SR_click:
                img_zoomer("assets/spawn_rect_shop.png",180,180,150,87)
                text_bliter("Spawn Platform","fonts/Dash.otf",mint,40,500,85)
                text_bliter("Spawns a handy platform below you.","fonts/bendy.ttf",dark_cyan,20,600,130)
                text_bliter(f"Platform Size        cooldown","fonts/bendy.ttf",dark_cyan,20,520,160)
        
                if upgrade_hover == False and spawn_rectcdconst != 7:
                    text_bliter_acc(f"{round(spawn_rectcdconst) - 1} sec","fonts/bendy.ttf",mint,18,653,149)
                    text_bliter_acc(f"{spr_w + 25}","fonts/bendy.ttf",mint,18,523,149)
                else: 
                    text_bliter_acc(f"{round(spawn_rectcdconst)} sec","fonts/bendy.ttf",dark_cyan,18,653,149)
                    text_bliter_acc(f"{spr_w}","fonts/bendy.ttf",dark_cyan,18,523,149) 
                if Owned_items_list[2] == 0:
                    button("Buy 1199",350,225,150,50,dark_cyan, terquois,rect_hkm)
                if Owned_items_list[2] == 1:
                    button("Equip",350,225,150,50,dark_cyan, terquois,rect_eqiup)
                    button(f"Upgrade       {price_level_list[skill_level_list[2]]}",550,225,251,50,dark_cyan, terquois,rect_gupgrade)
                    img_zoomer("assets/coin.png",55,55,680,222)
                    text_bliter("-","fonts/sign_font.ttf",mint,28,630,90)
                    text_bliter(f"Level. {skill_level_list[2]}","fonts/Dash.otf",mint,28,680,90)
                if Owned_items_list[2] == 2:
                    button("Equipped",350,225,150,50,dark_cyan, terquois)
                    button(f"Upgrade       {price_level_list[skill_level_list[2]]}",550,225,251,50,dark_cyan, terquois,rect_gupgrade)
                    img_zoomer("assets/coin.png",55,55,680,222)
                    text_bliter("-","fonts/sign_font.ttf",mint,28,630,90)
                    text_bliter(f"Level. {skill_level_list[2]}","fonts/Dash.otf",mint,28,680,90)
                

                
        pygame.display.update()
        click_check()
        clock.tick(15)

def display_text_animation(string):
    text = ''
    for i in range(len(string)):
        text += string[i]
        font = pygame.font.Font("fonts/Dash.otf",50,bold=True)
        text_surface = font.render(text, True, dark_cyan)
        text_rect = text_surface.get_rect()
        text_rect.center = (WIDTH/2, HEIGHT/2)
        WIN.blit(text_surface, text_rect)
        pygame.display.update()
        pygame.time.wait(100)





def game_intro():
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        

        WIN.fill(grey)
        WIN.blit(bg,(0,0))
        largeText = pygame.font.Font("fonts/Dash.otf",45,bold=True)
        TextSurf, TextRect = text_objects("× Nitro Rush", largeText)
        TextRect.center = ((WIDTH/7),(HEIGHT/12))
        WIN.blit(TextSurf, TextRect)
        Highscore = database_update("highscore", "view")
        largeText1 = pygame.font.Font("fonts/bendy.ttf",30)
        TextSurf, TextRect = text_objects2(f"Your Highscore: {Highscore}", largeText1)
        TextRect.center = ((WIDTH/2),(HEIGHT/1.3))
        WIN.blit(TextSurf, TextRect)
        largeText1 = pygame.font.Font("fonts/bendy.ttf",20)
        TextSurf, TextRect = text_objects(" By Hakashi Katake and Jayden...", largeText1)
        TextRect.center = ((WIDTH/4.5),(HEIGHT/7))
        WIN.blit(TextSurf, TextRect)
        img_zoomer("assets/nitro_rush.png",45,45,5,25)
        
        
       


        
       
        
        
        
        
        
        button("Go!", 200, 300, 225, 55, (0, 50, 77), (112, 219, 219), restart)
        button("Exit", 450, 300, 225, 55, (0, 50, 77), (112, 219, 219),quit_game)
        button("Shop", 200, 380, 475, 55, (0, 50, 77),(112, 219, 219) ,shop)
        
        pygame.display.update()
        clock.tick(15)
            
def main():
    global fps, pause
    run = True
    gamemusic = "sound/gamemusic.mp3"
    pygame.mixer.music.load(gamemusic)
    pygame.mixer.music.play(-1)
    while run:
        clock.tick(fps)
        global fullscreen
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause = True
                    paused()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    if fullscreen == False:
                        fullscreen = True
                    else:
                        fullscreen = False
                if fullscreen == False:
                    pygame.display.set_mode((WIDTH, HEIGHT))
                if fullscreen == True:
                    pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
        
   
                    


        keys_pressed = pygame.key.get_pressed()
        draw_window(keys_pressed)
        gravity()
        nitro_fill()
        player_fly(keys_pressed)
        player_glide(keys_pressed)
        platform_generator()
        click_check()
        toggle_check()
        if player.y > 600:
            kill()
        pygame.display.update()
        
     
        
        

game_intro()
main()


if __name__ == "__Nitro Rush__":
    main()

    