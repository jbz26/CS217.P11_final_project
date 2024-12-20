import json
import os
from .type.chemical_equation import solve_chemical_equation
from .type.find_weight import find_weight
from .type.search_chemical_info import  cal_atomic_mass
from .type.balance_equation import balance_solve
from .type.chem_classify import solve_classify_chems
folder = 'data'
# Open and read the JSON file
with open(os.path.join(folder,'Chemical compounds.json') , 'r') as file:
    compounds = json.load(file)
with open(os.path.join(folder, 'Reacts_with_IDs.json', 'r')) as file:
    reacts = json.load(file)
    
def solve(id,input):
    if id ==1:
        return cal_atomic_mass(input,compounds)
    elif id ==2:
        return find_weight(input,reacts,compounds)
    elif id ==3:
        return balance_solve(input)
    elif id == 4:
        return solve_chemical_equation(input,reacts,compounds)
    elif id == 5:
        return solve_classify_chems(input,reacts,compounds)



'''
    # In phương trình ra
problem_text = """Khi cho 11,2 gam (CaO) phản ứng với khí (CO2) thu được 20 gam (CaCO3). Tính khối lượng của khí (CO2) phản ứng
"""
# Gọi hàm mở rộng
find_weight(problem_text,reacts)

problem_text = """Cho 13 gam kẽm (Zn) tác dụng với dung dịch hydrochloric acid (HCl) thu được 27,2 gam kẽm clorua (ZnCl2) và 0,4 gam khí hiđro (H2). Tính khối lượng của hydrochloric acid (HCl) đã phản ứng.
"""

'''






