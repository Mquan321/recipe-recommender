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

# --- CSS: refined, ensure tabs are in card, headings inside card, images normalized ---
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

:root{{
  --card-bg: rgba(255,255,255,0.96);
  --card-border: rgba(0,0,0,0.06);
  --accent-1: #FF6B6B;
  --accent-2: #FF8E53;
  --accent-contrast: #1f2933;
  --muted: #6b7280;
  --card-radius: 14px;
  --shadow: 0 10px 30px rgba(12,12,12,0.08);
  --ui-gap: 1rem;
  --font-family: "Inter", system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial;
}}

body, .stApp {{
  font-family: var(--font-family);
}}

/* Background image + overlay for legibility */
.stApp {{
    {f'background-image: url("data:image/jpg;base64,{bg_img}");' if bg_img else ''}
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
    position: relative;
}}
.app-overlay {{
    position: fixed;
    inset: 0;
    background: rgba(255,255,255,0.74); /* slightly more opaque to ensure contrast */
    z-index: 0;
    pointer-events: none;
}

/* main header card */
.main-header {{
    background: linear-gradient(90deg, var(--accent-1), var(--accent-2));
    padding: 1rem 1.25rem;
    border-radius: 12px;
    color: white;
    box-shadow: var(--shadow);
    margin-bottom: 1rem;
    position: relative;
    z-index: 2;
}}
.main-header h1 {{
    margin: 0;
    font-size: 1.9rem;
    font-weight: 700;
    letter-spacing: -0.3px;
}}
.main-header p {{
    margin: 4px 0 0 0;
    opacity: 0.95;
    font-size: 0.95rem;
}}

/* Tab container: ensure tabs look like cards and content is inside */
.stTabs [role="tablist"] {{
    z-index: 3;
}}
.tab-card-wrapper {{
    margin-top: 0.75rem;
    background: linear-gradient(180deg, rgba(255,255,255,0.98), rgba(247,247,247,0.98));
    border-radius: 12px;
    padding: 0.9rem;
    box-shadow: var(--shadow);
    border: 1px solid var(--card-border);
    position: relative;
    z-index: 2;
}}

/* Section card (used for headings + text blocks) */
.card {{
    background: var(--card-bg);
    border-radius: 12px;
    padding: 0.9rem;
    box-shadow: var(--shadow);
    border: 1px solid var(--card-border);
    margin-bottom: 0.9rem;
}}

/* Stats grid - uniform cards */
.stat-grid {{
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
  gap: 0.9rem;
}}
.stat {{
  background: linear-gradient(180deg, #fff, #fbfbfb);
  padding: 0.8rem;
  border-radius: 10px;
  border: 1px solid rgba(0,0,0,0.04);
  text-align: center;
}}
.stat .label{{ font-size:0.88rem; color:var(--muted); margin-bottom:6px; }}
.stat .value{{ font-size:1.45rem; font-weight:700; color:var(--accent-contrast); }}

/* EDA image grid: images not in card, but layout controlled and captions inside card below */
.eda-grid {{
  display: grid;
  gap: 0.75rem;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  align-items: start;
}}
.eda-img-wrap {{
  width: 100%;
  height: 220px; /* unified height */
  overflow: hidden;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(180deg, #fff, #f7f7f7);
  border: 1px solid rgba(0,0,0,0.03);
}}
.eda-img-wrap img {{
  width: 100%;
  height: 100%;
  object-fit: cover; /* ensures uniform crop */
  display: block;
}}

/* caption card under images */
.caption-row {{
  display: grid;
  gap: 0.5rem;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  margin-top: 0.5rem;
}}
.caption {{
  background: rgba(255,255,255,0.98);
  padding: 0.6rem;
  border-radius: 8px;
  border: 1px solid rgba(0,0,0,0.03);
  color: var(--muted);
  font-size: 0.92rem;
}}

/* Recipe card + shimmer */
.recipe-grid {{
  display: grid;
  gap: 0.9rem;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
}}
.recipe-card {{
  padding: 0.8rem;
  border-radius: 10px;
  border: 1px solid rgba(0,0,0,0.04);
  background: linear-gradient(180deg,#fff,#fbfbfb);
  transition: transform .22s ease, box-shadow .22s ease;
}}
.recipe-card:hover {{
  transform: translateY(-6px);
  box-shadow: 0 22px 40px rgba(12,12,12,0.12);
}}
.recipe-title{{font-weight:700;color:var(--accent-contrast);margin-bottom:6px;}}
.recipe-sub{{color:var(--muted);font-size:0.88rem;}}

/* footer */
.footer {{
  margin-top: 1rem;
  padding: 1rem;
  text-align: center;
  color: var(--muted);
  font-size: 0.95rem;
  border-radius: 10px;
  border: 1px solid rgba(0,0,0,0.03);
  background: rgba(255,255,255,0.96);
}}

/* Accessibility fallback for high contrast */
@media (prefers-contrast: more) {{
  :root {{ --card-bg: #fff; --accent-contrast: #000; }}
}}

/* small screens tweak */
@media (max-width:640px) {{
  .eda-img-wrap {{ height: 160px; }}
}}
</style>
""", unsafe_allow_html=True)

# overlay to ensure readability over background
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
    <p style="margin:6px 0 0 0;">Personalized recommendations — 872K ratings • Clean, accessible UI for any browser</p>
</div>
""", unsafe_allow_html=True)

# === 2 TABS ===
tab1, tab2 = st.tabs(["Data & EDA", "Model & Recommendation"])

with tab1:
    # whole tab wrapped in a card wrapper so tab content is always on card layer
    st.markdown('<div class="tab-card-wrapper">', unsafe_allow_html=True)

    # Overview card (title + stats inside same card)
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<h3 style="margin:0 0 8px 0;">Tổng quan Dữ liệu</h3>', unsafe_allow_html=True)
    st.markdown("""
      <div class="stat-grid" style="margin-top:6px;">
        <div class="stat"><div class="label">Tổng Ratings</div><div class="value">872,021</div></div>
        <div class="stat"><div class="label">Số User (≥5)</div><div class="value">23,086</div></div>
        <div class="stat"><div class="label">Tổng Recipes</div><div class="value">231,637</div></div>
        <div class="stat"><div class="label">Rating TB</div><div class="value">4.41</div></div>
      </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # EDA header (in card)
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<h3 style="margin:0 0 6px 0;">Phân tích Dữ liệu (EDA)</h3>', unsafe_allow_html=True)
    st.markdown('<div style="color:var(--muted); font-size:0.95rem;">Các hình ảnh minh họa bên dưới được căn chỉnh đồng đều; mô tả ngắn gọn nằm trong khung để luôn đọc được.</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # EDA images grid (images themselves outside card but placed in uniform grid)
    eda_images = [
        ("assets/eda_rating_distribution.png", "**Phân bố điểm đánh giá**: Hầu hết chấm 4-5 sao."),
        ("assets/eda_Ratings_per_Recipe.png", "**Số lượt đánh giá mỗi công thức**: Phân bố lệch phải."),
        ("assets/eda_Average Rating vs Number of Ingredients.png", "**Số nguyên liệu vs Rating**."),
        ("assets/eda_Word Cloud for Ingredients.png", "**Từ khóa nguyên liệu phổ biến**."),
        ("assets/eda_Word Cloud for Tags.png", "**Từ khóa thẻ (tags)**.")
    ]

    # create image grid
    st.markdown('<div class="eda-grid">', unsafe_allow_html=True)
    for img_path, _ in eda_images:
        p = Path(img_path)
        if p.exists():
            st.markdown(f'<div class="eda-img-wrap"><img src="{img_path}" alt="EDA image"></div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="eda-img-wrap"><div style="color:var(--muted);padding:6px;text-align:center;">Missing: {p.name}</div></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # captions in a unified caption-row (each caption is inside a small card)
    st.markdown('<div class="caption-row" style="margin-top:10px;">', unsafe_allow_html=True)
    for img_path, caption in eda_images:
        st.markdown(f'<div class="caption">{caption}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)  # close tab-card-wrapper

with tab2:
    st.markdown('<div class="tab-card-wrapper">', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<h3 style="margin:0 0 8px 0;">Chọn Model & User</h3>', unsafe_allow_html=True)
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
    st.markdown('</div>', unsafe_allow_html=True)

    # recommendation area card
    st.markdown('<div class="card">', unsafe_allow_html=True)
    if st.button("Recommend Top-20", type="primary", use_container_width=True):
        top20 = recs[model_key].get(user_id, [])

        # performance / metrics inside card
        st.markdown('<h4 style="margin:0 0 8px 0;">Hiệu suất Model</h4>', unsafe_allow_html=True)
        if model_key == 'fast':
            rmse, r2 = "0.9471", "0.0869"
            p20, r20, ndcg20, map20 = "0.0030", "0.0600", "0.0259", "0.0170"
        else:
            rmse, r2 = "0.9467", "0.0878"
            p20, r20, ndcg20, map20 = "0.0020", "0.0400", "0.0141", "0.0067"

        st.markdown(f"""
            <div class="stat-grid" style="margin-top:6px;margin-bottom:12px;">
                <div class="stat"><div class="label">RMSE</div><div class="value">{rmse}</div></div>
                <div class="stat"><div class="label">R²</div><div class="value">{r2}</div></div>
                <div class="stat"><div class="label">P@20</div><div class="value">{p20}</div></div>
                <div class="stat"><div class="label">R@20</div><div class="value">{r20}</div></div>
            </div>
        """, unsafe_allow_html=True)

        st.markdown('<h4 style="margin:6px 0 8px 0;">Top-20 Recipe Đề Xuất</h4>', unsafe_allow_html=True)
        if not top20:
            st.info("No recommendation available for this user.")
        else:
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

    st.markdown('</div>', unsafe_allow_html=True)  # close recommendation card
    st.markdown('</div>', unsafe_allow_html=True)  # close tab-card-wrapper

# footer
st.markdown("""
<div class='footer'>
    <p><strong>NHÓM 8</strong> | Recipe Recommender System | Project 2025</p>
    <p><em>Đề xuất cá nhân hóa từ 872K đánh giá – Hybrid SVD + CBF</em></p>
</div>
""", unsafe_allow_html=True)
