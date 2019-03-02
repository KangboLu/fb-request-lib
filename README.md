# fb-request-lib
A friendly request library for Facebook API query in python2

## Section 0: What is this library for?
This Facebook Marketing Api request library is designed for making  
GET API call easier to **Facebook Marketing API V3.2** to study  
the digital data of Latin America Facebook users.  
(32 countires are studied since Facebook does not have Cuba's data) 

**How to use it?**
```python
# import the whole library
import request_lib

# or import the library and change the reference name
import request_lib as lib

# or import specific function
import request_lib.get_credential as get_credential
from request_lib import get_credential # alternative
```

## Section 1: Implementations
**Library used:** csv, requests, urllib, json, time, os

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
The input .csv file must have its 1st column to a column of id number and  
the 2nd column to be category type for 1st column's id number.  
This function will open the file contains all the query categories. Then, it  
will read the file line by line and build a python dictionary with key as id  
number and value as category type. At the end, a dictionary contains all the  
category info will be returned from this function.  

```python
# function to build a dictionary of countries with code as key
def build_country_dictionary(country_filname):
```
**Input:** a filename for a .csv file contains all the query countries  
**Output:** a python dictionary with key as full country name, and value as 2 letter coding for country.  

TODO

```python
# build params per job
def build_params(country, group_id, id_type):
```
**Input:** 2 letter country code, category id number, category type  
**Output:** a list of python dictionary of parameters for API request  

TODO

```python
# build list of url from given params
def build_url(params, access_token, ad_id):
```
**Input:** request paramters list, your access token, your ad id  
**Output:** a list of constructed URL for making API call   

TODO

```python
# check response limit
def check_request_limit(response):
```
**Input:** API call response returned after making request  
**Output:** a boolean value to indicate whether limit is reached  

TODO

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

TODO 

```python
# get checking point after terminating request
def starting_points(checkpoint_fname):
```
**Input:** a file name for your request checkpoint file  
**Output:**  
1. category_start: request start position for the category list  
2. country_start: request start position for the country list  
3. url_stary: request start position for the url list  

TODO

```python
# write api response to file
def write_reseponse(filename, api_responses):
```
**Input:** filename for output, your api responses from api request  
**Output:** (appending new responses to the output file)  

TODO
