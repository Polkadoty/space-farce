from galaxy_gen import Galaxy
import os
import time
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def main():
    output_dir = "Python/output-tests"
    os.makedirs(output_dir, exist_ok=True)
    
    print("Generating galaxy...")
    galaxy = Galaxy(num_systems=100, seed=42)
    
    # Save static galaxy map
    galaxy.visualize_galaxy(f"{output_dir}/galaxy_static.png")

    galaxy.save_to_json(f"{output_dir}/galaxy_data.json")
    
    # Save animated galaxy map
    # galaxy.animate_galaxy(f"{output_dir}/galaxy_animated.gif")
    
    # Generate system visualizations for first 5 systems
    for i in range(5):
        fig = galaxy.visualize_system(i)
        plt.savefig(f"{output_dir}/system_{i}.png")
        plt.close(fig)

if __name__ == "__main__":
    main()