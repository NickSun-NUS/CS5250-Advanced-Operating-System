from simulator import SJF_scheduling, read_input, write_output, RR_scheduling
import sys

input_file = 'input.txt'

def getRRQuantum(process_list):
    bestQuantem = leastTime = float('inf')
    for i in range(1,11):
        s, t = RR_scheduling(process_list, i)
        if t < leastTime:
            leastTime = t
            bestQuantem = i
    print(bestQuantem, leastTime)

def getSJFAlpha(process_list):
    bestAlpha = leastTime = float('inf')
    for i in range(0,101):
        alpha = float(i) / 100
        s, t = SJF_scheduling(process_list, alpha)
        if t < leastTime:
            bestAlpha = alpha
            leastTime = t
    print(bestAlpha, leastTime)

def main(argv):
    input_file='input.txt'
    process_list = read_input()
    getRRQuantum(process_list)
    getSJFAlpha(process_list)

if __name__ == '__main__':
    main(sys.argv[1:])