# Insight Data Engineering H1B statistics challenge

## Problem

Obtain top 10 most common occupations and states of certified H1B visa applications.


## Approach

### 1. Obtain csv file of data

This is done for us.


### 2. Parse the input csv file, unmarshalling the data

We can use the `csv` module for this.

To identify the column in the csv file containing the data we want, we can first parse the first row of the csv file. Then we can look for the index of the element containing an appropriate keyword, eg "SOC_NAME" or "STATE", in this row. We can then use that index to read the desired data from the subsequent rows of that csv file.

This part of the code is a little fragile, in that we are depending on the format of the input csv files to not deviate too strongly from our assumptions, which we have made based on the csv files made available in the past.

### 3. Calculate the desired quantities

There are a number of approaches to calculating the most frequent occupations and states that might be suitable. They include:

1. We can create a hash table mapping from occupations (or states) to the frequency of that occupation. We can create such a table by reading the input file one row at a time, and incrementing the value of the key corresponding to the job in the row by 1. Then, we can form a list of jobs paired with their frequencies, and sort the list. We can read the first 10 elements of the sorted list to get our desired answer.

2. We maintain a max-heap which contains 2-tuples of jobs paired with their frequencies. If we read in a new job that isn't in the heap, we push a tuple containing that job with a frequency of 1 into the heap. If we read in a job that we have in the heap, we increment the frequency of that job's tuple by 1, then sift up to maintain the heap invariant. To get the top 10, we can simply pop the heap 10 times after reading in all the data.

3. Both approaches above take O(n log n) time, where n is the number of rows in the input data file. There is another option that has better time complexity: using a doubly linked list to store the 2-tuples of jobs + frequencies, along with some hash tables storing additional information. This allows us to update the linked list in constant time, resulting in O(n) time complexity overall. See below for more details on this data structure (which I call the FreqMax data structure).

Also, I created two separate functions for calculating the most frequent jobs and states because the details of those calculations might change in the future. For example, we may want to tabulate job titles in addition to SOC_NAMEs, or calculate the most frequent states from all visa applications, not just certified applications. In general, although the code may look like it isn't following DRY (don't repeat yourself), I think overzealously applying DRY is also a mistake, so I chose to break the two calculations into separate functions for ease of extendability in the future.

### 4. Write the desired quantities to the output file(s)

We can use the `csv` module for this as well.


## Running instructions

Put a file containing appropriately formatted data, named `h1b_input.csv`, in the `input` folder.

Then execute `run.sh`.


## Additional details on the FreqMax data structure

A doubly linked list is used to keep track of the keys (eg, jobs or states). Each node in the list contains the key as well as the number of times that key has occurred so far. The nodes are ordered by the keys' frequencies.

This means that returning the k most frequently occuring keys is easy. Simply read k nodes from the head of the linked list, which takes O(k) time. However, updating the list as the frequencies of the keys increase is where the complexity gets pushed to.

When a key is seen, and its frequency needs to be incremented by 1, a hash table is first used to find the node holding that key. This node can then be spliced out of the linked list and spliced back in at a location where the ordering of the list is restored.

One way to do this would be to traverse the list upwards from the updated node, until we find a node whose key has a frequency greater than or equal to the updated node's frequency. Then, we can make the found node the parent of the updated node, and splice it back in.

The problem with this approach is that the search for the new parent could degenerate into a linear scan of the entire list, if there were long runs of keys each occuring with the same frequency. To surmount this, we maintain another hash table. This 'gaps' hash table maps from frequencies to the last node in the linked list that has a key with that frequency. Using this, after updating the frequency of a node, we can look up, in constant time, the new parent of this node. After splicing the node in, we update the gaps hash table to point to the spliced-in node, as it is now the last node in the linked list with that frequency. 

As a result, the frequency of a key can be updated in O(1) time.

