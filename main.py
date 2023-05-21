# Ismael, Louai, Hatim, P5




# Importation des modules
import pygame 
from pygame import mixer
from PIL import Image
import time
import os

# Cette fonction prend en entrée le chemin d'un fichier image (img), une nouvelle largeur (x) et une nouvelle hauteur (y), et redimensionne l'image aux dimensions spécifiées.
def resize_img(img, x, y):           
    image = Image.open(img)
    new_image = image.resize((x, y))
    new_image.save('new_background.jpg')       


# On utilise la classe Rect_Txt pour créer une fenêtre rectangle qui peut être centré sur l'écran.  
class Rect_Txt:
    def __init__(self, screenX, screenY):
        self.H = screenY/8
        self.W = screenX/2
        self.X = screenX/2 - self.W/2
        self.Y = screenY/2 - self.H/2
        self.P = self.W*2 + self.H*2      


pygame.init()
screen = pygame.display.set_mode((1280,720), pygame.RESIZABLE) # Résolution du premier écran.
pygame.display.set_caption('Jeu de rapidité | Ismael Louai Hatim | Projet de NSI') # Nom de la fenêtre ouverte.
clock = pygame.time.Clock()

# Stockage des dimensions actuelles de la fenêtre dans les deux variables.
screenX = screen.get_width()
screenY = screen.get_height()

resize_img('background.jpg', screenX, screenY) # Redimensionne l'arrière plan (background.jpg) en fonction de la fenêtre.
background = pygame.image.load('new_background.jpg') # Redimensionne et stock le nouvelle arrière plan (new_background.jpg) dans la variable background.

running = True

# Initialisation de l'affichage et des animations ainsi que la couleur.
line_length = 1
animation = False
animation2 = False
animation3 = False
falling = False
animation4 = False
animation5 = False
animation6 = False
red, green, blue = (0,255,0)


# Variables booléenes qui seront utilisées pour contrôler l'affichage.
bot_line = False
top_line = False


# Variables de position de la ligne.
line_X = 0  # position horizontale de départ de la ligne.
line_X2 = screenX  # position horizontale finale de la ligne (limite de l'écran).
top_lineY = -5  # position verticale de la ligne supérieure (hors de l'écran).

run_once = 0
run_once2 = 0
run_once3 = 0
run_once4 = 0
run_once5 = 0
run_once6 = 0

# Booléens pour la validation et la souris
validation = False
mouse = False

while running:  # Boucle principale du jeu tant que running est vrai

    screen.fill((0,0,0))  # Remplit l'écran avec la couleur noire
    screen.blit(background, (0,0))  # Affiche l'image de fond en position (0,0)

    screenX = screen.get_width()  # Récupère la largeur de l'écran
    screenY = screen.get_height()  # Récupère la hauteur de l'écran
    
    rect = Rect_Txt(screenX, screenY)  # Créé un objet Rect_Txt avec les dimensions de l'écran
    play_rect = pygame.rect.Rect(rect.X, rect.Y, rect.W, rect.H)  # Créé un rectangle pour le bouton jouer

    font_jouer = pygame.font.Font('font.ttf', int(rect.H))  # Charge la police de caractère pour le bouton jouer
    jouer = font_jouer.render("jouer", True, (red, green, blue))  # Créé un texte "jouer" avec la police de caractère chargée

    if run_once3 == 0:  # Si c'est la première fois que cette condition est vérifiée
        jouer_Y = 0 - jouer.get_height()  # Déplace le texte "jouer" en dehors de l'écran en position (0, hauteur de l'écran négative)
        run_once3 = 1  # Passe run_once3 à 1 pour que cette condition ne soit plus vérifiée

    for event in pygame.event.get():  # Réécupère la liste des événements pygame depuis la dernière fois qu'elle a été appelée

        if event.type == pygame.QUIT:  # Si l'utilisateur ferme la fenêtre
            os._exit(0)  # Arrête le programme

        
        if event.type == pygame.VIDEORESIZE:  # Si l'utilisateur redimensionne la fenêtre
            screenX = screen.get_width()  # Récupère la largeur de la nouvelle fenêtre
            screenY = screen.get_height()  # Récupère la hauteur de la nouvelle fenêtre
            resize_img('background.jpg', screenX, screenY)  # Redimensionne l'image de fond à la taille de la fenêtre
            background = pygame.image.load('new_background.jpg')  # Charge la nouvelle image de fond
            line_X2 = screenX  # Ajuste la position de la ligne de séparation des deux joueurs

        if animation6:  # Si l'animation 6 est en cours

            if play_rect.collidepoint(pygame.mouse.get_pos()):  # Si la souris est sur le bouton jouer
                
                if run_once6 == 0:  # Si c'est la première fois que cette condition est vérifiée
                    red, green, blue = 255, 255, 255  # change la couleur du texte en blanc
                    run_once6 = 1  # Passe run_once6 à 1 pour que cette condition ne soit plus vérifiée
                green -= 20  # Réduit la valeur de green de 20 pour produire un effet de fondu en vert
                blue -= 20  # Réduit la valeur de blue de 20 pour produire un effet de fondu en bleu
                if green < 0:  # Si la valeur de green est négative
                    green = 0  # La met à 0
                if blue < 0:   # Si la valeur de blue est négative
                    blue = 0   # La met à 0
                
                
                # Si le bouton gauche de la souris est cliqué, on coupe la musique, on quitte Pygame et on lance le freemode.
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == pygame.BUTTON_LEFT:
                        mixer.music.unload()
                        pygame.display.quit()
                        import freemode
                        os._exit(0)

            # Si le curseur de la souris ne se trouve pas dans la zone du bouton jouer, on réinitialise les valeurs rouge, vert et bleu à 255            
            if play_rect.collidepoint(pygame.mouse.get_pos()) == False:
                red, green,blue = 255,255,255
                




    

    

    # Si la longueur de la ligne est inférieure à la largeur du rectangle et que l'animation n'est pas activée, on l'agrandit progressivement
    if line_length < rect.W and animation == False:
        line_length += rect.W / 425

    # Sinon, si la ligne est suffisamment longue ou si l'animation est activée, on fixe la longueur de la ligne à la largeur du rectangle
    elif line_length >= rect.W:
        animation = True
        line_length = rect.W
    # Si la longueur de la ligne n'est pas égale à la largeur du rectangle , on la fixe à nouveau à la largeur du rectangle    
    elif line_length != rect.W:
        line_length = rect.W
    
    
    # Si l'animation de chargement n'est pas activée :
    if animation == False:
        font_chargement = pygame.font.Font('font.ttf', int(screenX/25)) # On définit une police d'une taille proportionnelle à la largeur de l'écran
        chargement = font_chargement.render('chargement...', True, 'white') # On crée une surface de texte "chargement" avec la police définie
        screen.blit(chargement, (screenX/2 - chargement.get_width()/2, rect.Y + rect.H + chargement.get_height()/2)) # On blit la surface de texte au centre de l'écran, juste en dessous du bouton jouer
    
    # Si l'animation est en cours, on augmente les valeurs rouge et bleu jusqu'à ce qu'elles atteignent 255
    if animation:
        if red < 255 and blue < 255:
            red += 2
            blue += 2
          
            # Si les valeurs rouge et bleu dépassent 255, on les réinitialise à 255
            if red > 255 or blue > 255:
                red, blue = 255,255

        
    # Dessine une ligne en utilisant la couleur RGB actuelle, artant du point en haut à gauche de la zone de bouton jouer, et se terminant à une position variable sur la droite
    pygame.draw.line(screen, (red, green, blue), (rect.X, rect.Y + rect.H), (rect.X + line_length, rect.Y + rect.H), 5)

    # Vérifie si les valeurs de rouge et de bleu sont égales à 255.
    if red == 255 or blue == 255:
        bot_line = True
        top_line = True
    
    
    if bot_line:
        # Si bot_line est vrai, dessiner une ligne sur l'écran
        pygame.draw.line(screen, (red, green, blue), (line_X, rect.Y), (line_X, rect.Y + rect.H), 5)
        
        if line_X < rect.X and animation2 == False:
            # Si line_X est inférieur à rect.X et animation2 est faux, augmenter line_X de 10
            line_X += 10
        elif line_X >= rect.X:
            # Si line_X est supérieur ou égal à rect.X, marquer l'animation2 comme terminée et fixer line_X à rect.X
            animation2 = True
            line_X = rect.X
        elif line_X != rect.X:
            # Si line_X est différent de rect.X (cas improbable), fixer line_X à rect.X
            line_X = rect.X
        
    if top_line:
        # Si top_line est vrai, dessiner une autre ligne sur l'écran
        pygame.draw.line(screen, (red, green, blue), (line_X2, rect.Y), (line_X2, rect.Y + rect.H), 5)

        if line_X2 > rect.X + rect.W and animation3 == False:
            # Si line_X2 est supérieur à rect.X + rect.W et animation3 est faux, diminuer line_X2 de 10
            line_X2 -= 10
        elif line_X <= rect.X + rect.W:
            # Si line_X est inférieur ou égal à rect.X + rect.W, marquer l'animation3 comme terminée et fixer line_X2 à rect.X + rect.W
            animation3 = True
            line_X2 = rect.X + rect.W
        elif line_X != rect.X + rect.W:
            # Si line_X est différent de rect.X + rect.W (cas improbable), fixer line_X2 à rect.X + rect.W
            line_X2 = rect.X + rect.W
        
    if animation2 and animation3 and run_once == 0:
        # Si animation2 et animation3 sont toutes deux terminées et run_once est 0, charger et jouer le fichier audio 'hit.wav'
        mixer.music.load('hit.wav')
        mixer.music.play()
        run_once = 1
        time.sleep(1)
        falling = True

    
    if falling:
        # Si falling est vrai et run_once2 est 0, charger et jouer le fichier audio 'falling.wav'
        if run_once2 == 0:
            mixer.music.load('falling.wav')
            mixer.music.play()
            run_once2 = 1
        
        if mixer.music.get_busy() == False or validation:

            validation = True
            screen.blit(jouer, (rect.X + rect.W/2 - jouer.get_width()/2, jouer_Y))
            

            if jouer_Y < rect.Y and animation4 == False:
                jouer_Y += 20
            elif jouer_Y >= rect.Y:
                animation4 = True
                jouer_Y = rect.Y
            elif jouer_Y != rect.Y:
                jouer_Y = rect.Y
            
        if animation4:
            if run_once4 == 0:
                mixer.music.load('hit.wav')
                mixer.music.play()
                run_once4 = 1
            if mixer.music.get_busy() == False or animation6:
                pygame.draw.line(screen, (red, green, blue), (rect.X,  top_lineY), (rect.X + rect.W, top_lineY), 5)

                if top_lineY < rect.Y and animation5 == False:
                    top_lineY += 10
                elif top_lineY >= rect.Y:
                    animation5 = True
                    top_lineY = rect.Y
                elif top_lineY != rect.Y:
                    top_lineY = rect.Y

                if animation5:
                    animation6 = True
                    if run_once5 == 0:
                        mixer.music.play()
                        run_once5 = 1


    







    
    



    pygame.display.flip()
    clock.tick(90)
    