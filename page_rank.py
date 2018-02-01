# CSE 3504 Project Part 2
# Brandon Haas

import csv

# Read hollins.dat
with open("hollins.dat", "r") as data:
    read = csv.reader(data, delimiter = ' ', skipinitialspace = True)
    columns = next(read)

    number_of_nodes = int(columns[0])
    number_of_edges = int(columns[1])
    links = {}

    # Variables for page_rank function
    transition_matrix = [ [0] * number_of_nodes for x in range(number_of_nodes)]
    initial_state_vector = []
    damping = .85	
    incoming_links = [set() for x in range(number_of_nodes)]
    outgoing_links = [0 for x in range(number_of_nodes)]

    for x in range(number_of_nodes):
        line = next(read)
        index = int(line[0])
        links[index] = line[1]

    for x in range(number_of_edges):
        line = next(read)
        source_link = int(line[0])
        destination_link = int(line[1])

        outgoing_links[source_link - 1] += 1
        incoming_links[destination_link - 1].add(source_link - 1)

    for x in range(number_of_nodes):
        initial_state_vector.append(1 / number_of_nodes)

    for i in range(number_of_nodes):
        for j in incoming_links[i]:
            transition_matrix[i][j] = 1 / outgoing_links[j]

def page_rank(trans_matrix, init_state_vector, damp, inc_links):
    iterations = 0
    length = len(init_state_vector)
    next_state_vector = [0] * length

    while iterations < 100:	# Iterate 100 times to achieve final PageRank
        for i in range(length):
            temp_next_state_vector = 0
            for j in inc_links[i]:
                temp_next_state_vector += init_state_vector[j] * trans_matrix[i][j]
            next_state_vector[i] = (1 - damp) + (damp * temp_next_state_vector)
        init_state_vector = next_state_vector
        iterations += 1

    return next_state_vector

final_rankings = page_rank(transition_matrix, initial_state_vector, damping, incoming_links)

# Sort and write final_rankings to text file
with open("final_rankings.txt", "w") as file:
    sorted_rankings = []

    for i in range(len(final_rankings)):
        sorted_rankings.append((final_rankings[i], i))
    sorted_rankings.sort()
    sorted_rankings.reverse()

    for i in sorted_rankings:
        rank = i[0]
        index = i[1]
        line = str(index + 1) + ' ' + str(rank) + ' ' + links[index + 1] + '\n'
        file.write(line)
