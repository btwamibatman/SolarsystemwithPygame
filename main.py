import pygame
import math
import sys

import sidebar

pygame.init()

WIDTH, HEIGHT = 1200, 700
WINDOW_TITLE = "Solar System"
FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(WINDOW_TITLE)

try:
    background = pygame.image.load("images/Solarsystem.jpg")
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
except pygame.error as e:
    print(f"Ошибка загрузки изображения фона: {e}")
    sys.exit()

textures = {
    "Mercury": pygame.image.load("images/mercury.png"),
    "Venus": pygame.image.load("images/venus.png"),
    "Earth": pygame.image.load("images/earth.png"),
    "Mars": pygame.image.load("images/mars.png"),
    "Jupiter": pygame.image.load("images/yupiter.png"),
    "Saturn": pygame.image.load("images/saturn.png"),
    "Uranus": pygame.image.load("images/uranus.png"),
}

CENTER_X, CENTER_Y = WIDTH // 2, HEIGHT // 2

planets = [
    {"name": "Mercury", "radius": 5,  "distance":  50, "speed": 0.04,  "angle": 0},
    {"name": "Venus",   "radius": 8,  "distance": 100, "speed": 0.03,  "angle": 0},
    {"name": "Earth",   "radius": 10, "distance": 150, "speed": 0.02,  "angle": 0},
    {"name": "Mars",    "radius": 7,  "distance": 200, "speed": 0.018, "angle": 0},
    {"name": "Jupiter", "radius": 15, "distance": 250, "speed": 0.01,  "angle": 0},
    {"name": "Saturn",  "radius": 12, "distance": 300, "speed": 0.008, "angle": 0},
    {"name": "Uranus",  "radius": 10, "distance": 350, "speed": 0.006, "angle": 0},
]

for planet in planets:
    textures[planet["name"]] = pygame.transform.scale(
        textures[planet["name"]], 
        (planet["radius"] * 4, planet["radius"] * 4)
    )


camera_x = 0.0
camera_y = 0.0
zoom = 1.0

sidebar_open = True

font = pygame.font.SysFont(None, 30)

def draw_planet(screen, planet, texture, camera_x, camera_y, zoom):
    planet["angle"] += planet["speed"]
    

    world_x = math.cos(planet["angle"]) * planet["distance"]
    world_y = math.sin(planet["angle"]) * planet["distance"]

    screen_x = CENTER_X + (world_x - camera_x) * zoom
    screen_y = CENTER_Y + (world_y - camera_y) * zoom


    orbit_radius = planet["distance"] * zoom
    pygame.draw.circle(
        screen,
        WHITE,
        (int(CENTER_X - camera_x * zoom), int(CENTER_Y - camera_y * zoom)),
        int(orbit_radius), 
        1
    )

    texture_rect = texture.get_rect(center=(int(screen_x), int(screen_y)))
    screen.blit(texture, texture_rect)

def main():
    global sidebar_open, camera_x, camera_y, zoom

    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                sidebar_open, camera_x, camera_y, zoom = sidebar.handle_sidebar_click(
                    event.pos,
                    planets,
                    sidebar_open,
                    camera_x,
                    camera_y,
                    zoom
                )

            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_EQUALS, pygame.K_KP_PLUS):
                    zoom += 0.1
                elif event.key in (pygame.K_MINUS, pygame.K_KP_MINUS):
                    zoom = max(0.1, zoom - 0.1)

        
        screen.blit(background, (0, 0))

        
        sun_x = CENTER_X + (-camera_x) * zoom
        sun_y = CENTER_Y + (-camera_y) * zoom
        pygame.draw.circle(screen, YELLOW, (int(sun_x), int(sun_y)), int(20 * zoom))

        for planet in planets:
            draw_planet(screen, planet, textures[planet["name"]], camera_x, camera_y, zoom)

        sidebar.draw_sidebar(screen, font, planets, sidebar_open)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()