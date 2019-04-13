'''
CS5250 Assignment 4, Scheduling policies simulator
Sample skeleton program
Input file:
    input.txt
Output files:
    FCFS.txt
    RR.txt
    SRTF.txt
    SJF.txt
'''
import sys

from copy import deepcopy

input_file = 'input.txt'

class Process:
    last_scheduled_time = 0
    def __init__(self, id, arrive_time, burst_time):
        self.id = id
        self.arrive_time = arrive_time
        self.burst_time = burst_time
    #for printing purpose
    def __repr__(self):
        return ('[id %d : arrival_time %d,  burst_time %d]'%(self.id, self.arrive_time, self.burst_time))

def FCFS_scheduling(process_list):
    #store the (switching time, proccess_id) pair
    schedule = []
    current_time = 0
    waiting_time = 0
    for process in process_list:
        if(current_time < process.arrive_time):
            current_time = process.arrive_time
        schedule.append((current_time,process.id))
        waiting_time = waiting_time + (current_time - process.arrive_time)
        current_time = current_time + process.burst_time
    average_waiting_time = waiting_time/float(len(process_list))
    return schedule, average_waiting_time

#Input: process_list, time_quantum (Positive Integer)
#Output_1 : Schedule list contains pairs of (time_stamp, proccess_id) indicating the time switching to that proccess_id
#Output_2 : Average Waiting Time
def RR_scheduling(process_list, time_quantum ):
    process_list = deepcopy(process_list)
    schedule = []
    current_time = 0
    waiting_time = 0
    process_number = len(process_list)

    while len(process_list) != 0:
        flag = 0
        for process in process_list[:]:
            if process.burst_time > 0:
                if current_time >= process.arrive_time:
                    schedule.append((current_time, process.id))
                    waiting_time += current_time - process.arrive_time if process.last_scheduled_time == 0 else current_time - process.last_scheduled_time
                    consume_time = time_quantum if process.burst_time > time_quantum else process.burst_time
                    current_time += consume_time
                    flag = 1
                    process.last_scheduled_time = current_time
                    process.burst_time -= consume_time
                    if process.burst_time <= 0:
                        process_list.remove(process)
        if flag == 0:
            current_time = process_list[0].arrive_time

    average_waiting_time = waiting_time / process_number
    return (schedule, average_waiting_time)

def SRTF_scheduling(process_list):
    process_list = deepcopy(process_list)
    schedule = []
    current_time = 0
    waiting_time = 0
    process_number = len(process_list)

    while len(process_list) != 0:
        if len(list(filter(lambda x: current_time >= x.arrive_time, process_list))) != 0:
            current_process = min(filter(lambda x: current_time >= x.arrive_time, process_list), key=lambda x:x.burst_time)
        else:
            current_process = min(process_list, key=lambda x:x.arrive_time)
            current_time = current_process.arrive_time
        schedule.append((current_time, current_process.id))
        waiting_time += current_time - current_process.arrive_time if current_process.last_scheduled_time == 0 else current_time - current_process.last_scheduled_time
        while current_process == min(filter(lambda x: current_time >= x.arrive_time, process_list), key=lambda x:x.burst_time):
            current_process.burst_time -= 1
            current_time += 1
            current_process.last_scheduled_time = current_time
            if current_process.burst_time == 0:
                process_list.remove(current_process)
                break

    average_waiting_time = waiting_time / process_number
    return (schedule, average_waiting_time)

def SJF_scheduling(process_list, alpha):
    process_list = deepcopy(process_list)
    schedule = []
    current_time = 0
    waiting_time = 0
    process_number = len(process_list)
    process_predict = {}
    for process in process_list:
        if process.id not in process_predict.keys():
            process_predict[process.id] = 5
    print(process_predict)

    while len(process_list) != 0:
        if len(list(filter(lambda x:current_time>=x.arrive_time, process_list))) > 0:
            current_process = min(filter(lambda x:current_time>=x.arrive_time, process_list), key=lambda x:process_predict[x.id])
        else:
            current_process = min(process_list, key=lambda x:x.arrive_time)
            current_time = current_process.arrive_time
        schedule.append((current_time, current_process.id))
        waiting_time += current_time - current_process.arrive_time
        current_time += current_process.burst_time
        process_predict[current_process.id] = alpha*current_process.burst_time + (1-alpha)*process_predict[current_process.id]
        process_list.remove(current_process)

    average_waiting_time = waiting_time / process_number
    return (schedule, average_waiting_time)


def read_input():
    result = []
    with open(input_file) as f:
        for line in f:
            array = line.split()
            if (len(array)!= 3):
                print ("wrong input format")
                exit()
            result.append(Process(int(array[0]),int(array[1]),int(array[2])))
    return result
def write_output(file_name, schedule, avg_waiting_time):
    with open(file_name,'w') as f:
        for item in schedule:
            f.write(str(item) + '\n')
        f.write('average waiting time %.2f \n'%(avg_waiting_time))


def main(argv):
    process_list = read_input()
    print ("printing input ----")
    for process in process_list:
        print (process)
    print ("simulating FCFS ----")
    FCFS_schedule, FCFS_avg_waiting_time =  FCFS_scheduling(process_list)
    write_output('FCFS.txt', FCFS_schedule, FCFS_avg_waiting_time )
    print ("simulating RR ----")
    RR_schedule, RR_avg_waiting_time =  RR_scheduling(process_list,time_quantum = 2)
    write_output('RR.txt', RR_schedule, RR_avg_waiting_time )
    print ("simulating SRTF ----")
    SRTF_schedule, SRTF_avg_waiting_time =  SRTF_scheduling(process_list)
    write_output('SRTF.txt', SRTF_schedule, SRTF_avg_waiting_time )
    print ("simulating SJF ----")
    SJF_schedule, SJF_avg_waiting_time =  SJF_scheduling(process_list, alpha = 0.5)
    write_output('SJF.txt', SJF_schedule, SJF_avg_waiting_time )

if __name__ == '__main__':
    main(sys.argv[1:])

