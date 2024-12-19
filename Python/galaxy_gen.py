import random
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation

class Galaxy:
    STAR_TYPES = {
        "Red": (1, 2),
        "Orange": (3, 4),
        "Yellow": (5, 6),
        "White": (7, 8),
        "Blue": (9, 0)
    }

    SYSTEM_TYPES = {
        "Single Star": (1, 7),
        "Binary Star": (8, 9),
        "Starless Nexus": (0, 0)
    }

    def __init__(self, num_systems=100, seed=None):
        if seed:
            random.seed(seed)
        
        self.num_systems = num_systems
        self.systems = {}
        self.graph = nx.Graph()
        self.generate_galaxy()

    def roll_d10(self):
        return random.randint(0, 9)

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

    def generate_galaxy(self):
        # Generate systems
        for i in range(self.num_systems):
            system_type = self.determine_system_type()
            star_type = self.determine_star_type() if system_type != "Starless Nexus" else None
            num_warp_points = self.determine_warp_points(system_type, star_type)
            
            self.systems[i] = {
                "id": i,
                "system_type": system_type,
                "star_type": star_type,
                "num_warp_points": num_warp_points,
                "connected_systems": set()
            }
            
            self.graph.add_node(i)

        # Generate warp point connections
        for system_id, system in self.systems.items():
            while len(system["connected_systems"]) < system["num_warp_points"]:
                target = random.randint(0, self.num_systems - 1)
                if (target != system_id and 
                    target not in system["connected_systems"] and
                    len(self.systems[target]["connected_systems"]) < self.systems[target]["num_warp_points"]):
                    system["connected_systems"].add(target)
                    self.systems[target]["connected_systems"].add(system_id)
                    self.graph.add_edge(system_id, target)

    def get_node_colors(self):
        colors = []
        for i in range(self.num_systems):
            if self.systems[i]["system_type"] == "Starless Nexus":
                colors.append('black')
            elif self.systems[i]["star_type"] == "Red":
                colors.append('red')
            elif self.systems[i]["star_type"] == "Orange":
                colors.append('orange')
            elif self.systems[i]["star_type"] == "Yellow":
                colors.append('yellow')
            elif self.systems[i]["star_type"] == "White":
                colors.append('white')
            else:  # Blue
                colors.append('blue')
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

    def animate_galaxy(self, save_to_file=None):
        fig = plt.figure(figsize=(12, 8), facecolor='black')
        ax = fig.add_subplot(111)
        ax.set_facecolor('black')
        
        pos = nx.spring_layout(self.graph)
        colors = self.get_node_colors()
        shapes = self.get_node_shapes()

        def update(frame):
            ax.clear()
            ax.set_facecolor('black')
            
            # Draw edges (warp points)
            nx.draw_networkx_edges(self.graph, pos, edge_color='gray', alpha=0.3)
            
            # Draw nodes (systems)
            for shape in set(shapes):
                node_list = [node for node in self.graph.nodes() if shapes[node] == shape]
                nx.draw_networkx_nodes(self.graph, pos, 
                                     nodelist=node_list,
                                     node_color=[colors[node] for node in node_list],
                                     node_shape=shape,
                                     node_size=100)
            
            plt.title("Space Farce Galaxy Map", color='white')
            return ax

        ani = animation.FuncAnimation(fig, update, frames=60, interval=50)
        
        if save_to_file:
            ani.save(save_to_file, writer='pillow')
        else:
            plt.show()

if __name__ == "__main__":
    # Create a galaxy with 100 systems
    galaxy = Galaxy(num_systems=100, seed=42)
    
    # Visualize the galaxy
    galaxy.animate_galaxy()


