from json import load
from urllib.parse import urlparse
from sys import exit


print("Filtering: how many entries of a particular website are required before being included in the output file? Any amount below this will be omitted. 30 is in my experience a nice starting point: ", end = "")
def ThresholdPrompt():

    try:
        threshold = int(input())
    except ValueError:
        print("Input must be a natural number. Try again: ", end = "")
        threshold = ThresholdPrompt()
    
    print("\n")
    return threshold

threshold = ThresholdPrompt()
rank = {}


try:
    with open("chrome_history.json", encoding="UTF-8") as f: # open json file exported from browser extension: https://chrome.google.com/webstore/detail/export-historybookmarks-t/dcoegfodcnjofhjfbhegcgjgapeichlf
        data = load(f)

        for e in data: # Iterate through each website visit
            url = e["url"] # Strip away unnecessary information 
            website = (urlparse(url).hostname) # Remove everything but the hostname (ish). This isn't perfect, more info here: https://stackoverflow.com/questions/1521592/get-root-domain-of-link 

            if website in rank: # If website already present in dict, increase count. If not, add a new entry.
                rank[website] += 1
            
            else:
                rank[website] = 1

except FileNotFoundError:
    print("Could not find file. Make sure the chrome_history.json file is placed in this file's parent directory.")
    exit()



# Sorting based on number of visits. Kinda unnecessary since it is most logical to analyze this data in excel or similar.
sorted_dict = {}
sorted_keys = sorted(rank, key=rank.get, reverse=True) 

for w in sorted_keys:
    sorted_dict[w] = rank[w]


#Saving
csv = "" # String to be saved to csv file

for site in sorted_dict: # Filtering out unfrequent sites.
    if sorted_dict[site] > threshold:
        csv = csv + (f"{site}; {sorted_dict[site]}\n") 

with open('rank.csv', 'w') as f: # Exporting to csv file
    f.write(csv)
