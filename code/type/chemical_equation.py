import re
#from balance_equation import balace_equation
from .reprocessing import parse_chemical_equation,print_equation_with_weight,parse_chemical_equation_with_missing,check_chemical
from .balance_equation import balance_equation


def fill_chemical_equation(inputs,outputs,reacts):
    output = []
    if "?" in set(inputs):
        if "?" not in set(outputs):
            count_inp = inputs.count("?")
            temp_in = set(inputs)
            temp_in.remove("?")
            for i in reacts:
                set_then = set(i["then"])
                set_if = set(i["if"])
                if set_then == set(outputs):
                    if temp_in.issubset(set_if) and (len(temp_in) + count_inp == len(set_if)):                
                        output.append(i["id"]-1)
        else:
            count_inp = inputs.count("?")
            count_out = outputs.count("?")
            temp_in = set(inputs)
            temp_in.remove("?")
            temp_out = set(outputs)
            temp_out.remove("?")
            if(len(temp_in)==len(temp_out)==0):
                return -1
            for i in reacts:
                set_then = set(i["then"])
                set_if = set(i["if"])
                if temp_out.issubset(set_then) and (len(temp_out) + count_out == len(set_then)):
                    if temp_in.issubset(set_if) and (len(temp_in) + count_inp == len(set_if)):                
                        output.append(i["id"]-1)
            #print(output)
    else:   
        count_out = outputs.count("?")
        temp_out = set(outputs)
        if "?" in temp_out:
            temp_out.remove("?")
        for i in reacts:
            #print(temp_out,count_out)
            if set(inputs) == set(i["if"]):
                set_then = set(i["then"])
                if temp_out.issubset(set_then) and (len(temp_out) + count_out == len(set_then)) or  "?" not in outputs:
                    output.append(i["id"]-1)
    #print(output)
    if len(output)==0:
        return -1
    else:
        return output
def find_all_from_chemical_equation(input,reacts):
    rules = set()
    A = input.copy()
    A_old = input.copy()
    while True:
        for i in reacts:
            if i["id"] not in rules and set(i["if"]) <= A:
                A |= set(i["then"])
                rules.add(i["id"]-1)
        if A == A_old:
            return rules
        else:
            A_old = A.copy()

def solve_chemical_equation(input_string,reacts,compounds):
    
    inputs , outputs = parse_chemical_equation_with_missing(input_string)
    print(inputs,outputs)
    for i in inputs:
        if not check_chemical(i,compounds) and i !="?":
            return f"error: Không tìm thấy công thức chất {i}!"
    for i in outputs:
        if not check_chemical(i,compounds) and i !="?":
            return f"error: Không tìm thấy công thức chất {i}!"
    id = fill_chemical_equation(inputs,outputs,reacts)
    if id!=-1:
        outputs = []
        for i in id:
            print(i)
            left = reacts[i]["if"]
            right = reacts[i]["then"]
            weight = balance_equation(left,right,mode="short")
            if "error" in weight:
                return "error: Không thể cân bằng phương trình"
            if "condition" in reacts[i].keys():
                condition = reacts[i]["condition"]
            else:
                condition = -1
            outputs.extend(print_equation_with_weight(weight,left,right,condition))
        return outputs
    else:
        return "error: Không thể tìm thấy phương trình"
