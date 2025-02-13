import pygame
import math
import sys
import sidebar
import lower_bar

pygame.init()

WIDTH, HEIGHT = 1200, 700
FPS = 60

COLORS = {
    "BLACK": (0, 0, 0),
    "WHITE": (255, 255, 255),
    "YELLOW": (255, 255, 0),
    "GREY": (50, 50, 50),
    "LIGHT_GREY": (100, 100, 100)
}

class SolarSystem:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Solar System Simulator")
        
        # Load planet data without "info" fields (info now comes from lower_bar)
        self.planets = self.load_planets_data()
        self.textures = self.load_textures()
        self.background = self.load_background()

        self.camera_pos = pygame.Vector2(0, 0)
        self.zoom = 1.0
        self.sidebar_open = True
        self.selected_planet = None
        self.speed_multiplier = 1.0
        self.font = pygame.font.SysFont("Arial", 24)

        self.dragging = False
        self.last_mouse_x = 0
        self.last_mouse_y = 0

    def load_background(self):
        try:
            background = pygame.image.load("images/Solarsystem.jpg").convert()
            return pygame.transform.scale(background, (WIDTH, HEIGHT))
        except pygame.error as e:
            print(f"Error loading background: {e}")
            sys.exit()

    def load_textures(self):
        textures = {}
        try:
            for planet in self.planets:
                # Expect an image file named like "sun.png", "mercury.png", etc.
                img = pygame.image.load(f"images/{planet['name'].lower()}.png").convert_alpha()
                textures[planet['name']] = pygame.transform.scale(img, (planet['radius'] * 4, planet['radius'] * 4))
            return textures
        except pygame.error as e:
            print(f"Error loading textures: {e}")
            sys.exit()


    def load_planets_data(self):
        return [
             {"name": "sun", "radius": 10, "distance": 0, "speed": 0, "angle": 0},
            {"name": "mercury", "radius": 2, "distance": 39, "speed": 0.04, "angle": 0,
            "info": "Mercury is the closest planet to the Sun."},
            {"name": "venus", "radius": 3, "distance": 72, "speed": 0.03, "angle": 0,
            "info": "Venus has a thick atmosphere and extreme temperatures."},
            {"name": "earth", "radius": 4, "distance": 100, "speed": 0.02, "angle": 0,
            "info": "Earth is our home planet, full of life."},
            {"name": "mars", "radius": 3.5, "distance": 152, "speed": 0.018, "angle": 0,
            "info": "Mars is known as the Red Planet."},
            {"name": "yupiter", "radius": 16, "distance": 520, "speed": 0.01, "angle": 0,
            "info": "Jupiter is the largest planet in our Solar System."},
            {"name": "saturn", "radius": 11, "distance": 958, "speed": 0.008, "angle": 0,
            "info": "Saturn is famous for its stunning rings."},
            {"name": "uranus", "radius": 7, "distance": 1922, "speed": 0.006, "angle": 0,
            "info": "Uranus rotates on its side."}
        ]

    def world_to_screen(self, position):
        return (
            WIDTH // 2 + (position[0] - self.camera_pos.x) * self.zoom,
            HEIGHT // 2 + (position[1] - self.camera_pos.y) * self.zoom
        )

    def draw_orbit(self, planet):
        if planet["distance"] > 0:
            points = []
            for angle in range(0, 360, 5):
                x = math.cos(math.radians(angle)) * planet["distance"]
                y = math.sin(math.radians(angle)) * planet["distance"]
                points.append(self.world_to_screen((x, y)))
            pygame.draw.lines(self.screen, COLORS["WHITE"], True, points, 1)

    def handle_input(self):
        keys = pygame.key.get_pressed()
        move_speed = 10 / self.zoom

        if keys[pygame.K_w]:
            self.camera_pos.y -= move_speed
        if keys[pygame.K_s]:
            self.camera_pos.y += move_speed
        if keys[pygame.K_a]:
            self.camera_pos.x -= move_speed
        if keys[pygame.K_d]:
            self.camera_pos.x += move_speed

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # Sidebar click to update selected_planet, toggle menu, or adjust speed
                    self.sidebar_open, self.selected_planet, self.camera_pos, self.zoom, self.speed_multiplier = \
                        sidebar.handle_sidebar_click(
                            event.pos, self.planets, self.sidebar_open, self.selected_planet, self.camera_pos, self.zoom, self.speed_multiplier
                        )
                elif event.button == 3:
                    self.dragging = True
                    self.last_mouse_x, self.last_mouse_y = event.pos
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 3:
                    self.dragging = False
            elif event.type == pygame.MOUSEMOTION and self.dragging:
                dx = event.pos[0] - self.last_mouse_x
                dy = event.pos[1] - self.last_mouse_y
                self.camera_pos.x -= dx / self.zoom
                self.camera_pos.y -= dy / self.zoom
                self.last_mouse_x, self.last_mouse_y = event.pos
            elif event.type == pygame.MOUSEWHEEL:
                zoom_factor = 1.1 if event.y > 0 else 0.9
                self.zoom = max(0.1, min(5.0, self.zoom * zoom_factor))

    def run(self):
        clock = pygame.time.Clock()
        while True:
            self.screen.blit(self.background, (0, 0))
            self.handle_input()

            # Draw the Sun (central star)
            pygame.draw.circle(self.screen, COLORS["YELLOW"], self.world_to_screen((0, 0)), int(20 * self.zoom))

            for planet in self.planets:
                self.draw_orbit(planet)
                planet["angle"] += planet["speed"] * self.speed_multiplier
                world_x = math.cos(planet["angle"]) * planet["distance"]
                world_y = math.sin(planet["angle"]) * planet["distance"]

                # If a planet is selected, center the camera on it
                if self.selected_planet and self.selected_planet["name"] == planet["name"]:
                    self.camera_pos.update(world_x, world_y)

                screen_pos = self.world_to_screen((world_x, world_y))
                scaled_texture = pygame.transform.scale(
                    self.textures[planet["name"]],
                    (int(planet["radius"] * 6 * self.zoom), int(planet["radius"] * 6 * self.zoom))
                )
                self.screen.blit(scaled_texture, scaled_texture.get_rect(center=screen_pos))
            
            # Draw the sidebar and lower info bar
            sidebar.draw_sidebar(self.screen, self.font, self.planets, self.sidebar_open, self.selected_planet, self.speed_multiplier)
            lower_bar.draw_lower_bar(self.screen, self.font, self.selected_planet)
            
            pygame.display.flip()
            clock.tick(FPS)

if __name__ == "__main__":
    simulator = SolarSystem()
    simulator.run()