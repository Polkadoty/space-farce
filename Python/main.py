from galaxy_gen import Galaxy
import os

def main():
    # Create output directory if it doesn't exist
    output_dir = "output-tests"
    os.makedirs(output_dir, exist_ok=True)
    
    # Create galaxies
    galaxy = Galaxy()
    custom_galaxy = Galaxy(num_systems=150, seed=123)
    
    # Save static visualizations (fast)
    galaxy.visualize_galaxy(save_to_file=f"{output_dir}/default_galaxy_static.png")
    custom_galaxy.visualize_galaxy(save_to_file=f"{output_dir}/custom_galaxy_static.png")
    
    # # Optionally, save animations (slower)
    # galaxy.animate_galaxy(
    #     save_to_file=f"{output_dir}/default_galaxy_animated.gif",
    #     frames=30,  # Reduced number of frames
    #     interval=100  # Increased interval between frames
    # )
    # custom_galaxy.animate_galaxy(
    #     save_to_file=f"{output_dir}/custom_galaxy_animated.gif",
    #     frames=30,
    #     interval=100
    # )

if __name__ == "__main__":
    main()