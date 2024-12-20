import random
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import os
import json

class Galaxy:
    STAR_TYPES = {
        "Red": (1, 2),
        "Orange": (3, 4),
        "Yellow": (5, 6),
        "White": (7, 8),
        "Blue": (9, 10)
    }

    SYSTEM_TYPES = {
        "Single Star": (1, 7),
        "Binary Star": (8, 9),
        "Starless Nexus": (10, 10)
    }

    def __init__(self, num_systems=100, seed=None):
        self.seed = seed  # Store the seed
        if seed:
            random.seed(seed)
        
        self.num_systems = num_systems
        self.systems = {}
        self.graph = nx.Graph()
        self.history = []  # Store generation history
        self.generate_galaxy()

    def roll_d10(self):
        """Returns a number from 1 to 10 (where 0 represents 10)"""
        roll = random.randint(1, 10)
        return roll

    def determine_system_type(self):
        roll = self.roll_d10()
        for system_type, (min_val, max_val) in self.SYSTEM_TYPES.items():
            if min_val <= roll <= max_val:
                return system_type
        return "Single Star"  # Default fallback

    def determine_star_type(self):
        roll = self.roll_d10()
        for star_type, (min_val, max_val) in self.STAR_TYPES.items():
            if min_val <= roll <= max_val:
                return star_type
        return "Yellow"  # Default fallback

    def determine_warp_points(self, system_type, star_type):
        base_roll = self.roll_d10()
        
        # Apply modifiers
        modifiers = 0
        if star_type in ["Orange", "Red"]:
            modifiers -= 1
        if star_type == "Blue":
            modifiers += 1
        if system_type == "Binary Star":
            modifiers += 1
        if system_type == "Starless Nexus":
            modifiers += 2
            
        modified_roll = base_roll + modifiers
        
        # Convert to number of warp points
        if modified_roll <= 1:
            return 0
        elif modified_roll <= 4:
            return 1
        elif modified_roll <= 6:
            return 2
        elif modified_roll <= 8:
            return 3
        elif modified_roll <= 10:
            return 4
        elif modified_roll == 11:
            return 5
        else:
            return 6

    def determine_num_planets(self, star_type):
        """Returns number of planets for a given star type"""
        roll = self.roll_d10()
        
        # Convert table ranges to dictionary format for easier lookup
        planet_ranges = {
            "Red": {0: (1, 4), 4: (5, 6), 5: (7, 7), 6: (8, 8), 
                    7: (9, 9), 8: (10, 10)},
            "Orange": {0: (1, 3), 4: (4, 5), 5: (6, 7), 6: (8, 8), 
                       7: (9, 9), 8: (10, 10)},
            "Yellow": {0: (1, 2), 4: (3, 3), 5: (4, 5), 6: (6, 7), 
                       7: (8, 8), 8: (9, 9), 9: (10, 10)},
            "White": {0: (1, 2), 4: (3, 4), 5: (5, 6), 6: (7, 7), 
                      7: (8, 8), 8: (9, 9), 9: (10, 10)},
            "Blue": {0: (1, 3), 5: (4, 5), 6: (6, 6), 7: (7, 7), 
                     8: (8, 9), 9: (10, 10)}
        }
        
        # Find matching range for the roll
        for num_planets, (min_val, max_val) in planet_ranges[star_type].items():
            if min_val <= roll <= max_val:
                return num_planets
        return 0  # Default fallback

    def determine_planet_types(self, star_type, num_planets):
        """Returns list of planet types based on star type and number"""
        if num_planets == 0:
            return []
        
        # Planet type configurations based on star type and number
        planet_configs = {
            "Red": {
                4: ["R", "G", "I", "I"],
                5: ["R", "G", "G", "I", "I"],
                6: ["R", "G", "G", "I", "I", "I"],
                7: ["R", "R", "G", "G", "I", "I", "I"],
                8: ["rH", "R", "G", "G", "G", "I", "I", "I"]
            },
            "Orange": {
                3: ["R", "G", "I"],
                4: ["R", "G", "I", "I"],
                5: ["R", "G", "G", "I", "I"],
                6: ["rH", "G", "G", "I", "I", "I"],
                7: ["rH", "R", "G", "G", "I", "I", "I"],
                8: ["rH", "R", "G", "G", "G", "I", "I", "I"]
            },
            "Yellow": {
                2: ["R", "G"],
                3: ["rH", "G", "I"],
                4: ["rH", "G", "I", "I"],
                5: ["rH", "G", "G", "I", "I"],
                6: ["rH", "R", "G", "G", "I", "I"],
                7: ["rH", "R", "G", "G", "G", "I", "I"],
                8: ["rH", "R", "G", "G", "G", "I", "I", "I"]
            },
            "White": {
                2: ["R", "G"],
                3: ["R", "G", "I"],
                4: ["rH", "G", "I", "I"],
                5: ["rH", "G", "G", "I", "I"],
                6: ["rH", "R", "G", "G", "I", "I"],
                7: ["rH", "R", "G", "G", "G", "I", "I"],
                8: ["rH", "R", "G", "G", "G", "I", "I", "I"]
            },
            "Blue": {
                3: ["R", "G", "I"],
                4: ["R", "G", "I", "I"],
                5: ["R", "G", "G", "I", "I"],
                6: ["rH", "G", "G", "I", "I", "I"],
                7: ["R", "R", "G", "G", "I", "I", "I"],
                8: ["R", "R", "R", "G", "G", "G", "I", "I"],
                9: ["R", "R", "rH", "rH", "G", "G", "G", "G", "I"]
            }
        }
        
        if star_type in planet_configs and num_planets in planet_configs[star_type]:
            planets = planet_configs[star_type][num_planets].copy()
            
            # Handle rH planets
            for i, planet in enumerate(planets):
                if planet == "rH":
                    # Roll 1-5 for habitable
                    if self.roll_d10() <= 5:
                        planets[i] = "H"
                    else:
                        planets[i] = "R"
                        
            # Handle G planet gravity effects
            for i in range(len(planets)-1, -1, -1):
                if planets[i] == "G":
                    if self.roll_d10() <= 2:  # 1-2 destroys next inner planet
                        if i > 0:  # Only if there's an inner planet
                            planets[i-1] = "A"  # Asteroids
                            
            return planets
        
        return []

    def determine_moons(self):
        """Roll for number of moons (1-10 where 0 = 10)"""
        roll = self.roll_d10()
        if roll == 1:
            return 0
        elif roll <= 3:
            return 1
        elif roll <= 6:
            return 2
        elif roll <= 8:
            return 3
        else:
            return 4

    def determine_asteroid_sites(self):
        """Determine number of special sites in asteroid belt (max 5)"""
        return min(5, self.roll_d10() // 2)  # 1-5 based on d10/2 rounded down

    def determine_planet_ep(self, planet_type):
        """Calculate Economic Points for a planet"""
        if planet_type == "H":
            return 40
        elif planet_type == "R":
            return 10
        elif planet_type == "G":
            moons = self.determine_moons()
            return 4 * moons, moons  # Return both EP and number of moons
        elif planet_type == "I":
            return 4
        elif planet_type == "A":
            sites = self.determine_asteroid_sites()
            return min(10, 2 * sites), sites  # Return both EP and number of sites
        return 0

    def generate_galaxy(self):
        # Generate systems
        for i in range(self.num_systems):
            system_type = self.determine_system_type()
            
            # Handle star type(s)
            if system_type == "Starless Nexus":
                star_types = [None]
            elif system_type == "Binary Star":
                star_types = [self.determine_star_type(), self.determine_star_type()]
            else:
                star_types = [self.determine_star_type()]
            
            num_warp_points = self.determine_warp_points(system_type, star_types[0])  # Use primary star for warp points
            
            planets = []
            planet_ep = []
            planet_moons = []  # New list for moon counts
            planet_sites = []  # New list for asteroid sites
            
            if system_type != "Starless Nexus":
                if system_type == "Binary Star":
                    # Handle planets for each star
                    for star_type in star_types:
                        num_planets = self.determine_num_planets(star_type)
                        num_planets = max(1, num_planets // 4)  # Binary star rule
                        planets.extend(self.determine_planet_types(star_type, num_planets))
                    planets.append("A")  # Add asteroid belt for binary system
                else:
                    num_planets = self.determine_num_planets(star_types[0])
                    planets.extend(self.determine_planet_types(star_types[0], num_planets))
                    
                for planet in planets:
                    if planet == "G":
                        ep, moons = self.determine_planet_ep(planet)
                        planet_ep.append(ep)
                        planet_moons.append(moons)
                        planet_sites.append(0)
                    elif planet == "A":
                        ep, sites = self.determine_planet_ep(planet)
                        planet_ep.append(ep)
                        planet_moons.append(0)
                        planet_sites.append(sites)
                    else:
                        planet_ep.append(self.determine_planet_ep(planet))
                        planet_moons.append(0)
                        planet_sites.append(0)
            
            self.systems[i] = {
                "id": i,
                "system_type": system_type,
                "star_types": star_types,
                "num_warp_points": num_warp_points,
                "connected_systems": set(),
                "planets": planets,
                "planet_ep": planet_ep,
                "planet_moons": planet_moons,
                "planet_sites": planet_sites,
                "total_ep": sum(planet_ep)  # Calculate total EP when creating system
            }
            
            self.graph.add_node(i)
            
            # Store system creation in history
            self.history.append({
                "type": "add_system",
                "system": self.systems[i].copy(),
                "connections": []
            })
            
            # Connect warp points
            available_targets = [
                t for t in range(i) 
                if len(self.systems[t]["connected_systems"]) < self.systems[t]["num_warp_points"]
            ]
            
            connections_made = []
            while (len(self.systems[i]["connected_systems"]) < num_warp_points and 
                   available_targets):
                target = random.choice(available_targets)
                self.systems[i]["connected_systems"].add(target)
                self.systems[target]["connected_systems"].add(i)
                self.graph.add_edge(i, target)
                connections_made.append(target)
                available_targets.remove(target)
            
            if connections_made:
                self.history[-1]["connections"] = connections_made

            self.log_system_generation(i)

        self.ensure_connectivity()

    def ensure_connectivity(self):
        """Ensure all nodes are connected to at least one other node"""
        # First check for completely isolated nodes
        for sys_id, system in self.systems.items():
            if len(system["connected_systems"]) == 0:
                # Find a random target that isn't full
                available_targets = [
                    t for t in self.systems.keys() 
                    if t != sys_id and 
                    len(self.systems[t]["connected_systems"]) < self.systems[t]["num_warp_points"]
                ]
                
                if available_targets:
                    target = random.choice(available_targets)
                    # Add bidirectional connection
                    system["connected_systems"].add(target)
                    self.systems[target]["connected_systems"].add(sys_id)
                    self.graph.add_edge(sys_id, target)
                else:
                    # If no available targets, create connection to random system
                    target = random.choice([t for t in self.systems.keys() if t != sys_id])
                    system["connected_systems"].add(target)
                    self.systems[target]["connected_systems"].add(sys_id)
                    self.graph.add_edge(sys_id, target)
        
        # Then check for isolated components
        components = list(nx.connected_components(self.graph))
        while len(components) > 1:
            # Connect each isolated component to the largest component
            main_component = max(components, key=len)
            for component in components:
                if component != main_component:
                    # Pick random nodes from each component
                    node1 = random.choice(list(component))
                    node2 = random.choice(list(main_component))
                    
                    # Add bidirectional connection
                    self.systems[node1]["connected_systems"].add(node2)
                    self.systems[node2]["connected_systems"].add(node1)
                    self.graph.add_edge(node1, node2)
            
            # Recalculate components
            components = list(nx.connected_components(self.graph))

        # Final verification - ensure minimum connections
        MIN_CONNECTIONS = 1
        for sys_id, system in self.systems.items():
            while len(system["connected_systems"]) < MIN_CONNECTIONS:
                available_targets = [
                    t for t in self.systems.keys() 
                    if t != sys_id and 
                    sys_id not in self.systems[t]["connected_systems"]
                ]
                if available_targets:
                    target = random.choice(available_targets)
                    system["connected_systems"].add(target)
                    self.systems[target]["connected_systems"].add(sys_id)
                    self.graph.add_edge(sys_id, target)

    def get_node_colors(self):
        colors = []
        for i in range(self.num_systems):
            if self.systems[i]["system_type"] == "Starless Nexus":
                colors.append('grey')
            elif self.systems[i]["system_type"] == "Binary Star":
                colors.append('white')
            else:
                colors.append(self.systems[i]["star_types"][0].lower())
        return colors

    def get_node_shapes(self):
        shapes = []
        for i in range(self.num_systems):
            if self.systems[i]["system_type"] == "Single Star":
                shapes.append('o')  # Circle
            elif self.systems[i]["system_type"] == "Binary Star":
                shapes.append('s')  # Square
            else:  # Starless Nexus
                shapes.append('^')  # Triangle
        return shapes

    def get_legend_elements(self):
        """Returns legend elements for both system types and star types"""
        system_elements = [
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='gray', 
                      markersize=10, label='Single Star', linestyle=''),
            plt.Line2D([0], [0], marker='s', color='w', markerfacecolor='gray', 
                      markersize=10, label='Binary Star', linestyle=''),
            plt.Line2D([0], [0], marker='^', color='w', markerfacecolor='gray', 
                      markersize=10, label='Starless Nexus', linestyle='')
        ]
        
        star_elements = [
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='red', 
                      markersize=10, label='Red Star', linestyle=''),
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='orange', 
                      markersize=10, label='Orange Star', linestyle=''),
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='yellow', 
                      markersize=10, label='Yellow Star', linestyle=''),
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='white', 
                      markersize=10, label='White Star', linestyle=''),
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='blue', 
                      markersize=10, label='Blue Star', linestyle='')
        ]
        
        return system_elements, star_elements

    def visualize_system(self, system_id):
        system = self.systems[system_id]
        
        # Create figure with more space
        fig = plt.figure(figsize=(20, 10), facecolor='black')
        plt.subplots_adjust(right=0.85, left=0.1)
        
        ax = fig.add_subplot(111)
        ax.set_facecolor('black')
        
        # Set up the plot with more space
        ax.set_xlim(-2, 15)  # Extend x-axis for more planets
        ax.set_ylim(-3, 3)   # More vertical space
        ax.grid(False)
        ax.set_xticks([])
        ax.set_yticks([])
        
        # Draw the star(s)
        if system['system_type'] == 'Starless Nexus':
            ax.scatter([0], [0], c='black', s=3000, alpha=0.8)
        elif system['system_type'] == 'Binary Star':
            ax.scatter([-0.5], [0], c=system['star_types'][0].lower(), s=3000, alpha=0.8)
            ax.scatter([0.5], [0], c=system['star_types'][1].lower(), s=3000, alpha=0.8)
        else:
            ax.scatter([0], [0], c=system['star_types'][0].lower(), s=3000, alpha=0.8)
        
        # Only draw planets if not a Starless Nexus
        if system['system_type'] != 'Starless Nexus':
            # Draw planets in a line
            for i, (planet, ep, moons, sites) in enumerate(zip(
                system['planets'], 
                system['planet_ep'],
                system['planet_moons'],
                system['planet_sites']
            )):
                x_pos = 2.0 + (i * 1.5)  # More space between planets
                
                # Set planet color and size based on type
                if planet == 'H':
                    color = 'lightgreen'
                    size = 1000
                elif planet == 'R':
                    color = 'brown'
                    size = 600
                elif planet == 'G':
                    color = 'purple'
                    size = 1400
                elif planet == 'I':
                    color = 'lightblue'
                    size = 800
                else:  # Asteroids
                    color = 'gray'
                    size = 400
                    # Draw asteroid belt as a cluster with deterministic positioning
                    for j in range(20):
                        y_offset = (self.roll_d10() / 10) * 0.6 - 0.3  # Maps 1-10 to -0.3 to 0.3
                        x_offset = (self.roll_d10() / 10) * 0.6 - 0.3  # Maps 1-10 to -0.3 to 0.3
                        ax.scatter(x_pos + x_offset, y_offset, c=color, s=size/10, alpha=0.5)
                    continue
                
                ax.scatter(x_pos, 0, c=color, s=size, alpha=0.8)
                ax.text(x_pos, 1.0, f'{planet}\nEP:{ep}', 
                        color='white', ha='center', va='bottom', fontsize=12)
                
                # Add moon visualization
                if moons > 0:
                    moon_positions = np.linspace(-0.4, 0.4, moons)
                    for moon_y in moon_positions:
                        ax.scatter(x_pos, moon_y, c='lightgray', s=100, alpha=0.8)
                    ax.text(x_pos, -1.0, f'Moons: {moons}', 
                           color='white', ha='center', va='top', fontsize=10)
                
                # Add asteroid site visualization
                if sites > 0:
                    ax.text(x_pos, -1.2, f'Sites: {sites}', 
                           color='white', ha='center', va='top', fontsize=10)
        
        # Add legend elements
        legend_elements = [
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='lightgreen',
                      markersize=10, label='Habitable (H)', linestyle=''),
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='brown',
                      markersize=10, label='Rocky (R)', linestyle=''),
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='purple',
                      markersize=10, label='Gas Giant (G)', linestyle=''),
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='lightblue',
                      markersize=10, label='Ice Giant (I)', linestyle=''),
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='gray',
                      markersize=10, label='Asteroids (A)', linestyle='')
        ]
        
        # Add legend with better positioning
        leg = ax.legend(handles=legend_elements, loc='center left',
                       bbox_to_anchor=(1.1, 0.5), frameon=False)
        plt.setp(leg.get_texts(), color='white')
        
        plt.title(f"System {system_id:03d}\n{system['system_type']}" + 
                  (f" - {system['star_types'][0] if system['star_types'][0] else 'Starless Nexus'}" if system['system_type'] != 'Starless Nexus' else ''),
                  color='white', pad=20)
        
        return fig

    def animate_galaxy(self, save_to_file=None, interval=200):
        """Animated visualization showing system generation process"""
        # Create figure with more space for legends
        fig = plt.figure(figsize=(15, 10), facecolor='black')
        plt.subplots_adjust(right=0.85, left=0.15)  # Adjust subplot parameters
        
        ax = fig.add_subplot(111)
        ax.set_facecolor('black')
        
        pos = nx.spring_layout(self.graph, k=1, iterations=50)
        
        def init():
            ax.clear()
            ax.set_facecolor('black')
            return []
        
        def update(frame):
            ax.clear()
            ax.set_facecolor('black')
            
            # Add legends with better positioning
            system_elements, star_elements = self.get_legend_elements()
            leg1 = ax.legend(handles=system_elements, loc='center left', 
                            bbox_to_anchor=(-0.2, 0.5),
                            title='System Types', frameon=False)
            leg2 = ax.legend(handles=star_elements, loc='center left',
                            bbox_to_anchor=(1.0, 0.5),
                            title='Star Types', frameon=False)
            ax.add_artist(leg1)
            
            # Make legend text white
            for leg in [leg1, leg2]:
                plt.setp(leg.get_texts(), color='white')
                plt.setp(leg.get_title(), color='white')
            
            # Draw systems up to current frame
            current_systems = {}
            edges = set()
            
            for i in range(min(frame + 1, len(self.history))):
                event = self.history[i]
                system = event["system"]
                current_systems[system["id"]] = system
                
                for target in event["connections"]:
                    edges.add((system["id"], target))
            
            # Draw edges
            edge_list = list(edges)
            if edge_list:
                nx.draw_networkx_edges(self.graph, pos, 
                                     edgelist=edge_list,
                                     edge_color='gray', 
                                     alpha=0.3)
            
            # Draw nodes
            for system_id, system in current_systems.items():
                color = self.get_node_colors()[system_id]
                shape = self.get_node_shapes()[system_id]
                nx.draw_networkx_nodes(self.graph, pos,
                                     nodelist=[system_id],
                                     node_color=[color],
                                     node_shape=shape,
                                     node_size=100)
            
            plt.title(f"Space Farce Galaxy Map - System {frame + 1}/{self.num_systems}", 
                     color='white', pad=20)
            return ax
        
        ani = animation.FuncAnimation(fig, update, frames=len(self.history),
                                    init_func=init, interval=interval, blit=False)
        
        if save_to_file:
            ani.save(save_to_file, writer='pillow')
        else:
            plt.show()

    def visualize_galaxy(self, save_to_file=None):
        fig = plt.figure(figsize=(12, 8), facecolor='black')
        ax = fig.add_subplot(111)
        ax.set_facecolor('black')
        
        # Add iterations and weight parameters to make layout faster
        pos = nx.spring_layout(self.graph, k=1, iterations=50)
        colors = self.get_node_colors()
        shapes = self.get_node_shapes()
        
        # Draw edges (warp points)
        nx.draw_networkx_edges(self.graph, pos, edge_color='gray', alpha=0.3)
        
        # Draw nodes (systems)
        for shape in set(shapes):
            node_list = [node for node in self.graph.nodes() if shapes[node] == shape]
            nx.draw_networkx_nodes(self.graph, pos, 
                                 nodelist=node_list,
                                 node_color=[colors[node] for node in node_list],
                                 node_shape=shape,
                                 node_size=[self.get_node_sizes()[node] for node in node_list])
        
        plt.title("Space Farce Galaxy Map", color='white')
        
        if save_to_file:
            plt.savefig(save_to_file)
        else:
            plt.show()

    def log_system_generation(self, system_id, log_file="Python/output-tests/generation_log.txt"):
        """Log system generation details to file"""
        system = self.systems[system_id]
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        
        with open(log_file, 'a') as f:
            f.write(f"\nSystem {system_id:03d}\n")
            f.write(f"Type: {system['system_type']}\n")
            if system['system_type'] == "Binary Star":
                f.write(f"Stars: {system['star_types'][0]} and {system['star_types'][1]}\n")
            else:
                f.write(f"Star: {system['star_types'][0] if system['star_types'][0] else 'Starless Nexus'}\n")
            f.write(f"Warp Points: {system['num_warp_points']}\n")
            f.write(f"Planets: {len(system['planets'])}\n")
            f.write(f"Total EP: {system['total_ep']}\n")
            for i, (planet, ep, moons, sites) in enumerate(zip(
                system['planets'], 
                system['planet_ep'],
                system['planet_moons'],
                system['planet_sites']
            )):
                details = []
                if moons > 0:
                    details.append(f"{moons} moons")
                if sites > 0:
                    details.append(f"{sites} sites")
                detail_str = f" ({', '.join(details)})" if details else ""
                f.write(f"  Planet {i+1}: {planet} (EP: {ep}){detail_str}\n")
            f.write("Connected Systems: " + 
                    ", ".join(str(x) for x in system['connected_systems']) + "\n")
            f.write("-" * 40 + "\n")

    def calculate_system_ep(self):
        """Calculate total EP for the system"""
        total_ep = 0
        for i in range(self.num_systems):
            system = self.systems[i]
            system_ep = sum(system['planet_ep'])
            self.systems[i]['total_ep'] = system_ep

    def get_node_sizes(self):
        """Returns list of node sizes based on system EP"""
        sizes = []
        max_ep = max(system['total_ep'] for system in self.systems.values())
        min_size = 100
        max_size = 500
        
        for i in range(self.num_systems):
            if self.systems[i]['system_type'] == "Starless Nexus":
                sizes.append(min_size)
            else:
                # Scale size between min_size and max_size based on EP
                ep = self.systems[i]['total_ep']
                if max_ep > 0:
                    size = min_size + (max_size - min_size) * (ep / max_ep)
                else:
                    size = min_size
                sizes.append(size)
        return sizes

    def export_to_json(self):
        """Export galaxy data in a JSON-compatible format"""
        galaxy_data = {
            "metadata": {
                "num_systems": self.num_systems,
                "seed": self.seed,
                "version": "1.0.0"
            },
            "systems": {},
            "connections": []
        }
        
        # Export systems
        for sys_id, system in self.systems.items():
            galaxy_data["systems"][str(sys_id)] = {
                "id": system["id"],
                "system_type": system["system_type"],
                "stars": [
                    {
                        "type": star_type
                    } for star_type in system["star_types"] if star_type is not None
                ],
                "warp_points": {
                    "count": system["num_warp_points"],
                    "connections": list(system["connected_systems"])
                },
                "planets": [
                    {
                        "type": planet,
                        "position": idx,
                        "economic_points": ep,
                        "features": {
                            "moons": moon_count,
                            "asteroid_sites": site_count
                        },
                        # Extensible sections for future features
                        "structures": [],
                        "fleets": [],
                        "colonies": []
                    }
                    for idx, (planet, ep, moon_count, site_count) in enumerate(
                        zip(system["planets"], 
                            system["planet_ep"],
                            system["planet_moons"],
                            system["planet_sites"])
                    )
                ],
                "total_ep": system["total_ep"]
            }
        
        # Export connections as separate array for easier graph reconstruction
        for sys_id, system in self.systems.items():
            for connection in system["connected_systems"]:
                if int(sys_id) < connection:  # Only add each connection once
                    galaxy_data["connections"].append([int(sys_id), connection])
        
        return galaxy_data

    def save_to_json(self, filename="galaxy_data.json"):
        """Save galaxy data to JSON file"""
        with open(filename, 'w') as f:
            json.dump(self.export_to_json(), f, indent=2)

if __name__ == "__main__":
    # Create a galaxy with 100 systems
    galaxy = Galaxy(num_systems=100, seed=42)
    
    # Visualize the galaxy
    # galaxy.animate_galaxy()


