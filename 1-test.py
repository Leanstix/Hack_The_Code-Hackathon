def read_input_file(filename):
    with open(filename, "r", encoding="ascii") as f:
        lines = f.read().strip().split("\n")
    
    # Read initial game parameters
    D, R, T = map(int, lines[0].split())
    
    # Read resources
    resources = []
    for i in range(1, R + 1):
        parts = lines[i].split()
        RI, RA, RP, RW, RM, RL, RU = map(int, parts[:7])
        RT = parts[7]
        RE = int(parts[8]) if len(parts) > 8 else None
        resources.append({
            "RI": RI, "RA": RA, "RP": RP, "RW": RW,
            "RM": RM, "RL": RL, "RU": RU, "RT": RT, "RE": RE
        })
    
    # Read turns
    turns = []
    for i in range(R + 1, R + 1 + T):
        TM, TX, TR = map(int, lines[i].split())
        turns.append({"TM": TM, "TX": TX, "TR": TR})
    
    return D, resources, turns

def simulate_biogas_generator(input_file, output_file="biogas_simulation_output.txt"):
    # Read input parameters
    budget, resources, turns = read_input_file(input_file)
    
    # Extract biogas generator parameters (assuming only 1 biogas generator exists)
    biogas = next(r for r in resources if r["RT"] == "D")
    RA, RP, RW, RM, RL, RU, RE = biogas["RA"], biogas["RP"], biogas["RW"], biogas["RM"], biogas["RL"], biogas["RU"], biogas["RE"]
    RT_bonus = 1 + (RE / 100)  # Renewable Plant effect as percentage
    
    active_turns = 0
    downtime_turns = 0
    resource_active = False
    output_lines = []
    
    for turn_index, turn in enumerate(turns, 1):
        TM, TX, TR = turn["TM"], turn["TX"], turn["TR"]
        
        if not resource_active and budget >= RA:
            budget -= RA
            resource_active = True
            active_turns = RW
            output_lines.append(f"Turn {turn_index}: Biogas Generator Activated. Budget: ${budget}")
        
        if resource_active:
            buildings_powered = min(TX, RU)
            if buildings_powered < TM:
                profit = 0
            else:
                profit = int(buildings_powered * TR * RT_bonus)
            
            budget += profit - RP
            output_lines.append(f"Turn {turn_index}: Powered {buildings_powered} buildings. Profit: ${profit}. Budget: ${budget}")
            
            active_turns -= 1
            if active_turns == 0:
                resource_active = False
                downtime_turns = RM
                output_lines.append(f"Turn {turn_index}: Biogas Generator requires maintenance.")
        
        elif downtime_turns > 0:
            downtime_turns -= 1
            if downtime_turns == 0:
                resource_active = True
                active_turns = RW
                output_lines.append(f"Turn {turn_index}: Biogas Generator is operational again.")
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(output_lines))
    
    return output_lines

# Example usage
# simulate_biogas_generator("input.txt")
