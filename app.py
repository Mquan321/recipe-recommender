# app.py
import streamlit as st
import pickle
import base64

st.set_page_config(
    page_title="NHÓM 8- Recipe Recommender",
    page_icon="🍳",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

bg_img = get_base64_image("assets/bg_food.jpg")

st.markdown(f"""
<style>
    /* ===== Page background ===== */
    .stApp {{
        background-image: url("data:image/jpg;base64,{bg_img}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        min-height: 100vh;
        color: #222;
    }}

    /* overlay to soften background so text is readable */
    .page-overlay {{
        position: fixed;
        inset: 0;
        background: linear-gradient(180deg, rgba(255,255,255,0.88), rgba(255,255,255,0.92));
        z-index: 0;
        pointer-events: none;
        backdrop-filter: blur(4px);
    }}

    /* ===== Main header ===== */
    .main-header {{
        background: linear-gradient(90deg, #FF6B6B, #FF8E53);
        padding: 1.25rem;
        border-radius: 14px;
        text-align: center;
        box-shadow: 0 8px 22px rgba(0,0,0,0.12);
        margin: 1rem 0 1.5rem 0;
        position: relative;
        z-index: 2;
    }}
    .main-header h1 {{
        color: white;
        margin: 0;
        font-size: 2.1rem;
        font-weight: 800;
        text-shadow: 0 3px 8px rgba(0,0,0,0.2);
        letter-spacing: 0.6px;
    }}

    /* ===== Section (tab) wrapper ===== */
    .tab-frame {{
        background: linear-gradient(180deg, rgba(255,255,255,0.98), rgba(248,248,248,0.98));
        border-radius: 14px;
        padding: 1.25rem;
        box-shadow: 0 8px 18px rgba(0,0,0,0.06);
        border: 1px solid rgba(34,34,34,0.06);
        margin-bottom: 1.25rem;
        position: relative;
        z-index: 2;
        overflow: hidden;
    }}

    /* Title inside frame */
    .section-title {{
        display: inline-block;
        background: linear-gradient(90deg, #ffffff, #fff6f3);
        padding: 0.6rem 1rem;
        border-radius: 10px;
        font-weight: 700;
        color: #333;
        box-shadow: 0 4px 12px rgba(0,0,0,0.04);
        margin-bottom: 1rem;
    }}

    /* Metrics grid */
    .metric-grid {{
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1rem;
        margin-bottom: 1rem;
    }}
    .metric-card {{
        background: linear-gradient(180deg, #fff, #fffefd);
        padding: 1rem;
        border-radius: 12px;
        box-shadow: 0 6px 16px rgba(0,0,0,0.06);
        text-align: center;
        border: 1px solid rgba(34,34,34,0.05);
        min-height: 96px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }}
    .metric-card .label {{
        font-size: 0.95rem;
        color: #666;
        margin-bottom: 0.5rem;
        font-weight: 600;
    }}
    .metric-card .value {{
        font-size: 1.4rem;
        font-weight: 800;
        color: #111;
    }}

    /* EDA images area */
    .eda-grid {{
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 1rem;
        margin-top: 0.75rem;
    }}
    .eda-item {{
        background: white;
        border-radius: 12px;
        overflow: hidden;
        padding: 0.65rem;
        box-shadow: 0 8px 18px rgba(0,0,0,0.04);
        border: 1px solid rgba(34,34,34,0.04);
    }}
    .eda-item img {{
        width: 100%;
        height: auto;
        display: block;
        border-radius: 8px;
    }}
    .eda-caption {{
        margin-top: 0.4rem;
        color: #555;
        font-size: 0.92rem;
    }}

    /* Recipe cards grid */
    .recipes-grid {{
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1rem;
        margin-top: 1rem;
    }}
    .recipe-card {{
        background: linear-gradient(180deg, #ffffff, #fffaf8);
        padding: 0.9rem;
        border-radius: 14px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.06);
        transition: transform 0.25s ease, box-shadow 0.25s ease;
        border: 1px solid rgba(34,34,34,0.04);
        position: relative;
        overflow: hidden;
        min-height: 120px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }}
    .recipe-card:hover {{
        transform: translateY(-8px);
        box-shadow: 0 20px 36px rgba(0,0,0,0.12);
        border-color: rgba(255,107,107,0.18);
    }}
    .recipe-title {{
        font-weight: 700;
        color: #222;
        margin-bottom: 0.25rem;
    }}
    .recipe-meta {{
        color: #ff6b6b;
        font-weight: 600;
        font-size: 0.88rem;
    }}

    /* Button styling */
    .stButton>button {{
        background: linear-gradient(45deg, #FF6B6B, #FF8E53);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.6rem 1.2rem;
        font-weight: 700;
        width: 100%;
        font-size: 1rem;
        box-shadow: 0 8px 20px rgba(255,107,107,0.12);
    }}
    .stButton>button:hover {{
        transform: translateY(-2px);
    }}

    /* Shimmer (lóe sáng) effect on hover for titles and tabs */
    .shimmer {{
        position: relative;
        overflow: hidden;
        border-radius: 10px;
    }}
    .shimmer::after {{
        content: "";
        position: absolute;
        top: -50%;
        left: -75%;
        width: 50%;
        height: 200%;
        background: linear-gradient(120deg, rgba(255,255,255,0.0) 0%, rgba(255,255,255,0.55) 50%, rgba(255,255,255,0.0) 100%);
        transform: rotate(25deg);
        transition: all 0.9s ease;
        opacity: 0;
    }}
    .shimmer:hover::after {{
        left: 150%;
        opacity: 1;
        transition: all 0.9s ease;
    }}

    /* Footer */
    .footer {{
        text-align: center;
        margin-top: 1.5rem;
        padding: 1rem;
        color: #444;
        font-size: 0.92rem;
        background: rgba(255,255,255,0.95);
        border-radius: 10px;
        border: 1px solid rgba(34,34,34,0.04);
        box-shadow: 0 6px 16px rgba(0,0,0,0.04);
    }}

    /* Responsive tweaks */
    @media (max-width: 900px) {{
        .metric-grid {{ grid-template-columns: repeat(2, 1fr); }}
        .eda-grid {{ grid-template-columns: 1fr; }}
        .recipes-grid {{ grid-template-columns: repeat(2, 1fr); }}
    }}
    @media (max-width: 520px) {{
        .metric-grid {{ grid-template-columns: 1fr; }}
        .recipes-grid {{ grid-template-columns: 1fr; }}
    }}
</style>
""", unsafe_allow_html=True)

# overlay element
st.markdown('<div class="page-overlay"></div>', unsafe_allow_html=True)

@st.cache_resource
def load_data():
    with open('recommendations.pkl', 'rb') as f:
        recs = pickle.load(f)
    with open('light_recipe_info.pkl', 'rb') as f:
        info = pickle.load(f)
    return recs, info

recs, recipe_info = load_data()

# Header
st.markdown("""
<div class="main-header shimmer">
    <h1>NHÓM 8 - Recipe Recommender System</h1>
</div>
""", unsafe_allow_html=True)

# === 2 TABS ===
tab1, tab2 = st.tabs(["Data & EDA", "Model & Recommendation"])

with tab1:
    # entire tab inside a framed card
    st.markdown('<div class="tab-frame">', unsafe_allow_html=True)

    st.markdown('<div class="section-title shimmer">Tổng quan Dữ liệu</div>', unsafe_allow_html=True)

    # Metrics as cards (guarantee text inside the card)
    st.markdown('<div class="metric-grid">', unsafe_allow_html=True)
    st.markdown(f'''
        <div class="metric-card">
            <div class="label">Tổng Ratings</div>
            <div class="value">872,021</div>
        </div>
    ''', unsafe_allow_html=True)
    st.markdown(f'''
        <div class="metric-card">
            <div class="label">Số User (≥5)</div>
            <div class="value">23,086</div>
        </div>
    ''', unsafe_allow_html=True)
    st.markdown(f'''
        <div class="metric-card">
            <div class="label">Tổng Recipes</div>
            <div class="value">231,637</div>
        </div>
    ''', unsafe_allow_html=True)
    st.markdown(f'''
        <div class="metric-card">
            <div class="label">Rating TB</div>
            <div class="value">4.41</div>
        </div>
    ''', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)  # close metric-grid

    # EDA title and images inside frame
    st.markdown('<div class="section-title" style="margin-top:0.8rem;">Phân tích Dữ liệu (EDA)</div>', unsafe_allow_html=True)
    st.markdown('<div class="eda-grid">', unsafe_allow_html=True)

    # Use the same eda images but wrap inside eda-item card so no stray white frames
    eda_imgs = [
        ("assets/eda_rating_distribution.png", "**Phân bố điểm đánh giá**: Hầu hết người dùng chấm 4-5 sao → dữ liệu tích cực."),
        ("assets/eda_Ratings_per_Recipe.png", "**Số lượt đánh giá mỗi công thức**: Phân bố lệch phải, vài món rất phổ biến."),
        ("assets/eda_Average Rating vs Number of Ingredients.png", "**Mối quan hệ giữa số nguyên liệu và điểm trung bình**: Công thức đơn giản (5-10 nguyên liệu) được đánh giá cao hơn."),
        ("assets/eda_Word Cloud for Ingredients.png", "**Từ khóa nguyên liệu phổ biến**: Chicken, sugar, butter, flour, garlic...")
    ]

    for img_path, caption in eda_imgs:
        st.markdown(f'''
            <div class="eda-item">
                <img src="{img_path}" alt="EDA">
                <div class="eda-caption">{caption}</div>
            </div>
        ''', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)  # close eda-grid
    st.markdown('</div>', unsafe_allow_html=True)  # close tab-frame

with tab2:
    st.markdown('<div class="tab-frame">', unsafe_allow_html=True)

    st.markdown('<div class="section-title shimmer">Model & Recommendation</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        model_choice = st.selectbox(
            "Chọn Model",
            ["Hybrid Simple (α=0.9 SVD)", "Hybrid CBF (α=0.7 SVD + 0.3 CBF)"],
            help="Hybrid Simple: ưu tiên hành vi | Hybrid CBF: kết hợp nội dung"
        )
        model_key = 'fast' if "Simple" in model_choice else 'best'
    with col2:
        # show user list in a card style select box area
        st.markdown('<div style="padding:6px;border-radius:8px;background:#fff;border:1px solid rgba(34,34,34,0.04);box-shadow:0 6px 12px rgba(0,0,0,0.03);">', unsafe_allow_html=True)
        user_id = st.selectbox(
            "Chọn User ID",
            sorted(recs[model_key].keys()),
            help="10 user có nhiều tương tác nhất"
        )
        st.markdown('</div>', unsafe_allow_html=True)

    if st.button("Recommend Top-20", type="primary", use_container_width=True):
        # get top20
        top20 = recs[model_key][user_id]

        st.markdown('<div style="margin-top:1rem;">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Hiệu suất Model</div>', unsafe_allow_html=True)

        if model_key == 'fast':
            rmse, r2 = "0.9471", "0.0869"
            p20, r20, ndcg20, map20 = "0.0030", "0.0600", "0.0259", "0.0170"
        else:
            rmse, r2 = "0.9467", "0.0878"
            p20, r20, ndcg20, map20 = "0.0020", "0.0400", "0.0141", "0.0067"

        st.markdown('<div class="metric-grid">', unsafe_allow_html=True)
        st.markdown(f'''
            <div class="metric-card">
                <div class="label">RMSE</div>
                <div class="value">{rmse}</div>
            </div>
        ''', unsafe_allow_html=True)
        st.markdown(f'''
            <div class="metric-card">
                <div class="label">R²</div>
                <div class="value">{r2}</div>
            </div>
        ''', unsafe_allow_html=True)
        st.markdown(f'''
            <div class="metric-card">
                <div class="label">P@20</div>
                <div class="value">{p20}</div>
            </div>
        ''', unsafe_allow_html=True)
        st.markdown(f'''
            <div class="metric-card">
                <div class="label">R@20</div>
                <div class="value">{r20}</div>
            </div>
        ''', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)  # close metric-grid

        st.markdown('<div class="section-title" style="margin-top:1rem;">Top-20 Recipe Đề Xuất</div>', unsafe_allow_html=True)

        # recipes grid
        st.markdown('<div class="recipes-grid">', unsafe_allow_html=True)
        for i, rid in enumerate(top20):
            info = recipe_info.get(rid, {})
            name = info.get('name', f"Recipe {rid}")
            tags = ", ".join(info.get('tags', [])[:2])
            st.markdown(f'''
                <div class="recipe-card shimmer">
                    <div class="recipe-title">{name}</div>
                    <div class="recipe-meta"><code>{rid}</code> • {tags}</div>
                </div>
            ''', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)  # close recipes-grid

        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)  # close tab-frame

# footer
st.markdown("""
<div class='footer'>
    <p><strong>NHÓM 8</strong> | Recipe Recommender System | Project 2025</p>
    <p><em>Đề xuất món ăn cá nhân hóa từ 872K đánh giá – Hybrid SVD + CBF</em></p>
</div>
""", unsafe_allow_html=True)
