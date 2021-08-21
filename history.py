import json
from urllib.parse import urlparse

rank = {}

with open("history.json", encoding="UTF-8") as f: # open json file exported from browser extension: https://chrome.google.com/webstore/detail/export-historybookmarks-t/dcoegfodcnjofhjfbhegcgjgapeichlf
    data = json.load(f) # parse file

    for e in data: # Iterate through each website visit
        url = e["url"] # Strip away unnecessary information 
        website = (urlparse(url).hostname) # Remove everything but the hostname (ish). This isn't perfect, more info here: https://stackoverflow.com/questions/1521592/get-root-domain-of-link 

        if website in rank: # If website already present in dict, increase count. If not, add a new entry.
            rank[website] += 1
        
        else:
            rank[website] = 1


# Sorting based on number of visits. Kinda unnecessary since it is most logical to analyze this data in excel or similar.
sorted_dict = {}
sorted_keys = sorted(rank, key=rank.get, reverse=True) 

for w in sorted_keys:
    sorted_dict[w] = rank[w]


#Saving
csv = "" # String to save to csv file

for site in sorted_dict: # Filtering out unfrequent sites.
    if sorted_dict[site] > 30:
        csv = csv + (f"{site}; {sorted_dict[site]}\n") 

with open('rank.csv', 'w') as f: # Exporting to csv file
    f.write(csv)
