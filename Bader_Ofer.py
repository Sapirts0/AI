#!/usr/bin/env python
# coding: utf-8

# In[3]:


def threshold(election):

    #Given the election number, returns the voting threshold implemented in that election. 
    
    if election <= 12:
        return 1 / 100
    elif election <= 16:
        return 1.5 / 100
    elif election <= 19:
        return 2 / 100
    else:
        return 3.25 / 100


data_file = open("votes.csv", "r")
data_lines = data_file.readlines()

odafim_pairs_file = open("agreements.csv", "r")
odafim_pair_lines = odafim_pairs_file.readlines()

PARLIAMENT_SIZE = 120



def bader_ofer(election, data, odafim_pairs):
    """
    election - an integer of the election number
    data - a dictionary mapping party name to number of votes it received in the election
    odafim_pairs - a dictionary mapping every party to a tuple of (id of the odafim agreements, other party),
                    and also mapping the id of the odafim agreements to (party1, party2) of the agreement.

    return - a dictionary mapping every party in data to the mandates it should receive.
    """
    
    mandates = dict()
    votes_odafim = dict()
    votes_with_pairs = dict()
    moded_lamandat = dict()
    

    num_of_votes = 0
    for key in data:
        num_of_votes = num_of_votes + int(data[key])
        
    basic_price = num_of_votes / PARLIAMENT_SIZE

    for key in data:
        mandates[key] = int(int(data[key]) / basic_price)

    num_of_remained_mandates = 120
    for key in mandates:
        num_of_remained_mandates = num_of_remained_mandates - mandates[key]
        
    while (num_of_remained_mandates > 0):
        
        for key in data:
            if key in odafim_pairs:
                running_ID = odafim_pairs[key][0]
                party_2 = odafim_pairs[key][1]
                votes_with_pairs[running_ID] = data[key] + data[party_2]
            else:
                votes_with_pairs[key] = data[key]
        
                
        for key in votes_with_pairs:
            if key in odafim_pairs:
                prty1 = odafim_pairs[key][0]
                prty2 = odafim_pairs[key][1]
                number_of_total_votes = votes_with_pairs[key]
                number_of_initial_mandates_plus1 = mandates[prty1] + mandates[prty2] + 1
                moded_lamandat[key] = number_of_total_votes / number_of_initial_mandates_plus1
            else:
                number_of_total_votes = votes_with_pairs[key]
                moded_lamandat[key] = number_of_total_votes / (mandates[key] + 1)

        max_number = 0
        max_miflaga = None

        for key, value in moded_lamandat.items():
            if value > max_number:
                max_miflaga = key
                max_number = value
                
        if isinstance(max_miflaga, int):
            prty1 = odafim_pairs[max_miflaga][0]
            prty2 = odafim_pairs[max_miflaga][1]
            number_of_total_votes1 = data[prty1]
            number_of_total_votes2 = data[prty2]
            moded1 = number_of_total_votes1 / (mandates[prty1] + 1)
            moded2 = number_of_total_votes2 / (mandates[prty2] + 1)
            if moded1 >= moded2:
                mandates[prty1] = mandates[prty1] + 1
            else:
                mandates[prty2] = mandates[prty2] + 1
        else:
            mandates[max_miflaga] = mandates[max_miflaga] + 1

        num_of_remained_mandates = num_of_remained_mandates - 1

    predictions = mandates
    return predictions


elections = {}
election_results = {}
odafim_pairs = {}

running_id = 0

for line in odafim_pair_lines[1:]:
    election, party1, party2 = line.split(",")
    election = int(election)
    party2 = party2.strip()
    if election not in odafim_pairs:
        odafim_pairs[election] = {}

    odafim_pairs[election][party1] = [running_id, party2]
    odafim_pairs[election][party2] = [running_id, party1]
    odafim_pairs[election][running_id] = [party1, party2]
    running_id += 1


for line in data_lines[1:]:
    election, party, mandates, votes = line.split(",")
    party = party.strip()
    votes = int(votes)
    mandates = int(mandates)
    election = int(election)
    if election not in elections:
        elections[election] = {}
        election_results[election] = {}
    elections[election][party] = votes
    election_results[election][party] = mandates

success = True

for election in elections:
    data = elections[election]
    predictions = bader_ofer(election, data, odafim_pairs[election])
    if predictions != election_results[election]:
        print("Error in election {}, predicted: {}, actual: {}".format(election, predictions, election_results[election]))
        success = False

if success:
    print("Success! All elections 17-23 predicted correctly")


# In[ ]:




