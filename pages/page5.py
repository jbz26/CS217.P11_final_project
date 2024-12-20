import streamlit as st
import json
from code.main import solve
logo = "./images/logo.png"

st.set_page_config(
    page_icon=logo,
    page_title="UITC2"
)
st.logo(logo, size="large", link=None, icon_image=logo)

st.title("Phân biệt dung dịch các chất:")
st.divider()
st.write("###### Nhập tên các dung dịch cần phân biệt bằng phản ứng hóa học:")
temp = st.text_input("Ví dụ: Na2SO4, NaCl, H2SO4, HCl")
if (temp !=""):
    temp = temp.strip()
    output = solve(5,temp)
    #print(output)
    if 'error' in output:
        st.error(f"{output.split(':')[1]}")
    if isinstance(output,list):
        st.subheader("Kết quả: ")
        #st.write(output)
        for i in output:
            if "$" in i:
                st.latex(i.replace("$", "\small "))
            else:
                st.write(f"{i}")
with st.sidebar:
        st.page_link('app.py', label='Trang chính', icon='🔥')
        st.page_link('pages/page1.py', label='Khối lượng mol của chất', icon='🧪')
        st.page_link('pages/page2.py', label='Bảo toàn khối lượng', icon='⚖️')
        st.page_link('pages/page3.py', label='Cân bằng phương trình', icon='🧮')
        st.page_link('pages/page4.py', label='Phản ứng hóa học', icon='💥')
        st.page_link('pages/page5.py', label='Nhận biết dung dịch', icon='🔎')