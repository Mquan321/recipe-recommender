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

# ---------- Helpers ----------
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

ASSETS = Path("assets")
bg_path = ASSETS / "bg_food.jpg"
bg_img = get_base64_image(bg_path) if bg_path.exists() else None

# ---------- CSS: full redesign for cards, tab headers, image grid ----------
st.markdown(f"""
<style>
:root {{
  --card-bg: rgba(255,255,255,0.98);
  --card-border: rgba(20,20,20,0.06);
  --accent-1: #FF6B6B;
  --accent-2: #FF8E53;
  --accent-contrast: #222;
  --muted: #6b7280;
  --glass-blur: 6px;
  --card-radius: 14px;
  --shadow: 0 10px 30px rgba(10,10,10,0.06);
  --font-sans: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial;
}}

body, .stApp {{
    font-family: var(--font-sans);
}}

/* Background + overlay for contrast */
.stApp {{
    {f'background-image: url("data:image/jpg;base64,{bg_img}");' if bg_img else ''}
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}}
.app-overlay {{
    position: fixed; inset: 0;
    background: rgba(250,250,250,0.70); /* light dim to ensure readability across themes */
    z-index: 0;
    pointer-events: none;
}

/* header card */
.main-header {{
    margin-bottom: 1rem;
    border-radius: 16px;
    padding: 1.1rem;
    background: linear-gradient(90deg, var(--accent-1), var(--accent-2));
    color: white;
    box-shadow: var(--shadow);
    z-index: 3;
    position: relative;
}}
.main-header h1 {{ margin:0; font-size:1.95rem; font-weight:700; }}
.main-header p {{ margin:6px 0 0; opacity:0.95; }}

/* Generic card wrapper used everywhere */
.card {{
    background: var(--card-bg);
    border: 1px solid var(--card-border);
    border-radius: var(--card-radius);
    padding: 0.9rem;
    box-shadow: var(--shadow);
    margin-bottom: 1rem;
    position: relative;
    z-index: 2;
}}

/* Tabs container: style tab headers and active state */
div[role="tablist"] {{
    display:flex;
    gap:0.6rem;
    padding: 0.4rem;
    background: linear-gradient(180deg, rgba(255,255,255,0.95), rgba(250,250,250,0.94));
    border-radius: 12px;
    border: 1px solid var(--card-border);
    margin-bottom: 0.75rem;
}}
div[role="tablist"] button[role="tab"] {{
    border: none;
    padding: 0.55rem 0.95rem;
    border-radius: 10px;
    font-weight: 600;
    background: transparent;
    cursor: pointer;
    transition: transform .18s ease, box-shadow .18s ease, background .18s ease;
    color: var(--accent-contrast);
    box-shadow: none;
    border: 1px solid transparent;
}}
div[role="tablist"] button[role="tab"]:hover {{
    transform: translateY(-3px);
    box-shadow: 0 6px 16px rgba(12,12,12,0.08);
}}
div[role="tablist"] button[role="tab"][aria-selected="true"] {{
    background: linear-gradient(90deg, rgba(255,107,107,0.12), rgba(255,142,83,0.10));
    border: 1px solid rgba(255,107,107,0.18);
    color: var(--accent-contrast);
    box-shadow: 0 8px 24px rgba(255,107,107,0.06);
}}

/* Content area under tabs: wrap in a card to avoid background noise */
[role="tabpanel"] > .card {{
    padding-top: 0.6rem;
}}

/* Headings inside cards */
.card h2 {{
    margin: 0 0 0.6rem 0;
    color: var(--accent-contrast);
    font-size: 1.15rem;
    font-weight: 700;
}}
.card h3 {{
    margin: 0 0 0.45rem 0;
    color: var(--accent-contrast);
    font-size: 1rem;
    font-weight: 650;
}}

/* Stat grid: uniform cards for metrics */
.stat-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 0.9rem;
    margin-bottom: 0.6rem;
}}
.stat {{
    background: linear-gradient(180deg, rgba(255,255,255,0.99), rgba(247,247,247,0.99));
    padding: 0.9rem;
    border-radius: 10px;
    border: 1px solid rgba(0,0,0,0.03);
    text-align: center;
}}
.stat .label {{ color: var(--muted); font-size:0.88rem; margin-bottom:6px; }}
.stat .value {{ font-weight:700; font-size:1.45rem; color:var(--accent-contrast); }}

/* EDA image grid - uniform cards, consistent image size */
.eda-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
    gap: 1rem;
}}
.eda-item {{
    border-radius: 10px;
    overflow: hidden;
    display:flex;
    flex-direction:column;
    height: 260px; /* uniform item height */
    border: 1px solid rgba(0,0,0,0.04);
    background: linear-gradient(180deg, #fff, #fbfbfb);
}}
.eda-item img {{
    width:100%;
    height: 170px; /* allocate top area for image */
    object-fit: cover;
    display:block;
    flex-shrink:0;
}}
.eda-caption {{
    padding: 0.6rem;
    font-size:0.9rem;
    color: var(--muted);
    border-top: 1px dashed rgba(0,0,0,0.03);
    background: rgba(255,255,255,0.97);
    flex:1;
}}

/* Recipe grid and cards */
.recipe-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 1rem;
}}
.recipe-card {{
    padding: 0.9rem;
    border-radius: 12px;
    transition: transform .18s ease, box-shadow .18s ease;
    border: 1px solid rgba(0,0,0,0.04);
    min-height: 130px;
    background: linear-gradient(180deg,#fff,#fbfbfb);
}}
.recipe-card:hover {{
    transform: translateY(-6px);
    box-shadow: 0 18px 36px rgba(12,12,12,0.10);
    border-color: rgba(255,107,107,0.14);
}}
.recipe-title {{ font-weight:700; color:var(--accent-contrast); margin-bottom:6px; }}
.recipe-sub {{ color:var(--muted); font-size:0.86rem; }}

/* shimmer for cards (subtle) */
.recipe-card::after {{
    content: "";
    position: absolute;
    inset: 0;
    pointer-events: none;
    background: linear-gradient(120deg, transparent 0%, rgba(255,255,255,0.12) 40%, rgba(255,255,255,0.16) 50%, transparent 60%);
    opacity: 0;
    transform: translateX(-160%);
    transition: transform .9s ease, opacity .35s ease;
    border-radius: 12px;
}}
.recipe-card:hover::after {{
    transform: translateX(160%);
    opacity: 1;
}}

/* footer */
.footer {{
    text-align:center;
    padding:0.9rem;
    border-radius:10px;
    color:var(--muted);
    border:1px solid rgba(0,0,0,0.03);
    background: rgba(255,255,255,0.95);
    margin-top: 0.8rem;
}}

/* High contrast mode fallback */
@media (prefers-contrast: more) {{
  :root {{ --card-bg: #ffffff; --card-border: #00000022; --accent-contrast: #000; }}
}}

/* Responsive tweaks */
@media (max-width: 640px) {{
  .eda-item {{ height: 220px; }}
  .eda-item img {{ height: 130px; }}
}}
</style>
""", unsafe_allow_html=True)

# overlay element to improve legibility over bg image
st.markdown('<div class="app-overlay"></div>', unsafe_allow_html=True)

# ---------- Data loader ----------
@st.cache_resource
def load_data():
    with open('recommendations.pkl', 'rb') as f:
        recs = pickle.load(f)
    with open('light_recipe_info.pkl', 'rb') as f:
        info = pickle.load(f)
    return recs, info

recs, recipe_info = load_data()

# ---------- Header ----------
st.markdown("""
<div class="main-header">
  <h1>NHÓM 8 - Recipe Recommender System</h1>
  <p>Personalized recommendations — 872K ratings | Hybrid SVD + CBF</p>
</div>
""", unsafe_allow_html=True)

# ---------- Tabs (wrapped content) ----------
tab1, tab2 = st.tabs(["Data & EDA", "Model & Recommendation"])

with tab1:
    # outer card to ensure both tab header and content appear inside a framed card
    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.markdown('<h2>Tổng quan Dữ liệu</h2>', unsafe_allow_html=True)

    # stat grid inside card
    st.markdown("""
    <div class="stat-grid">
      <div class="stat"><div class="label">Tổng Ratings</div><div class="value">872,021</div></div>
      <div class="stat"><div class="label">Số User (≥5)</div><div class="value">23,086</div></div>
      <div class="stat"><div class="label">Tổng Recipes</div><div class="value">231,637</div></div>
      <div class="stat"><div class="label">Rating TB</div><div class="value">4.41</div></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<hr style="border:none;height:1px;background:linear-gradient(90deg,rgba(0,0,0,0.04),rgba(0,0,0,0.02));margin:10px 0 14px 0;">', unsafe_allow_html=True)

    # EDA section heading inside card
    st.markdown('<h3>Phân tích Dữ liệu (EDA)</h3>', unsafe_allow_html=True)

    # collect image paths
    eda_imgs = [
        ("assets/eda_rating_distribution.png", "**Phân bố điểm đánh giá**: Hầu hết chấm 4-5 sao."),
        ("assets/eda_Ratings_per_Recipe.png", "**Số lượt đánh giá mỗi công thức**: Phân bố lệch phải."),
        ("assets/eda_Average Rating vs Number of Ingredients.png", "**Số nguyên liệu vs Rating**: Công thức 5-10 nguyên liệu có rating tốt hơn."),
        ("assets/eda_Word Cloud for Ingredients.png", "**Từ khóa nguyên liệu phổ biến**."),
        ("assets/eda_Word Cloud for Tags.png", "**Từ khóa thẻ (tags)**.")
    ]

    # render images in a responsive grid (uniform sizes)
    st.markdown('<div class="eda-grid">', unsafe_allow_html=True)
    for p, caption in eda_imgs:
        if Path(p).exists():
            # each item in a small card with image + caption inside
            st.markdown(f'''
                <div class="eda-item">
                    <img src="{p}" alt="eda">
                    <div class="eda-caption">{caption}</div>
                </div>
            ''', unsafe_allow_html=True)
        else:
            st.markdown(f'''
                <div class="eda-item" style="align-items:center;justify-content:center;display:flex;">
                    <div style="padding:10px;color:var(--muted);">Missing: {p}</div>
                </div>
            ''', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)  # close outer card for tab1

with tab2:
    # outer card
    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.markdown('<h2>Model & Recommendation</h2>', unsafe_allow_html=True)

    # model selection inside small card
    st.markdown('<div class="card" style="padding:0.6rem;margin-bottom:0.8rem;">', unsafe_allow_html=True)
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
            user_list = ["user_1","user_2"]
        user_id = st.selectbox("Chọn User ID", user_list, help="Top users by interactions")
    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("Recommend Top-20", type="primary", use_container_width=True):
        top20 = recs[model_key].get(user_id, [])

        # performance card
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<h3>Hiệu suất Model</h3>', unsafe_allow_html=True)
        if model_key == 'fast':
            rmse, r2 = "0.9471", "0.0869"
            p20, r20, ndcg20, map20 = "0.0030", "0.0600", "0.0259", "0.0170"
        else:
            rmse, r2 = "0.9467", "0.0878"
            p20, r20, ndcg20, map20 = "0.0020", "0.0400", "0.0141", "0.0067"

        st.markdown(f"""
            <div class="stat-grid" style="margin-top:6px;">
                <div class="stat"><div class="label">RMSE</div><div class="value">{rmse}</div></div>
                <div class="stat"><div class="label">R²</div><div class="value">{r2}</div></div>
                <div class="stat"><div class="label">P@20</div><div class="value">{p20}</div></div>
                <div class="stat"><div class="label">R@20</div><div class="value">{r20}</div></div>
            </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # recommendations grid
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<h3>Top-20 Recipe Đề Xuất</h3>', unsafe_allow_html=True)

        if not top20:
            st.info("No recommendation available for this user.")
        else:
            st.markdown('<div class="recipe-grid">', unsafe_allow_html=True)
            for rid in top20:
                info = recipe_info.get(rid, {})
                name = info.get('name', f"Recipe {rid}")
                tags = ", ".join(info.get('tags', [])[:3])
                # show thumbnail if exists in info (not required)
                thumb_html = ""
                if info.get('image') and isinstance(info.get('image'), str):
                    thumb_html = f'<img src="{info["image"]}" style="width:100%;height:110px;object-fit:cover;border-radius:8px;margin-bottom:8px;">'
                st.markdown(f'''
                    <div class="recipe-card">
                        {thumb_html}
                        <div class="recipe-title">{name}</div>
                        <div class="recipe-sub"><code style="color:var(--muted);">{rid}</code></div>
                        <div style="height:6px"></div>
                        <div class="recipe-sub">Tags: {tags}</div>
                    </div>
                ''', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)  # close recipe-grid

        st.markdown('</div>', unsafe_allow_html=True)  # close recommendations card

    st.markdown('</div>', unsafe_allow_html=True)  # close outer card for tab2

# Footer
st.markdown("""
<div class='footer'>
  <div style="font-weight:700">NHÓM 8 - Recipe Recommender System</div>
  <div style="font-size:0.92rem;margin-top:6px;color:var(--muted)">Personalized recommendations from 872K ratings — Hybrid SVD + CBF</div>
</div>
""", unsafe_allow_html=True)
