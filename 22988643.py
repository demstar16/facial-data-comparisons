__author__ = "Dempsey Thompson - 22988643"
__version__ = "1.0"


def main(csvfile, adultIDs):
    # Make the adultIDs case insensitive
    for i in range(len(adultIDs)):
        adultIDs[i] = adultIDs[i].upper()

    # Read the csvfile
    if read_csvfile(csvfile) != (None, None):
        data, ids_missing_data = read_csvfile(csvfile)
    else:
        return [None, None], None, [None, None], [None, None]
    
    # Holds all data in nested lists, where each nested lists holds all for a specific ID
    id_data = id_data_sort(data)

    # Checks to see if our input is corrupt, if so nothing can happen
    corrupted_data = corruption(id_data, ids_missing_data)
    
    for i in corrupted_data:
        if i in adultIDs:
            print("adultIDs are corrupted")
            return [None, None], None, [None, None], [None, None]

    # Get corrupition free data
    corrupt_free_data = corrupiton_free_data(id_data, ids_missing_data) 
    
    # Trim the data, so we just have what we want (To improve efficiency where possible)
    wanted_data = data_sort(data, adultIDs)

    # Make sure input IDs are valid
    if valid_id(adultIDs, data) == None: 
        return [None, None], None, [None, None], [None, None]
    
    # Splits the adults data up respectively
    adult1_data = wanted_data[:15]
    adult2_data = wanted_data[15:]

    # Gain euclidean distance dictionary for each adult
    euclidean_dict1 = euclidean_dist_dict(adult1_data)
    euclidean_dict2 = euclidean_dist_dict(adult2_data)

    # Create our OP1 return variable
    OP1 = [euclidean_dict1, euclidean_dict2]
    
    # Create our OP2 return variable
    OP2 = round(cosine_sim(euclidean_dict1, euclidean_dict2), 4)
    
    # Create our OP3 return variable
    OP3 = []
    cosine_comp_list1 = cosine_comparisons(corrupt_free_data, adultIDs, euclidean_dict1)
    cosine_comp_list2 = cosine_comparisons(corrupt_free_data, adultIDs, euclidean_dict2)
    OP3.append(cosine_comp_list1)
    OP3.append(cosine_comp_list2)

    # Create our OP4 return variable
    OP4 = []
    euclidean_avgs1 = euclidean_avg_dist(cosine_comp_list1, corrupt_free_data)
    euclidean_avgs2 = euclidean_avg_dist(cosine_comp_list2, corrupt_free_data)
    OP4.append(euclidean_avgs1)
    OP4.append(euclidean_avgs2)

    return OP1, OP2, OP3, OP4

# Function to check the validity of the adult IDs
def valid_id(adultIDs, data):
    truth1 = False
    truth2 = False
    for i in data:
        if i[0] == adultIDs[0]:
            truth1 = True
        elif i[0] == adultIDs[1]:
            truth2 = True
    if truth1 and truth2:
        pass
    else:
        print("Invalid Adult IDs")
        return None
    return True
    
# Function to read all of the csvfile
def read_csvfile(csvfile):
    ids_missing_data = []
    data = []
    order = []
    for i in range(5):
        order.append(0)
    try:
        with open(csvfile, 'r') as f:
            # Stores the order of the data given
            header = f.readline().strip('\n').split(',')

            # Orders CSV data into specific format/order --> ['AdultID', 'Landmark', 'X', 'Y', 'Z']
            for i, heading in enumerate(header):
                if heading == 'AdultID':
                    order[0] = i 
                elif heading == 'Landmark':
                    order[1] = i 
                elif heading == 'X':
                    order[2] = i 
                elif heading == 'Y':
                    order[3] = i 
                elif heading == 'Z':
                    order[4] = i 
            
            # Obtain all the data
            for line in f:
                currentline = line.strip('\n').split(",")
                if currentline == '': continue
                if len(currentline) == 5 and '' not in currentline:
                   
                    # To make sure values are within required range
                    if float(currentline[order[2]]) > -200 and float(currentline[order[2]]) < 200:
                        if float(currentline[order[3]]) > -200 and float(currentline[order[3]]) < 200:
                            if float(currentline[order[4]]) > -200 and float(currentline[order[4]]) < 200:

                                data.append((str(currentline[order[0]]).upper(), str(currentline[order[1]]).upper(), 
                                float(currentline[order[2]]), float(currentline[order[3]]), float(currentline[order[4]])))
                else:
                    ids_missing_data.append(currentline[0])
    except FileNotFoundError:
        print("Error finding the file")
        return None, None
    
    return data, ids_missing_data

# Function to return a list of corrupted IDs
def corruption(id_data, ids_missing_data):
    corrupted_ids = []

    # Checks for missing Landmarks
    for i in range(len(id_data)):
        count = 0
        landmarks = ['EX_L', 'EN_L', 'N', 'EN_R', 'EX_R', 'PRN', 'AL_L', 'AL_R', 'SBAL_L', 'SBAL_R', 'CH_L', 'CH_R', 
        'SN', 'FT_L', 'FT_R']
        # Makes sure all landmarks are present for an adult
        for j in range(len(id_data[i])):
            if id_data[i][j][1] in landmarks:
                count += 1

            # Makes sure each adult has the right amount of data
            if len(id_data[i][j]) != 5:
                corrupted_ids.append(id_data[i][0][0])
        
        if count == 15: 
            pass
        else:
            corrupted_ids.append(id_data[i][0][0])

    for id in ids_missing_data:
        if id not in corrupted_ids:
            corrupted_ids.append(id)
    return corrupted_ids

# Function to return the mass data sorted and free of corrupiton
def corrupiton_free_data(id_data, ids_missing_data):
    corrupt_free = []
    #list of corrupted adultIDs
    corrupted_ids = corruption(id_data, ids_missing_data)

    for i in id_data:
        if i[0][0] not in corrupted_ids:
            corrupt_free.append(i)
            
    return corrupt_free

# Function to return a list only containing data relevant to given adultIDs
def data_sort(data, adultIDs):
    wanted_data = []
    for i in range(len(data)):
        if data[i][0] == adultIDs[0] or data[i][0] == adultIDs[1]:
            wanted_data.append(data[i])
    return wanted_data

# Function to help sort the data into their respective facial features
def facial_feat_sort(data):
    face_dist_names = ['FW', 'OCW', 'LEFL', 'REFL', 'ICW', 'NW', 'ABW', 'MW', 'NBL', 'NH']
    euclidean_dist = {i: [] for i in face_dist_names} 

    for i in range(len(data)):
        if data[i][1] == 'EX_L':
            euclidean_dist['OCW'].insert(1, data[i])
            euclidean_dist['LEFL'].insert(1, data[i])

        elif data[i][1] == 'EN_L':
            euclidean_dist['LEFL'].insert(0, data[i])
            euclidean_dist['ICW'].insert(1, data[i])

        elif data[i][1] == 'N':
            euclidean_dist['NBL'].insert(1, data[i])
            euclidean_dist['NH'].insert(1, data[i])

        elif data[i][1] == 'EN_R':
            euclidean_dist['REFL'].insert(1, data[i])
            euclidean_dist['ICW'].insert(0, data[i])

        elif data[i][1] == 'EX_R':
            euclidean_dist['OCW'].insert(0, data[i])
            euclidean_dist['REFL'].insert(0, data[i])

        elif data[i][1] == 'PRN':
            euclidean_dist['NBL'].insert(0, data[i])

        elif data[i][1] == 'AL_L':
            euclidean_dist['NW'].insert(1, data[i])
            
        elif data[i][1] == 'AL_R':
            euclidean_dist['NW'].insert(0, data[i])
            
        elif data[i][1] == 'SBAL_L':
            euclidean_dist['ABW'].insert(1, data[i])

        elif data[i][1] == 'SBAL_R':
            euclidean_dist['ABW'].insert(0, data[i])

        elif data[i][1] == 'CH_L':
            euclidean_dist['MW'].insert(1, data[i])

        elif data[i][1] == 'CH_R':
            euclidean_dist['MW'].insert(0, data[i])

        elif data[i][1] == 'SN':
            euclidean_dist['NH'].insert(0, data[i])

        elif data[i][1] == 'FT_L':
            euclidean_dist['FW'].insert(1, data[i])

        elif data[i][1] == 'FT_R':
            euclidean_dist['FW'].insert(0, data[i])

    return euclidean_dist

# 3D distance between two points A = (x1, y1, z1) and B = (x2, y2, z2) in cartesian plain stored in a dictionary
def euclidean_dist_dict(adultID_data):
    face_dist_names = ['FW', 'OCW', 'LEFL', 'REFL', 'ICW', 'NW', 'ABW', 'MW', 'NBL', 'NH']
    euclidean_distances = {i:None for i in face_dist_names}
    sorted_dict = facial_feat_sort(adultID_data)

    for abvn in sorted_dict.keys():
        val1 = 0
        val2 = 0
        val3 = 0
       
        for face_feat in sorted_dict[abvn]:
            if val1 == 0 and val2 == 0 and val3 == 0:
                val1 += face_feat[2]
                val2 += face_feat[3]
                val3 += face_feat[4]
            else:
                val1 -= face_feat[2]
                val2 -= face_feat[3]
                val3 -= face_feat[4]
        
        euc_formula = ((val1**2) + (val2**2) + (val3**2))**0.5
        euclidean_distances[abvn] = round(euc_formula, 4)
  
    return euclidean_distances

# Find cosine similarity between faces using the cosine similarity formula
def cosine_sim(dict1, dict2):
    cosine_similarity = 0
    sum_of_multiples = 0
    if len(dict1) == len(dict2):
        for key1, key2 in zip(dict1, dict2):
            sum_of_multiples += (dict1[key1] * dict2[key2])

    dict1_sqr_rt_vals = sum_under_sqr_rt(dict1)
    dict2_sqr_rt_vals = sum_under_sqr_rt(dict2)

    cosine_similarity = (sum_of_multiples) / (dict1_sqr_rt_vals * dict2_sqr_rt_vals)
    return cosine_similarity

# Function to sum items in a list and square root the result
def sum_under_sqr_rt(dict):
    sum = 0
    for i in dict.values():
        sum += i**2
    return sum**0.5    

# Sort the mass data into a list of lists where each nested list holds all data for a particular ID
def id_data_sort(data):
    IDs = []
    sorted_data = [] 
    
    for i in range(len(data)):
        if data[i][0] not in IDs:
            IDs.append(data[i][0]) 
 
    for index, id in enumerate(IDs):
        sorted_data.append(list())
        for j in range(len(data)):
            if data[j][0] == id:
                sorted_data[index].append(data[j])
                
    return sorted_data

# Function to compare cosine similarities of one face with every other face in data file
def cosine_comparisons(data, adultIDs, euclidean_dict):
    list = []
    for i in range(len(data)):
        if data[i][0][0] not in adultIDs:
            euclidean_dict_id = euclidean_dist_dict(data[i])
            current_cosine_sim = cosine_sim(euclidean_dict, euclidean_dict_id)
            list.append((data[i][0][0], current_cosine_sim))
    
    list.sort(key=lambda u:(-u[1],u[0]))
    top_5_comparisons = list[:5]

    # For rounding purposes
    rounded_t5 = []
    for i in top_5_comparisons:
        rounded_t5.append((i[0], round(i[1], 4)))
        
    return rounded_t5     

# Function for finding the average euclidean distances between faces for each facial feature
def euclidean_avg_dist(cosine_comparison_list, data):
    face_dist_names = ['FW', 'OCW', 'LEFL', 'REFL', 'ICW', 'NW', 'ABW', 'MW', 'NBL', 'NH']
    list = []
    euclideans = []
    avg_dict = {i: None for i in face_dist_names}
        
    for i in cosine_comparison_list:
        list.append(i[0])
    for i in range(len(list)):
        for j in range(len(data)):
            if data[j][0][0] == list[i]:
                euclideans.append(euclidean_dist_dict(data[j]))
    
    if len(euclideans) == 0:
        print("Not enough Test data for Average Euclidean Distance functionality")
        return None

    for key in avg_dict:
      avg_dict[key] = round(sum(d[key] for d in euclideans) / len(euclideans), 4)
    
    return avg_dict


