import websocket
import json
import requests
from galaxy_gen import Galaxy
import pygame
import sys
from pygame_visualizer import GalaxyVisualizer

class TestClient:
    def __init__(self, server_url="http://localhost:8080"):
        self.server_url = server_url
        self.ws = None
        
    def create_game(self, galaxy_size=100):
        response = requests.post(
            f"{self.server_url}/api/v1/games/create",
            json={
                "galaxy_size": galaxy_size,
                "max_players": 4
            }
        )
        return response.json()
        
    def connect_to_game(self, game_id, token):
        ws_url = f"ws://localhost:8080/api/v1/games/{game_id}/ws"
        headers = {
            "Authorization": f"Bearer {token}"
        }
        self.ws = websocket.create_connection(ws_url, header=headers)
        
    def generate_and_verify_galaxy(self, seed, size):
        galaxy = Galaxy(size, seed)
        galaxy.generate_galaxy()
        return galaxy
        
    def compare_galaxies(self, galaxy1, galaxy2):
        # Compare all systems and their properties
        if len(galaxy1.systems) != len(galaxy2.systems):
            return False
            
        for sys_id in galaxy1.systems:
            sys1 = galaxy1.systems[sys_id]
            sys2 = galaxy2.systems[sys_id]
            
            # Compare all system properties
            if (sys1["system_type"] != sys2["system_type"] or
                sys1["star_types"] != sys2["star_types"] or
                sys1["num_warp_points"] != sys2["num_warp_points"] or
                sys1["planets"] != sys2["planets"] or
                sys1["planet_ep"] != sys2["planet_ep"] or
                sys1["total_ep"] != sys2["total_ep"]):
                return False
                
        return True

def run_visualization_test():
    pygame.init()
    
    window_size = (1280, 800)
    screen = pygame.display.set_mode(window_size)
    pygame.display.set_caption("Space Farce Galaxy Visualization")
    
    client = TestClient()
    visualizer = GalaxyVisualizer(window_size[0], window_size[1])
    
    # Get auth token and create game
    auth_response = requests.post(
        "http://localhost:8080/api/v1/auth/login",
        json={"username": "test_user", "password": "test_pass"}
    ).json()
    token = auth_response["token"]
    
    # Create game with fixed seed
    seed = 42
    headers = {"Authorization": f"Bearer {token}"}
    game_data = requests.post(
        f"{client.server_url}/api/v1/games/create",
        headers=headers,
        json={"galaxy_size": 100, "max_players": 4, "seed": seed}
    ).json()
    
    game_id = game_data["id"]
    client.connect_to_game(game_id, token)
    galaxy = client.generate_and_verify_galaxy(seed, game_data["galaxy_size"])
    
    visualizer.calculate_layout(galaxy)
    
    running = True
    clock = pygame.time.Clock()
    selected_system = None
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    clicked_system = visualizer.get_clicked_system(event.pos)
                    if clicked_system is not None:
                        selected_system = clicked_system
                elif event.button == 3:  # Right click
                    selected_system = None
                elif event.button == 4:  # Mouse wheel up
                    visualizer.zoom = min(2.0, visualizer.zoom * 1.1)
                elif event.button == 5:  # Mouse wheel down
                    visualizer.zoom = max(0.5, visualizer.zoom / 1.1)
        
        screen.fill((0, 0, 0))
        
        if selected_system is not None:
            surface = visualizer.draw_system_detail(galaxy, selected_system)
        else:
            visualizer.update_layout()
            surface = visualizer.draw(galaxy)
            
        screen.blit(surface, (0, 0))
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    run_visualization_test() 