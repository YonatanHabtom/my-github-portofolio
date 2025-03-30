import math

def main():
    print("=== Pipe Head Loss Calculator ===")
    print("This program calculates the head loss in pipes due to friction.")
    
    # Constants
    g = 9.81  # Acceleration due to gravity (m/s²)
    
    # Ask user to choose calculation method
    print("\nPlease select the method to calculate head loss:")
    print("1. Darcy-Weisbach equation")
    print("2. Hazen-Williams equation")
    
    while True:
        try:
            method_choice = int(input("Enter your choice (1 or 2): "))
            if method_choice in [1, 2]:
                break
            else:
                print("Invalid choice. Please enter 1 or 2.")
        except ValueError:
            print("Invalid input. Please enter a number.")
    
    if method_choice == 1:
        calculate_darcy_weisbach(g)
    else:
        calculate_hazen_williams()


def calculate_darcy_weisbach(g):
    """Calculate head loss using the Darcy-Weisbach equation."""
    print("\n=== Darcy-Weisbach Method ===")
    
    # Get inputs from user
    D = float(input("Enter pipe diameter (D) in meters: "))
    L = float(input("Enter pipe length (L) in meters: "))
    Q = float(input("Enter flow rate (Q) in cubic meters per second (m³/s): "))
    nu = float(input("Enter kinematic viscosity (ν) in square meters per second (m²/s): "))
    epsilon = float(input("Enter absolute roughness (ε) of pipe material in meters: "))
    
    # Calculate velocity and Reynolds number
    A = math.pi * (D/2)**2  # Cross-sectional area of pipe
    v = Q / A  # Flow velocity (m/s)
    Re = (v * D) / nu  # Reynolds number (dimensionless)
    
    print(f"\nCalculated flow velocity: {v:.4f} m/s")
    print(f"Calculated Reynolds number: {Re:.0f}")
    
    # Determine flow regime
    if Re < 2000:
        flow_regime = "Laminar"
    elif Re <= 4000:
        flow_regime = "Transitional"
    else:
        flow_regime = "Turbulent"
    
    print(f"Flow regime: {flow_regime}")
    
    # Friction factor calculation options
    print("\nSelect method for calculating the Darcy friction factor (f):")
    print("1. Colebrook-White equation (iterative solution)")
    print("2. Swamee-Jain equation (explicit approximation for turbulent flow)")
    print("3. Simplified method based on flow regime")
    
    while True:
        try:
            friction_choice = int(input("Enter your choice (1, 2, or 3): "))
            if friction_choice in [1, 2, 3]:
                break
            else:
                print("Invalid choice. Please enter 1, 2, or 3.")
        except ValueError:
            print("Invalid input. Please enter a number.")
    
    # Calculate friction factor based on selected method
    if friction_choice == 1:
        # Colebrook-White equation (iterative solution)
        f = colebrook_white(epsilon, D, Re)
        method_name = "Colebrook-White equation"
    elif friction_choice == 2:
        # Swamee-Jain equation
        f = swamee_jain(epsilon, D, Re)
        method_name = "Swamee-Jain equation"
    else:
        # Simplified method based on flow regime
        f = simplified_friction_factor(Re, epsilon, D)
        method_name = "Simplified method"
    
    print(f"\nFriction factor calculated using {method_name}: {f:.6f}")
    
    # Calculate head loss using Darcy-Weisbach equation
    h_L = f * (L/D) * (v**2 / (2 * g))
    
    print(f"\nHead loss (hL) = {h_L:.4f} meters")
    print("Formula used: hL = f * (L/D) * (v² / (2*g))")


def colebrook_white(epsilon, D, Re):
    """
    Calculate the Darcy friction factor using the Colebrook-White equation
    This is an implicit equation requiring an iterative solution
    """
    # Initial guess for friction factor (fixed value of 0.002)
    f = 0.002
    
    # Iterative solution (fixed-point iteration)
    max_iterations = 50
    tolerance = 1e-6
    
    print("\nSolving Colebrook-White equation iteratively...")
    print(f"Starting with initial friction factor f = {f}")
    
    for i in range(max_iterations):
        # Colebrook-White equation: 1/sqrt(f) = -2 * log10((ε/(3.7*D)) + (2.51/(Re*sqrt(f))))
        relative_roughness = epsilon/D
        f_new = 1 / (-2 * math.log10((relative_roughness/3.71) + (2.51/(Re*math.sqrt(f)))))**2
        
        # Check convergence
        if abs(f_new - f) < tolerance:
            print(f"Converged after {i+1} iterations")
            return f_new
        
        f = f_new
        
        if i % 10 == 0:  # Print status every 10 iterations
            print(f"Iteration {i+1}, f = {f:.6f}")
    
    print(f"Maximum iterations reached. Last value: f = {f:.6f}")
    return f


def swamee_jain(epsilon, D, Re):
    """
    Calculate the Darcy friction factor using the Swamee-Jain equation
    This is an explicit approximation valid for turbulent flow (4000 < Re < 10^8) and (10^-6 < ε/D < 10^-2)
    """
    # Check if flow conditions are within the valid range for Swamee-Jain
    relative_roughness = epsilon / D
    
    if Re <= 4000 or Re >= 10**8 or relative_roughness < 10**-6 or relative_roughness > 10**-2:
        print("Warning: Flow conditions are outside the recommended range for the Swamee-Jain equation.")
        print("Results may not be accurate.")
    
    # Swamee-Jain equation: f = 0.25 / [log10((ε/3.7D) + (5.74/Re^0.9))]²
    f = 0.25 / (math.log10((relative_roughness/3.7) + (5.74/(Re**0.9))))**2
    return f


def simplified_friction_factor(Re, epsilon, D):
    """Calculate friction factor using simplified methods based on flow regime."""
    relative_roughness = epsilon / D
    
    if Re < 2000:
        # Laminar flow: f = 64/Re
        f = 64 / Re
        print("Using laminar flow equation: f = 64/Re")
    else:
        # Ask user to choose turbulent flow approach
        print("\nFor turbulent flow, choose an approach:")
        print("1. Use Blasius equation (smooth pipes): f = 0.316/Re^0.25")
        print("2. Use fixed value based on relative roughness")
        
        while True:
            try:
                turb_choice = int(input("Enter your choice (1 or 2): "))
                if turb_choice in [1, 2]:
                    break
                else:
                    print("Invalid choice. Please enter 1 or 2.")
            except ValueError:
                print("Invalid input. Please enter a number.")
        
        if turb_choice == 1:
            # Blasius equation for smooth pipes
            f = 0.316 / (Re**0.25)
            print("Using Blasius equation: f = 0.316/Re^0.25")
        else:
            # Fixed value based on relative roughness categories
            if relative_roughness < 0.0001:
                f = 0.022  # Smooth pipes
                print("Using fixed value for smooth pipes (f = 0.022)")
            elif relative_roughness < 0.001:
                f = 0.030  # Moderately rough pipes
                print("Using fixed value for moderately rough pipes (f = 0.030)")
            else:
                f = 0.038  # Rough pipes
                print("Using fixed value for rough pipes (f = 0.038)")
    
    return f


def calculate_hazen_williams():
    """Calculate head loss using the Hazen-Williams equation."""
    print("\n=== Hazen-Williams Method ===")
    
    # Get inputs from user
    D = float(input("Enter pipe diameter (D) in meters: "))
    L = float(input("Enter pipe length (L) in meters: "))
    Q = float(input("Enter flow rate (Q) in cubic meters per second (m³/s): "))
    
    # Get Hazen-Williams coefficient with suggestions
    print("\nSuggested Hazen-Williams coefficients (C) for different pipe materials:")
    print("PVC, plastic pipes: 140-150")
    print("New copper, brass, or tubing: 130-140")
    print("New steel or cast iron: 130")
    print("Concrete: 120-140")
    print("Galvanized iron: 120")
    print("Clay: 100")
    print("Old cast iron: 80-100")
    print("Old, deteriorated pipes: 40-80")
    
    C = float(input("\nEnter Hazen-Williams coefficient (C) for pipe material: "))
    
    # Calculate head loss using Hazen-Williams equation
    # hL = 10.67 * Q^1.85 * L / (C^1.85 * D^4.87)
    h_L = (10.67 * (Q**1.85) * L) / ((C**1.85) * (D**4.87))
    
    print(f"\nHead loss (hL) = {h_L:.4f} meters")
    print("Formula used: hL = 10.67 * Q^1.85 * L / (C^1.85 * D^4.87)")


if __name__ == "__main__":
    main()