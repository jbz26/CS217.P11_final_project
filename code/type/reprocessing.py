import re
def check_chemical(chem,compounds):
    for i in compounds:
        for temp in compounds[i]:
            if chem == temp['Formula']:
                return True
    return False
def check_equation(left,right,reacts):
    for i in reacts:
        if set(left) == set(i["if"]) and set(right) == set(i["then"]):
            return True    
    return False
def parse_chemical_equation(equation,compounds):
    # Tách phần trước và sau dấu mũi tên
    parts = equation.split("->")
    if len(parts) != 2 or isinstance(parts,str):
        return "error: Phương trình không hợp lệ.",-1
    inputs =  [compound.strip() for compound in parts[0].split("+")]
    outputs = [compound.strip() for compound in parts[1].split("+")]
    outputs = [re.sub(r'^\d*', '', compound) for compound in outputs]
    inputs = [re.sub(r'^\d*', '', compound) for compound in inputs]
    for i in inputs:
        if not check_chemical(i,compounds):
            return f"error: Phương trình không hợp lệ", -1
    for i in outputs:
        if not check_chemical(i,compounds):
            return f"error: Phương trình không hợp lệ", -1

    return  inputs, outputs
def parse_chemical_equation_with_missing(equation):
    # Tách phần trước và sau dấu mũi tên
    parts = equation.split("->")
    if len(parts) != 2 or isinstance(parts,str):
        return "error: Phương trình không hợp lệ.",-1
    inputs =  [compound.strip() for compound in parts[0].split("+")]
    outputs = [compound.strip() for compound in parts[1].split("+")]
    if '' in outputs:
        outputs.remove('')
    print(f"output2 {outputs}")
    outputs = [re.sub(r'^\d*', '', compound) for compound in outputs]
    inputs = [re.sub(r'^\d*', '', compound) for compound in inputs]
    return  inputs, outputs
def to_subscript(chemical):
    subscript_map = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
    return chemical.translate(subscript_map)
    
def print_equation_with_weight(weight,left,right,condition):
    left = left.copy()
    right = right.copy()
    check = [-1,-1,-1]
    xuc_tac = ""
    if condition!=-1:
        for i in condition:
            print("Condition:",i)
            if "t" == i:
                check[0] = 1
            elif "t:" in i:
                temp = i.split(":")[1]
                if "and" in temp:
                    output = temp.split("and")
                    output = [j.split("=")[1] for j in output]
                else:
                    output = temp
                check[0] = output
            if "đặc" == i:
                check[1] =1
                if "HNO3" in left:
                    temp2 = left.index("HNO3")
                    left[temp2] = left[temp2] + "(đặc)"
                elif "H2SO4" in left:
                    temp2 = left.index("H2SO4")
                    left[temp2] = left[temp2] + "(đặc)"
            elif "loãng" == i:
                check[2] = 1
                print(" aaaa", left)

                if "HNO3" in left:
                    temp2 = left.index("HNO3")
                    left[temp2] = left[temp2] + "(loãng)"
                elif "H2SO4" in left:
                    temp2 = left.index("H2SO4")
                    left[temp2] = left[temp2] + "(loãng)"
            if "xuctac:" in i:
                xuc_tac = i.split(":")[1]

    left = [to_subscript(chem) for chem in left]
    right = [to_subscript(chem) for chem in right]
    before = ["Phương trình phản ứng:"]
    print(check)    
    print(left)
    outputs = []
    for i in range(len(left)):
        sol = weight[i]
        if sol ==1:
            outputs.append( f"{left[i]}")
        else:
            outputs.append( f"{sol}{left[i]}")
    #print(left)
    if check[0]!=-1:
        if isinstance(check[0],list):
            if xuc_tac !="":
                temp23 = rf" \overset{{{"<= t <= ".join(check[0])}^0\,C , {xuc_tac}}} {{\longrightarrow}}"
            else:
                temp23 = rf" \overset{{{"<= t <= ".join(check[0])}^0\,C  }} {{\longrightarrow}}"
            #temp23 = rf"2NaCl + H_2SO_4 \overset{{\geq {temp222}^0\,C}}{{\longrightarrow}} Na_2SO_4 + 2HCl"

        elif check[0]==1:
            if xuc_tac!="":
                temp23 = rf"\overset{{t^0, {xuc_tac}}}{{\longrightarrow}}"
            else:
                temp23 = r"\overset{t^0}{\longrightarrow}"
        else:
            if xuc_tac!="":
                temp23 = rf"\overset{{{check[0]}^0\,C , {xuc_tac}}}{{\longrightarrow}}"
            else:
                temp23 = rf"\overset{{{check[0]}^0\,C}}{{\longrightarrow}}"

    else:
        temp23 = r"{\longrightarrow}"

    chemical_equation = "$" +  " + ".join(outputs) + temp23 + " "
    outputs = []
    for i in range(len(right)):
        sol = weight[i+len(left)]
        if sol ==1:
            outputs.append( f"{right[i]}")
        else:
            outputs.append( f"{sol}{right[i]}")
    chemical_equation += " + ".join(outputs)
    before.append(chemical_equation)
    return before
