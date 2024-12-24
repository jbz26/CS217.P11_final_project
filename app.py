import streamlit as st
import json
from code.main import solve
from streamlit_extras.switch_page_button import switch_page
from streamlit_extras.colored_header import colored_header
from streamlit_extras.let_it_rain import rain
from streamlit_extras.app_logo import add_logo
logo_icon = "./images/logo.png"
logo = "./images/logo copy.png"
st.set_page_config(
    page_icon=logo_icon,
    page_title="UITC2"
)

st.logo(logo, size="large", link=None, icon_image=logo_icon)
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
st.image("./images/animated.gif",width=650)


st.markdown(
    """
    <style>
    .custom-container {
        background-color: #f0a800; /* Nền light blue */
        padding: 10px; /* Khoảng cách bên trong */
        border-radius: 10px; /* Bo tròn góc */
        margin-bottom: 20px; /* Khoảng cách bên dưới */
    }
    .custom-column {
        text-align: center; /* Căn giữa nội dung */
        background-color: #f0f8ff; /* Nền light blue */

    }
    </style>
    """,
    unsafe_allow_html=True
)

# Bắt đầu container
st.markdown('<div class="custom-container">', unsafe_allow_html=True)

# Chia cột và thêm nội dung
col1,_, col2, _,col3 = st.columns([1,0.1,1,0.1,1])

with col1:
    st.markdown('<div class="custom-column">', unsafe_allow_html=True)
    st.image("./images/qr code.png", caption="QR Code")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="custom-column">', unsafe_allow_html=True)
    st.markdown("**Thông tin giữa**")
    st.markdown("- Mô tả 1")
    st.markdown("- Mô tả 2")
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="custom-column">', unsafe_allow_html=True)
    st.markdown("**Cột 3**")
    st.markdown("- Nội dung thêm")
    st.markdown('</div>', unsafe_allow_html=True)

# Kết thúc container
st.markdown('</div>', unsafe_allow_html=True)
