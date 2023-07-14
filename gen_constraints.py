import sys

# Reads from a file.

def generate_constraint(strn):
    strn = strn.strip()
    nums = strn.split(',', 3)
    i = nums[0]
    j = nums[1]
    color = nums[2]
    return f"c({color}, [{i}|{j}])"

def generate_constraints(lines):
    constraints = list(map(generate_constraint, lines))
    arg = ",".join(constraints)
    return '"[' + arg + ']"'
    
def spec_to_constraints(spec):
    lines = spec.splitlines()
    return generate_constraints(lines)

def main():
    if len(sys.argv) < 2:
        sys.exit("Pass in a file name.")
    else:
        filename = sys.argv[1]
        with open(filename) as f:
            lines = f.readlines()
            print(generate_constraints(lines))
            

if __name__ == '__main__':
    main()
