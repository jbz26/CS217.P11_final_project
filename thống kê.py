import json
import os

folder = 'data'
# Open and read the JSON file
with open(os.path.join(folder,'Chemical compounds.json') , 'r') as file:
    compounds = json.load(file)
with open(os.path.join(folder, 'Reacts_with_IDs.json' ), 'r') as file:
    reacts = json.load(file)

with open( 'new.json' , 'r') as new_file:
    new = json.load(new_file)

i = 1
count =0
for temp in new:
    if temp["id"] != i:
        count+=1
        temp["id"] = i
    i+=1
    if "weight" in temp.keys():
        temp.pop("weight")
print(count)
i = 1
count =0
for temp in new:
    if temp["id"] != i:
        count+=1
        temp["id"] = i
    i+=1
print(count)
modified_json = json.dumps(new,indent=4)
with open( 'new.json' , 'w') as new_file:
    #new = json.load(file)
    new_file.write(modified_json)
'''


print(len(reacts)) #1254 phản ứng
reacts_chems = set()
for i in reacts:
    reacts_chems.update([j for j in i["if"]])
    reacts_chems.update([j for j in i["then"]])


compounds_set = set()
for i in compounds:
    for j in compounds[i]:
        compounds_set.add(j["Formula"])
print("com",len(compounds_set))
print(len(compounds_set - reacts_chems))
diff = list(reacts_chems - compounds_set)
print(diff)
print(len(diff))
for i in range(len(diff)//10):
    print(diff[i*10:(i+1)*10])
'''