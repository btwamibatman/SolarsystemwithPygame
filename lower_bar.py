
import pygame

BAR_HEIGHT = 100
BAR_COLOR = (30, 30, 30)    
TEXT_COLOR = (255, 255, 255)  

def draw_lower_bar(screen, font, selected_planet):
    screen_width = screen.get_width()
    screen_height = screen.get_height()
    
    pygame.draw.rect(screen, BAR_COLOR, (0, screen_height - BAR_HEIGHT, screen_width, BAR_HEIGHT))
    
    if selected_planet:
        info_text = (
            f"Name: {selected_planet['name']} | "
            f"Radius: {selected_planet['radius']} | "
            f"Distance: {selected_planet['distance']} | "
            f"Speed: {selected_planet['speed']}"
        )
        extra_info = selected_planet.get("info", "")
        full_text = info_text + " | " + extra_info
        
        text_surface = font.render(full_text, True, TEXT_COLOR)
        screen.blit(text_surface, (10, screen_height - BAR_HEIGHT + 10))
    else:
        default_text = "No planet selected. Click on a planet's name in the sidebar for more info."
        text_surface = font.render(default_text, True, TEXT_COLOR)
        screen.blit(text_surface, (10, screen_height - BAR_HEIGHT + 10))
    