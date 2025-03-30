import numpy as np
import matplotlib.pyplot as plt

def calculate_hydraulic_jump(y1, v1):
    """
    Calculate the properties of a hydraulic jump in an open channel.
    
    Parameters:
    y1 (float): Initial flow depth in meters
    v1 (float): Initial flow velocity in meters per second
    
    Returns:
    tuple: Containing Froude number (Fr1), sequent depth (y2), and energy loss (ΔE)
    """
    # Constants
    g = 9.81  # Acceleration due to gravity (m/s²)
    
    # Calculate Froude number before the jump
    Fr1 = v1 / np.sqrt(g * y1)
    
    # Calculate sequent depth after the jump
    y2 = y1 / 2 * (np.sqrt(1 + 8 * Fr1**2) - 1)
    
    # Calculate energy loss
    delta_E = ((y2 - y1)**3) / (4 * y1 * y2)
    
    return Fr1, y2, delta_E

def visualize_hydraulic_jump(y1, y2):
    """
    Create a simple visualization of the hydraulic jump showing the water surface profile.
    
    Parameters:
    y1 (float): Initial flow depth in meters
    y2 (float): Sequent depth in meters
    """
    # Create distance array (10 meters total length)
    x = np.linspace(0, 10, 100)
    
    # Create water surface profile
    # Initial depth from x=0 to x=5
    # Transition at x=5
    # Sequent depth from x=5 to x=10
    y = np.ones_like(x)
    for i, xi in enumerate(x):
        if xi < 5:
            y[i] = y1
        elif xi > 5.5:
            y[i] = y2
        else:
            # Smooth transition (not physically accurate, but visually helpful)
            y[i] = y1 + (y2 - y1) * (xi - 5) / 0.5
    
    # Create plot
    plt.figure(figsize=(10, 6))
    
    # Plot channel bottom
    plt.plot(x, np.zeros_like(x), 'k-', linewidth=2, label='Channel Bottom')
    
    # Plot water surface
    plt.plot(x, y, 'b-', linewidth=3, label='Water Surface')
    
    # Fill water area
    plt.fill_between(x, np.zeros_like(x), y, color='skyblue', alpha=0.4)
    
    # Add labels and annotations
    plt.annotate(f'y₁ = {y1:.2f} m', xy=(2.5, y1/2), ha='center', va='center',
                 bbox=dict(boxstyle='round', fc='white', alpha=0.7))
    plt.annotate(f'y₂ = {y2:.2f} m', xy=(7.5, y2/2), ha='center', va='center',
                 bbox=dict(boxstyle='round', fc='white', alpha=0.7))
    
    # Add flow direction arrow
    plt.arrow(1, y1 + 0.2, 1, 0, head_width=0.1, head_length=0.2, fc='black', ec='black')
    plt.text(1.5, y1 + 0.3, 'Flow Direction', ha='center')
    
    # Add hydraulic jump label
    plt.annotate('Hydraulic Jump', xy=(5, max(y1, y2) + 0.2), ha='center',
                xytext=(5, max(y1, y2) + 0.5), 
                arrowprops=dict(arrowstyle='->'))
    
    # Set labels and title
    plt.xlabel('Distance (m)')
    plt.ylabel('Water Depth (m)')
    plt.title('Hydraulic Jump in an Open Channel')
    plt.grid(True)
    plt.legend()
    
    # Set axis limits
    plt.ylim(0, max(y2 * 1.5, y1 * 1.5))
    
    plt.tight_layout()
    plt.show()

def main():
    """Main function to run the hydraulic jump calculator."""
    print("\n====== HYDRAULIC JUMP CALCULATOR ======\n")
    
    # Get user inputs
    try:
        y1 = float(input("Enter initial flow depth (y₁) in meters: "))
        v1 = float(input("Enter initial flow velocity (v₁) in meters per second: "))
        
        # Validate inputs
        if y1 <= 0 or v1 <= 0:
            print("Error: Depth and velocity must be positive values.")
            return
            
        # Calculate hydraulic jump properties
        Fr1, y2, delta_E = calculate_hydraulic_jump(y1, v1)
        
        # Print results
        print("\n------ RESULTS ------")
        print(f"Froude Number (Fr₁): {Fr1:.2f}")
        
        # Check jump type based on Froude number
        if Fr1 < 1:
            print("   -> Subcritical flow: No hydraulic jump will form.")
        elif Fr1 < 1.7:
            print("   -> Undular jump: Weak oscillating waves will form.")
        elif Fr1 < 2.5:
            print("   -> Weak jump: Low energy dissipation.")
        elif Fr1 < 4.5:
            print("   -> Oscillating jump: Periodic surges may occur.")
        elif Fr1 < 9.0:
            print("   -> Steady jump: Stable and efficient energy dissipation.")
        else:
            print("   -> Strong jump: Highly turbulent with significant energy dissipation.")
            
        print(f"Sequent Depth (y₂): {y2:.2f} meters")
        print(f"Depth Ratio (y₂/y₁): {y2/y1:.2f}")
        print(f"Energy Loss (ΔE): {delta_E:.2f} meters")
        print(f"Energy Loss (%): {(delta_E / (y1 + v1**2/(2*9.81))) * 100:.1f}% of initial energy")
        
        # Create visualization
        visualize_hydraulic_jump(y1, y2)
        
    except ValueError:
        print("Error: Please enter valid numerical values.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
