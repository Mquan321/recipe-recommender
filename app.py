# app.py
import streamlit as st
import pickle
import base64

# === CẤU HÌNH TRANG ===
st.set_page_config(
    page_title="NHÓM 8 - Recipe Recommender",
    page_icon="Cooking",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# === HÀM MÃ HÓA ẢNH ===
def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except:
        return None

bg_img = get_base64_image("assets/bg_food.jpg")

# === CSS ĐẸP, SẠCH, HIỆU ỨNG LẤP LÁNH ===
st.markdown(f"""
<style>
    /* Background + Overlay */
    .stApp {{
        background-image: url("data:image/jpg;base64,{bg_img}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    .overlay {{
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        background: rgba(255, 255, 255, 0.94);
        z-index: -1;
    }}

    /* Container chính */
    .main-container {{
        background: rgba(255, 255, 255, 0.96);
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.12);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.4);
        margin: 1rem auto;
        max-width: 1400px;
    }}

    /* Header */
    .main-header {{
        background: linear-gradient(135deg, #FF6B6B, #FF8E53);
        padding: 1.8rem;
        border-radius: 16px;
        text-align: center;
        box-shadow: 0 8px 20px rgba(255, 107, 107, 0.3);
        margin-bottom: 2rem;
        transform: translateY(0);
        transition: all 0.3s ease;
    }}
    .main-header:hover {{
        transform: translateY(-4px);
        box-shadow: 0 12px 28px rgba(255, 82, 82, 0.4);
    }}
    .main-header h1 {{
        color: white;
        margin: 0;
        font-size: 2.8rem;
        font-weight: 800;
        text-shadow: 0 3px 6px rgba(0,0,0,0.3);
    }}

    /* Tab Container */
    .tab-container {{
        background: rgba(255, 255, 255, 0.97);
        padding: 1.5rem;
        border-radius: 16px;
        box-shadow: 0 6px 18px rgba(0,0,0,0.08);
        border: 1px solid rgba(0,0,0,0.05);
        margin-bottom: 1.5rem;
    }}

    /* Tab Button - Hiệu ứng lấp lánh */
    .stTabs [data-baseWeb="tab"] {{
        background: linear-gradient(45deg, #f8f9fa, #e9ecef);
        color: #495057;
        border-radius: 12px;
        padding: 0.8rem 1.5rem;
        margin: 0 0.5rem;
        font-weight: 600;
        border: 1px solid #dee2e6;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }}
    .stTabs [data-baseWeb="tab"]:hover {{
        background: linear-gradient(45deg, #FF6B6B, #FF8E53);
        color: white;
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(255, 107, 107, 0.3);
        border-color: #FF6B6B;
    }}
    .stTabs [data-baseWeb="tab"]:hover::after {{
        content: '';
        position: absolute;
        top: 50%; left: 50%;
        width: 300px; height: 300px;
        background: rgba(255,255,255,0.3);
        border-radius: 50%;
        transform: translate(-50%, -50%) scale(0);
        animation: ripple 0.6s ease-out;
    }}
    @keyframes ripple {{
        to {{
            transform: translate(-50%, -50%) scale(1);
            opacity: 0;
        }}
    }}

    /* Nội dung tab */
    .tab-content {{
        background: rgba(255, 255, 255, 0.98);
        padding: 2rem;
        border-radius: 14px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.06);
        border: 1px solid rgba(0,0,0,0.04);
        min-height: 500px;
    }}

    /* Metric Card */
    .metric-card {{
        background: white;
        padding: 1.3rem;
        border-radius: 12px;
        box-shadow: 0 3px 10px rgba(0,0,0,0.08);
        text-align: center;
        border: 1px solid #f1f3f5;
        height: 100%;
        transition: all 0.3s ease;
    }}
    .metric-card:hover {{
        transform: translateY(-4px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.12);
        border-color: #FF6B6B;
    }}

    /* Recipe Card */
    .recipe-card {{
        background: white;
        padding: 1.3rem;
        border-radius: 14px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.07);
        height: 100%;
        transition: all 0.3s ease;
        border: 1px solid #e9ecef;
    }}
    .recipe-card:hover {{
        transform: translateY(-6px);
        box-shadow: 0 12px 28px rgba(255, 107, 107, 0.2);
        border-color: #FF6B6B;
    }}

    /* Button */
    .stButton>button {{
        background: linear-gradient(45deg, #FF6B6B, #FF8E53);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.8rem 2rem;
        font-weight: 700;
        width: 100%;
        font-size: 1.1rem;
        box-shadow: 0 5px 15px rgba(255, 107, 107, 0.3);
        transition: all 0.3s ease;
    }}
    .stButton>button:hover {{
        background: linear-gradient(45deg, #FF5252, #FF7043);
        transform: translateY(-3px);
        box-shadow: 0 8px 20px rgba(255, 82, 82, 0.4);
    }}

    /* Footer */
    .footer {{
        text-align: center;
        margin-top: 3rem;
        padding: 2rem;
        color: #555;
        font-size: 0.95rem;
        background: rgba(255, 255, 255, 0.95);
        border-radius: 14px;
        backdrop-filter: blur(6px);
        border: 1px solid rgba(0,0,0,0.05);
    }}

    /* Ẩn khung thừa của Streamlit */
    .css-1d391kg, .css-1y0t6an, .css-1cpxqw2 {{ display: none !important; }}
</style>
""", unsafe_allow_html=True)

# === OVERLAY + CONTAINER CHÍNH ===
st.markdown('<div class="overlay"></div>', unsafe_allow_html=True)
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# === TẢI DỮ LIỆU ===
@st.cache_resource
def load_data():
    with open('recommendations.pkl', 'rb') as f:
        recs = pickle.load(f)
    with open('light_recipe_info.pkl', 'rb') as f:
        info = pickle.load(f)
    return recs, info

recs, recipe_info = load_data()

# === HEADER ===
st.markdown("""
<div class="main-header">
    <h1>NHÓM 8 - Recipe Recommender System</h1>
</div>
""", unsafe_allow_html=True)

# === 2 TABS TRONG KHUNG ===
st.markdown('<div class="tab-container">', unsafe_allow_html=True)
tab1, tab2 = st.tabs(["Data & EDA", "Model & Recommendation"])
st.markdown('</div>', unsafe_allow_html=True)

# ========================================
# TAB 1: DATA & EDA
# ========================================
with tab1:
    st.markdown("<div class='tab-content'>", unsafe_allow_html=True)

    st.markdown("## Tổng quan Dữ liệu")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.metric("Tổng Ratings", "872,021")
        st.markdown("</div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.metric("Số User (≥5)", "23,086")
        st.markdown("</div>", unsafe_allow_html=True)
    with col3:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.metric("Tổng Recipes", "231,637")
        st.markdown("</div>", unsafe_allow_html=True)
    with col4:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.metric("Rating TB", "4.41")
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("## Phân tích Dữ liệu (EDA)")

    st.image("assets/eda_rating_distribution.png", use_column_width=True)
    st.caption("**Phân bố điểm đánh giá**: Hầu hết người dùng chấm 4-5 sao → dữ liệu tích cực.")

    st.image("assets/eda_Ratings_per_Recipe.png", use_column_width=True)
    st.caption("**Số lượt đánh giá mỗi công thức**: Phân bố lệch phải, vài món rất phổ biến.")

    st.image("assets/eda_Average Rating vs Number of Ingredients.png", use_column_width=True)
    st.caption("**Mối quan hệ giữa số nguyên liệu và điểm trung bình**: Công thức đơn giản (5-10 nguyên liệu) được đánh giá cao hơn.")

    st.image("assets/eda_Word Cloud for Ingredients.png", use_column_width=True)
    st.caption("**Từ khóa nguyên liệu phổ biến**: Chicken, sugar, butter, flour, garlic...")

    st.image("assets/eda_Word Cloud for Tags.png", use_column_width=True)
    st.caption("**Từ khóa thẻ (tags)**: Easy, quick, dessert, healthy...")

    st.markdown("</div>", unsafe_allow_html=True)

# ========================================
# TAB 2: MODEL & RECOMMENDATION
# ========================================
with tab2:
    st.markdown("<div class='tab-content'>", unsafe_allow_html=True)

    st.markdown("## Chọn Model & User")
    col1, col2 = st.columns(2)
    with col1:
        model_choice = st.selectbox(
            "Chọn Model",
            ["Hybrid Simple (α=0.9 SVD)", "Hybrid CBF (α=0.7 SVD + 0.3 CBF)"],
            help="Hybrid Simple: ưu tiên hành vi | Hybrid CBF: kết hợp nội dung"
        )
        model_key = 'fast' if "Simple" in model_choice else 'best'
    with col2:
        user_id = st.selectbox(
            "Chọn User ID",
            sorted(recs[model_key].keys()),
            help="10 user có nhiều tương tác nhất"
        )

    if st.button("Recommend Top-20", type="primary", use_container_width=True):
        top20 = recs[model_key][user_id]

        st.markdown("## Hiệu suất Model")
        if model_key == 'fast':
            rmse, r2 = "0.9471", "0.0869"
            p20, r20, ndcg20, map20 = "0.0030", "0.0600", "0.0259", "0.0170"
        else:
            rmse, r2 = "0.9467", "0.0878"
            p20, r20, ndcg20, map20 = "0.0020", "0.0400", "0.0141", "0.0067"

        colm1, colm2 = st.columns([1, 2])
        with colm1:
            st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
            st.metric("RMSE", rmse)
            st.metric("R²", r2)
            st.markdown("</div>", unsafe_allow_html=True)
        with colm2:
            st.markdown("### Ranking Metrics @ K=20")
            colx1, colx2, colx3, colx4 = st.columns(4)
            colx1.metric("P@20", p20)
            colx2.metric("R@20", r20)
            colx3.metric("nDCG@20", ndcg20)
            colx4.metric("mAP@20", map20)

        st.markdown("## Top-20 Recipe Đề Xuất")
        cols = st.columns(4)
        for i, rid in enumerate(top20):
            with cols[i % 4]:
                name = recipe_info.get(rid, {}).get('name', 'Unknown')
                tags = ", ".join(recipe_info.get(rid, {}).get('tags', [])[:2])
                st.markdown(f"""
                <div class='recipe-card'>
                    <p style='margin:0;font-weight:600;color:#333;font-size:1.1rem;'>{name}</p>
                    <p style='margin:0.3rem 0 0;font-size:0.9rem;color:#666;'><code>{rid}</code></p>
                    <p style='margin:0.2rem 0 0;font-size:0.85rem;color:#FF6B6B;'>Tags: {tags}</p>
                </div>
                """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# === FOOTER ===
st.markdown("""
<div class='footer'>
    <p><strong>NHÓM 8</strong> | Recipe Recommender System | Project 2025</p>
    <p><em>Đề xuất món ăn cá nhân hóa từ 872K đánh giá – Hybrid SVD + CBF</em></p>
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # Đóng main-container
