# app.py (updated — tabs fully card-wrapped, images uniform grid, captions inside cards)
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

# --- CSS: ensure all text inside card layers; images presented in uniform grid; remove blank cards ---
st.markdown(f"""
<style>
:root{{
  --card-bg: rgba(255,255,255,0.96);
  --card-border: rgba(0,0,0,0.06);
  --accent-1: #FF6B6B;
  --accent-2: #FF8E53;
  --accent-contrast: #2b2b2b;
  --muted: #666;
  --card-radius: 14px;
  --shadow: 0 6px 18px rgba(13, 13, 13, 0.08);
}}

/* Background & overlay for contrast */
.stApp {{
    {f'background-image: url("data:image/jpg;base64,{bg_img}");' if bg_img else ''}
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}}
.app-overlay {{
    position: absolute;
    inset: 0;
    background: rgba(255,255,255,0.72);
    z-index: 0;
    pointer-events:none;
}}

/* Header */
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
.main-header h1 {{ margin: 0; font-size: 2.2rem; font-weight:700; }}

/* Big card wrapper for each tab — ensures tab area is always a card */
.tab-card-wrapper {{
    padding: 1rem;
    border-radius: var(--card-radius);
    background: linear-gradient(180deg, rgba(255,255,255,0.98), rgba(250,250,250,0.94));
    border: 1px solid var(--card-border);
    box-shadow: var(--shadow);
    margin-bottom: 1rem;
    position: relative;
    z-index: 2;
}}

/* Section title inside card */
.section-title {{
    margin: 0 0 0.5rem 0;
    color: var(--accent-contrast);
    font-size: 1.25rem;
    font-weight:700;
}}

/* Stat grid */
.stat-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 1rem;
    margin-bottom: 0.9rem;
}}
.stat {{
    background: linear-gradient(180deg, rgba(255,255,255,0.98), rgba(245,245,245,0.96));
    border-radius: 10px;
    padding: 0.9rem;
    text-align: center;
    border: 1px solid rgba(0,0,0,0.04);
}}
.stat .label {{ font-size:0.9rem; color:var(--muted); margin-bottom:0.3rem; }}
.stat .value {{ font-size:1.45rem; font-weight:700; color:var(--accent-contrast); }}

/* EDA image grid — images are NOT inside card boxes; captions below are in small caption cards */
.eda-grid {{
    display: grid;
    gap: 0.8rem;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    align-items: start;
}}
.eda-item {{
    display:flex;
    flex-direction:column;
    gap:6px;
}}
.eda-img {{
    width:100%;
    height:160px;           /* uniform height */
    object-fit:cover;       /* crop but keep aspect */
    border-radius:10px;
    display:block;
    box-shadow: 0 6px 14px rgba(12,12,12,0.06);
}}
.eda-caption {{
    background: rgba(255,255,255,0.96);
    border-radius:8px;
    padding:8px;
    font-size:0.92rem;
    color:var(--muted);
    border:1px solid rgba(0,0,0,0.03);
}}

/* Recipe card + shimmer */
.recipe-grid {{
    display:grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1rem;
    margin-top: 0.6rem;
}}
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
.recipe-card:hover {{ transform: translateY(-6px); box-shadow: 0 18px 36px rgba(12,12,12,0.12); border-color: rgba(255,107,107,0.25); }}
.recipe-card::after {{
    content: "";
    position:absolute; inset:0;
    background: linear-gradient(120deg, transparent 0%, rgba(255,255,255,0.14) 30%, rgba(255,255,255,0.18) 50%, transparent 70%);
    transform: translateX(-120%);
    transition: transform .8s ease; pointer-events:none; border-radius:12px; opacity:0;
}}
.recipe-card:hover::after {{ transform: translateX(120%); opacity:1; }}
.recipe-title {{ font-weight:700; color:var(--accent-contrast); font-size:1rem; margin-bottom:4px; }}
.recipe-sub {{ color:var(--muted); font-size:0.86rem; }}

/* Footer card */
.footer {{
    text-align:center; margin-top:1rem; padding:1rem;
    color:var(--muted); font-size:0.95rem;
    border-radius:10px; background:rgba(255,255,255,0.9); border:1px solid rgba(0,0,0,0.03);
}}

/* Accessibility: high contrast fallback */
@media (prefers-contrast: more) {{
  :root {{ --card-bg: #ffffff; --card-border: #00000015; --accent-contrast: #000; }}
}}
</style>
""", unsafe_allow_html=True)

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

# ---- TAB 1: Data & EDA (all inside a big card wrapper) ----
with tab1:
    st.markdown('<div class="tab-card-wrapper">', unsafe_allow_html=True)

    # Title inside card
    st.markdown('<div class="section-title">Tổng quan Dữ liệu</div>', unsafe_allow_html=True)

    # Stat grid (all inside card) - avoids default streamlit metric boxes that create stray white frames
    st.markdown("""
    <div class="stat-grid" aria-hidden="false">
        <div class="stat"><div class="label">Tổng Ratings</div><div class="value">872,021</div></div>
        <div class="stat"><div class="label">Số User (≥5)</div><div class="value">23,086</div></div>
        <div class="stat"><div class="label">Tổng Recipes</div><div class="value">231,637</div></div>
        <div class="stat"><div class="label">Rating TB</div><div class="value">4.41</div></div>
    </div>
    """, unsafe_allow_html=True)

    # EDA section: title inside the same card
    st.markdown('<div class="section-title" style="margin-top:6px;">Phân tích Dữ liệu (EDA)</div>', unsafe_allow_html=True)

    # Image grid: images are displayed in uniform tiles (images themselves NOT wrapped in card; captions are below in small caption box)
    eda_images = [
        ("assets/eda_rating_distribution.png", "**Phân bố điểm đánh giá**: Hầu hết chấm 4-5 sao."),
        ("assets/eda_Ratings_per_Recipe.png", "**Số lượt đánh giá mỗi công thức**: Phân bố lệch phải."),
        ("assets/eda_Average Rating vs Number of Ingredients.png", "**Số nguyên liệu vs Rating**: Công thức 5-10 nguyên liệu tốt hơn."),
        ("assets/eda_Word Cloud for Ingredients.png", "**Từ khóa nguyên liệu**: chicken, garlic, sugar..."),
        ("assets/eda_Word Cloud for Tags.png", "**Từ khóa thẻ (tags)**: easy, quick, dessert...")
    ]

    # Build the HTML grid for images (uniform height via CSS .eda-img)
    eda_html = ['<div class="eda-grid">']
    for img_path, caption in eda_images:
        if Path(img_path).exists():
            eda_html.append(f'''
            <div class="eda-item">
                <img class="eda-img" src="{img_path}" alt="eda">
                <div class="eda-caption">{caption}</div>
            </div>
            ''')
        else:
            eda_html.append(f'''
            <div class="eda-item">
                <div style="height:160px;border-radius:10px;background:linear-gradient(180deg,#f6f6f6,#efefef);display:flex;align-items:center;justify-content:center;color:#999;border:1px solid rgba(0,0,0,0.03);">
                    Missing: {img_path}
                </div>
                <div class="eda-caption">Missing image: {img_path}</div>
            </div>
            ''')
    eda_html.append('</div>')
    st.markdown(''.join(eda_html), unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)  # close tab card wrapper

# ---- TAB 2: Model & Recommendation ----
with tab2:
    st.markdown('<div class="tab-card-wrapper">', unsafe_allow_html=True)

    st.markdown('<div class="section-title">Chọn Model & User</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        model_choice = st.selectbox(
            "Chọn Model",
            ["Hybrid Simple (α=0.9 SVD)", "Hybrid CBF (α=0.7 SVD + 0.3 CBF)"],
            help="Hybrid Simple: ưu tiên hành vi | Hybrid CBF: kết hợp nội dung"
        )
        model_key = 'fast' if "Simple" in model_choice else 'best'
    with col2:
        try:
            user_list = sorted([str(x) for x in recs[model_key].keys()])
        except Exception:
            user_list = ["user_1", "user_2"]
        user_id = st.selectbox("Chọn User ID", user_list, help="10 user có nhiều tương tác nhất")

    if st.button("Recommend Top-20", type="primary", use_container_width=True):
        top20 = recs[model_key].get(user_id, [])

        # performance metrics inside same card wrapper
        st.markdown('<div style="margin-top:10px;">', unsafe_allow_html=True)
        if model_key == 'fast':
            rmse, r2 = "0.9471", "0.0869"
            p20, r20, ndcg20, map20 = "0.0030", "0.0600", "0.0259", "0.0170"
        else:
            rmse, r2 = "0.9467", "0.0878"
            p20, r20, ndcg20, map20 = "0.0020", "0.0400", "0.0141", "0.0067"

        st.markdown(f"""
            <div class="stat-grid">
                <div class="stat"><div class="label">RMSE</div><div class="value">{rmse}</div></div>
                <div class="stat"><div class="label">R²</div><div class="value">{r2}</div></div>
                <div class="stat"><div class="label">P@20</div><div class="value">{p20}</div></div>
                <div class="stat"><div class="label">R@20</div><div class="value">{r20}</div></div>
            </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="section-title" style="margin-top:8px;">Top-20 Recipe Đề Xuất</div>', unsafe_allow_html=True)

        if not top20:
            st.info("No recommendation available for this user.")
        else:
            # recipe grid
            st.markdown('<div class="recipe-grid">', unsafe_allow_html=True)
            for rid in top20:
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

        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)  # close tab card wrapper

# footer
st.markdown("""
<div class='footer'>
    <p><strong>NHÓM 8</strong> | Recipe Recommender System | Project 2025</p>
    <p><em>Đề xuất cá nhân hóa từ 872K đánh giá – Hybrid SVD + CBF</em></p>
</div>
""", unsafe_allow_html=True)
