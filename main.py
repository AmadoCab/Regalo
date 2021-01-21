import pygame
import math as m
import subprocess

#comentario de intento

# Constants
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUESITO = (12, 165, 232, 91)
COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')


# Classes
class InputBox:
    """
    Author of this class https://stackoverflow.com/users/6220679/skrx with
    little changes.
    """

    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    respuesta = self.text
                    self.text = ''
                    self.txt_surface = FONT.render(self.text, True, self.color)
                    return respuesta
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = FONT.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)

# Variables
rosco_n = [i+1 for i in range(25)]
answers = [
    ('amado', 'amado'), ('bizarro', 'bizarra'), ('confesonario', 'confesionario'),
    ('desmayo', 'desmayo'), ('eon', 'eon'), ('forraje', 'forraje'),
    ('gaceta', 'gaceta'), ('haiga', 'haiga'), ('iridiscencia', 'iridiscencia'),
    ('jadeara', 'jadease'), ('lee', 'lee'), ('mariana', 'marianita'),
    ('nekomata', 'nekomata'), ('puerto españa', 'puerto españa'),
    ('ostracismo', 'ostracismo'), ('procrastinar', 'procrastinar'),
    ('becquer', 'becquer'), ('rimbombante', 'rimbombante'), ('subatomico','subatomica'),
    ('tiranicidio', 'tiranicidio'), ('uebos', 'uebos'), ('versar', 'versar'),
    ('tex', 'tex'), ('biyectivo','biyectiva'), ('abuelazon', 'abuelazon')
]

# Functions
def increase(counter):
    if counter == 24:
        counter = 0
    else:
        counter += 1
    return counter

def chargeletter(number):
    imagen = pygame.image.load(f'result/{number}.png')
    size = tuple([round(i/4) for i in imagen.get_size()])
    letra = pygame.transform.scale(imagen, size)
    return letra

def chargedef(number):
    imagen = pygame.image.load(f'result2/{number}.png')
    size = tuple([round(i/4.5) for i in imagen.get_size()])
    definicion = pygame.transform.scale(imagen, size)
    return definicion

def create_rosco(lista):
    listaletras = list()
    for n in lista:
        listaletras.append(chargeletter(n))
    return listaletras

def place(imagen, pos):
    screen.blit(imagen, pos)

def question(numero):
    place(chargedef(numero), (123.5, 207.5))

def draw(geometria, color, pos):
    pygame.draw.rect(screen, color, geometria, border_radius=10)
    place(FONT.render('Pasapalabra', True, WHITE), pos)

def rosco(letras):
    if len(letras) == 25:
        i = 0
        for letra in letras:
            posx = 300*m.cos(m.radians(90-i*360/25))+314
            posy = -300*m.sin(m.radians(90-i*360/25))+303
            place(letra, (posx, posy))
            i += 1
    else:
        raise Exception

def win(lista):
    for i in range(1, 25+1):
        if i in lista:
            return False
    for i in range(51, 75+1):
        if i in lista:
            return False
    return True

# Game init
pygame.init()

FONT = pygame.font.Font(None, 32)

input_box = InputBox(250, 500, 100, 30)
screen = pygame.display.set_mode((700,678))

boton = pygame.Rect(20, 610, 145, 40)

cont = 0
running = True
while running:
    screen.fill(WHITE)
    letters = create_rosco(rosco_n)
    rosco(letters)
    question(cont+1)
    input_box.draw(screen)
    draw(boton, BLUESITO, (25,618))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif 25 < rosco_n[cont] <= 50:
            cont = increase(cont)
        else:
            respuestam = input_box.handle_event(event)
            if respuestam == None or respuestam == '' or respuestam == '\n':
                pass
            else:
                respuestam = respuestam.lower()
                respuestam = respuestam.replace('á', 'a')
                respuestam = respuestam.replace('é', 'e')
                respuestam = respuestam.replace('í', 'i')
                respuestam = respuestam.replace('ó', 'o')
                respuestam = respuestam.replace('ú', 'u')
                # print(f'{respuestam} in {answers[cont]}')
                # print(respuestam in answers[cont])
                if respuestam in answers[cont]:
                    if 0 < rosco_n[cont] <= 25:
                        rosco_n[cont] = rosco_n[cont]+25
                    elif 50 < rosco_n[cont] <= 75:
                        rosco_n[cont] = rosco_n[cont]-25
                else:
                    if 0 < rosco_n[cont] <= 25:
                        rosco_n[cont] = rosco_n[cont]+50
                    elif 50 < rosco_n[cont] <= 75:
                        pass
                cont = increase(cont)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if boton.collidepoint(event.pos):
                cont = increase(cont)
    if win(rosco_n):
        data = "tiamu"
        subprocess.run("pbcopy", universal_newlines=True, input=data)
        running = False

    input_box.update()
    pygame.display.update()
#
