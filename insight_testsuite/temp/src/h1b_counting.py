import csv
import sys
import itertools
from FreqMax import FreqMax


def flatmap(a):
    return itertools.chain.from_iterable(a)


def get_jobs(input_file):
    '''Get top 10 most common jobs listed in the input file,
    provided that they are from certified visa applications.
    Also include the frequency of those jobs, along with
    the percentage of all certified applications they comprise.
    '''
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
        sys.exit('Columns not found')

    jobmax = FreqMax()
    totaljobs = 0
    with open(input_file) as f:
        reader = csv.reader(f, delimiter=';')
        
        for i,line in enumerate(reader):
            if i == 0 or line[status_index] != 'CERTIFIED': continue        
            jobmax.add(line[job_title_index])
            totaljobs += 1

    # Obtain a list of lists containing the most frequent jobs,
    # ordered by frequencies.
    # That is, jobs looks like ([job1], [job2, job3], [job4])
    # where job2 and job3 are in the same list because 
    # they have the same frequency.
    jobs = jobmax.getmaxgrouped(10)
    # Put all jobs with the same frequency in alphabetical order
    # relative to each other.
    jobs = (sorted(l) for l in jobs)

    # Using generators here because lazy evaluation leaves room for
    # optimizing the code to be more efficient
    top10jobs = itertools.islice(flatmap(jobs), 10)

    output = [(datum.key, datum.value, '{0}%'.format(round(100 * datum.value / totaljobs, 1))) \
    for datum in top10jobs]

    return output


def get_states(input_file):
    '''Get top 10 most common states listed in the input file,
    provided that they are from certified visa applications.
    Also include the frequency of those states, along with
    the percentage of all certified applications they comprise.
    '''
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
        sys.exit('Columns not found')
            
    statemax = FreqMax()
    totalstates = 0
    with open(input_file) as f:
        reader = csv.reader(f, delimiter=';')
        
        for i,line in enumerate(reader):
            if i == 0 or line[status_index] != 'CERTIFIED': continue
            statemax.add(line[state_index])
            totalstates += 1        

    # Obtain a list of lists containing the most frequent states,
    # ordered by frequencies.
    # That is, states looks like ([state1], [state2, state3], [state4])
    # where state2 and state3 are in the same list because 
    # they have the same frequency.
    states = statemax.getmaxgrouped(10)
    # Put all states with the same frequency in alphabetical order
    # relative to each other.
    states = (sorted(l) for l in states)

    # Using generators here because lazy evaluation leaves room for
    # optimizing the code to be more efficient
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
    '''This file should be run from the command line as follows:
    $ python3 <input file> <output file for jobs> <output file for states>
    '''
    input_file = sys.argv[1]
    output_jobs = sys.argv[2]
    output_states = sys.argv[3]
    main(input_file, output_jobs, output_states)
