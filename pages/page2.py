import streamlit as st
import json
from code.main import solve
logo = "./images/logo.png"

st.set_page_config(
    page_icon=logo,
    page_title="UITC2"
)
st.logo(logo, size="large", link=None, icon_image=logo)

st.title("Tìm khối lượng các chất tham gia phản ứng")
st.divider()
st.write("###### Nhập bài toán:")
temp = st.text_input("Ví dụ: Khi cho 11,2 gam (CaO) phản ứng với khí (CO2) thu được 20 gam (CaCO3). Tính khối lượng của khí (CO2) phản ứng")
if (temp !=""):
    temp = temp.strip()
    output = solve(2,temp)
    print(output)
    if 'error' in output:
        st.error(f"{output.split(':')[1]}")
    if '\n' in output:
        st.subheader("Kết quả: ")
        temp_out = output.split('\n')
        
        for i in temp_out:
            st.write(f"{i}")
with st.sidebar:
        st.page_link('app.py', label='Trang chính', icon='🔥')
        st.page_link('pages/page1.py', label='Khối lượng mol của chất', icon='🧪')
        st.page_link('pages/page2.py', label='Bảo toàn khối lượng', icon='⚖️')
        st.page_link('pages/page3.py', label='Cân bằng phương trình', icon='🧮')
        st.page_link('pages/page4.py', label='Phản ứng hóa học', icon='💥')
        st.page_link('pages/page5.py', label='Nhận biết dung dịch', icon='🔎')