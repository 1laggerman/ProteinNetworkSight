import requests 
from time import sleep

string_api_url = "https://string-db.org/api"
output_format = "tsv-no-header"
app_name = "personal_cancer_med_project"     # our app name
human = 9606    

#----------API Connection----------#

def api_request(method, params, wait_time = 1):
    """[summary]
    Args:
        method ([type]): [description]
        params ([type]): [description]
    Returns:
        [type]: [description]
    """
    # Construct URL
    request_url = "/".join([string_api_url, output_format, method])
    # call STRING
    response =  requests.post(request_url, data=params)
    # wait a sec between calls 
    sleep(wait_time)
    
    return response


def map_uid(org_id, clean_id):
    """[summary]
    Args:
        org_id ([type]): [description]
        clean_id ([type]): [description]
        print_result ([type]): [description]
    Returns:
        [type]: [description]
    """    
    clean_id = clean_id.upper()   
    
    # request string
    method = "get_string_ids"
    params = {
        "identifiers" : clean_id, # protein list
        "species" : human, 
        # "limit" : 5, # five (best) identifier per input protein
        "caller_identity" : app_name
    } 
    response = api_request(method, params)
    
    # parse the result
    str_suggestions = [] 
    for line in response.text.strip().split("\n"):
        l = line.split("\t")
        if(len(l) > 4):
            str_suggestions.append(l[4])
    
    if len(str_suggestions)  == 0:
        print("Attention: didn't find string id for:", org_id, ", after cleaning:", clean_id)
    else:
        print("Found: string id for:", org_id, ", after cleaning:", clean_id, "string suggestions:", str_suggestions)
   
    return str_suggestions  


def network_interactions(genes, score_threshold):
    """
    """
    # set parameters
    method = "network"        
    params = {
        "identifiers" : "%0d".join(genes), 
        "species" : human, 
        "caller_identity" : app_name
    }
    response = api_request(method, params)
    
    scores = []
    for line in response.text.strip().split("\n"):
        # takes the proteins names
        l = line.strip().split("\t")
        p1, p2 = l[2], l[3]

        # filter the interaction according to experimental score, prevent doubles
        experimental_score = float(l[10])
        if experimental_score > score_threshold:
            score = (p1, p2, experimental_score)
            if score not in scores:
                scores.append(score)

    return scores

