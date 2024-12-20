import streamlit as st
import json
from code.main import solve
from streamlit_extras.switch_page_button import switch_page
from streamlit_extras.colored_header import colored_header
from streamlit_extras.let_it_rain import rain
from streamlit_extras.app_logo import add_logo
logo = "./images/logo.png"

st.set_page_config(
    page_icon=logo,
    page_title="UITC2"
)
st.logo(logo, size="large", link=None, icon_image=logo)

st.title("Hóa giải hóa học - UITC2")
def example():
    colored_header(
        label="My New Pretty Colored Header",
        description="This is a description",
        color_name="violet-70",
    )

#with st.sidebar: st.image(logo, width=60)
#add_logo(logo, height=300)
#add_logo("https://cdn.haitrieu.com/wp-content/uploads/2021/10/Logo-DH-Cong-Nghe-Thong-Tin-UIT.png")


rain(
    emoji="❄️",
    font_size=20,
    falling_speed=5,
    animation_length="infinite",
)

#st.divider()
with st.sidebar:
        st.page_link('app.py', label='Trang chính', icon='🔥')
        st.page_link('pages/page1.py', label='Khối lượng mol của chất', icon='🧪')
        st.page_link('pages/page2.py', label='Bảo toàn khối lượng', icon='⚖️')
        st.page_link('pages/page3.py', label='Cân bằng phương trình', icon='🧮')
        st.page_link('pages/page4.py', label='Phản ứng hóa học', icon='💥')
        st.page_link('pages/page5.py', label='Nhận biết dung dịch', icon='🔎')
string = "Với UITC2, bạn có thể giải quyết hầu hết các bài toán hóa học bậc THCS"
string2 = "Một số dạng toán:"
listitem = """
<ol >
<li><strong>Tính toán khối lượng mol của chất:</strong>
    <br> Tính khối lượng mol dựa trên công thức hóa học của chất.
</li>
<li> <strong>Định luật bảo toàn khối lượng: </strong>
    <br> Áp dụng định luật bảo toàn khối lượng để tính toán khối lượng các chất tham gia phản ứng.
</li>
<li> <strong> Cân bằng phương trình hóa học: </strong>
    <br> Chi tiết cách cân bằng phương trình hóa học dựa trên định luật bảo toàn nguyên tố.
</li>
<li><strong> Phản ứng hóa học: </strong> 
    <br> Chỉ cần cung cấp một số thông tin các chất, chúng tôi sẽ giúp bạn hoàn thành phản ứng.
</li>
<li> <strong> Nhận biết dung dịch: </strong>
    <br> Áp dụng các phương pháp hóa học để phân biệt các hóa chất.
</li>
</ol>
"""
st.markdown(listitem,unsafe_allow_html= True)
st.divider()
choice = st.selectbox("Chọn bài toán bạn cần xử lý ",["1. Tính khối lượng mol","2. Tính khối lượng các chất tham gia phản ứng", "3. Cân bằng phương trình", "4. Hoàn thành phương trình hóa học", "5. Phân biệt các lọ dung dịch"],placeholder="Hãy chọn bài toán bạn cần xử lý tại đây!",index=None)
if choice!=None:
    temp = choice.split(".")[0]   
    switch_page(f"page{temp}")
    