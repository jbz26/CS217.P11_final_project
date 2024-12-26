import re
from collections import defaultdict
import json
from .reprocessing import to_subscript,check_chemical
def parse_chemical_formula(formula):
    def multiply_counts(element_counts, multiplier):
        """Nhân số lượng nguyên tố bởi một hệ số."""
        return {element: count * multiplier for element, count in element_counts.items()}

    def parse_subformula(subformula):
        """Phân tích một subformula không có dấu ngoặc."""
        element_counts = defaultdict(int)
        for match in re.finditer(r"([A-Z][a-z]*)(\d*)", subformula):
            element = match.group(1)  # Tên nguyên tố
            count = int(match.group(2)) if match.group(2) else 1  # Số lượng (nếu không có thì là 1)
            element_counts[element] += count
        return element_counts

    # Kiểm tra định dạng của công thức hóa học trước khi xử lý
    if not re.fullmatch(r"[A-Za-z0-9()]+", formula):
        return "error: Công thức không hợp lệ (chỉ chứa ký tự chữ, số và dấu ngoặc)."

    # Sử dụng stack để xử lý các dấu ngoặc và subformula lồng nhau
    stack = []
    current_counts = defaultdict(int)

    i = 0
    while i < len(formula):
        char = formula[i]
        if char == '(':
            # Gặp dấu ngoặc mở, lưu trạng thái hiện tại và bắt đầu subformula mới
            stack.append(current_counts)
            current_counts = defaultdict(int)
        elif char == ')':
            # Gặp dấu ngoặc đóng, lấy hệ số nhân sau ngoặc (nếu có)
            i += 1
            multiplier_match = re.match(r"\d+", formula[i:])
            multiplier = int(multiplier_match.group(0)) if multiplier_match else 1
            if multiplier_match:
                i += len(multiplier_match.group(0)) - 1
            
            # Nhân subformula hiện tại với hệ số và cộng vào trạng thái trước đó
            if not stack:
                return "error: Công thức không hợp lệ (dấu ngoặc đóng không có dấu mở tương ứng)."
            previous_counts = stack.pop()
            for element, count in multiply_counts(current_counts, multiplier).items():
                previous_counts[element] += count
            current_counts = previous_counts
        else:
            # Phân tích một phần tử hoặc subformula không có dấu ngoặc
            match = re.match(r"([A-Z][a-z]*\d*)", formula[i:])
            if match:
                subformula = match.group(0)
                sub_counts = parse_subformula(subformula)
                for element, count in sub_counts.items():
                    current_counts[element] += count
                i += len(subformula) - 1
            else:
                return f"error: Công thức không hợp lệ tại vị trí {i} '{char}' không hợp lệ."
        i += 1

    if stack:
        return "error: Công thức không hợp lệ (dấu ngoặc mở không có dấu đóng tương ứng)."

    return dict(current_counts)

def find_element(chem,elements):
    for e in elements:
        simple_formula = e['Formula']
        simple_formula = re.match(r"([A-Z][a-z]*)", simple_formula).group(0)
        #print(simple_formula)
        if simple_formula == chem:
            e['Formula'] = simple_formula
            return e
    return -1
    
def cal_atomic_mass(chem,compounds):
    elements = []
    output = []
    output.append(f"Chất {to_subscript(chem)}:")
    for e in compounds['Elements']:
        elements.append(e)
    if not check_chemical(chem,compounds):
        return f"error: Không tồn tại chất {chem}!"

    result = parse_chemical_formula(chem)
    if isinstance(result,str):
        return result
    mass = 0
    temp_output = "Gồm các nguyên tố: "
    count_ouput = []
    cal_output = []
    cal_output1 = []

    for e in result.keys():
        temp = find_element(e,elements)
        if temp == -1:
            return f"error: Không tìm thấy nguyên tố {e}"
        temp_output += f"{e} ({temp['Atomic mass']} g/mol); "
        count_ouput.append(f"- {temp["Formula"]}: {result[e]}")
        cal_output.append(f"{temp['Atomic mass']} * {result[e]}")
        cal_output1.append(f"{e} * {result[e]}")
        mass += temp['Atomic mass'] * result[e]
    mass = round(mass,3)
    output.append(temp_output)
    output.append("Số lượng các nguyên tố trong hợp chất:")
    output.extend(count_ouput)
    cal_output =f"$M({chem})= " +" + ".join(cal_output)
    cal_output1 = f"$M({chem})= " +" + ".join(cal_output1)
    output.append(cal_output1)
    output.append(cal_output)
    output.append(f"$M({chem})= {mass}")

    output.append(f"Vậy khối lượng mol của {to_subscript(chem)} là: {mass} (g/mol)")
    return output

                