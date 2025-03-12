import sys
import os

def parse_input(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Read initial values
    D, R, T = map(int, lines[0].split())
    
    # Read resources
    resources = []
    for i in range(1, R + 1):
        parts = lines[i].split()
        resources.append({
            "RI": int(parts[0]),
            "RA": int(parts[1]),
            "RP": int(parts[2]),
            "RW": int(parts[3]),
            "RM": int(parts[4]),
            "RL": int(parts[5]),
            "RU": int(parts[6]),
            "RT": parts[7],
            "RE": int(parts[8]) if len(parts) > 8 else 0
        })
    
    # Read turns
    turns = []
    for i in range(R + 1, R + 1 + T):
        TM, TX, TR = map(int, lines[i].split())
        turns.append({"TM": TM, "TX": TX, "TR": TR})
    
    return D, resources, turns


def generate_output(D, resources, turns):
    budget = D
    active_resources = []
    output_lines = []
    
    for t, turn in enumerate(turns):
        TM, TX, TR = turn["TM"], turn["TX"], turn["TR"]
        
        # Strategy: Pick cheapest resource that meets needs
        best_resource = None
        for res in resources:
            if res["RA"] <= budget:
                best_resource = res
                break
        
        if best_resource:
            budget -= best_resource["RA"]
            active_resources.append(best_resource)
            output_lines.append(f"{t} 1 {best_resource['RI']}")
        
        # Compute powered buildings and profit
        n = sum(r["RU"] for r in active_resources)
        if n >= TM:
            profit = min(n, TX) * TR
        else:
            profit = 0
        
        # Deduct periodic costs
        total_maintenance = sum(r["RP"] for r in active_resources)
        budget += profit - total_maintenance
    
    return output_lines


def main():
    if len(sys.argv) < 2:
        print("Usage: python script.py <input_file>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = os.path.splitext(input_file)[0] + "1.txt"
    
    D, resources, turns = parse_input(input_file)
    output_lines = generate_output(D, resources, turns)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("\n".join(output_lines) + "\n")
    
    print(f"Output written to {output_file}")


if __name__ == "__main__":
    main()
