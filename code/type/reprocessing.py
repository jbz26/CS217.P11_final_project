import re
def check_chemical(chem,compounds):
    for i in compounds:
        for temp in compounds[i]:
            if chem == temp['Formula']:
                return True
    return False
def parse_chemical_equation(equation):
    # Tách phần trước và sau dấu mũi tên
    parts = equation.split("->")
    if len(parts) != 2:
        return "error: Phương trình không hợp lệ."
    inputs =  [compound.strip() for compound in parts[0].split("+")]
    outputs = [compound.strip() for compound in parts[1].split("+")]
    outputs = [re.sub(r'^\d*', '', compound) for compound in outputs]
    inputs = [re.sub(r'^\d*', '', compound) for compound in inputs]
    return  inputs, outputs
def parse_chemical_equation_with_missing(equation):
    # Tách phần trước và sau dấu mũi tên
    print(equation)
    parts = equation.split("->")
    if len(parts) != 2:
        return "error: Phương trình không hợp lệ."
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
    
def print_equation_with_weight(weight,left,right):
    left = [to_subscript(chem) for chem in left]
    right = [to_subscript(chem) for chem in right]
    before = ["Phương trình phản ứng:"]
    outputs = []
    for i in range(len(left)):
        sol = weight[i]
        if sol ==1:
            outputs.append( f"{left[i]}")
        else:
            outputs.append( f"{sol}{left[i]}")
    #print(left)
    chemical_equation = "$" +  " + ".join(outputs) + " → "
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
