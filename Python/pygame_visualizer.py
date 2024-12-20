import pygame
import math
import random
from galaxy_gen import Galaxy

class GalaxyVisualizer:
    COLORS = {
        "Red": (255, 100, 100),
        "Orange": (255, 165, 0),
        "Yellow": (255, 255, 100),
        "White": (255, 255, 255),
        "Blue": (100, 100, 255),
        "Starless": (50, 50, 50)
    }

    def __init__(self, width=800, height=600):
        self.width = width
        self.height = height
        self.surface = pygame.Surface((width, height))
        self.nodes = {}  # Store node positions
        self.node_colors = {}
        self.connections = set()
        
    def calculate_layout(self, galaxy):
        # Use the galaxy's seed for consistent layouts
        random.seed(galaxy.seed)
        
        self.nodes = {}
        for sys_id in galaxy.systems:
            # Use deterministic positions based on system ID and seed
            angle = (sys_id / len(galaxy.systems)) * 2 * math.pi
            radius = min(self.width, self.height)/4  # Reduced radius to 1/4
            self.nodes[sys_id] = {
                'pos': [
                    self.width/2 + math.cos(angle) * radius,
                    self.height/2 + math.sin(angle) * radius
                ],
                'vel': [0, 0]
            }
            
            # Set node color based on primary star
            star_type = galaxy.systems[sys_id]['star_types'][0]
            self.node_colors[sys_id] = self.COLORS.get(
                star_type if star_type else "Starless"
            )

    def update_layout(self):
        # Apply forces between nodes
        for sys_id, node in self.nodes.items():
            for other_id, other in self.nodes.items():
                if sys_id != other_id:
                    dx = other['pos'][0] - node['pos'][0]
                    dy = other['pos'][1] - node['pos'][1]
                    dist = max(1, math.sqrt(dx*dx + dy*dy))
                    
                    # Repulsive force
                    force = 1000 / (dist * dist)
                    node['vel'][0] -= (dx/dist) * force
                    node['vel'][1] -= (dy/dist) * force

        # Apply velocities
        for node in self.nodes.values():
            node['pos'][0] += node['vel'][0] * 0.1
            node['pos'][1] += node['vel'][1] * 0.1
            node['vel'][0] *= 0.9
            node['vel'][1] *= 0.9
            
            # Keep within bounds
            node['pos'][0] = max(50, min(self.width-50, node['pos'][0]))
            node['pos'][1] = max(50, min(self.height-50, node['pos'][1]))

    def draw(self, galaxy):
        self.surface.fill((0, 0, 0))
        
        # Draw connections first
        for sys_id, system in galaxy.systems.items():
            for connected_id in system['connected_systems']:
                if (sys_id, connected_id) not in self.connections and \
                   (connected_id, sys_id) not in self.connections:
                    self.connections.add((sys_id, connected_id))
                    
        for conn in self.connections:
            if conn[0] in self.nodes and conn[1] in self.nodes:
                start_pos = self.nodes[conn[0]]['pos']
                end_pos = self.nodes[conn[1]]['pos']
                pygame.draw.line(self.surface, (30, 30, 30), 
                               start_pos, end_pos, 1)

        # Draw nodes with smaller sizes
        for sys_id, node in self.nodes.items():
            system = galaxy.systems[sys_id]
            # Reduce base size and scaling further
            size = int(2 + (system['total_ep'] / 40))  # Smaller base and scaling
            size = min(size, 6)  # Lower maximum size
            pygame.draw.circle(self.surface, self.node_colors[sys_id],
                             node['pos'], size)

        return self.surface 