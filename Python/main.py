from galaxy_gen import Galaxy
import os

def main():
    # Create output directory if it doesn't exist
    output_dir = "output-tests"
    os.makedirs(output_dir, exist_ok=True)
    
    # Create galaxies
    galaxy = Galaxy()
    custom_galaxy = Galaxy(num_systems=150, seed=123)
    
    # Save visualizations to files
    galaxy.animate_galaxy(save_to_file=f"{output_dir}/default_galaxy.gif")
    custom_galaxy.animate_galaxy(save_to_file=f"{output_dir}/custom_galaxy.gif")
    
    # Optionally, also display them
    galaxy.animate_galaxy()
    custom_galaxy.animate_galaxy()

if __name__ == "__main__":
    main()