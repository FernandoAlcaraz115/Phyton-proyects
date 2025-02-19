import pygame
import pygame.image 

pygame.init()
screen = pygame.display.set_mode((450, 450))
pygame.display.set_caption("TicTacToe")

fondo = pygame.image.load('Tablero.png.jpg')
circulo = pygame.image.load('circulo_neon.png.webp')
equis = pygame.image.load('cruz_neon.png.webp')

fondo = pygame.transform.scale(fondo, (450, 450))
circulo = pygame.transform.scale(circulo, (125, 125))
equis = pygame.transform.scale(equis, (125, 125))

coor = [[(0,0),(0,0),(0,0)],
        [(0,0),(0,0),(0,0)],
        [(0,0),(0,0),(0,0)]]
tablero = [['', '', ''],
           ['', '', ''],
           ['', '', '']]

turno = 'X'
game_over = False
clock = pygame.time.Clock()

while not game_over:
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

    screen.blit(fondo, (0, 0))
    screen.blit(circulo, (40, 50))
    screen.blit(equis, (160, 165))
    pygame.display.update()
pygame.quit()

        