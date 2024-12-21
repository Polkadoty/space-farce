import pygame
import math
import random
import numpy as np
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

    PLANET_COLORS = {
        "H": (100, 255, 100),  # Light green
        "R": (139, 69, 19),    # Brown
        "G": (128, 0, 128),    # Purple
        "I": (173, 216, 230),  # Light blue
        "A": (128, 128, 128)   # Gray
    }

    def __init__(self, width=800, height=600):
        self.width = width
        self.height = height
        self.surface = pygame.Surface((width, height))
        self.nodes = {}
        self.node_colors = {}
        self.connections = set()
        pygame.font.init()
        self.font = pygame.font.SysFont('Arial', 32)
        self.small_font = pygame.font.SysFont('Arial', 24)
        self.header_height = 60
        self.zoom = 1.0
        
    def calculate_layout(self, galaxy):
        # Use the galaxy's seed for consistent layouts
        random.seed(galaxy.seed)
        
        # Calculate galaxy center
        center_x = self.width / 2
        center_y = (self.height - self.header_height) / 2 + self.header_height
        
        # Create spiral layout with more spread
        num_systems = len(galaxy.systems)
        golden_angle = np.pi * (3 - np.sqrt(5))  # Golden angle
        
        self.nodes = {}
        for sys_id in range(num_systems):
            # Calculate radius and angle for spiral
            # Increase spread by adjusting the radius calculation
            radius = np.sqrt(sys_id) * (min(self.width, self.height) * 0.4 / np.sqrt(num_systems))
            theta = sys_id * golden_angle
            
            # Add some random variation to make it look more natural
            radius += random.uniform(-20, 20)
            theta += random.uniform(-0.1, 0.1)
            
            # Convert to cartesian coordinates
            x = center_x + radius * np.cos(theta)
            y = center_y + radius * np.sin(theta)
            
            self.nodes[sys_id] = {
                'pos': [x, y],
                'vel': [0, 0]
            }
            
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
                    
                    # Reduced repulsive force for better spread
                    force = 500 / (dist * dist)
                    node['vel'][0] -= (dx/dist) * force
                    node['vel'][1] -= (dy/dist) * force

        # Apply velocities with damping
        for node in self.nodes.values():
            node['pos'][0] += node['vel'][0] * 0.1
            node['pos'][1] += node['vel'][1] * 0.1
            node['vel'][0] *= 0.9
            node['vel'][1] *= 0.9

    def draw_header(self, galaxy, selected_system=None):
        # Draw header background
        pygame.draw.rect(self.surface, (20, 20, 30), 
                        (0, 0, self.width, self.header_height))
        pygame.draw.line(self.surface, (40, 40, 50),
                        (0, self.header_height), (self.width, self.header_height), 2)
        
        # Draw title and controls
        if selected_system is None:
            title = "Space Farce Galaxy Map"
            controls = "Left Click: Select System | Right Click: Reset View | Mouse Wheel: Zoom"
        else:
            system = galaxy.systems[selected_system]
            title = f"System {selected_system:03d} - {system['system_type']}"
            controls = "Right Click: Return to Galaxy View"
        
        title_surf = self.font.render(title, True, (255, 255, 255))
        controls_surf = self.small_font.render(controls, True, (200, 200, 200))
        
        self.surface.blit(title_surf, (20, 10))
        self.surface.blit(controls_surf, (20, 35))

    def draw(self, galaxy):
        self.surface.fill((0, 0, 0))
        self.draw_header(galaxy)
        
        # Calculate visible area based on zoom
        center_x = self.width / 2
        center_y = (self.height - self.header_height) / 2 + self.header_height
        
        # Draw connections first
        for sys_id, system in galaxy.systems.items():
            for connected_id in system['connected_systems']:
                if (sys_id, connected_id) not in self.connections and \
                   (connected_id, sys_id) not in self.connections:
                    self.connections.add((sys_id, connected_id))
        
        for conn in self.connections:
            if conn[0] in self.nodes and conn[1] in self.nodes:
                start = self.nodes[conn[0]]['pos']
                end = self.nodes[conn[1]]['pos']
                start_pos = (
                    (start[0] - center_x) * self.zoom + center_x,
                    (start[1] - center_y) * self.zoom + center_y
                )
                end_pos = (
                    (end[0] - center_x) * self.zoom + center_x,
                    (end[1] - center_y) * self.zoom + center_y
                )
                pygame.draw.line(self.surface, (30, 30, 30), start_pos, end_pos, 1)
        
        # Draw systems
        for sys_id, node in self.nodes.items():
            system = galaxy.systems[sys_id]
            size = int(3 + (system['total_ep'] / 40))
            size = min(size, 8)
            
            pos = (
                (node['pos'][0] - center_x) * self.zoom + center_x,
                (node['pos'][1] - center_y) * self.zoom + center_y
            )
            
            pygame.draw.circle(self.surface, self.node_colors[sys_id], pos, size)
        
        return self.surface

    def get_clicked_system(self, pos):
        # Adjust click detection based on zoom level
        for sys_id, node in self.nodes.items():
            center_x = self.width / 2
            center_y = (self.height - self.header_height) / 2 + self.header_height
            
            # Transform position based on zoom
            node_x = (node['pos'][0] - center_x) * self.zoom + center_x
            node_y = (node['pos'][1] - center_y) * self.zoom + center_y
            
            dx = pos[0] - node_x
            dy = pos[1] - node_y
            if math.sqrt(dx*dx + dy*dy) < 15:  # Increased click radius
                return sys_id
        return None
        
    def draw_system_detail(self, galaxy, system_id):
        self.surface.fill((0, 0, 0))
        self.draw_header(galaxy, system_id)
        
        system = galaxy.systems[system_id]
        
        # Position star(s) on the left side
        star_x = self.width * 0.2
        center_y = (self.height - self.header_height) / 2 + self.header_height
        
        # Draw star(s)
        star_size = 80
        if system['system_type'] == "Starless Nexus":
            pygame.draw.circle(self.surface, self.COLORS["Starless"],
                             (star_x, center_y), star_size)
        elif system['system_type'] == "Binary Star":
            pygame.draw.circle(self.surface, self.COLORS[system['star_types'][0]],
                             (star_x, center_y - 50), star_size)
            pygame.draw.circle(self.surface, self.COLORS[system['star_types'][1]],
                             (star_x, center_y + 50), star_size)
        else:
            pygame.draw.circle(self.surface, self.COLORS[system['star_types'][0]],
                             (star_x, center_y), star_size)
        
        # Draw planets in a line to the right
        if system['system_type'] != 'Starless Nexus':
            planet_start_x = self.width * 0.35
            planet_spacing = (self.width * 0.6) / max(len(system['planets']), 1)
            
            for i, (planet, ep, moons, sites) in enumerate(zip(
                system['planets'],
                system['planet_ep'],
                system['planet_moons'],
                system['planet_sites']
            )):
                x_pos = planet_start_x + (i * planet_spacing)
                
                # Draw orbit line to just before the planet
                if planet != "A":
                    pygame.draw.line(self.surface, (30, 30, 30),
                                   (star_x + star_size, center_y),
                                   (x_pos - 35, center_y), 1)
                    pygame.draw.line(self.surface, (30, 30, 30),
                                   (x_pos + 35, center_y),
                                   (x_pos + planet_spacing - 35, center_y), 1)
                
                # Draw planet or asteroid belt
                if planet == "A":
                    # Draw clustered asteroid belt
                    asteroid_radius = 30
                    for j in range(8):
                        angle = (j / 8) * 2 * math.pi
                        asteroid_x = x_pos + math.cos(angle) * asteroid_radius
                        asteroid_y = center_y + math.sin(angle) * asteroid_radius
                        pygame.draw.circle(self.surface, self.PLANET_COLORS[planet],
                                        (asteroid_x, asteroid_y), 5)
                else:
                    # Draw planet
                    planet_radius = 30
                    pygame.draw.circle(self.surface, self.PLANET_COLORS[planet],
                                     (x_pos, center_y), planet_radius)
                    
                    # Draw EP inside planet
                    ep_text = self.small_font.render(str(ep), True, (255, 255, 255))
                    ep_rect = ep_text.get_rect(center=(x_pos, center_y))
                    self.surface.blit(ep_text, ep_rect)
                
                # Draw planet info below
                info_parts = []
                if planet != "A":
                    info_parts.append(planet)
                    text_surf = self.small_font.render(" ".join(info_parts), True, (255, 255, 255))
                    text_rect = text_surf.get_rect(center=(x_pos, center_y + 50))
                    self.surface.blit(text_surf, text_rect)
                    
                    # Draw moon count on separate line
                    if moons > 0:
                        moon_text = self.small_font.render(f"M:{moons}", True, (200, 200, 200))
                        moon_rect = moon_text.get_rect(center=(x_pos, center_y + 75))
                        self.surface.blit(moon_text, moon_rect)
        
        return self.surface