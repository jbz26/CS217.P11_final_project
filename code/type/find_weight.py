import re
import sympy as sp
from .chemical_equation import fill_chemical_equation
from .reprocessing import to_subscript,check_chemical,print_equation_with_weight
from .balance_equation import balance_equation
def extract_all_substances_in_sentences(problem_text):
    problem_text.replace(".",",")
    # Biểu thức để tìm các chất kèm khối lượng hoặc không
    pattern_no_mass = r'\s*\[([A-Za-z0-9\(\)]+)\]'
    pattern_with_mass = r'(\d+(?:,\d+)?)\s+gam\s+([^\[\]]+)?\s*\[([A-Za-z0-9\(\)]+)\]'
    temp = problem_text.split("Tính")[0]
    reactant_text= temp.split("thu được")[0]
    product_text = temp.split("thu được")[1]
    # Tìm chất có khối lượng
    react = re.findall(pattern_with_mass, reactant_text)
    react_substances = {
            match[2]: float(match[0].replace(",","."))
            for match in react
        }
    print(react)
    product = re.findall(pattern_with_mass, product_text)
    print(product)

    product_substances = {
            match[2]: float(match[0].replace(",","."))
            for match in product
        }
    # Tìm tất cả các chất
    matches_all = re.findall(pattern_no_mass, problem_text)
    all_substances = set(matches_all)
    react = set([match[2] for match in react])
    product = set([match[2] for match in product])
  
    find_substances = all_substances - (react.union(product))
    react = re.findall(pattern_no_mass, reactant_text)
    product = re.findall(pattern_no_mass, product_text)
    
    return react_substances, product_substances, react,product, find_substances

def find_weight(problem_text,reacts,compounds):
    react_substances,product_substances, react, product, find_substances = extract_all_substances_in_sentences(problem_text)
    if len(find_substances)==0:
        return f"error: Khối lượng các chất đã đầy đủ, không cần tính toán!"
    if len(find_substances)>1:
        return f"error: Có trên 1 chất còn thiếu khối lượng, không thể áp dụng định luật bảo toàn khối lượng!"
    if len(react) ==0:
        return f"error: Vui lòng điền thông tin các chất phản ứng đầy đủ!"
    if len(product) ==0:
        return f"error: Vui lòng điền thông tin các chất phản tạo thành đầy đủ!"
    for i in react:
        if not check_chemical(i,compounds):
            return f"error: Không tìm thấy công thức chất {i}!"
        print(i)
    for i in product:
        if not check_chemical(i,compounds):
            return f"error: Không tìm thấy công thức chất {i}!"
    id = fill_chemical_equation(react,product,reacts)
    if id==-1:
        return "error: Không tìm thấy phương trình!"
    
    output = print_equation_without_weight(reacts[id[0]])
    left = " + ".join(f"m{symbol}" for symbol in react)
    right = " + ".join(f"m{symbol}" for symbol in product)
    temp = react_substances.copy()
    temp.update(product_substances) 
    temp1 = {f"m{key}": value for key, value in temp.items()}
    output.append("Áp dụng định luật bảo toàn khối lượng, ta có:")
    output.append(f"${to_subscript(str(left))} = {to_subscript(str(right))}")
    '''
    print(left,right)
    temp_left = left.replace("(", "").replace(")", "")
    temp_right = right.replace("(", "").replace(")", "")
    print(temp_left,temp_right)
    equation = sp.Eq(sp.sympify(temp_left), sp.sympify(temp_right))
    target = sp.symbols(f"m{list(find_substances)[0].replace("(", "").replace(")", "") }")
    print(equation,target)
    solution = sp.solve(equation, target)
    '''
    print(temp)
    target = list(find_substances)[0]
    print(react,product)
    print(f"\t {target}")
    output.append(f"Giải phương trình:")
    if target in product:
        right_solve = " + ".join(f"m{symbol}" for symbol in react)
        temp_solve = " - ".join([f"m{i}" for i in product if i != target])
        right_solve =right_solve + " - " + temp_solve
    else:
        right_solve = " + ".join(f"m{symbol}" for symbol in product)
        temp_solve = " - ".join([f"m{i}" for i in react if i != target])
        right_solve =right_solve + " - " + temp_solve
    mass_left = 0
    mass_right = 0
    for i in temp:
        if i in react and i!=target:
            mass_left +=temp[i]
        elif i!=target:
            mass_right+=temp[i]
    if target in product:
        value = mass_left - mass_right
    else:
        value = mass_right - mass_left
    value = round(value,4)
    print(right_solve)
    output.append(f"$m{to_subscript(list(find_substances)[0])} = {to_subscript(right_solve)}")

    # Thay thế các giá trị đã biết vào phương trình và tính kết quả
    output.append(f"$ m{to_subscript(list(find_substances)[0])} = {value}")

    output.append(f" Vậy khối lượng của {to_subscript(str(target)[1:])} là: {value} (gram)")
    if (value<=0):
        output.append(f"#### Khối lượng của chất không thể bé hơn hoặc bằng không, hãy kiểm tra lại tính chính xác của đề bài toán!")
    return output
def print_equation_without_weight(react):
    left = react["if"].copy()
    right = react["then"].copy()
    weight = balance_equation(left,right,"short")
    for i in range(len(right)):
        right[i] = right[i]
    if "condition" in react.keys():
        condition = react["condition"]
    else:
        condition = -1
    return print_equation_with_weight(weight,left,right,condition)