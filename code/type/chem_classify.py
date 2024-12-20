import json
import os
from .chemical_equation import check_chemical,fill_chemical_equation,find_all_from_chemical_equation
from .balance_equation import balance_equation
from .reprocessing import print_equation_with_weight,to_subscript
folder = 'data'
# Open and read the JSON file
with open(os.path.join(folder,'Chemical compounds.json') , 'r') as file:
    compounds = json.load(file)
with open(os.path.join(folder, 'Reacts_with_IDs.json'), 'r') as file:
    reacts = json.load(file)
def find_physical(input,compounds):
    for i in compounds:
        for j in compounds[i]:
            if j["Formula"] == input:
                return j
def find_same_reactants(inputs,reacts):
    all_reacts = set()
    for i in inputs:
        temp =  find_all_reactants(i,reacts)
        if (len(all_reacts) == 0):
            all_reacts.update(temp)
        else:
            all_reacts = all_reacts.intersection(temp)
    return all_reacts
def find_all_reactants(input,reacts):
    reactants = set()
    for i in reacts:
        if input in i["if"]:
            reactant = [x for x in i["if"] if x!=input]
            reactants.update(reactant)
    return reactants
def find_diff_reactants(inputs,reacts):
    new_dict = {}
    same = find_same_reactants(inputs,reacts)

    for chem in inputs:
        for i in reacts:
            if chem in i["if"] and len(i['if'])==2:
                temp = {}
                key = (set(i["if"]) - set([chem])).pop()
                #print(key)
                if key not in same:
                    temp[key] = i["id"]
                    if chem in new_dict.keys():
                        new_dict[chem].update(temp)
                    else:
                        new_dict[chem] = dict(temp)
    return new_dict
    #print(new_dict)
def get_products(new_dict,compounds):
    for i in new_dict:
        for j in new_dict[i]:
            #print(j)
            check_1 = check_chem(j,compounds)
            if (check_1==-1):
                react_id = new_dict[i][j]
                products = reacts[react_id-1]["then"]
                check =check_product(products,compounds)
                if check !=-1:
                    return i,j,check
                
def check_product(products,compounds):
    for i in products:
        #print(i)
        output = check_chem(i,compounds)
        #print(output)
        if output!=-1:
            return output
    return -1
def compare_by_PH(inputs,compounds):
    new_dict = {}
    red = set()
    colorless = set()
    blue = set()
    for chem in inputs:
        phy = find_physical(chem,compounds)
        new_dict[chem] = phy
        if phy["Type"] =="Base":
            blue.add(chem)
        elif phy["Type"] == "Acid":
            red.add(chem)
        else:
            colorless.add(chem)
    return red,colorless,blue

def check_chem(chem,compounds):
    phy = find_physical(chem,compounds)
    #print(phy,chem)
    if phy["State"] == "Gas":
        return phy,1
    if phy["Solubility"] not in [ "Soluble","Universal solvent"]:
        return phy, 2
    return -1

def classify_chems(inputs,reacts,compounds):
    temp_inputs = inputs.copy()
    tab = "" 
    tab2 = " - "
    outputs = [f" ##### Các chất cần nhận biết {", ".join([to_subscript(i) for i in temp_inputs])}"]
    #print(temp_inputs)
    acid, other, hidroxit = compare_by_PH(temp_inputs,compounds)
    print(acid,other,hidroxit)
    outputs.append(f"Trích mẫu thử từ các chất và đánh số thứ tự.")
    if (len(acid)!=0 and len(hidroxit)!=0 ) or (len(acid)!=0 and len(other)!=0) or (len(hidroxit)!=0 and len(other) !=0):
        outputs.append(" ##### Dùng quỳ tím làm thuốc thử: ")
    if len(acid) == 1:
        #chem = acid.pop()
        outputs.append(f"{tab}Mẫu thử nào làm quỳ tím chuyển sang màu đỏ thì dung dịch đó là {to_subscript(list(acid)[0])} ")
    if len(other) == 1:
        #chem = other.pop()
        outputs.append(f"{tab}Mẫu thử không làm quỳ tím đổi màu là {to_subscript(list(other)[0])}")
    if len(hidroxit) == 1:
        #chem = hidroxit.pop()
        outputs.append(f"{tab}Mẫu thử nào làm quỳ tím chuyển sang màu xanh thì dung dịch đó là {to_subscript(list(hidroxit)[0])}")
    print(acid,other,hidroxit)

    if len(other)>1:
        if len(acid) !=0 or len(hidroxit) !=0 :
            outputs.append(f"{tab}Mẫu thử không làm quỳ tím đổi màu là {", ".join([to_subscript(i) for i in other])}")
        outputs.extend(classify_chems_on_type(other,reacts,compounds,tab2))
        outputs.append("-"*100)
    if len(hidroxit)>1:
        if len(acid) !=0 or len(other) !=0 :
            outputs.append(f"{tab}Mẫu thử nào làm quỳ tím chuyển sang màu xanh thì dung dịch đó là {", ".join([to_subscript(i) for i in hidroxit])}")
        outputs.extend(classify_chems_on_type(hidroxit,reacts,compounds,tab2))
    if len(acid)>1:
        if len(hidroxit) !=0 or len(other) !=0 :
            outputs.append(f"{tab}Mẫu thử nào làm quỳ tím chuyển sang màu đỏ thì dung dịch đó là {", ".join([to_subscript(i) for i in acid])}")
        print(acid)
        outputs.extend(classify_chems_on_type(acid,reacts,compounds,tab2))
    print(acid,other,hidroxit)

    return outputs
def classify_chems_on_type(chems,reacts,compounds,tab):
    outputs = []
    chems2 = chems.copy()
    outputs.append(f"Phân biệt :  {", ".join([to_subscript(i) for i in chems2])}")
    while len(chems2)>1:
        #print(temp_inputs)    
        new_dict = find_diff_reactants(chems2,reacts)
        temp = get_products(new_dict,compounds)
        #print(temp)
        reactant = temp[1]
        pro = temp[2][0]
        if (temp[2][1]) ==2:
            product = f"kết tủa màu {pro["Color"]}"
            special = {pro["Formula"]: "↓"}
        else:
            product = f"khí thoát ra"
            special = {pro["Formula"]: "↑"}
        outputs.append(f"{tab}Cho {reactant} vào {len(chems2)} dung dịch, mẫu thử nào xuất hiện {product} thì dung dịch ban đầu là {to_subscript(temp[0])} ")
        e_inputs = set([temp[0],reactant] )
        id = fill_chemical_equation(e_inputs,"",reacts)
        outputs.extend(print_equation_without_weight(reacts[id[0]],special))
        chems2.discard(temp[0])

    outputs.append(f"{tab}Còn lại là: {to_subscript(chems2.pop())}")
    return outputs
def print_equation_without_weight(react,special):
    left = react["if"].copy()
    right = react["then"].copy()
    weight = balance_equation(left,right,"short")
    for i in range(len(right)):
        if right[i] in special.keys():
            right[i] = right[i] + special[right[i]]
    return print_equation_with_weight(weight,left,right)
#inputs = set(['BaSO4' , "Na2SO4","NaOH","NaCl"])
#inputs = set(['HCl' , "NaOH","Na2SO4","NaCl"])


#inputs = set(['HCl' , "NaOH","H2SO4","Na2CO3"])


#inputs = set(['NaCl' , "NaOH","Ba(OH)2","BaCl2"])

#inputs = set(['AgNO3' , "Na2SO4","K2CO3","BaCl2"])

#inputs = set(['KNO3' , "Cu(NO3)2","AgNO3","Fe(NO3)3"])
def parse_chems_from_string(input,compounds):
    temp = input.strip().split(",")
    #print(temp)
    if len(temp)<2:
        return f"error: Vui lòng nhập từ hai chất trở lên, ngăn cách bởi dấu phẩy (,)!"
    for i in range(len(temp)):
        temp[i] = temp[i].strip()
        if not check_chemical(temp[i],compounds):
            return f"error: Không tìm thấy chất {temp[i]} !"
    return temp

#print(find_same_reactants(inputs,reacts))
#classify_chems(inputs,reacts,compounds)
def solve_classify_chems(inputs,reacts,compounds):
    inputs = parse_chems_from_string(inputs,compounds)
    #print(inputs)
    if "error" in inputs:
        return inputs
    else:
        return classify_chems(inputs,reacts,compounds)
#inputs = "Na2SO4, NaCl, H2SO4, HCl"
#print(solve_classify_chems(inputs,reacts,compounds))
#find_diff_reactants(inputs,reacts)
#print(compare_two_chems("BaSO4", "BaCO3",compounds))

'''
def compare_two_chems(chems1, chems2,compounds):
    chems1 = find_physical(chems1,compounds)
    chems2 = find_physical(chems2,compounds)
    types = ["Base","Acide", "Salt"]
    if chems1["Type"] in types and chems2["Type"] in types and chems2["Type"] !=chems1["Type"]:
        return True, 0
    if chems1["Color"] !=chems2["Color"]:
        return True,1
    if chems1["Solubility"] !=chems2["Solubility"]:
        return True,2
    if chems1["State"] != chems2["State"] and "Gas" in [chems1["State"],chems2["State"]]:
        return True, 3
    return False, -1
def compare_by_solubility(inputs,compounds):
    new_dict = {}
    solub = set()
    not_solub = set()
    slow_solub = set()
    for chem in inputs:
        phy = find_physical(chem,compounds)
        new_dict[chem] = phy
        if phy["Solubility"] == "Soluble":
            solub.add(chem)
        elif phy["Solubility"] == "Slightly soluble":
            slow_solub.add(chem)
        else:
            not_solub.add(chem)

    return solub,not_solub,slow_solub
'''