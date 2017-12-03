from urllib import request
# -*- coding: utf-8 -*-

import http.client, urllib.parse, json

# **********************************************
# *** Update or verify the following values. ***
# **********************************************

# Replace the subscriptionKey string value with your valid subscription key.
subscriptionKey = "33f4b68b3743478abfabe7673ec66161"

# Verify the endpoint URI.  At this writing, only one endpoint is used for Bing
# search APIs.  In the future, regional endpoints may be available.  If you
# encounter unexpected authorization errors, double-check this value against
# the endpoint for your Bing Web search instance in your Azure dashboard.
search_name = 'Mail.Ru Group, Email & Portal'

search_name = search_name.split(' ')
if len(search_name) == 1:
    term = search_name[0]
elif len(search_name) == 2:
    term = search_name[0]+" "+search_name[1]
else: 
    term = search_name[1]+" "+search_name[2]
term+='+logo+picture'

host = "api.cognitive.microsoft.com"
path = "/bing/v7.0/search"
print(term)




def BingWebSearch(search):
    "Performs a Bing Web search and returns the results."

    headers = {'Ocp-Apim-Subscription-Key': subscriptionKey}
    conn = http.client.HTTPSConnection(host)
    query = urllib.parse.quote(search)
    conn.request("GET", path + "?q=" + query, headers=headers)
    response = conn.getresponse()
    headers = [k + ": " + v for (k, v) in response.getheaders()
                   if k.startswith("BingAPIs-") or k.startswith("X-MSEdge-")]
    return headers, response.read().decode("utf8")

if len(subscriptionKey) == 32:

    print('Searching the Web for: ', term)

    headers, result = BingWebSearch(term)
    print("\nRelevant HTTP Headers:\n")
    print("\n".join(headers))
    print("\nJSON Response:\n")
#     print(json.dumps(json.loads(result), indent=4))
    res1=json.loads(result)
    pic_url=res1['images']['value'][0]['contentUrl']
    print(res1['images']['value'][0]['contentUrl'])
    request.urlretrieve(pic_url,"pic.jpg")
    
    

else:

    print("Invalid Bing Search API subscription key!")
    print("Please paste yours into the source code.")