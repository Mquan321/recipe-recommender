# app.py
import streamlit as st
import pickle
import base64

st.set_page_config(
    page_title="NHÓM 10 - Recipe Recommender",
    page_icon="Cooking",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

bg_img = get_base64_image("assets/background_food.jpg")

st.markdown(f"""
<style>
    .stApp {{
        background-image: url("data:image/jpg;base64,{bg_img}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    .background-overlay {{
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        background: rgba(255, 255, 255, 0.92);
        z-index: -1;
    }}
    .main-header {{
        background: linear-gradient(90deg, #FF6B6B, #FF8E53);
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
        margin-bottom: 2rem;
        position: relative;
        z-index: 1;
    }}
    .main-header h1 {{
        color: white;
        margin: 0;
        font-size: 2.5rem;
        font-weight: 700;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }}
    .tab-content {{
        background-color: rgba(255, 255, 255, 0.95);
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 6px 16px rgba(0,0,0,0.1);
        margin-bottom: 1.5rem;
        backdrop-filter: blur(8px);
        border: 1px solid rgba(255, 255, 255, 0.3);
    }}
    .metric-card {{
        background-color: white;
        padding: 1.2rem;
        border-radius: 12px;
        box-shadow: 0 3px 8px rgba(0,0,0,0.1);
        text-align: center;
        border: 1px solid #f0f0f0;
    }}
    .recipe-card {{
        background-color: white;
        padding: 1.2rem;
        border-radius: 14px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.08);
        height: 100%;
        transition: all 0.3s ease;
        border: 1px solid #eee;
    }}
    .recipe-card:hover {{
        transform: translateY(-6px);
        box-shadow: 0 12px 24px rgba(0,0,0,0.15);
        border-color: #FF6B6B;
    }}
    .stButton>button {{
        background: linear-gradient(45deg, #FF6B6B, #FF8E53);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.7rem 1.8rem;
        font-weight: 600;
        width: 100%;
        font-size: 1.1rem;
        box-shadow: 0 4px 8px rgba(255, 107, 107, 0.3);
    }}
    .stButton>button:hover {{
        background: linear-gradient(45deg, #FF5252, #FF7043);
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(255, 82, 82, 0.4);
    }}
    .footer {{
        text-align: center;
        margin-top: 3rem;
        padding: 2rem;
        color: #555;
        font-size: 0.95rem;
        background: rgba(255, 255, 255, 0.9);
        border-radius: 12px;
        backdrop-filter: blur(5px);
    }}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="background-overlay"></div>', unsafe_allow_html=True)

@st.cache_resource
def load_data():
    with open('recommendations.pkl', 'rb') as f:
        recs = pickle.load(f)
    with open('light_recipe_info.pkl', 'rb') as f:
        info = pickle.load(f)
    return recs, info

recs, recipe_info = load_data()

st.markdown("""
<div class="main-header">
    <h1>Cooking NHÓM 10 - Recipe Recommender System</h1>
</div>
""", unsafe_allow_html=True)

# === 2 TABS ===
tab1, tab2 = st.tabs(["Data & EDA", "Model & Recommendation"])


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
                name = recipe_info[rid]['name']
                tags = ", ".join(recipe_info[rid]['tags'][:2])
                st.markdown(f"""
                <div class='recipe-card'>
                    <p style='margin:0;font-weight:600;color:#333;font-size:1.1rem;'>{name}</p>
                    <p style='margin:0.3rem 0 0;font-size:0.9rem;color:#666;'><code>{rid}</code></p>
                    <p style='margin:0.2rem 0 0;font-size:0.85rem;color:#FF6B6B;'>Tags: {tags}</p>
                </div>
                 """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("""
<div class='footer'>
    <p><strong>NHÓM 8</strong> | Recipe Recommender System | Project 2025</p>
    <p><em>Đề xuất món ăn cá nhân hóa từ 872K đánh giá – Hybrid SVD + CBF</em></p>
</div>
""", unsafe_allow_html=True)




