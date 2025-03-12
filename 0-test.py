import json

def simulate_biogas_generator(turns=50, initial_budget=50000):
    # Resource Parameters
    RA = 12000  # Activation cost ($)
    RP = 800  # Periodic cost ($ per turn)
    RW = 40  # Active turns before downtime
    RM = 3  # Downtime turns
    RL = 400  # Total lifecycle turns
    RU_min, RU_max = 20, 40  # Buildings powered per turn
    TR = 3  # Profit per building ($)
    RT_bonus = 1.1  # Renewable Plant effect (+10% profit per building)
    
    # Simulation Variables
    budget = initial_budget
    active_turns = 0
    downtime_turns = 0
    total_profit = 0
    buildings_powered = 0
    resource_active = False
    
    output_lines = []
    
    for turn in range(1, turns + 1):
        if not resource_active and budget >= RA:
            budget -= RA
            resource_active = True
            active_turns = RW
            output_lines.append(f"Turn {turn}: Biogas Generator Activated. Budget: ${budget}")
        
        if resource_active:
            buildings_powered = RU_max  # Assume max efficiency
            profit = min(buildings_powered, RU_max) * TR * RT_bonus
            profit = int(profit)  # Convert to integer (rounding down)
            budget += profit - RP
            total_profit += profit
            output_lines.append(f"Turn {turn}: Powered {buildings_powered} buildings. Profit: ${profit}. Budget: ${budget}")
            
            active_turns -= 1
            if active_turns == 0:
                resource_active = False
                downtime_turns = RM
                output_lines.append(f"Turn {turn}: Biogas Generator requires maintenance.")
        
        elif downtime_turns > 0:
            downtime_turns -= 1
            if downtime_turns == 0:
                resource_active = True
                active_turns = RW
                output_lines.append(f"Turn {turn}: Biogas Generator is operational again.")
    
    # Save output to file
    with open("biogas_simulation_output.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(output_lines))
    
    return output_lines

# Run Simulation
simulate_biogas_generator()
