import math

def calculate_darcy_weisbach():
    """
    Calculate head loss using the Darcy-Weisbach equation.
    This method is more accurate and applies to all fluids and flow regimes.
    """
    # Get user inputs
    print("\n--- Darcy-Weisbach Equation Inputs ---")
    
    # Pipe diameter in meters
    D = float(input("Enter pipe diameter (D) in meters: "))
    
    # Pipe length in meters
    L = float(input("Enter pipe length (L) in meters: "))
    
    # Flow rate in cubic meters per second
    Q = float(input("Enter flow rate (Q) in cubic meters per second (m³/s): "))
    
    # Kinematic viscosity in square meters per second
    nu = float(input("Enter kinematic viscosity (ν) of the fluid in m²/s: "))
    
    # Absolute roughness in meters
    epsilon = float(input("Enter absolute roughness (ε) of the pipe material in meters: "))
    
    # Gravitational acceleration (m/s²)
    g = 9.81
    
    # Calculate flow velocity (v) in m/s
    # v = Q / A, where A is the cross-sectional area of the pipe
    A = math.pi * (D/2)**2
    v = Q / A
    print(f"\nCalculated flow velocity: {v:.4f} m/s")
    
    # Calculate Reynolds number (Re)
    # Re = (v * D) / ν
    Re = (v * D) / nu
    print(f"Calculated Reynolds number: {Re:.0f}")
    
    # Determine flow regime and calculate friction factor (f)
    if Re < 2000:
        # Laminar flow: f = 64/Re
        f = 64 / Re
        print(f"Flow regime: Laminar (Re < 2000)")
    else:
        # Turbulent flow: Use Swamee-Jain equation (explicit approximation of Colebrook equation)
        # The Swamee-Jain equation is valid for 5000 < Re < 10^8 and 10^-6 < ε/D < 0.01
        print(f"Flow regime: Turbulent (Re ≥ 2000)")
        
        # Check if Re is in the transitional region
        if Re < 4000:
            print("Note: Reynolds number is in the transitional region (2000-4000). Results may be less accurate.")
        
        # Calculate relative roughness
        relative_roughness = epsilon / D
        print(f"Relative roughness (ε/D): {relative_roughness:.6f}")
        
        # Swamee-Jain equation for friction factor
        f = 0.25 / (math.log10(relative_roughness/3.7 + 5.74/(Re**0.9))**2)
    
    print(f"Calculated friction factor (f): {f:.6f}")
    
    # Calculate head loss (hL) using Darcy-Weisbach equation
    # hL = f * (L/D) * (v²/(2g))
    h_L = f * (L/D) * (v**2 / (2*g))
    
    return h_L

def calculate_hazen_williams():
    """
    Calculate head loss using the Hazen-Williams equation.
    This method is commonly used for water flow in pipes under normal conditions.
    """
    # Get user inputs
    print("\n--- Hazen-Williams Equation Inputs ---")
    
    # Pipe diameter in meters
    D = float(input("Enter pipe diameter (D) in meters: "))
    
    # Pipe length in meters
    L = float(input("Enter pipe length (L) in meters: "))
    
    # Flow rate in cubic meters per second
    Q = float(input("Enter flow rate (Q) in cubic meters per second (m³/s): "))
    
    # Hazen-Williams coefficient
    print("\nTypical Hazen-Williams C values:")
    print("- New cast iron: 130")
    print("- Steel or new ductile iron: 140")
    print("- Concrete: 120-140")
    print("- PVC/plastic: 140-150")
    print("- Old cast iron: 80-120")
    print("- Galvanized iron: 120")
    C = float(input("\nEnter Hazen-Williams coefficient (C) for the pipe material: "))
    
    # Calculate head loss using Hazen-Williams equation
    # hL = 10.67 * Q^1.85 * L / (C^1.85 * D^4.87)
    h_L = (10.67 * (Q**1.85) * L) / ((C**1.85) * (D**4.87))
    
    return h_L

def main():
    """Main function to run the pipe head loss calculator program."""
    print("=== Pipe Head Loss Calculator ===")
    print("\nThis program calculates the head loss in a pipe due to friction.")
    print("\nChoose the calculation method:")
    print("1. Darcy-Weisbach equation (accurate for all fluids and flow regimes)")
    print("2. Hazen-Williams equation (simplified, commonly used for water at normal temperatures)")
    
    # Get user choice
    while True:
        try:
            choice = int(input("\nEnter your choice (1 or 2): "))
            if choice in [1, 2]:
                break
            else:
                print("Please enter either 1 or 2.")
        except ValueError:
            print("Please enter a valid number.")
    
    # Calculate head loss based on user choice
    if choice == 1:
        head_loss = calculate_darcy_weisbach()
    else:
        head_loss = calculate_hazen_williams()
    
    # Display the result
    print(f"\n=== Result ===")
    print(f"Calculated head loss: {head_loss:.4f} meters")

if __name__ == "__main__":
    main()
