import request_lib as lib
import time

def main():
    # get token and ad id
    ACCESSTOKEN, ADID = lib.get_credential()

    # build id dictionary
    id_dictionary = lib.build_id_dictionary("categories.csv")
    group_ids = sorted(list(id_dictionary.keys()))

    # build country dictionary
    country_dictionary = lib.build_country_dictionary("country_codes.csv")
    country_codes = sorted(list(country_dictionary.keys()))

    # obtain starting point for each request iteration
    checkpoint_fname = "checkpoint.txt"
    category_start, country_start, url_start = lib.starting_points(checkpoint_fname)
    category_end = len(group_ids)
    country_end = len(country_codes)

    # for each job id
    for i in range(category_start, category_end):
        GROUP_ID = group_ids[i]
        ID_TYPE = id_dictionary[GROUP_ID]

        # for each country code make request
        for j in range(country_start, country_end):
            COUNTRY = country_codes[j]

            # build query params
            params = lib.build_params(COUNTRY, GROUP_ID, ID_TYPE)

            # build urls with given params
            url_list = lib.build_url(params, ACCESSTOKEN, ADID)
            
            # make api request and store responses
            api_responses, end_position, reach_limit = \
                lib.api_request(url_list, url_start, COUNTRY, GROUP_ID)
            url_start = 0

            # output response to file
            output_filename = "api_responses.csv"
            lib.write_reseponse(output_filename, api_responses)

            # all process finished
            if i == category_end-1 and j == country_end-1 and end_position == 11:
                last_request_location = open(checkpoint_fname, "w")
                check_point_code = str(i) + "," + str(j) + "," + str(end_position)
                last_request_location.write(check_point_code)
                last_request_location.close()
                print("all requests done!")
                return 1

            # limit reached, save checkpoint
            if reach_limit == True:
                print("limit reached")
                last_request_location = open(checkpoint_fname, "w")
                check_point_code = str(i) + "," + str(j) + "," + str(end_position)
                last_request_location.write(check_point_code)
                last_request_location.close()
                return 0
            
            last_request_location = open(checkpoint_fname, "w")
            check_point_code = str(i) + "," + str(j) + "," + str(end_position)
            last_request_location.write(check_point_code)
            last_request_location.close()
        country_start = 0

# get data if all requests are not finished
# otherwise, it will keep collect data and 
# wait if specified limit reached
while True:
    if main() == 1:
        break
    print("limit reached, sleep 200s...")
    time.sleep(200)
