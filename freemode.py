import time 
import pygame
import random
import sys
import string
from PIL import Image
from pygame import mixer
import math
import subprocess
import os

pygame.init()


#-------------------------------------------------------------------------------------------------------------------
dictionnaire = open("liste_francais.txt", 'r', encoding='utf-8')
dico = [x.rstrip('\n') for x in dictionnaire]
dictionnaire.close()
dico = [x.lower() for x in dico]

def replace_c(dico):
    dico = list(dico)
    dico2 = []
    for words in dico:
        car = ''
        words = list(words)
        if "ç" in words:
            for i in range(len(words)):
                if words[i] == "ç":
                    words[i] = "c"
        for x in range(len(words)):
            car += words[x]
        dico2.append(car)

    return dico2

dico = replace_c(dico)

rdm_word = random.choice(dico)

rdm_list = []
characters = list(string.ascii_lowercase) + ['8', '2', '7', '0' ,'6', 'ù']


lim_taille = 25
timer_end = False


pygame.display.set_caption("FreeMode")
screen = pygame.display.set_mode((1920,1080), pygame.RESIZABLE)
clock = pygame.time.Clock()


first_music = False
first_music_end = False
second_music = False

voice = False

poping_done = False


screenX = screen.get_width()
screenY = screen.get_height()

class Rect_Values:
    def __init__(self ,screenX, screenY):
        self.W = screenX/4
        self.H = screenY/8
        self.X = screenX/2 - self.W/2
        self.Y = screenY/1.25


class RdmTxt_values:
    def __init__(self, screenX, screenY, rdmtxt):
        
        self.W = rdmtxt.get_width()
        self.H = rdmtxt.get_height()
        self.X = screenX/2 - self.W/2
        self.Y = screenY/5

class SoundCircle:
    def __init__(self, screenX, screenY):
        self.W = sound_up.get_width()
        self.H = sound_up.get_height()
        self.X = screenX - self.W*1.2 + self.W/2
        self.Y = screenY - self.H*1.2 + self.H/2
        self.MIDX = self.X + self.W/2
        self.MIDY = self.Y - self.H/2
        self.RAD = self.W/2
    
def distance(mouseX, mouseY, circleX, circleY, rad):
    distance = math.sqrt((mouseX-circleX)**2 + (mouseY-circleY)**2)
    if distance < rad:
        return True
    else:
        return False


    
def resize_img(img, x, y):
    image = Image.open(img)
    new_image = image.resize((x, y))
    new_image.save('new_background.jpg')

def resize_sound(img, x, y):
    image = Image.open(img)
    new_image = image.resize((x, y))
    new_image.save('new_sound.png')


def display_timer(x, y, start_time, countdown, font_timer):
    current_time = time.time()
    if countdown - (current_time-start_time) > 10:
        timer = font_timer.render(str(int(countdown - (current_time-start_time))), True, "white")
        screen.blit(timer, (x, y))
    elif countdown - (current_time-start_time) >1:
        timer = font_timer.render('0'+str(int(countdown - (current_time-start_time))), True, "red")
        screen.blit(timer, (x, y))
    else: 
        global timer_end
        timer_end = True

    if countdown - (current_time-start_time) < 3:
        volume = pygame.mixer.music.get_volume()
        if volume > 0:
            volume -= 0.005
            pygame.mixer.music.set_volume(volume)
            


def display_starter_timer(x, y, start_time, countdown, font_timer):
    current_time = time.time()
    if countdown - (current_time-start_time) > 1:
        timer = font_timer.render(str(int(countdown - (current_time-start_time))), True, "white")
        screen.blit(timer, (x - timer.get_width()/2 , y - timer.get_height()/2 ))
        
    else: 

        timer = font_timer.render("ÉCRIVEZ", True, "white")
        timer_w = timer.get_width()
        screen.blit(timer, (x-timer_w/2, y - timer.get_height()/2))
        pygame.display.flip()

        
        mixer.music.load("background.wav")
        mixer.music.play()

        if sound == False:
            mixer.music.pause()

        global first_music
        first_music = True
        global starter
        starter = False
        global start_timer
        start_timer = True
        time.sleep(1)
    
def display_stats(start_time, screenX, screenY):               
    current_time = time.time()
    time_until_start = current_time-start_time

    if time_until_start < 2:
        font_stop = pygame.font.Font('font.ttf', int(screenX/10 + screenY/10))
        stop = font_stop.render('stop', True, 'white')
        screen.blit(stop, (screenX/2 - stop.get_width()/2, screenY/2 - stop.get_height()/2))
        global run_once

        if run_once == 0 and sound:
            
            mixer.music.load('stop.wav')
            mixer.music.play()
            run_once = 1
    
    elif time_until_start < 4.5:

        
        font_annonce = pygame.font.Font('font.ttf', int(screenX/20 + screenY/20))
        annonce = font_annonce.render('vous avez eu un score de...', True, 'white')
        screen.blit(annonce,(screenX/2 - annonce.get_width()/2, screenY/2 - annonce.get_height()/2))


        global run_once2
        if run_once2 == 0 and sound:
            mixer.music.unload()
            mixer.music.load('drum.wav')
            mixer.music.play()
            run_once2 = 1

    if time_until_start > 4.5:
        global police_score1
        global police_score2

        if len(rdm_list) < 22:
            color_number = 'red'
        elif len(rdm_list) <= 28:
            color_number = 'orange'
        else:
            color_number = 'green'
        

        font_score1 = pygame.font.Font(None,police_score1)
        font_score2 = pygame.font.Font('font.ttf', police_score2)
        score1 = font_score1.render(str(len(rdm_list)), True, color_number)
        score2 = font_score2.render(' mots/min', True, 'white')
        screen.blit(score1,(screenX/2 - score1.get_width()/2 - score2.get_width()/2, screenY/2 - score1.get_height()/2))
        screen.blit(score2,(screenX/2 - score2.get_width()/2 + score1.get_width()/2, screenY/2 - score2.get_height()/2))

        global poping_done

        if police_score1 < int(screenX/5 + screenY/5) and poping_done == False:
            police_score1+=6

        elif police_score1 < int(screenX/5 + screenY/5):
            police_score1 = int(screenX/5 + screenY/5)

        if police_score1 > int(screenX/5 + screenY/5):
            police_score1 = int(screenX/5 + screenY/5)
        
        if police_score1 == int(screenX/5 + screenY/5):
            poping_done = True
            
            
        if police_score2 < int(screenX/15 + screenY/15) and poping_done == False:
            police_score2 +=2

        elif police_score2 < int(screenX/15 + screenY/15):
            police_score2 = int(screenX/15 + screenY/15)

        if police_score2 > int(screenX/15 + screenY/15):
            police_score2 = int(screenX/15 + screenY/15)

        if police_score2 == int(screenX/15 + screenY/15):
            poping_done = True            

        global run_once3
        if run_once3 == 0 and sound:
            mixer.music.load('score.wav')
            mixer.music.play()
            run_once3 = 1
            
        global run_once6
        if len(rdm_list) <= 10 and mixer.music.get_busy() == False and sound and run_once6 == 0:
            mixer.music.load('oof.wav')
            mixer.music.play()
            run_once6 = 1
            


    if time_until_start > 8:
        font_moyenne = pygame.font.Font('font.ttf', int(screenX/50 + screenY/50))
        moyenne = font_moyenne.render('le score moyen est de 25 mots/min', True, 'white')
        screen.blit(moyenne, (screenX/2 - moyenne.get_width()/2, screenY/8))

    if time_until_start > 10:
        global restart_button
        restart_button = True




def display_input_rect(input_rect):
    pygame.draw.rect(screen, "white", input_rect, 2)
    


def display_rdmword(word):
    font_rdmtxt = pygame.font.Font('font.ttf', int(screenX/20 + screenY/20))
    rdmtxt = font_rdmtxt.render(word, True, "white")
    Rdm = RdmTxt_values(screenX, screenY, rdmtxt)
    screen.blit(rdmtxt, (Rdm.X, Rdm.Y))
    global rdm_txt_w, rdm_txt_h, rdm_txt_x, rdm_txt_y
    rdm_txt_w, rdm_txt_h, rdm_txt_x, rdm_txt_y = Rdm.W, Rdm.H, Rdm.X, Rdm.Y

    

def check_letters(user_word, word):

    try:
        for i in range(len(user_word)):
            if user_word[i] != word[i]:
                return "red"
    except:
        return "red"
    return "green"


running = True 
user_text = ""
clicked_rect = False
back_key = False
letter_key = False

color = "white"
start = []
start2 = []
start3 = []
starter = False
i = 0

start_timer = False
rdm_txt_w = 0
rdm_txt_h = 0
rdm_txt_x = 0
rdm_txt_y = 0

resize_img('background.jpg', screenX, screenY)
background = pygame.image.load('new_background.jpg')

sound = True
sound_up = pygame.image.load('sound_up.png')
sound_down = pygame.image.load('sound_down.png')
resized = False
sound_clicked = False


run_once = 0
run_once1 = 0
run_once2 = 0
run_once3 = 0
run_once4 = 0
run_once5 = 0
run_once6 = 0

color_restart = 'black'
restart_button = False

police_score1 = 1
police_score2 = 1

MUSIC_END = pygame.USEREVENT
pygame.mixer.music.set_endevent(MUSIC_END)


#-------------------------------------------------------------------------------------------------------------------

while running:
    

    screen.fill((0,0,0)) 
    screen.blit(background, (0,0))

    screenX = screen.get_width()
    screenY = screen.get_height()
    rect = Rect_Values(screenX, screenY)
    input_rect = pygame.rect.Rect(rect.X, rect.Y,rect.W,rect.H)


    while starter and i == 1:

        
        
        screen.fill((0,0,0)) 
        screen.blit(background, (0,0))

        screenX = screen.get_width()
        screenY = screen.get_height()


        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                os._exit(0)

            if event.type == pygame.VIDEORESIZE:
                width, height = event.size
                resize_img('background.jpg', width, height)
                background = pygame.image.load('new_background.jpg')


        if voice == False and sound:
            mixer.music.load('countdown(3-1).wav')
            mixer.music.play()
            voice = True  

        
        start2.append(time.time())
        font_starter_timer = pygame.font.Font('font.ttf', int(screenY/5))
        display_starter_timer(screenX/2, screenY/2, start2[0], 4, font_starter_timer)



        pygame.display.flip()

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            os._exit(0)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == pygame.BUTTON_LEFT:
                if input_rect.collidepoint(event.pos):
                    clicked_rect = True
                    starter = True
                    i += 1
            
                mouseX, mouseY = event.pos
                new_screenX = screen.get_width()
                circle = SoundCircle(screenX, screenY)

                if distance(mouseX, mouseY, circle.X, circle.Y, circle.RAD):

                    if sound:
                        sound = False
                        sound_clicked = True
                        resize_sound('sound_down.png',int(new_screenX/20), int(new_screenX/20))
                        sound_down = pygame.image.load('new_sound.png')
                    else:
                        sound = True
                        sound_clicked = True
                        resize_sound('sound_up.png',int(new_screenX/20), int(new_screenX/20))
                        sound_up = pygame.image.load('new_sound.png')
            


        
        if event.type == pygame.KEYDOWN and clicked_rect == True:
            if event.key == pygame.K_F10:
                timer_end = True
            if event.key == pygame.K_BACKSPACE:
                back_key = True
                
            else:
                if pygame.key.name(event.key) in characters:
                    if len(user_text) < lim_taille :
                        user_text += event.unicode
                        if user_text == rdm_word:
                            user_text = ""
                            rdm_list.append(rdm_word)
                            rdm_word = random.choice(dico)
                        

                
        elif event.type == pygame.KEYUP and clicked_rect == True:
            if event.key == pygame.K_BACKSPACE:
                back_key = False
        
        if event.type == pygame.VIDEORESIZE:
            width, height = event.size
            if width < 600:
                width = 600
            if height < 400:
                height = 400

            resize_img('background.jpg', width, height)
            background = pygame.image.load('new_background.jpg')
            screen = pygame.display.set_mode((width,height), pygame.RESIZABLE)
            if sound:
                resize_sound('sound_up.png', int(width/20), int(width/20))
                sound_up = pygame.image.load('new_sound.png')
                resized = True
            else:
                resize_sound('sound_down.png', int(width/20), int(width/20))
                sound_down = pygame.image.load('new_sound.png')
                resized = True

            police = int(rect.H)
        
        if event.type == MUSIC_END:
            first_music = False
            first_music_end = True
        

            
            

            

    if back_key and len(user_text) > 0:
        time.sleep(0.1)
        user_text = user_text[:-1]
        police += 4
        
        


    
    rect = Rect_Values(screenX, screenY)
    circle = SoundCircle(screenX, screenY)

    display_input_rect(input_rect)

    if len(user_text) <= 3 :
        police = int(rect.H)


    if run_once1 == 0:
        police = int(rect.H)
        run_once1 = 1



    
    font_txt = pygame.font.Font('font.ttf', police)
    txt = font_txt.render(user_text, True, color)


    if txt.get_width() > rect.W:
        police -= 3


    

    screen.blit(txt, txt.get_rect(center = input_rect.center))
    

    display_rdmword(rdm_word)

    color = check_letters(user_text, rdm_word)

    font_timer = pygame.font.Font(None, int(screenY/5))

    if start_timer == False:
        font_instructions = pygame.font.Font('font.ttf', int(screenY/40))
        instructions = font_instructions.render("cliquez sur le rectangle", True, "red")
        instructions2 = font_instructions.render("pour commencer le jeu", True, "red")
        instructions3 = font_instructions.render("----------------------------->", True, "red")
        screen.blit(instructions, (rect.X - instructions.get_width()*1.2, rect.Y + rect.H/4))
        screen.blit(instructions2, (rect.X - instructions.get_width()*1.2, rect.Y + rect.H/4 + instructions.get_height()))
        screen.blit(instructions3, (rect.X - instructions.get_width()*1.2, rect.Y + rect.H/4 + instructions.get_height()+ instructions2.get_height()))

        instructions4 = font_instructions.render("vous devez écrire", True, "red")
        instructions5 = font_instructions.render("le mot en haut de page", True, "red")
        instructions6 = font_instructions.render("le plus vite possible", True, "red")
        instructions7 = font_instructions.render("<------------------------", True, "red")
        screen.blit(instructions4, (rdm_txt_x + rdm_txt_w + rdm_txt_w/8, rdm_txt_y + rdm_txt_h/8))
        screen.blit(instructions5, (rdm_txt_x + rdm_txt_w + rdm_txt_w/8, rdm_txt_y + rdm_txt_h/8 + instructions4.get_height()))
        screen.blit(instructions6, (rdm_txt_x + rdm_txt_w + rdm_txt_w/8, rdm_txt_y + rdm_txt_h/8 + instructions4.get_height() + instructions5.get_height()))
        screen.blit(instructions7, (rdm_txt_x + rdm_txt_w + rdm_txt_w/8, rdm_txt_y + rdm_txt_h/8 + instructions4.get_height() + instructions5.get_height() + instructions6.get_height()))

    if start_timer:
        start.append(time.time())
        display_timer(screenX- screenX/10, screenY/200, start[0], 61, font_timer)

    
    if first_music_end == True and second_music == False and first_music == False:
        mixer.music.unload()
        mixer.music.load("background2.wav")
        mixer.music.play(-1)
        second_music = True

    if sound:
        
        screen.blit(sound_up, (screenX - sound_up.get_width()*1.2, screenY - sound_up.get_height()*1.2))
        if sound_clicked:
            mixer.music.unpause()
    else:

        screen.blit(sound_down, (screenX - sound_down.get_width()*1.2, screenY - sound_down.get_height()*1.2))
        if sound_clicked:
            mixer.music.pause()

    
    

    if timer_end:

        mixer.music.stop()
        mixer.music.unload()
        mixer.music.set_volume(1)

        while running:

            screen.fill((0,0,0)) 
            screen.blit(background, (0,0))

            screenX = screen.get_width()
            screenY = screen.get_height()


            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    os._exit(0)

                if event.type == pygame.VIDEORESIZE:
                    width, height = event.size
                    resize_img('background.jpg', width, height)
                    background = pygame.image.load('new_background.jpg')
                
                if restart_button:

                    if restart_rect.collidepoint(pygame.mouse.get_pos()):
                        color_restart = (149, 149 ,149)

                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if event.button == pygame.BUTTON_LEFT:
                                running = False
                            

                    else:
                        color_restart = 'black'
            
            start3.append(time.time())
            display_stats(start3[0], screenX, screenY)

            if restart_button:
                rect = Rect_Values(screenX, screenY)

                if run_once4 == 0:
                    police2 = int(rect.H*0.5)
                    run_once4 = 1

                restart_rect = pygame.rect.Rect(rect.X, rect.Y, rect.W, rect.H)
                pygame.draw.rect(screen, color_restart, restart_rect)
                pygame.draw.rect(screen, 'white', restart_rect, 2)
                font_restart = pygame.font.Font('font.ttf', police2)
                restart = font_restart.render('recommencer?', True, 'red')
                screen.blit(restart, restart.get_rect(center = restart_rect.center))

                if restart.get_width() > rect.W:
                    police2 -= 2
                if restart.get_width() < rect.W - rect.W/25:
                    police2 += 2




            
            
            
            

            pygame.display.flip()
            clock.tick(60)


    pygame.display.flip()
    clock.tick(60)




pygame.display.quit()
subprocess.call([sys.executable, os.path.realpath('freemode.py')] +
sys.argv[1:])