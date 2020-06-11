# fb-request-lib (Updated in 2020 June)
A friendly request library for using Facebook Graph API to study  
reachable audience comprehensively.  
**Both Python2 and Python3 are supported!**

If you encounter problem, please describe problem with screenshot  
in the "Issues" section of the repository. I will try to answer and  
solve it with you as possible as I can.  

**Files in the directory**
```
CREDENTIAL                 # your credential is stored at here
FB Marketing API Setup.pdf # instruction for getting your credential
README.md                  # documentation for functions in request_lib.py
categories.csv             # a csv file contains all the categories needed
country_codes.csv          # a csv file contains all the countries needed
generate_folder.py         # a py file creates directories to distribute smaller categories.csv to different people
get_audience_data.py       # a py file for making GET call to Facebook API and save responses to a file
request_lib.py             # the library used in the "get_audience_data.py" file for making requests
transform.py               # a py file to transform your api_responses.csv output to a more readable format
```

## Section 0: What is this library for?
This Facebook Marketing API request library is designed for making  
GET API call easier to **Facebook Marketing API 7.0**.  

**How to obtain Facebook Marketing API Credential?**  
[See the pdf instruction in this repository!](https://github.com/KangboLu/request-lib/blob/master/FB%20Marketing%20API%20Setup.pdf)  
Your Access Token will expire in **2-3 months** after you extended the access token. Otherwise, it will only last for **1 hour**.

**How to Import the request_lib library?**
```python
# import the whole library
import request_lib

# or import the library and change the reference name
import request_lib as lib

# or import specific function
import request_lib.get_credential as get_credential
from request_lib import get_credential # alternative
```

**How to use it?**  
1. Modify the ```CREDENTIAL``` file with your access token and ad id after  
you have followed the above pdf instruction to set up an Facebook app  
and created a Facebook ad.

2. Install ```requests``` libaray first!  
```pip install requests```  

3. Run the ```get_audience_data.py``` file to collect data. The code  
is clearly commented. Read the comment first to see how the data  
collect process is conducted. A file called "api_responses.csv" will  
be created for your output and another file called "checkpoint.txt"  
will be created to insure smooth data collection process.  

4. Run ```transform.py``` after you have collected all your data  
and having a file called "api_responses.csv". It create a more readable  
file called "dataset.csv" for you.  

<img src="https://github.com/KangboLu/request-lib/blob/master/general_workflow.PNG" height="70%" width="70%">

## Section 1: Implementations
**Library used:** csv, requests, urllib, json, time, os  
Besides **requests**, all the library are python2 or python3 built-in packages.  

```python
# get credenial stored in CREDENTIAL file
def get_credential():
```
**Input:** none  
**Output:** 1. your access token, 2. your ad id  

This function will open the "CREDENTIAL" file in the directory. Then,  
it will read your access token ("CREDENTIAL" file's first line), and read your  
Ad id ("CREDENTIAL" file's second line). It will return your acess token and  
your ad id at the end.  

```python
# function to build category dictionary with id as key 
def build_id_dictionary(category_filename):
```
**Input:** a filename for a .csv file contains all the query categories  
**Output:** a python dictionary with key as id number, and value as category type.  

Input requirement:  
The input .csv file must have its 1st column to be a column of id number and  
the 2nd column to be the category type for 1st column's id number.  

This function will open the file contains all the query categories. Then, it  
will read the file line by line and build a python dictionary with key as id  
number and value as category type. At the end, a dictionary contains all the  
category info will be returned from this function.  

```python
# function to build a dictionary of countries with code as key
def build_country_dictionary(country_filname):
```
**Input:** a filename for a .csv file contains all the query countries  
**Output:** a python dictionary with key as full country name, and value  
as 2 letter coding for country.  

Input requirement:  
The input .csv file must have its 1st column to be a column of country names  
and the 2nd column to be 2 letter country name for the 1st column.  

This function open the file contains the country names and read each line to  
build a python dictionary with key as full country name, and value as 2 letter  
coding for country. At the end, the function will return the dictionary.  

```python
# build params per job
def build_params(country, group_id, id_type):
```
**Input:** 2 letter country code, category id number, category type  
**Output:** a list of python dictionary of parameters for API request  

In this function, it will build a list of 12 parameters for API request.  
Why 12 parameters? It is because there are 2 genders and each gender can have  
6 age groups. Hence, 2 x 6 = 12 paramters. For each gender, and for each  
gender's age group, it will create a parameter and append it to the list for  
function output. At the end, the list of parameters will be returned.  

```python
# build list of url from given params
def build_url(params, access_token, ad_id):
```
**Input:** request paramters list, your access token, your ad id  
**Output:** a list of constructed URL for making API call   

For each request parameters of the "params" input, it will create a specific  
url combined with "access_token" and "ad_id". A list of url will be returned  
from this function for the "api_request()" function to make API calls.  

```python
# check response limit
def check_request_limit(response):
```
**Input:** API call response returned after making request  
**Output:** a boolean value to indicate whether limit is reached  

For each Facebook Marketing API call, the response header of the API request  
contains a field called "x-ad-account-usage" and it has a field called  
"acc_id_util_pct". "acc_id_util_pct" contains the data indicate the current  
rate limit of your API call. Higher the number, lower the number of request  
you can make in the future. This function set 50% as default. You can change  
the return statement to adjust the threshold of checking rate limit.  
This function should return **True** when you have not exceeded rate limit 50%.   
Otherwise, it will return **False** to indicate you have exceeded 50% rate limit.   
 
```python
# make api request with given built urls
def api_request(url_list, url_start, country, group_id):
```
**Input:** 
1. a list of url  
2. start position of url request in the url list  
3. 2 letter country code  
4. category id number 

**Output:**
1. outcome: a list of processed API call response with details  
2. last_url_index: 11 if all 12 requests are made successfully; otherwise,  
                   it will be the last request didn't exceed request limit  
3. reach_limit: a boolean indicator for your request has exceeded limit or not.  
For each url from the input "url_list", this function will make GET request.  
Using "requests" library, the function call "requests.get()" will actually  
make get request and the return will be JSON after calling "json.loads()".  
Then, each response is formatted in a nicer way to output and appended to a  
list of outputs.

For each request, "last_url_index" will store the most recently index of the  
requested url from the "url_list" to insure the position is noted and returned.  
Why returning last_url_index? It is because we want to have the index of url  
from the url_list when you reached the limit. The last_url_index will be stored  
in the checkpoint file for insurance purpose.  

For each request, "check_request_limit()" is also called with API request's  
reponse passed into as the argument. If limit reached, it will return false,  
"reach_limit" variable will be set to True and the request will be stopped.  

At the end of the function call, it will return the list of formatted outputs,  
a variable called "last_url_index", which is usually equal to 11 since all the  
urls from the "url_list" are used to request data from Facebook. However, it  
can also be any number from 0-11 since your request limit might reach before  
you can finish making all the request with the "url_list". And then, it will  
return the boolean indicator to see if you have reached the limit.    

```python
# get checking point after terminating request
def starting_points(checkpoint_fname):
```
**Input:** a file name for your request checkpoint file  
**Output:**  
1. category_start: request start position for the category list  
2. country_start: request start position for the country list  
3. url_stary: request start position for the url list  

This function should be called before calling "build_params" and "build_urls"  
since it reads the checkpoint file you provided to start the right place after  
your previous request since rate limit reached. If you have not made any request  
(first time making request), the category_start, country_start, and url_start will  
be set to 0 to indicate you are starting at the begining of all the requests.  
At the end, the starting indexes of category, country, and url will be returned.  

```python
# write api response to file
def write_reseponse(filename, api_responses):
```
**Input:** filename for output, your api responses from api request  
**Output:** (appending new responses to the output file)  

After you made requests, this function will be used to store your "api_responses"  
to a file designated with the argument called "filename". If the output file  
you specified doesn't exist, you will first create that file and write the header  
for the data you are about to write to. If the output file already exists, it  
will write in append mode to append data to it. And then, it will write request   
results from the "api_responses" line by line to the output file. 
