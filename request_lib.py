import csv
import requests 
import urllib
import json
import time
import os.path

# get credenial stored in CREDENTIAL file
def get_credential():
    credential = open("CREDENTIAL")
    access_token = credential.readline()
    ad_id = credential.readline()
    credential.close()
    return access_token, ad_id

# function to build category dictionary with id as key 
def build_id_dictionary(category_filename):
    dictionary = {}
    with open(category_filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1;
                continue
            else:
                dictionary[str(row[0])] = str(row[1])
    return dictionary

# function to build a dictionary of countries with code as key
def build_country_dictionary(country_filname):
    dictionary = {}
    with open(country_filname) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1;
                continue
            else:
                dictionary[str(row[1])] = str(row[0])
    return dictionary

# build params per job
def build_params(country, group_id, id_type):
    # contruct request params
    PARAMS = [];
    GENDERS = [[1],[2]]
    AGE_MINS = [13,21,31,41,51,61]
    AGE_MAXS = [20,30,40,50,60,65]

    # for each gender, generate params for each age group
    for i in range(len(GENDERS)):
        for j in range(len(AGE_MAXS)):
            param = {
                'geo_locations': {'countries': [country], },
                'genders': GENDERS[i],   
                'age_min': AGE_MINS[j], 
                'age_max': AGE_MAXS[j],  
                id_type: [group_id]
            }
            PARAMS.append(param)
    return PARAMS

# build list of url from given params
def build_url(params, access_token, ad_id):
    url_list = []
    for param in params:
        URL = "https://graph.facebook.com/v7.0/act_" + ad_id + \
              "/delivery_estimate?access_token=" + access_token + \
              "&optimization_goal=REACH&targeting_spec="
        URL += json.dumps(param)
        url_list.append(URL)
    return url_list

# check response limit
def check_request_limit(response):
    current_rate_limit = json.loads(response.headers["x-ad-account-usage"])["acc_id_util_pct"]
    print("current rate limit: " + str(current_rate_limit))
    return current_rate_limit < 50

# make api request with given built urls
def api_request(url_list, url_start, country, group_id):
    outcome = []
    last_url_index = 0
    reach_limit = False
    for i in range(url_start, len(url_list)):
        # make a request with specified params
        response = requests.get(url_list[i])

        # extracting data in json format 
        data = json.loads(response.text)
        DAU = data["data"][0]["estimate_dau"]
        MAU = data["data"][0]["estimate_mau"]

        # define age group
        AGE_GROUP = (i+1) % 6
        if AGE_GROUP == 0:
            AGE_GROUP = 6

        # define "gender" value
        GENDER = "1"
        if i > 5: GENDER = "2"

        # define output
        OUTPUT = str(country) + "," + \
                 GENDER + "," + \
                 str(DAU) + "," + \
                 str(MAU) + "," + \
                 str(AGE_GROUP) + "," + \
                 str(group_id) 
        print(OUTPUT)
        outcome.append(OUTPUT)
        print("sleep 0.6s")
        time.sleep(0.6)

        # if limit reached, return outcome and checkpoint index
        last_url_index = i
        if check_request_limit(response) == False:
            reach_limit = True
            break
    return outcome, last_url_index, reach_limit

# get checking point after terminating request
def starting_points(checkpoint_fname):
    need_read_checkpoint = os.path.isfile(checkpoint_fname)
    if need_read_checkpoint:
        checkpoint = open(checkpoint_fname, "r")
        contents = checkpoint.read().split(",")
        category_start = int(contents[0])
        country_start = int(contents[1])
        url_start = int(contents[2])+1
    else:
        category_start = 0
        country_start = 0
        url_start = 0
    return category_start, country_start, url_start

# write api response to file
def write_reseponse(filename, api_responses):
    # output file doesn't exit, add header
    if os.path.isfile(filename) == False:
        f = open(filename, "a")
        f.write("country,gender,dau,mau,age_group,group_id\n")
    else:
        f = open(filename, "a")

    # write request results to output file
    for res in api_responses:
        f.write(res + "\n")
    f.close()
