import csv
import sys
import itertools
from FreqMax import FreqMax

def flatmap(a):
        return itertools.chain.from_iterable(a)

def get_jobs(input_file):
    with open(input_file) as f:
        reader = csv.reader(f, delimiter=';')
        
        for line in reader:
            headers = line
            break
     
    for i,header in enumerate(headers):
        if 'SOC_NAME' in header:
            job_title_index = i
        if 'STATUS' in header:
            status_index = i
            
    if not job_title_index or not status_index:
        sys.exit('Column not found')

    jobmax = FreqMax()
    totaljobs = 0
    with open(input_file) as f:
        reader = csv.reader(f, delimiter=';')
        
        for i,line in enumerate(reader):
            if i == 0 or line[status_index] != 'CERTIFIED': continue        
            jobmax.add(line[job_title_index])
            totaljobs += 1

    jobs = jobmax.getmaxgrouped(10)
    jobs = (sorted(l) for l in jobs)

    top10jobs = itertools.islice(flatmap(jobs), 10)

    output = [(datum.key, datum.value, '{0}%'.format(round(100 * datum.value / totaljobs, 1))) \
    for datum in top10jobs]

    return output


def get_states(input_file):
    with open(input_file) as f:
        reader = csv.reader(f, delimiter=';')
        
        for line in reader:
            headers = line
            break
     
    for i,header in enumerate(headers):
        if 'STATUS' in header:
            status_index = i
            break;
            
    for i,header in enumerate(headers):        
        if 'WORK' in header and 'STATE' in header:
            state_index = i
            break

    if not state_index or not status_index:
        sys.exit('Column not found')
            
    statemax = FreqMax()
    totalstates = 0
    with open(input_file) as f:
        reader = csv.reader(f, delimiter=';')
        
        for i,line in enumerate(reader):
            if i == 0 or line[status_index] != 'CERTIFIED': continue
            statemax.add(line[state_index])
            totalstates += 1        

    states = statemax.getmaxgrouped(10)
    states = [sorted(l) for l in states]

    top10states = itertools.islice(flatmap(states), 10)

    output = [(datum.key, datum.value, '{0}%'.format(round(100 * datum.value / totalstates, 1))) \
    for datum in top10states]

    return output


def write_output(jobs, states, output_jobs, output_states):
    jobheader = ('TOP_OCCUPATIONS', 'NUMBER_CERTIFIED_APPLICATIONS', 'PERCENTAGE')
    with open(output_jobs, 'w') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(jobheader)
        writer.writerows(jobs)

    stateheader = ('TOP_STATES', 'NUMBER_CERTIFIED_APPLICATIONS', 'PERCENTAGE')
    with open(output_states, 'w') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(stateheader)
        writer.writerows(states)


def main(input_file, output_jobs, output_states):
    jobs = get_jobs(input_file)
    states = get_states(input_file)

    write_output(jobs, states, output_jobs, output_states)

if __name__ == '__main__':
    input_file = sys.argv[1]
    output_jobs = sys.argv[2]
    output_states = sys.argv[3]
    main(input_file, output_jobs, output_states)
