import re
import sympy as sp
from .chemical_equation import fill_chemical_equation, print_chemical_equation,check_chemical
from .reprocessing import to_subscript
def extract_all_substances_in_sentences(problem_text):
    problem_text.replace(".",",")
    # Biểu thức để tìm các chất kèm khối lượng hoặc không
    pattern_no_mass = r'\s+\(([A-Za-z0-9]+)\)'
    pattern_with_mass = r'(\d+(?:\,\d+)?)\s+gam\s+([^\d\(\)]+)?\s*\(([A-Za-z0-9]+)\)'
    temp = problem_text.split("Tính")[0]
    reactant_text= temp.split("thu được")[0]
    product_text = temp.split("thu được")[1]
    # Tìm chất có khối lượng
    react = re.findall(pattern_with_mass, reactant_text)
    react_substances = {
            match[2]: float(match[0].replace(",","."))
            for match in react
        }
    product = re.findall(pattern_with_mass, product_text)
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
    for i in react:
        if not check_chemical(i,compounds):
            return f"error: Không tìm thấy công thức chất {i}!"
    for i in product:
        if not check_chemical(i,compounds):
            return f"error: Không tìm thấy công thức chất {i}!"
    id = fill_chemical_equation(react,["?"],reacts)
    if id==-1:
        return "error: Không tìm thấy phương trình!"
    
    output = print_chemical_equation(reacts[id[0]])
    left = " + ".join(f"m{symbol}" for symbol in react)
    right = " + ".join(f"m{symbol}" for symbol in product)
    temp = react_substances.copy()
    temp.update(product_substances) 
    temp1 = {f"m{key}": value for key, value in temp.items()}
    out_temp = f"Áp dụng định luật bảo toàn khối lượng, ta có:\n \t{left} = {right}"
    output +="\n" + out_temp 
    equation = sp.Eq(sp.sympify(left), sp.sympify(right))
    target = sp.symbols(f"m{list(find_substances)[0] }")

    solution = sp.solve(equation, target)
    out_temp = f"Giải phương trình: \n \t{target} = {solution[0]}"
    output +="\n" + out_temp 

    # Thay thế các giá trị đã biết vào phương trình và tính kết quả
    value = solution[0].subs(temp1)
    out_temp = f" \t{target} = {value.round(4)}"
    output +="\n" + out_temp 

    out_temp = f" Vậy khối lượng của {target} là: {value.round(4)} (gram)"
    output +="\n" + out_temp
    #print(output)
    return output
