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

ASSETS = Path("assets")

def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

bg_img = None
bg_path = ASSETS / "bg_food.jpg"
if bg_path.exists():
    bg_img = get_base64_image(bg_path)

# ---------- CSS: tabs-as-cards, headings-in-cards, EDA images grid uniform ----------
st.markdown(f"""
<style>
:root {{
  --accent-1: #FF6B6B;
  --accent-2: #FF8E53;
  --muted: #6b7280;
  --dark: #111827;
  --card-bg: rgba(255,255,255,0.98);
  --glass: rgba(255,255,255,0.85);
  --card-radius: 14px;
  --shadow: 0 10px 30px rgba(15,23,42,0.08);
}}

.stApp {{
    {f'background-image: url("data:image/jpg;base64,{bg_img}");' if bg_img else ''}
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
    min-height: 100vh;
}}
.app-overlay {{
    position: absolute;
    inset: 0;
    background: rgba(255,255,255,0.70);
    z-index: 0;
    pointer-events: none;
}}

/* Header top card */
.header-card {{
  background: linear-gradient(90deg, var(--accent-1), var(--accent-2));
  padding: 1rem 1.25rem;
  border-radius: var(--card-radius);
  color: white;
  box-shadow: var(--shadow);
  margin-bottom: 1rem;
  z-index: 3;
}}
.header-card h1 {{ margin:0; font-size:1.9rem; font-weight:800; }}

/* Tab header container styled as card */
div[role="tablist"] {{
  display: inline-flex;
  gap: 0.5rem;
  padding: 8px;
  background: linear-gradient(180deg, rgba(255,255,255,0.96), rgba(250,250,250,0.94));
  border-radius: 12px;
  box-shadow: var(--shadow);
  border: 1px solid rgba(0,0,0,0.04);
  margin-bottom: 0.75rem;
  z-index: 3;
}}

/* Style individual Streamlit tabs (buttons) */
div[role="tablist"] > button {{
  background: transparent;
  border: none;
  padding: 10px 16px;
  border-radius: 10px;
  font-weight: 700;
  color: var(--dark);
  cursor: pointer;
  transition: transform .18s ease, box-shadow .18s ease;
  position: relative;
  overflow: hidden;
}}
div[role="tablist"] > button[aria-selected="true"] {{
  background: linear-gradient(90deg, var(--accent-1), var(--accent-2));
  color: white;
  box-shadow: 0 8px 20px rgba(255,107,107,0.12);
}}
div[role="tablist"] > button:hover {{
  transform: translateY(-3px);
  box-shadow: 0 12px 26px rgba(0,0,0,0.08);
}}

/* Main card wrapper for each tab's content */
.tab-content-card {{
  background: var(--card-bg);
  padding: 1rem;
  border-radius: 12px;
  box-shadow: var(--shadow);
  border: 1px solid rgba(0,0,0,0.04);
  margin-bottom: 1rem;
  z-index: 2;
}}

/* Headings inside cards: ensure they are within the card */
.card-heading {{
  font-size: 1.15rem;
  font-weight: 800;
  color: var(--dark);
  margin: 0 0 0.6rem 0;
}}

/* Stat Grid: uniform small cards inside tab card */
.stat-grid {{
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(170px, 1fr));
  gap: 12px;
  margin-bottom: 14px;
}}
.stat {{
  background: linear-gradient(180deg, rgba(255,255,255,0.98), rgba(248,248,248,0.98));
  padding: 0.7rem 0.9rem;
  border-radius: 10px;
  text-align: center;
  border: 1px solid rgba(0,0,0,0.04);
}}
.stat .label {{ color: var(--muted); font-size:0.88rem; }}
.stat .value {{ font-weight:800; font-size:1.35rem; color:var(--dark); }}

/* EDA image grid: uniform cells (image cropped to cover) */
.eda-grid {{
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 14px;
  align-items: start;
}}
.eda-item {{
  border-radius: 10px;
  overflow: hidden;
  background: linear-gradient(180deg, rgba(255,255,255,0.98), rgba(250,250,250,0.98));
  border: 1px solid rgba(0,0,0,0.04);
}}
.eda-item img {{
  width: 100%;
  height: 220px;
  object-fit: cover;
  display: block;
}}
.eda-caption {{
  padding: 10px;
  font-size: 0.92rem;
  color: var(--muted);
  background: rgba(255,255,255,0.98);
}}

/* recipe grid */
.recipe-grid {{
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 12px;
}}
.recipe-card {{
  padding: 12px;
  border-radius: 10px;
  border: 1px solid rgba(0,0,0,0.04);
  background: linear-gradient(180deg, rgba(255,255,255,0.98), rgba(248,248,248,0.98));
  transition: transform .22s ease, box-shadow .22s ease;
  min-height: 120px;
}}
.recipe-card:hover {{
  transform: translateY(-6px);
  box-shadow: 0 16px 36px rgba(12,12,12,0.08);
}}

/* caption and small text */
.small-muted {{ color: var(--muted); font-size:0.88rem; }}

/* footer */
.footer {{
  text-align:center;
  margin-top: 10px;
  padding: 10px;
  border-radius: 10px;
  color: var(--muted);
  background: rgba(255,255,255,0.96);
  border: 1px solid rgba(0,0,0,0.03);
}}

/* Accessibility high contrast fallback */
@media (prefers-contrast: more) {{
  :root {{ --card-bg: #ffffff; --muted:#111; --dark:#000; }}
}}
</style>
""", unsafe_allow_html=True)

# overlay element
st.markdown('<div class="app-overlay"></div>', unsafe_allow_html=True)

# --- Load data (unchanged) ---
@st.cache_resource
def load_data():
    with open('recommendations.pkl', 'rb') as f:
        recs = pickle.load(f)
    with open('light_recipe_info.pkl', 'rb') as f:
        info = pickle.load(f)
    return recs, info

recs, recipe_info = load_data()

# header
st.markdown("""
<div class="header-card">
  <h1>NHÓM 8 - Recipe Recommender System</h1>
  <div style="font-size:0.95rem;margin-top:6px;opacity:0.95">Personalized recommendations from 872K ratings — Hybrid SVD + CBF</div>
</div>
""", unsafe_allow_html=True)

# tabs
tab1, tab2 = st.tabs(["Data & EDA", "Model & Recommendation"])

# --- TAB 1 ---
with tab1:
    st.markdown('<div class="tab-content-card">', unsafe_allow_html=True)

    # Heading in card
    st.markdown('<div class="card-heading">Tổng quan Dữ liệu</div>', unsafe_allow_html=True)

    # stat grid (HTML)
    st.markdown("""
    <div class="stat-grid" aria-hidden="false">
        <div class="stat"><div class="label">Tổng Ratings</div><div class="value">872,021</div></div>
        <div class="stat"><div class="label">Số User (≥5)</div><div class="value">23,086</div></div>
        <div class="stat"><div class="label">Tổng Recipes</div><div class="value">231,637</div></div>
        <div class="stat"><div class="label">Rating TB</div><div class="value">4.41</div></div>
    </div>
    """, unsafe_allow_html=True)

    # EDA heading (in same tab card)
    st.markdown('<div style="height:8px;"></div>', unsafe_allow_html=True)
    st.markdown('<div class="card-heading">Phân tích Dữ liệu (EDA)</div>', unsafe_allow_html=True)

    # EDA images grid - uniform sizing & captions inside .eda-item
    def show_eda(img_path, caption):
        img_path = Path(img_path)
        if img_path.exists():
            st.markdown(f'''
                <div class="eda-item">
                    <img src="{img_path.as_posix()}" alt="{caption}">
                    <div class="eda-caption">{caption}</div>
                </div>
            ''', unsafe_allow_html=True)
        else:
            st.info(f"Missing image: {img_path.name}")

    # wrap grid container
    st.markdown('<div class="eda-grid">', unsafe_allow_html=True)
    show_eda(ASSETS / "eda_rating_distribution.png", "<strong>Phân bố điểm đánh giá</strong><div class='small-muted'>Hầu hết người dùng chấm 4-5 sao → dữ liệu tích cực.</div>")
    show_eda(ASSETS / "eda_Ratings_per_Recipe.png", "<strong>Số lượt đánh giá mỗi công thức</strong><div class='small-muted'>Phân bố lệch phải, vài món rất phổ biến.</div>")
    show_eda(ASSETS / "eda_Average Rating vs Number of Ingredients.png", "<strong>Số nguyên liệu vs Rating</strong><div class='small-muted'>Công thức đơn giản (5-10 nguyên liệu) được đánh giá cao hơn.</div>")
    show_eda(ASSETS / "eda_Word Cloud for Ingredients.png", "<strong>Từ khóa nguyên liệu</strong><div class='small-muted'>Chicken, sugar, butter, flour, garlic...</div>")
    show_eda(ASSETS / "eda_Word Cloud for Tags.png", "<strong>Từ khóa thẻ (tags)</strong><div class='small-muted'>Easy, quick, dessert, healthy...</div>")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# --- TAB 2 ---
with tab2:
    st.markdown('<div class="tab-content-card">', unsafe_allow_html=True)
    st.markdown('<div class="card-heading">Chọn Model & User</div>', unsafe_allow_html=True)
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
        st.markdown('<div style="height:8px;"></div>', unsafe_allow_html=True)
        st.markdown('<div class="card-heading">Hiệu suất Model</div>', unsafe_allow_html=True)

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

        st.markdown('<div style="height:8px;"></div>', unsafe_allow_html=True)
        st.markdown('<div class="card-heading">Top-20 Recipe Đề Xuất</div>', unsafe_allow_html=True)

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
                        <div style="font-weight:800;color:var(--dark);font-size:0.98rem;margin-bottom:6px;">{name}</div>
                        <div class="small-muted"><code>{rid}</code></div>
                        <div style="height:6px;"></div>
                        <div class="small-muted">Tags: {tags}</div>
                    </div>
                """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# footer
st.markdown("""
<div class="footer">
  <div><strong>NHÓM 8</strong> | Recipe Recommender System | Project 2025</div>
  <div style="font-size:0.92rem;color:var(--muted)">Đề xuất cá nhân hóa từ 872K đánh giá — Hybrid SVD + CBF</div>
</div>
""", unsafe_allow_html=True)
