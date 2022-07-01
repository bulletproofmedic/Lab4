#-----------------------------------------------------
#   Lab 2, PokeApi - COMP 593
#
#   Description:
#       Uploads info from the PokeDex to PasteBin.
#
#   Usage:
#       python pokeapi.py
#
#   Parameters:
#       No CLI parameters.
#
#   History:
#   Date        Author      Description
#   2022-02-07  A. Walker   Initial Creation
#-----------------------------------------------------

from http import client
import urllib
import json

pokeApi = client.HTTPSConnection('pokeapi.co', 443)
pasteBin = client.HTTPSConnection('pastebin.com', 443)

pokemon = input("What pokemon would you like to search for? ")
pokemon_url = "/api/v2/pokemon/" + pokemon.lower()
#Create GET Request
pokeApi.request('GET', pokemon_url)

#Check GET Response
response = pokeApi.getresponse()
if response.status == 200:
    print('Response:',response.status)
else:
    print('There was a problem. Response:', response.status)

# Extract body from response message from PokeAPI
# Response body should contain Pokemon info in JSON format
jsonData = response.read().decode()

# Convert JSON to dictionary so individual values can easily be accessed
dictionary = json.loads(jsonData)

#Pastebin API key
pasteBinApi = "cf22cc98eaef4ee514844f1a112fd17a"

type_list = dictionary['types']
#print(type(type_list))
#print(type_list)
type_dictionary = type_list[0]
#keys = type_dictionary.keys()
#print(keys)
type_dict = type_dictionary['type']
#keys = type_dict.keys()
#print(keys)
type = type_dict['name']
poke_info = "Name: " + dictionary['name'] + "\nWeight: " + str(dictionary['weight']) + "\nType(s): " + type

#Confirm info
print(poke_info)

#Refer to the documentation at https://pastebin.com/doc_api for instructions on these parameters
requestParams = {
    'api_dev_key': pasteBinApi,
    'api_option': 'paste',
    'api_paste_code': poke_info,
	'api_paste_name': pokemon
}

#This additional Method call will convert the Dictionary to a URL-Encoded string for PasteBin,
#Include this string as the body of your call to the HTTPConnection.request() method for your pasteBin connection.
requestBody = urllib.parse.urlencode(requestParams)

#Since we are URLEncoding the request Body, we need to tell Pastebin that it can expect x-www-form-urlencoded content, by adding this information to the request header
pasteBinHeaders = {'Content-Type': 'application/x-www-form-urlencoded'}

# Send request message to PasteBin API
pasteBinRequest = pasteBin.request('PUT', '/api/api_post.php', body=requestBody, headers=pasteBinHeaders)

# Get response message from PasteBin API
response = pasteBin.getresponse()

# Check whether response indicates success
if response.status == 200:
    print('Response:',response.status, "- your paste was successful.")
else:
    print('There was a problem. Response:', response.status)

# Extract body from response message from PasteBin API
print(response)
#response_body = pasteBin.HTTP.client.HTTPResponse.read()
#print(response_body)

# Response body should contain the URL of the new PasteBin paste in plain text
#paste_url = response_body

# Print the URL of the new PasteBin paste
#print(paste_url)
