import csv
import os

# function to build category dictionary with id as key 
def build_id_dictionary_transform(category_filename):
    dictionary = {}
    with open(category_filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1;
                continue
            else:
                dictionary[str(row[0])] = str(row[2])
    return dictionary

# function to build a dictionary of countries with code as key
def build_country_dictionary_transform(country_filename):
    dictionary = {}
    with open(country_filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1;
                continue
            else:
                dictionary[str(row[1])] = str(row[0])
    return dictionary

def transform_output(id_dict, country_dict, output_filename):
    gender_dict = {'1':"male", '2':"female"}
    age_groups_dict = {'1':"13-20", '2':"21-30", '3':"31-40", \
                       '4':"41-50", '5':"51-60", '6':"61-65+"}
    with open(output_filename) as inf, open('dataset.csv', 'w') as outf:
        reader = csv.reader(inf, delimiter=',')
        writer = csv.writer(outf, delimiter=',', lineterminator='\n')
        first_line = False
        for line in reader:
            if first_line == False:
                first_line = True
                templine = line
                templine[5] = "group_name"
                writer.writerow(templine)
            	continue
            templine = line
            templine[0] = country_dict[templine[0]].replace(" ", "_")
            templine[1] = gender_dict[templine[1]]
            templine[4] = age_groups_dict[templine[4]]
            templine[5] = id_dict[templine[5]].replace(" ", "_")
            writer.writerow(templine)

def transform():
    # build id dictionary
    id_dictionary = build_id_dictionary_transform("categories.csv")

    # build country dictionary
    country_dictionary = build_country_dictionary_transform("country_codes.csv")

    # transform the dataset back to more readable and friendlier contents
    transform_output(id_dictionary, country_dictionary, "api_responses.csv")

transform()
print("new file 'dataset.csv' created in the current directory!")
