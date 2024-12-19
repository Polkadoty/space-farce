import websocket
import json
import requests
from galaxy_gen import Galaxy

class TestClient:
    def __init__(self, server_url="http://localhost:8080"):
        self.server_url = server_url
        self.ws = None
        
    def create_game(self, galaxy_size=100):
        response = requests.post(
            f"{self.server_url}/api/v1/games/create",
            json={
                "galaxy_size": galaxy_size,
                "max_players": 4,
                "seed": 42  # Fixed seed for testing
            }
        )
        return response.json()
        
    def connect_to_game(self, game_id):
        ws_url = f"ws://localhost:8080/api/v1/games/{game_id}/ws"
        self.ws = websocket.create_connection(ws_url)
        
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

def run_verification_test(num_clients=4):
    clients = [TestClient() for _ in range(num_clients)]
    
    # First client creates the game
    game_data = clients[0].create_game()
    game_id = game_data["ID"]
    seed = game_data["Seed"]
    size = game_data["GalaxySize"]
    
    # Generate galaxies for all clients
    galaxies = []
    for client in clients:
        client.connect_to_game(game_id)
        galaxies.append(client.generate_and_verify_galaxy(seed, size))
    
    # Compare all galaxies with the first one
    for i in range(1, len(galaxies)):
        if not clients[0].compare_galaxies(galaxies[0], galaxies[i]):
            print(f"Galaxy mismatch detected between client 0 and client {i}")
            return False
            
    print("All galaxies verified as identical!")
    return True

if __name__ == "__main__":
    run_verification_test() 