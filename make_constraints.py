import sys

def make_constraint(strn):
    strn = strn.strip()
    nums = strn.split(',', 3)
    color = nums[0]
    i = nums[1]
    j = nums[2]
    return f"c({color}, [{i}|{j}])"

def main():
    if len(sys.argv) < 2:
        sys.exit("Pass in a file name.")
    filename = sys.argv[1]
    with open(filename) as f:
        lines = f.readlines()
    constraints = list(map(make_constraint, lines))
    arg = ",".join(constraints)
    print(arg)



if __name__ == '__main__':
    main()
