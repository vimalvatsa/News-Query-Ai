from Constants.constants import TypeOfSearch
import re

# def create_search_expresion(searching_doc_id, type_of_search):
#     if type_of_search == TypeOfSearch.default:
#         searching_doc_id = int(searching_doc_id)
#         expr = f"document_id in {[searching_doc_id]}"
#     elif type_of_search == TypeOfSearch.vault_model:
#         expr = f"unique_id in {[searching_doc_id]}"
#     return expr

def create_search_expression(type_of_search, query):
    #Extracting headings from query to perform search on
    pattern = r'heading - (.*?) accurately'
    matches = re.search(pattern, query, re.IGNORECASE)
    
    if matches:
        headings = matches.group(1).split(' ans ')
        headings = [heading.strip() for heading in headings] #Cleaning up headings
        
        if type_of_search == TypeOfSearch.default:
            expr = f"headings in {headings}"
        elif type_of_search == TypeOfSearch.vault_model:
            expr = f"headings in {headings}"
    else:
        #Fallback if no headings found
        expr = "1=0" #No valid search expression if no headings are found
    
    return expr