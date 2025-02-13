import pygame

BLACK = (0, 0, 0)
GREY = (50, 50, 50)
LIGHT_GREY = (100, 100, 100)
WHITE = (255, 255, 255)

SIDEBAR_WIDTH = 200
BUTTON_HEIGHT = 30

toggle_button_rect = pygame.Rect(0, 0, SIDEBAR_WIDTH, BUTTON_HEIGHT)
speed_button_rect = pygame.Rect(0, 35, SIDEBAR_WIDTH, BUTTON_HEIGHT)

def draw_sidebar(screen, font, planets, sidebar_open, selected_planet, speed_multiplier):
    if sidebar_open:
        # Draw sidebar background
        pygame.draw.rect(screen, GREY, (0, 0, SIDEBAR_WIDTH, screen.get_height()))
        # Toggle button to close the sidebar
        pygame.draw.rect(screen, LIGHT_GREY, toggle_button_rect)
        screen.blit(font.render("Close Menu", True, BLACK), (10, 5))
        # Speed control button
        pygame.draw.rect(screen, LIGHT_GREY, speed_button_rect)
        screen.blit(font.render(f"Speed: x{speed_multiplier}", True, BLACK), (10, 40))
        # List planets
        margin_top = 80
        for i, planet in enumerate(planets):
            item_y = margin_top + i * 50
            button_rect = pygame.Rect(10, item_y, 180, 40)
            is_selected = selected_planet and selected_planet["name"] == planet["name"]
            pygame.draw.rect(screen, LIGHT_GREY if is_selected else GREY, button_rect)
            text_surface = font.render(planet["name"], True, WHITE if is_selected else BLACK)
            screen.blit(text_surface, (20, item_y + 10))
    else:
        # When sidebar is closed, show only the toggle button to open it
        pygame.draw.rect(screen, LIGHT_GREY, toggle_button_rect)
        screen.blit(font.render("Open Menu", True, BLACK), (10, 5))

def handle_sidebar_click(mouse_pos, planets, sidebar_open, selected_planet, camera_pos, zoom, speed_multiplier):
    x, y = mouse_pos

    if toggle_button_rect.collidepoint(x, y):
        sidebar_open = not sidebar_open
        return sidebar_open, selected_planet, camera_pos, zoom, speed_multiplier

    if sidebar_open and speed_button_rect.collidepoint(x, y):
        speed_multiplier = 1.0 if speed_multiplier == 2.0 else 2.0
        return sidebar_open, selected_planet, camera_pos, zoom, speed_multiplier

    if sidebar_open:
        margin_top = 80
        for i, planet in enumerate(planets):
            item_y = margin_top + i * 50
            button_rect = pygame.Rect(10, item_y, 180, 40)
            if button_rect.collidepoint(x, y):
                # Toggle selection: if already selected, deselect; otherwise, select this planet.
                if selected_planet and selected_planet["name"] == planet["name"]:
                    selected_planet = None
                else:
                    selected_planet = planet
                break

    return sidebar_open, selected_planet, camera_pos, zoom, speed_multiplier
