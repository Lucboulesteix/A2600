import re
os.chdir('C:/Users/lucco/Desktop/emulator project')
def parse_case_statements(filename):
    cases = []
    with open(filename, 'r') as f:
        lines = f.readlines()
        in_case = False
        case = None
        for line in lines:
            if 'case' in line:
                in_case = True
                case = {'Z': None, 'X': None}
                match = re.search(r'//.*, (\d+)b (\d+)c', line)
                if match:
                    case['X'] = int(match.group(1))
                    case['Y'] = int(match.group(2))
            elif 'break;' in line:
                in_case = False
                cases.append(case)
            elif in_case:
                match = re.search(r'PC = PC \+ (\d+)', line)
                if match:
                    case['Z'] = int(match.group(1))
    return cases

def main():
    cases = parse_case_statements('cpu.cpp')
    mismatched = []
    for case in cases:
        if case['X'] != case['Z']:
            mismatched.append(case)
    if mismatched:
        print('Mismatched cases:')
        for case in mismatched:
            print(f'X: {case["X"]}, Z: {case["Z"]}')
    else:
        print('All cases match')

if __name__ == '__main__':
    main()
