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


st.title("Phân biệt dung dịch các chất:")
st.divider()
st.write("##### Nhập tên các dung dịch cần phân biệt bằng phản ứng hóa học:")

col1,  col2 = st.columns([3,0.2],vertical_alignment="bottom")

with col1:
    temp = st.text_input("Ví dụ: Na2SO4, NaCl, H2SO4, HCl")
with col2:
    reset = st.button(label="",icon='♻',type="primary")
if (temp !="") or (temp!="" and reset):
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