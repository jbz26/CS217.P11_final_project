import streamlit as st
import json
from code.main import solve
logo = "./images/logo.png"

st.set_page_config(
    page_icon=logo,
    page_title="UITC2"
)
st.logo(logo, size="large", link=None, icon_image=logo)

st.title("Cân bằng phương trình hóa học:")
st.divider()
st.write("##### Nhập phương trình cần cân bằng:")
temp = st.text_input("Ví dụ: NaOH + H2SO4 -> Na2SO4 + H2O")
if (temp !=""):
    temp = temp.strip()
    output = solve(3,temp)
    #print(output)
    if 'error' in output:
        st.error(f"{output.split(':')[1]}")
    if isinstance(output,list):
        st.subheader("Kết quả: ")
        for i in output:
            if "$" in i:
                st.latex(i.replace("$", ""))
            else:
                st.write(f"{i}")
with st.sidebar:
        st.page_link('app.py', label='Trang chính', icon='🔥')
        st.page_link('pages/page1.py', label='Khối lượng mol của chất', icon='🧪')
        st.page_link('pages/page2.py', label='Bảo toàn khối lượng', icon='⚖️')
        st.page_link('pages/page3.py', label='Cân bằng phương trình', icon='🧮')
        st.page_link('pages/page4.py', label='Phản ứng hóa học', icon='💥')
        st.page_link('pages/page5.py', label='Nhận biết dung dịch', icon='🔎')