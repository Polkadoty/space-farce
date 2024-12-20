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

def run_visualization_test(num_clients=4):
    pygame.init()
    
    # 1080p resolution divided by 2 for each quadrant
    window_size = (960, 540)  # Half of 1920x1080
    screen = pygame.display.set_mode((window_size[0] * 2, window_size[1] * 2))
    pygame.display.set_caption("Space Farce Galaxy Visualization")
    
    clients = [TestClient() for _ in range(num_clients)]
    visualizers = [GalaxyVisualizer(window_size[0], window_size[1]) 
                  for _ in range(num_clients)]
    
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
        f"{clients[0].server_url}/api/v1/games/create",
        headers=headers,
        json={"galaxy_size": 100, "max_players": 4, "seed": seed}
    ).json()
    
    game_id = game_data["id"]
    
    # Generate galaxies and store their JSON representations
    galaxies = []
    galaxy_jsons = []
    for client in clients:
        client.connect_to_game(game_id, token)
        galaxy = client.generate_and_verify_galaxy(seed, game_data["galaxy_size"])
        galaxies.append(galaxy)
        galaxy_jsons.append(galaxy.export_to_json())
    
    # Verify all galaxy JSONs are identical
    for i in range(1, len(galaxy_jsons)):
        if galaxy_jsons[0] != galaxy_jsons[i]:
            print(f"Warning: Galaxy {i} JSON differs from Galaxy 0")
            # Optional: print specific differences
            print(f"Differences in systems: {set(galaxy_jsons[0]['systems'].keys()) ^ set(galaxy_jsons[i]['systems'].keys())}")
    
    # Initialize visualizers with same seed
    for i, visualizer in enumerate(visualizers):
        visualizer.calculate_layout(galaxies[i])
    
    running = True
    clock = pygame.time.Clock()
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        screen.fill((0, 0, 0))
        
        # Update and draw each client's galaxy
        for i, (galaxy, visualizer) in enumerate(zip(galaxies, visualizers)):
            visualizer.update_layout()
            surface = visualizer.draw(galaxy)
            x = (i % 2) * window_size[0]
            y = (i // 2) * window_size[1]
            screen.blit(surface, (x, y))
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    run_visualization_test() 