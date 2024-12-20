import json

folder = 'data'
# Open and read the JSON file
with open(folder + "\\" + 'Chemical compounds.json', 'r') as file:
    compounds = json.load(file)
with open('mydata.json', 'r') as file:
    reacts = json.load(file)



'''
print(len(reacts)) #1254 phản ứng
reacts_chems = set()
for i in reacts:
    reacts_chems.update([j for j in i["if"]])
    reacts_chems.update([j for j in i["then"]])
print(len(reacts_chems))

compounds_set = set()
for i in compounds:
    for j in compounds[i]:
        compounds_set.add(j["Formula"])
print(len(compounds_set))
print(len(compounds_set - reacts_chems))
diff = list(reacts_chems - compounds_set)
print(diff)
print(len(diff))
for i in range(len(diff)//10):
    print(diff[i*10:(i+1)*10])
'''