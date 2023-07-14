import sys

# Reads from a file.

def generate_constraint(strn):
    strn = strn.strip()
    nums = strn.split(',', 3)
    i = nums[0]
    j = nums[1]
    color = nums[2]
    return f"c({color}, [{i}|{j}])"

def generate_constraints():
    constraints = list(map(generate_constraint, lines))
    arg = ",".join(constraints)
    print(arg)

def main():
    if len(sys.argv) < 2:
        sys.exit("Pass in a file name.")
    else:
        filename = sys.argv[1]
        with open(filename) as f:
            lines = f.readlines()

if __name__ == '__main__':
    main()
