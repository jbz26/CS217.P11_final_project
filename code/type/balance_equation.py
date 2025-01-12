import re
import math
from functools import reduce
from sympy import symbols, Eq, solve, Ne,linsolve,solve_undetermined_coeffs
import sympy as sp
import numpy as np
from .search_chemical_info import parse_chemical_formula
from .reprocessing import parse_chemical_equation,print_equation_with_weight,check_equation
def merge_two_dict(dict1, dict2):
    for i in dict2:
        if i in dict1.keys():
            dict1[i]+=dict2[i]
        else:
            dict1[i]=dict2[i]
    return dict1
def balance_equation(left, right, mode):
    dict_left = {}
    left_chems = []
    right_chems = []
    for i in left:
        temp = parse_chemical_formula(i)
        left_chems.append(temp)
        dict_left  = merge_two_dict(dict_left,temp)
    for i in right:
        temp = parse_chemical_formula(i)
        right_chems.append(temp)
    left_matrix_dict = {}
    for element in dict_left:
        left_temp = []
        for chem in left_chems:
            if element in chem.keys():
                left_temp.append(chem[element])
            else:
                left_temp.append(0)
        for chem in right_chems:
            if element in chem.keys():
                left_temp.append(-chem[element])
            else:
                left_temp.append(0)
        left_matrix_dict[element] = left_temp
    vars = []
    outputs = []
    #print(f"right {right}")
    for i in range(len(left) +len(right)):
        vars.append(chr(97+i))
    #print(f"vars: {vars}" )
    outputs.append(f"Gọi hệ số cân bằng của các chất ( {', '.join(left)}, {', '.join(right)}) lần lượt là: {', '.join(vars)}"  )
    outputs.append("Ta có phương trình phản ứng: ")
    #print(vars)
    outputs.extend(print_equation_with_weight(vars,left,right,-1))
    outputs.append("Áp dụng định luật bảo toàn nguyên tố, ta được: ")
    weight,outputs = solve_math_equation(left_matrix_dict,vars,outputs)
    if type(outputs)==str:
        print(weight)

        return weight
    if mode == "short":
        return weight
    outputs.extend(print_equation_with_weight(weight,left,right,-1))
    return outputs

def solve_math_equation(matrix_dict,vars,outputs):
    coefficients = np.array(list(matrix_dict.values()))
    #print(coefficients)
    ele = np.array(list(matrix_dict.keys()))
    #print(ele,vars)
    # Tự động tạo biến dựa trên số cột của ma trận
    num_variables = len(coefficients[0])
    variables = symbols(' '.join(vars))  # Từ 'a' đến 'z'

    # Tạo hệ phương trình
    equations = [
        Eq(sum(coefficients[i][j] * variables[j] if coefficients[i][j]>0 else 0 for j in range(num_variables)), 
           sum(-coefficients[i][j] * variables[j] if coefficients[i][j]<0 else 0 for j in range(num_variables)))
        for i in range(len(coefficients))
    ]
    equations2 = [
        Eq(sum(coefficients[i][j] * variables[j]  for j in range(num_variables)), 0)
        for i in range(len(coefficients))
    ]
    functs = []
    for i in range(len(ele)):
        outputs.append(f"Bảo toàn nguyên tố {ele[i]}: ")
        #print(equations[i])
        equa =equations[i]
        if equa != True:
            funct = f"${equa.lhs} = {equa.rhs}"
            outputs.append(funct)
            functs.append(f"${equations2[i].lhs} = 0" )
    solution = solve_equation(coefficients)
    if not solution or "error" in solution:
        return "error: Không có nghiệm cho hệ phương trình.", "error"
        # Giải hệ phương trình
    """
    solution = linsolve(equations, variables)
    print(solution)
    filtered_solutions = [sol for sol in solution if any(value != 0 for value in sol)]
    print(filtered_solutions)
    if not solution :
        return "error: Không có nghiệm cho hệ phương trình.", "error"
    solution = list(solution)[0]  # Lấy nghiệm

    if any(term.free_symbols for term in solution):
        free_var = next(iter(solution[0].free_symbols))  # Lấy biến tự do đầu tiên
        substitutions = {free_var: 1}  # Gán giá trị mặc định, ví dụ: 1
        solution = [term.subs(substitutions) for term in solution]
    print(solution)
    # Tìm bội số chung nhỏ nhất (LCM) để chuyển nghiệm về số nguyên
    lcm_value = sp.lcm([term.q if hasattr(term, 'q') else 1 for term in solution])
    solution = [int(term * lcm_value) for term in solution]
    """

    outputs.append("Hệ phương trình:")
    temp = r"$\begin{align*}"
    
    temp += r" \\ ".join(functs) + r"\end{align*}"
    outputs.append(temp)
    outputs.append("Nghiệm của hệ:")
    temp = "$"
    for var, value in zip(vars, solution):
        temp +=f"{var} = {value}, "
    outputs.append(temp)
    return solution, outputs

def solve_equation(A):
    rank = np.linalg.matrix_rank(A)
    U, S, Vt = np.linalg.svd(A)
    null_space = Vt[rank:].T
    if null_space.shape[1] == 0:
        return "error: Phương trình không thể cân bằng!"
    one = np.abs(null_space[:, 0])
    #print(one)
    integer_solutions = []
    max_iterations = 100000  # Prevent infinite loops

    for i in range(1, max_iterations + 1):
        candidate = one * i
        #print(candidate)
        if np.allclose(candidate, np.round(candidate)):  # Kiểm tra nếu là số nguyên
            integer_solutions = np.round(candidate).astype(int)
            ucln_all = reduce(math.gcd, integer_solutions)
            print(ucln_all)
            integer_solutions = [int(i/ucln_all) for i in integer_solutions]
            return integer_solutions
    print(integer_solutions)
    return [1 for i in range(len(one))]
def balance_solve(equation,compounds,reacts):
    left, right = parse_chemical_equation(equation,compounds)
    if "error" in left:
        return "error: Vui lòng nhập phương trình chính xác!"
    if not check_equation(left,right,reacts):
        return "error: Không tồn tại phương trình trên!"
    return balance_equation(left.copy(),right.copy(),mode = "full")
'''
test = "HNO3 + FeCO3  -> Fe(NO3)3 + NO2 +CO2  +H2O"
#test = "NaOH + HCl -> NaCl + H2O"
out = balance_solve(test)
for i in out:
    print(i)

''' 