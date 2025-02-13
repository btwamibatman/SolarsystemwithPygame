
import pygame
import sys
import main 

pygame.init()

WIDTH, HEIGHT = 1200, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Solar System Simulation - Main Menu")


try:
    background = pygame.image.load("images/Solarsystem.jpg").convert()
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
except pygame.error as e:
    print(f"Error loading background: {e}")
    background = None  


title_font = pygame.font.SysFont("Arial", 36)
button_font = pygame.font.SysFont("Arial", 30)


WHITE = (255, 255, 255)
GREEN = (0, 128, 0)
RED = (128, 0, 0)
BLACK = (0, 0, 0)

start_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 50)
quit_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 20, 200, 50)


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
   
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            
            if start_button.collidepoint(mouse_pos):
                running = False
            
            if quit_button.collidepoint(mouse_pos):
                pygame.quit()
                sys.exit()

    if background:
        screen.blit(background, (0, 0))
    else:
        screen.fill(BLACK)

    title_text = title_font.render("Abdygalym Hamza SE-2428, Solar system simulation", True, WHITE)
    title_rect = title_text.get_rect(center=(WIDTH // 2, 40))
    screen.blit(title_text, title_rect)

    
    pygame.draw.rect(screen, GREEN, start_button)
    start_text = button_font.render("Start", True, WHITE)
    start_text_rect = start_text.get_rect(center=start_button.center)
    screen.blit(start_text, start_text_rect)

    pygame.draw.rect(screen, RED, quit_button)
    quit_text = button_font.render("Quit", True, WHITE)
    quit_text_rect = quit_text.get_rect(center=quit_button.center)
    screen.blit(quit_text, quit_text_rect)

    pygame.display.flip()

simulator = main.SolarSystem()
simulator.run()
