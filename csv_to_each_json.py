import os, json
import pandas as pd

mainCsv = pd.read_csv("variant_data.csv")

# Detect and drop the columns with the keywords "Tickets" and "Odds"
droppedCsv = mainCsv[mainCsv.columns.drop(list(mainCsv.filter(regex="Tickets")))]
droppedCsv = droppedCsv[droppedCsv.columns.drop(list(droppedCsv.filter(regex="Material")))]
droppedCsv = droppedCsv[droppedCsv.columns.drop(list(droppedCsv.filter(regex="Odds")))]
    # This leaves a CSV only containing the attributes and their variants as first column
    # The variant are not indexes, they are the first column itself.

def jsonGenerator(index, attributesList):
     
    json_file = {
        "name": "NFT #" + str(index+1),
        "description": "The Description of the NFT project...", 
        "image": "https://rememberToEditThis", 
        "attributes": [ ], 
    }
    
    json_file["attributes"] = attributesList
      
    with open("./Output/" + str(index+1) + ".json", "w+" ) as f:
        json_dump = json.dump(json_file, f)

directory = "./Output/"
path, dirs, files = next(os.walk(directory))
file_count = len(files)

print ("Starting generation. Files to generate: " + str(file_count))

# Generate the Json File of each row with the
attributesList = []
for row in droppedCsv.index:
   
    attributesList.clear()

    for column in droppedCsv.columns:
        columnName = column.partition("Name")[0]
        if columnName == "Variant":
            continue

        columnName =  columnName.strip()  
        # print (columnName, row)
        trimmedCell = droppedCsv[column].iloc[row].partition("Variant")[0]

        traitType = columnName
        traitValue = trimmedCell
        attributesList.append({"trait_type": traitType, "value": traitValue})

    jsonGenerator(row, attributesList)

print ("Generated Successfuly " + str(file_count) + " metadata files.")
