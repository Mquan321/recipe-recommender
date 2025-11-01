# app.py (UI-enhanced version) — REPLACE your existing app.py with this content
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

# prepare page background (if exists)
bg_path = ASSETS / "bg_food.jpg"
bg_img = get_base64_image(bg_path) if bg_path.exists() else None

# ----------------- CSS (enhanced) -----------------
st.markdown(f"""
<style>
:root {{
  --card-radius: 14px;
  --card-bg: rgba(255,255,255,0.96);
  --muted: #6b6b6b;
  --accent-1: #FF6B6B;
  --accent-2: #FF8E53;
  --accent-contrast: #222;
  --glass: rgba(255,255,255,0.94);
  --shadow: 0 10px 30px rgba(12,12,12,0.08);
}}

/* Background */
.stApp {{
    {f'background-image: url("data:image/jpg;base64,{bg_img}");' if bg_img else ''}
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}}
.app-overlay {{
    position: absolute; inset: 0;
    background: rgba(255,255,255,0.70);
    z-index: 0;
    pointer-events: none;
}}

/* Header */
.main-header {{
    border-radius: var(--card-radius);
    padding: 1rem 1.25rem;
    background: linear-gradient(90deg,var(--accent-1),var(--accent-2));
    color: white;
    box-shadow: var(--shadow);
    position: relative; z-index: 3;
}}
.main-header h1 {{ margin: 0; font-size: 2.05rem; letter-spacing: -0.5px; }}
.main-header p {{ margin: 4px 0 0; opacity: .95 }}

/* Generic card */
.card {{
  background: var(--card-bg);
  border-radius: var(--card-radius);
  padding: 1rem;
  box-shadow: var(--shadow);
  border: 1px solid rgba(0,0,0,0.04);
  position: relative;
  z-index: 2;
  margin-bottom: 1rem;
}}

/* Tab container: wrap whole tabs into a visible card */
.tab-wrapper {{
  padding: 8px;
  border-radius: 12px;
  background: linear-gradient(180deg, rgba(255,255,255,0.98), rgba(247,247,247,0.96));
  border: 1px solid rgba(0,0,0,0.04);
  box-shadow: 0 8px 20px rgba(0,0,0,0.04);
  margin-bottom: 1rem;
}}

/* Streamlit tab buttons styling (generic selectors) */
div[role="tablist"] {{
    display: flex;
    gap: 8px;
    padding: 8px;
    margin-bottom: 8px;
}}
div[role="tablist"] button {{
    border-radius: 10px;
    padding: 8px 14px;
    border: 1px solid rgba(0,0,0,0.05);
    background: linear-gradient(180deg, rgba(255,255,255,0.98), rgba(249,249,249,0.98));
    box-shadow: 0 6px 14px rgba(0,0,0,0.04);
    transition: transform .18s ease, box-shadow .18s ease, background .18s ease;
    font-weight: 600;
    color: var(--accent-contrast);
}
div[role="tablist"] button:hover {{
    transform: translateY(-3px);
    box-shadow: 0 14px 28px rgba(0,0,0,0.08);
}}
div[role="tablist"] button[aria-selected="true"] {{
    background: linear-gradient(90deg,var(--accent-1),var(--accent-2));
    color: white;
    box-shadow: 0 16px 36px rgba(255,107,107,0.12);
    border: none;
}}

/* Headings inside sections */
.section-title {{
    font-size: 1.25rem;
    margin: 0 0 10px 0;
    color: var(--accent-contrast);
}}

/* stat grid: evenly spaced metric cards */
.stat-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
    gap: 12px;
    align-items: stretch;
}}
.stat {{
    background: linear-gradient(180deg, rgba(255,255,255,0.99), rgba(250,250,250,0.97));
    border-radius: 10px;
    padding: 12px;
    text-align: center;
    border: 1px solid rgba(0,0,0,0.04);
}}
.stat .label {{ color: var(--muted); font-size: 0.9rem; }}
.stat .value {{ font-size: 1.45rem; font-weight: 800; color: var(--accent-contrast); }}

/* EDA image grid tiles */
.eda-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
    gap: 12px;
    align-items: stretch;
}}
.eda-tile {{
    border-radius: 12px;
    overflow: hidden;
    background: linear-gradient(180deg, rgba(255,255,255,0.98), rgba(248,248,248,0.98));
    border: 1px solid rgba(0,0,0,0.04);
    display: flex;
    flex-direction: column;
    height: 240px;
}}
.eda-tile img {{
    width: 100%;
    height: 160px;
    object-fit: cover;
    display: block;
}}
.eda-tile .tile-body {{
    padding: 10px;
    flex: 1;
}}
.tile-caption {{
    color: var(--muted);
    font-size: 0.9rem;
    line-height: 1.15;
}}

/* recipe card */
.recipe-card {{
    border-radius: 12px;
    padding: 10px;
    min-height: 120px;
    transition: transform .2s ease, box-shadow .2s ease;
    border: 1px solid rgba(0,0,0,0.04);
    background: linear-gradient(180deg, rgba(255,255,255,0.98), rgba(247,247,247,0.96));
}}
.recipe-card:hover {{
    transform: translateY(-6px);
    box-shadow: 0 18px 36px rgba(0,0,0,0.08);
}}
.recipe-title {{ font-weight: 700; color: var(--accent-contrast); margin-bottom: 6px; }}
.recipe-sub {{ color: var(--muted); font-size: 0.85rem; }}

/* footer */
.site-footer {{
    margin-top: 16px;
    border-radius: 10px;
    padding: 12px;
    text-align: center;
    color: var(--muted);
    background: rgba(255,255,255,0.92);
    border: 1px solid rgba(0,0,0,0.03);
}}

/* Accessibility: high-contrast fallback */
@media (prefers-contrast: more) {{
  :root {{ --card-bg: #fff; --accent-contrast: #000; }}
}}

/* small screens: reduce image height */
@media (max-width: 640px) {{
  .eda-tile {{ height: 200px; }}
  .eda-tile img {{ height: 120px; }}
}}

</style>
""", unsafe_allow_html=True)

# overlay to keep text readable on images
st.markdown('<div class="app-overlay"></div>', unsafe_allow_html=True)

# ----------------- Data loading (unchanged) -----------------
@st.cache_resource
def load_data_pickles():
    with open('recommendations.pkl', 'rb') as f:
        recs = pickle.load(f)
    with open('light_recipe_info.pkl', 'rb') as f:
        info = pickle.load(f)
    return recs, info

recs, recipe_info = load_data_pickles()

# ----------------- Header -----------------
st.markdown("""
<div class="main-header">
  <h1>NHÓM 8 - Recipe Recommender System</h1>
  <p>Personalized recommendations from <strong>872K</strong> ratings — Hybrid SVD + CBF</p>
</div>
""", unsafe_allow_html=True)

# ----------------- Tabs inside a visible wrapper card -----------------
st.markdown('<div class="tab-wrapper card">', unsafe_allow_html=True)
tab1, tab2 = st.tabs(["Data & EDA", "Model & Recommendation"])

# ----------------- Tab 1: Data & EDA -----------------
with tab1:
    # wrap section in card
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Tổng quan Dữ liệu</div>', unsafe_allow_html=True)

    # metrics grid (HTML ensures no stray empty boxes)
    st.markdown("""
    <div class="stat-grid" style="margin-top:6px;">
        <div class="stat"><div class="label">Tổng Ratings</div><div class="value">872,021</div></div>
        <div class="stat"><div class="label">Số User (≥5)</div><div class="value">23,086</div></div>
        <div class="stat"><div class="label">Tổng Recipes</div><div class="value">231,637</div></div>
        <div class="stat"><div class="label">Rating TB</div><div class="value">4.41</div></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # EDA section card with responsive grid of tiles
    st.markdown('<div class="card" style="margin-top:10px;">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Phân tích Dữ liệu (EDA)</div>', unsafe_allow_html=True)

    # prepare list of eda images & captions (order matters)
    eda_files = [
        ("eda_rating_distribution.png", "**Phân bố điểm đánh giá**: Hầu hết chấm 4-5 sao."),
        ("eda_Ratings_per_Recipe.png", "**Số lượt đánh giá mỗi công thức**: Phân bố lệch phải."),
        ("eda_Average Rating vs Number of Ingredients.png", "**Số nguyên liệu vs Rating**: Công thức 5-10 nguyên liệu được ưa chuộng."),
        ("eda_Word Cloud for Ingredients.png", "**Từ khóa nguyên liệu**: Chicken, sugar, butter, flour, garlic..."),
        ("eda_Word Cloud for Tags.png", "**Từ khóa thẻ (tags)**: Easy, quick, dessert, healthy...")
    ]

    # build eda grid HTML with embedded base64 images (keeps layout consistent)
    tiles_html = ['<div class="eda-grid">']
    for fname, caption in eda_files:
        p = ASSETS / fname
        if p.exists():
            b64 = get_base64_image(p)
            tiles_html.append(f"""
            <div class="eda-tile">
                <img src="data:image/png;base64,{b64}" alt="{fname}" />
                <div class="tile-body">
                    <div class="tile-caption">{caption}</div>
                </div>
            </div>
            """)
        else:
            # placeholder tile (so layout stays stable)
            tiles_html.append(f"""
            <div class="eda-tile" style="display:flex;align-items:center;justify-content:center;">
                <div class="tile-body">
                    <div class="tile-caption">Missing: {fname}</div>
                </div>
            </div>
            """)
    tiles_html.append('</div>')
    st.markdown("".join(tiles_html), unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)  # end eda card

# ----------------- Tab 2: Model & Recommendation -----------------
with tab2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
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

    # action
    if st.button("Recommend Top-20", type="primary", use_container_width=True):
        top20 = recs[model_key].get(user_id, [])

        # performance card
        st.markdown('<div class="card" style="margin-top:10px;">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Hiệu suất Model</div>', unsafe_allow_html=True)
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

        # Top-20 grid
        st.markdown('<div class="card" style="margin-top:12px;">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Top-20 Recipe Đề Xuất</div>', unsafe_allow_html=True)

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
                        <div style="height:8px"></div>
                        <div class="recipe-sub">Tags: {tags}</div>
                    </div>
                    """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)  # end top20 card

    st.markdown('</div>', unsafe_allow_html=True)  # end model card

st.markdown("""
<div class="site-footer card">
    <div><strong>NHÓM 8</strong> | Recipe Recommender System | Project 2025</div>
    <div style="font-size:0.92rem; color: #555;"><em>Đề xuất cá nhân hóa từ 872K đánh giá – Hybrid SVD + CBF</em></div>
</div>
""", unsafe_allow_html=True)
