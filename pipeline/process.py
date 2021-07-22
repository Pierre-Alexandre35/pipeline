import json
import os

from settings import (
    RESULTS_FOLDER,
    DRUGS_FILENAME,
    CLINICAL_TRIALS_FILENAME,
    PUBMED_FILENAME,
    GRAPH_NAME
)  
    


def generate_mention_drug_item(type, drug_id, drug_name, title, journal, date):
    return {
        'type' : type,
        'drug_id' : drug_id,
        'drug_name' : drug_name,
        'title' : title,
        'journal' : journal,
        'date' : date,
    }
    

def generate_graph(input_dic, drugs_dic):
    mention_drug_items = []
    for id, journal in input_dic.items():
        target_item = journal['title']
        for id, drug in drugs_dic.items():
            keyword = drug['drug']
            if keyword.lower() in target_item.lower():
                new_mention_item = generate_mention_drug_item('pubmed', 
                                      drug['atccode'], 
                                      keyword, 
                                      target_item,
                                      journal['journal'],
                                      journal['date']
                                    )
                mention_drug_items.append(new_mention_item)
    
    json_result = json.dumps(mention_drug_items)
    print(mention_drug_items)
    with open(RESULTS_FOLDER + GRAPH_NAME, 'w') as f:
        f.write(json_result)

        
        
def process_data(storage_path):
    drugs = {
  "0": { "atccode": "A04AD", "drug": "DIPHENHYDRAMINE" },
  "1": { "atccode": "S03AA", "drug": "TETRACYCLINE" },
  "2": { "atccode": "V03AB", "drug": "ETHANOL" },
  "3": { "atccode": "A03BA", "drug": "ATROPINE" },
  "4": { "atccode": "A01AD", "drug": "EPINEPHRINE" },
  "5": { "atccode": "6302001", "drug": "ISOPRENALINE" },
  "6": { "atccode": "R01AD", "drug": "BETAMETHASONE" }
}
    for publication_type in os.listdir(storage_path):
        path = storage_path + str(publication_type)
        with open(path) as json_file:
            data = json.load(json_file)
            generate_graph(data, drugs)