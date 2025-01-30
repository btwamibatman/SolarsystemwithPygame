import pygame
import math

BLACK = (0, 0, 0)
GREY = (50, 50, 50)
LIGHT_GREY = (100, 100, 100)

SIDEBAR_WIDTH = 200

toggle_button_rect = pygame.Rect(0, 0, SIDEBAR_WIDTH, 30)

def draw_sidebar(screen, font, planets, sidebar_open):
    if sidebar_open:
        pygame.draw.rect(screen, GREY, (0, 0, SIDEBAR_WIDTH, screen.get_height()))
        
        pygame.draw.rect(screen, LIGHT_GREY, toggle_button_rect)
        toggle_text = font.render("Закрыть меню", True, BLACK)
        screen.blit(toggle_text, (10, 5))

        margin_top = 60
        item_height = 40
        for i, planet in enumerate(planets):
            item_y = margin_top + i * item_height
            button_rect = pygame.Rect(0, item_y, SIDEBAR_WIDTH, item_height)
            pygame.draw.rect(screen, LIGHT_GREY, button_rect)

            text_surface = font.render(planet["name"], True, BLACK)
            screen.blit(text_surface, (10, item_y + 8))
    else:
        # Когда панель закрыта, рисуем только кнопку "Открыть меню"
        pygame.draw.rect(screen, LIGHT_GREY, toggle_button_rect)
        toggle_text = font.render("Открыть меню", True, BLACK)
        screen.blit(toggle_text, (10, 5))


def handle_sidebar_click(mouse_pos, planets, sidebar_open, camera_x, camera_y, zoom):
    x, y = mouse_pos

    if toggle_button_rect.collidepoint(x, y):
        sidebar_open = not sidebar_open
        return sidebar_open, camera_x, camera_y, zoom

    if sidebar_open:
        margin_top = 60
        item_height = 40
        for i, planet in enumerate(planets):
            item_y = margin_top + i * item_height
            rect_item = pygame.Rect(0, item_y, SIDEBAR_WIDTH, item_height)
            
            if rect_item.collidepoint(x, y):
                #координаты планеты
                planet_world_x = math.cos(planet["angle"]) * planet["distance"]
                planet_world_y = math.sin(planet["angle"]) * planet["distance"]

                camera_x = planet_world_x
                camera_y = planet_world_y
                zoom = 1.5
                break

    return sidebar_open, camera_x, camera_y, zoom