# app.py
import streamlit as st
import pickle
import base64
from pathlib import Path

st.set_page_config(
    page_title="NHÓM 8- Recipe Recommender",
    page_icon="🍳",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- helper ---
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

ASSETS = Path("assets")
bg_path = ASSETS / "bg_food.jpg"
bg_img = get_base64_image(bg_path) if bg_path.exists() else None

# --- CSS: accessible, cards as layers, tab card + shimmer hover ---
st.markdown(f"""
<style>
:root{{
  --card-bg: rgba(255,255,255,0.96);
  --card-border: rgba(0,0,0,0.06);
  --accent-1: #FF6B6B;
  --accent-2: #FF8E53;
  --accent-contrast: #2b2b2b;
  --muted: #666;
  --glass-blur: 6px;
  --card-radius: 14px;
  --shadow: 0 6px 18px rgba(13, 13, 13, 0.08);
}}

/* Background image (light opacity overlay for readability) */
.stApp {{
    {f'background-image: url("data:image/jpg;base64,{bg_img}");' if bg_img else ''}
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}}
/* global overlay to dim background slightly - helps text contrast */
.app-overlay {{
    position: absolute;
    inset: 0;
    background: rgba(255,255,255,0.68);
    z-index: 0;
    pointer-events: none;
}}

/* Main container: provide comfortable padding */
.reportview-container .main {{
    padding-top: 1.25rem;
    padding-left: 1.25rem;
    padding-right: 1.25rem;
}}

/* Header card */
.main-header {{
    background: linear-gradient(90deg, var(--accent-1), var(--accent-2));
    padding: 1.25rem;
    border-radius: var(--card-radius);
    text-align: center;
    box-shadow: var(--shadow);
    color: white;
    z-index: 2;
    position: relative;
}}
.main-header h1 {{
    margin: 0;
    font-size: 2.2rem;
    font-weight: 700;
    letter-spacing: -0.6px;
}}

/* Generic card used for all content blocks */
.card {{
    background: var(--card-bg);
    border-radius: var(--card-radius);
    padding: 1rem;
    box-shadow: var(--shadow);
    border: 1px solid var(--card-border);
    position: relative;
    z-index: 2;
    margin-bottom: 1rem;
}}

/* Grid for stats (metrics) */
.stat-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 1rem;
}}
.stat {{
    background: linear-gradient(180deg, rgba(255,255,255,0.98), rgba(250,250,250,0.96));
    border-radius: 12px;
    padding: 0.9rem;
    text-align: center;
    border: 1px solid rgba(0,0,0,0.04);
}}
.stat .label {{
    font-size: 0.9rem;
    color: var(--muted);
    margin-bottom: 0.35rem;
}}
.stat .value {{
    font-size: 1.45rem;
    font-weight: 700;
    color: var(--accent-contrast);
    letter-spacing: -0.4px;
}}

/* Tab area wrapped in card */
.tab-card {{
    padding: 0.75rem;
    border-radius: 12px;
    background: linear-gradient(180deg, rgba(255,255,255,0.98), rgba(250,250,250,0.94));
    border: 1px solid rgba(0,0,0,0.04);
}}

/* Recipe card + hover shimmer */
.recipe-card {{
    background: linear-gradient(180deg, rgba(255,255,255,0.95), rgba(248,248,248,0.95));
    padding: 0.9rem;
    border-radius: 12px;
    border: 1px solid rgba(0,0,0,0.04);
    transition: transform .25s ease, box-shadow .25s ease;
    height: 140px;
    overflow: hidden;
    position: relative;
}}
.recipe-card:hover {{
    transform: translateY(-6px);
    box-shadow: 0 18px 36px rgba(12,12,12,0.12);
    border-color: rgba(255,107,107,0.25);
}}

/* shimmer */
.recipe-card::after {{
    content: "";
    position: absolute;
    inset: 0;
    background: linear-gradient(120deg, transparent 0%, rgba(255,255,255,0.14) 30%, rgba(255,255,255,0.18) 50%, transparent 70%);
    transform: translateX(-120%);
    transition: transform .8s ease;
    pointer-events: none;
    border-radius: 12px;
    opacity: 0;
}}
.recipe-card:hover::after {{
    transform: translateX(120%);
    opacity: 1;
}}

/* recipe text */
.recipe-title {{
    font-weight: 700;
    color: var(--accent-contrast);
    margin-bottom: 0.25rem;
    font-size: 1rem;
}}
.recipe-sub {{
    color: var(--muted);
    font-size: 0.84rem;
}}

/* ensure headings inside cards */
.card h2, .card h3 {{
    margin-top: 0;
    color: var(--accent-contrast);
}}

/* responsive images in card */
.card img {{
    max-width: 100%;
    border-radius: 8px;
    display: block;
    margin: 0.5rem 0;
}}

/* small footer styling */
.footer {{
    text-align: center;
    margin-top: 1.25rem;
    padding: 1rem;
    color: var(--muted);
    font-size: 0.95rem;
    border-radius: 10px;
    background: rgba(255,255,255,0.9);
    border: 1px solid rgba(0,0,0,0.03);
    z-index: 2;
}}

/* high contrast fallback for B/W rendering */
@media (prefers-contrast: more) {{
  :root {{ --card-bg: #ffffff; --card-border: #00000015; --accent-contrast: #000; }}
}}

</style>
""", unsafe_allow_html=True)

# overlay element to improve legibility over bg image
st.markdown('<div class="app-overlay"></div>', unsafe_allow_html=True)

# --- Load pickles cached resource ---
@st.cache_resource
def load_data():
    with open('recommendations.pkl', 'rb') as f:
        recs = pickle.load(f)
    with open('light_recipe_info.pkl', 'rb') as f:
        info = pickle.load(f)
    return recs, info

recs, recipe_info = load_data()

# --- header ---
st.markdown("""
<div class="main-header">
    <h1>NHÓM 8 - Recipe Recommender System</h1>
    <div style="font-size:0.95rem;margin-top:6px;color:rgba(255,255,255,0.92)">Personalized recommendations from 872K ratings</div>
</div>
""", unsafe_allow_html=True)

# === 2 TABS ===
tab1, tab2 = st.tabs(["Data & EDA", "Model & Recommendation"])

with tab1:
    # wrap tab content in card
    st.markdown('<div class="card tab-card">', unsafe_allow_html=True)

    st.markdown('<h2>Tổng quan Dữ liệu</h2>', unsafe_allow_html=True)

    # stat grid (custom HTML so no blank st boxes)
    st.markdown("""
    <div class="stat-grid">
        <div class="stat">
            <div class="label">Tổng Ratings</div>
            <div class="value">872,021</div>
        </div>
        <div class="stat">
            <div class="label">Số User (≥5)</div>
            <div class="value">23,086</div>
        </div>
        <div class="stat">
            <div class="label">Tổng Recipes</div>
            <div class="value">231,637</div>
        </div>
        <div class="stat">
            <div class="label">Rating TB</div>
            <div class="value">4.41</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<hr style="border:none;height:1px;background:linear-gradient(90deg,rgba(0,0,0,0.04),rgba(0,0,0,0.02));margin:12px 0;">', unsafe_allow_html=True)

    st.markdown("<h3>Phân tích Dữ liệu (EDA)</h3>", unsafe_allow_html=True)

    # EDA images inside cards to avoid blank frames
    def show_eda(img_path, caption):
        if Path(img_path).exists():
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.image(img_path, use_column_width=True)
            st.caption(caption)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info(f"Missing image: {img_path}")

    show_eda(ASSETS / "eda_rating_distribution.png", "**Phân bố điểm đánh giá**: Hầu hết chấm 4-5 sao.")
    show_eda(ASSETS / "eda_Ratings_per_Recipe.png", "**Số lượt đánh giá mỗi công thức**: Phân bố lệch phải.")
    show_eda(ASSETS / "eda_Average Rating vs Number of Ingredients.png", "**Số nguyên liệu vs Rating**.")
    show_eda(ASSETS / "eda_Word Cloud for Ingredients.png", "**Từ khóa nguyên liệu phổ biến**.")
    show_eda(ASSETS / "eda_Word Cloud for Tags.png", "**Từ khóa thẻ (tags)**.")

    st.markdown('</div>', unsafe_allow_html=True)


with tab2:
    st.markdown('<div class="card tab-card">', unsafe_allow_html=True)

    st.markdown('<h2>Chọn Model & User</h2>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        model_choice = st.selectbox(
            "Chọn Model",
            ["Hybrid Simple (α=0.9 SVD)", "Hybrid CBF (α=0.7 SVD + 0.3 CBF)"],
            help="Hybrid Simple: ưu tiên hành vi | Hybrid CBF: kết hợp nội dung"
        )
        model_key = 'fast' if "Simple" in model_choice else 'best'
    with col2:
        # safe sorted keys (cast to str to avoid weird html)
        try:
            user_list = sorted([str(x) for x in recs[model_key].keys()])
        except Exception:
            user_list = ["user_1", "user_2"]
        user_id = st.selectbox("Chọn User ID", user_list, help="10 user có nhiều tương tác nhất")

    if st.button("Recommend Top-20", type="primary", use_container_width=True):
        top20 = recs[model_key].get(user_id, [])

        st.markdown("<h3>Hiệu suất Model</h3>", unsafe_allow_html=True)
        if model_key == 'fast':
            rmse, r2 = "0.9471", "0.0869"
            p20, r20, ndcg20, map20 = "0.0030", "0.0600", "0.0259", "0.0170"
        else:
            rmse, r2 = "0.9467", "0.0878"
            p20, r20, ndcg20, map20 = "0.0020", "0.0400", "0.0141", "0.0067"

        # performance metrics in stat-grid
        st.markdown(f"""
            <div class="stat-grid" style="margin-top:8px;">
                <div class="stat"><div class="label">RMSE</div><div class="value">{rmse}</div></div>
                <div class="stat"><div class="label">R²</div><div class="value">{r2}</div></div>
                <div class="stat"><div class="label">P@20</div><div class="value">{p20}</div></div>
                <div class="stat"><div class="label">R@20</div><div class="value">{r20}</div></div>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("<h3 style='margin-top:14px;'>Top-20 Recipe Đề Xuất</h3>", unsafe_allow_html=True)
        cols = st.columns(4)
        if not top20:
            st.info("No recommendation available for this user.")
        else:
            for i, rid in enumerate(top20):
                with cols[i % 4]:
                    info = recipe_info.get(rid, {})
                    name = info.get('name', f"Recipe {rid}")
                    tags = ", ".join(info.get('tags', [])[:2])
                    st.markdown(f"""
                    <div class="recipe-card">
                        <div class="recipe-title">{name}</div>
                        <div class="recipe-sub"><code style="color:var(--muted);">{rid}</code></div>
                        <div style="height:6px"></div>
                        <div class="recipe-sub">Tags: {tags}</div>
                    </div>
                    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# footer
st.markdown("""
<div class='footer card'>
    <p><strong>NHÓM 8</strong> | Recipe Recommender System | Project 2025</p>
    <p><em>Đề xuất cá nhân hóa từ 872K đánh giá – Hybrid SVD + CBF</em></p>
</div>
""", unsafe_allow_html=True)
