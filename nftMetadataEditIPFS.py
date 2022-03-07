import json
import os

# Make sure that the directory points to the metadata and 
# find the imageCID folder in your IPFS file provider (e.g. Pinata)
directory = "./Output/metadata"
imagesCIDs = "ipfs://__CID__/"

# Get amount of json files inside the metadata folder
path, dirs, files = next(os.walk(directory))
file_count = len(files)

print ("Modifying metadata...")
# Modify each json file with the proper image IPFS link.
for i in range(1, file_count):
    with open(directory + "/" + str(i) + ".json", "r+") as f:
        print ("Modifying " + str(i) + ".json")
        data = json.load(f)
        data["image"] = imagesCIDs + str(i) + ".png"
        f.seek(0)
        json.dump(data, f)
        f.truncate()
        
print ("Process Completed. Modified " + str(file_count) + " metadata files.")