import streamlit as st
import json
from code.main import solve
logo_icon = "./images/logo.png"
logo = "./images/logo copy.png"
st.set_page_config(
    page_icon=logo_icon,
    page_title="UITC2"
)

st.logo(logo, size="large", link=None, icon_image=logo_icon)


st.title("Phản ứng hóa học")
st.divider()
st.write("##### Nhập phương trình cần điền khuyết hoặc cân bằng")
temp = st.text_input("Ví dụ: Mg + HCl ->  hoặc Mg + HCl -> MgCl2 + ?")
if (temp !=""):
    temp = temp.strip()
    output = solve(4,temp)
    print("AA", output)
    st.subheader("Kết quả: ")
    if "error" in output:
        st.error(f"{output.split(':')[1]}")
    else:
        if isinstance(output,str):
            st.write(f"{output}")
            print("?")
        else:
            
            if len(output)>2:
                count = 1
                for i in output:
                    if "$" in i:
                        st.latex(f"{i.replace("$", "")}")
                    else:
                        st.write(f"_{i.replace(":",f" thứ  {count}:_")}")
                        count+=1
            else:
                for i in output:
                    if "$" in i:
                        st.latex(f"{i.replace("$", "")}")
                    else:
                        st.write(f"_{i}_")
with st.sidebar:
        st.page_link('app.py', label='Trang chính', icon='🔥')
        st.page_link('pages/page1.py', label='Khối lượng mol của chất', icon='🧪')
        st.page_link('pages/page2.py', label='Bảo toàn khối lượng', icon='⚖️')
        st.page_link('pages/page3.py', label='Cân bằng phương trình', icon='🧮')
        st.page_link('pages/page4.py', label='Phản ứng hóa học', icon='💥')
        st.page_link('pages/page5.py', label='Nhận biết dung dịch', icon='🔎')
