import streamlit as st
import pickle
import base64
from pathlib import Path

# ====================== CONFIG ======================
st.set_page_config(
    page_title="NHÓM 8 - Recipe Recommender",
    page_icon="🍳",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ====================== UTILS ======================
def get_base64_image(path):
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except:
        return None

ASSETS = Path("assets")
bg_path = ASSETS / "bg_food.jpg"
bg_img = get_base64_image(bg_path)

# ====================== CSS ======================
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
:root{{
  --card-bg: rgba(255,255,255,0.98);
  --card-border: rgba(0,0,0,0.08);
  --accent-1: #FF6B6B;
  --accent-2: #FF8E53;
  --accent-contrast: #1a1a1a;
  --muted: #4a5568;
  --muted-light: #718096;
  --card-radius: 16px;
  --shadow: 0 8px 24px rgba(0,0,0,0.12);
  --shadow-hover: 0 12px 32px rgba(0,0,0,0.18);
  --transition: all 0.3s cubic-bezier(0.4,0,0.2,1);
}}
* {{ font-family: 'Inter', sans-serif; }}
.stApp {{ 
    {f'background-image: url("data:image/jpg;base64,{bg_img}");' if bg_img else ''}
    background-size: cover; background-position: center; background-attachment: fixed;
}}
.app-overlay {{ position:fixed; inset:0; background:linear-gradient(135deg,rgba(255,255,255,0.75),rgba(245,247,250,0.8)); z-index:0; pointer-events:none; }}
.main-header {{
    background: linear-gradient(135deg,#667eea,#764ba2,#f093fb);
    padding:2rem 1.5rem; border-radius:var(--card-radius); text-align:center;
    box-shadow:var(--shadow); color:white; margin-bottom:1.75rem;
    border:1px solid rgba(255,255,255,0.2);
}}
.main-header h1 {{ margin:0; font-size:2.5rem; font-weight:800; letter-spacing:-1.2px; }}
.main-header .subtitle {{ font-size:1.05rem; margin-top:0.5rem; opacity:0.95; }}
.stTabs {{ background:var(--card-bg); border-radius:var(--card-radius); padding:0.5rem;
    box-shadow:var(--shadow); border:1px solid var(--card-border); margin-bottom:1.5rem; }}
.stTabs [data-baseweb="tab"] {{
    background:linear-gradient(135deg,rgba(255,255,255,0.6),rgba(248,250,252,0.6));
    border-radius:12px; padding:0.85rem 2rem; font-weight:600; transition:var(--transition);
}}
.stTabs [data-baseweb="tab"]:hover {{ background:linear-gradient(135deg,rgba(255,255,255,0.9),rgba(248,250,252,0.9)); transform:translateY(-2px); }}
.stTabs [data-baseweb="tab"][aria-selected="true"] {{
    background:linear-gradient(135deg,var(--accent-1),var(--accent-2)); color:white;
    box-shadow:0 6px 20px rgba(255,107,107,0.35);
}}
.section-header {{ background:linear-gradient(135deg,rgba(102,126,234,0.08),rgba(118,75,162,0.08));
    padding:1.25rem 1.5rem; border-radius:12px; border-left:4px solid var(--accent-1); }}
.section-header h2, .section-header h3 {{ margin:0; color:var(--accent-contrast); font-weight:700; }}
.card {{ background:var(--card-bg); border-radius:var(--card-radius); padding:1.5rem;
    box-shadow:var(--shadow); border:1px solid var(--card-border); margin-bottom:1.25rem; }}
.stat-grid {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(200px,1fr)); gap:1.25rem; margin:1.5rem 0; }}
.stat {{ background:linear-gradient(135deg,rgba(255,255,255,0.98),rgba(250,252,255,0.98));
    border-radius:14px; padding:1.5rem 1.25rem; text-align:center; border:2px solid rgba(102,126,234,0.12); }}
.stat:hover {{ transform:translateY(-4px); box-shadow:0 12px 28px rgba(102,126,234,0.2); border-color:var(--accent-1); }}
.stat .label {{ font-size:0.95rem; color:var(--muted); font-weight:600; text-transform:uppercase; }}
.stat .value {{ font-size:2rem; font-weight:800; background:linear-gradient(135deg,var(--accent-1),var(--accent-2));
    -webkit-background-clip:text; -webkit-text-fill-color:transparent; }}
.eda-container {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(450px,1fr)); gap:1.5rem; margin:1.5rem 0; }}
.eda-card {{ background:var(--card-bg); border-radius:var(--card-radius); padding:1.25rem;
    box-shadow:var(--shadow); border:1px solid var(--card-border); }}
.eda-card:hover {{ transform:translateY(-4px); box-shadow:var(--shadow-hover); }}
.eda-caption {{ background:linear-gradient(135deg,rgba(102,126,234,0.05),rgba(118,75,162,0.05));
    padding:0.85rem 1.1rem; border-radius:8px; font-size:0.92rem; color:var(--muted); border-left:3px solid var(--accent-1); }}
.recipe-card {{ background:linear-gradient(135deg,rgba(255,255,255,0.98),rgba(250,252,255,0.98));
    padding:1.25rem; border-radius:14px; border:2px solid rgba(102,126,234,0.12); min-height:160px;
    position:relative; display:flex; flex-direction:column; justify-content:space-between; }}
.recipe-card:hover {{ transform:translateY(-6px); box-shadow:0 20px 40px rgba(102,126,234,0.2); border-color:var(--accent-1); }}
.recipe-card::after {{ content:""; position:absolute; inset:0;
    background:linear-gradient(120deg,transparent 0%,rgba(255,255,255,0.3) 50%,transparent 100%);
    transform:translateX(-120%); transition:transform 0.8s ease; opacity:0; border-radius:14px; }}
.recipe-card:hover::after {{ transform:translateX(120%); opacity:1; }}
.divider {{ border:none; height:2px; background:linear-gradient(90deg,transparent,rgba(102,126,234,0.2),transparent); margin:1.5rem 0; }}
.footer {{ text-align:center; margin-top:2.5rem; padding:1.5rem; background:var(--card-bg);
    border-radius:var(--card-radius); border:1px solid var(--card-border); box-shadow:var(--shadow); }}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="app-overlay"></div>', unsafe_allow_html=True)

# ====================== LOAD DATA + FIX KEY ERROR ======================
@st.cache_resource
def load_data():
    # Load recommendations
    with open('recommendations_3models.pkl', 'rb') as f:
        recs_raw = pickle.load(f)
    
    # FIX: chuyển tất cả recipe_id về int thuần
    recs = {}
    for model in recs_raw:
        recs[model] = {}
        for user, recipes in recs_raw[model].items():
            recs[model][user] = [int(rid) for rid in recipes]
    
    # Load recipe info
    with open('light_recipe_info.pkl', 'rb') as f:
        info_raw = pickle.load(f)
    
    # Đảm bảo key là int
    recipe_info = {int(k): v for k, v in info_raw.items()}
    
    return recs, recipe_info

recs, recipe_info = load_data()

# ====================== HEADER ======================
st.markdown("""
<div class="main-header">
    <h1>🍳 NHÓM 8 - Recipe Recommender System</h1>
    <div class="subtitle">Personalized recommendations from 872K ratings</div>
</div>
""", unsafe_allow_html=True)

# ====================== TABS ======================
tab1, tab2 = st.tabs(["📊 Data & EDA", "🤖 Model & Recommendation"])

with tab1:
    # --- Stats ---
    st.markdown("""
    <div class="section-header"><h2>📈 Tổng quan Dữ liệu</h2></div>
    <div class="stat-grid">
        <div class="stat"><div class="label">Tổng Ratings</div><div class="value">872,021</div></div>
        <div class="stat"><div class="label">Số User (≥5)</div><div class="value">23,086</div></div>
        <div class="stat"><div class="label">Tổng Recipes</div><div class="value">231,637</div></div>
        <div class="stat"><div class="label">Rating TB</div><div class="value">4.41</div></div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    # --- EDA Images ---
    st.markdown("""<div class="section-header"><h3>🔍 EDA</h3></div>""", unsafe_allow_html=True)
    eda_images = [
        ("eda_rating_distribution.png", "**Phân bố điểm đánh giá**"),
        ("eda_Ratings_per_Recipe.png", "**Số lượt đánh giá mỗi công thức**"),
        ("eda_Average Rating vs Number of Ingredients.png", "**Số nguyên liệu vs Rating**"),
        ("eda_Word Cloud for Ingredients.png", "**Từ khóa nguyên liệu phổ biến**"),
        ("eda_Word Cloud for Tags.png", "**Từ khóa thẻ (tags)**"),
    ]
    st.markdown('<div class="eda-container">', unsafe_allow_html=True)
    for fname, caption in eda_images:
        path = ASSETS / fname
        if path.exists():
            b64 = get_base64_image(path)
            st.markdown(f"""
            <div class="eda-card">
                <img src="data:image/png;base64,{b64}">
                <div class="eda-caption">{caption}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='eda-card'><div class='eda-caption'>⚠️ Missing: {fname}</div></div>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # --- Videos ---
    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown("""<div class="section-header"><h3>🎬 Dynamic Analysis</h3></div>""", unsafe_allow_html=True)
    _, c, _ = st.columns([0.5, 3, 0.5])
    with c:
        st.markdown('<div class="eda-container" style="grid-template-columns: repeat(2,1fr);">', unsafe_allow_html=True)
        for fname, caption in [
            ("eda_top_popular_recipes.mp4", "**Top Popular Recipes Animation**"),
            ("eda_Time vs Rating Correlation.mp4", "**Time vs Rating Correlation**")
        ]:
            path = ASSETS / fname
            if path.exists():
                b64 = get_base64_image(path)
                st.markdown(f"""
                <div class="eda-card">
                    <video width="100%" style="border-radius:10px;" autoplay loop muted playsinline>
                        <source src="data:video/mp4;base64,{b64}" type="video/mp4">
                    </video>
                    <div class="eda-caption">{caption}</div>
                </div>
                """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.markdown("""<div class="section-header"><h2>⚙️ Chọn Model & User</h2></div>""", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        model_choice = st.selectbox(
            "Chọn Model",
            [
                "Hybrid Simple (α=0.9 SVD)",
                "Hybrid CBF (α=0.7 SVD + 0.3 CBF)",
                "Hybrid SVD+Tag (α=0.6 SVD + 0.4 Tag)"
            ],
            help="Hybrid Simple: ưu tiên hành vi | CBF: nội dung | SVD+Tag: kết hợp tag genome"
        )
        model_key = 'fast' if "Simple" in model_choice else 'best' if "CBF" in model_choice else 'tag'
    
    with col2:
        user_id = st.selectbox(
            "Chọn User ID",
            sorted(recs[model_key].keys()),
            help="10 user có nhiều tương tác nhất"
        )

    if st.button("🎯 Recommend Top-20 Recipes", type="primary", use_container_width=True):
        top20 = recs[model_key][user_id]

        # --- Metrics ---
        st.markdown("""<div class="section-header"><h3>📊 Hiệu suất Model</h3></div>""", unsafe_allow_html=True)
        
        if model_key == 'fast':
            rmse, r2 = "0.9471", "0.0869"
            p20, r20, ndcg20, map20 = "0.0050", "0.1000", "0.0384", "0.0222"
        elif model_key == 'best':
            rmse, r2 = "0.9467", "0.0878"
            p20, r20, ndcg20, map20 = "0.0030", "0.0600", "0.0196", "0.0086"
        else:  # tag
            rmse, r2 = "0.9465", "0.0882"
            p20, r20, ndcg20, map20 = "0.0080", "0.1600", "0.0621", "0.0415"

        cm1, cm2 = st.columns([1, 2])
        with cm1:
            st.markdown(f"""
            <div style="background:linear-gradient(135deg,rgba(102,126,234,0.08),rgba(118,75,162,0.08));
                        padding:1.25rem; border-radius:12px; border-left:4px solid var(--accent-1);">
                <h4 style="margin:0 0 1rem 0; color:var(--accent-contrast); font-weight:700;">Regression Metrics</h4>
                <div class="stat"><div class="label">RMSE</div><div class="value">{rmse}</div></div>
                <div class="stat"><div class="label">R²</div><div class="value">{r2}</div></div>
            </div>
            """, unsafe_allow_html=True)
        with cm2:
            st.markdown(f"""
            <div style="background:linear-gradient(135deg,rgba(255,107,107,0.08),rgba(255,142,83,0.08));
                        padding:1.25rem; border-radius:12px; border-left:4px solid var(--accent-2);">
                <h4 style="margin:0 0 1rem 0; color:var(--accent-contrast); font-weight:700;">Ranking Metrics @20</h4>
                <div style="display:grid; grid-template-columns:repeat(4,1fr); gap:0.75rem;">
                    <div class="stat"><div class="label">P@20</div><div class="value">{p20}</div></div>
                    <div class="stat"><div class="label">R@20</div><div class="value">{r20}</div></div>
                    <div class="stat"><div class="label">nDCG@20</div><div class="value">{ndcg20}</div></div>
                    <div class="stat"><div class="label">mAP@20</div><div class="value">{map20}</div></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # --- Recommendations ---
        st.markdown("""<div class="section-header" style="margin-top:2rem;"><h3>🍽️ Top-20 Recipe Đề Xuất</h3></div>""", unsafe_allow_html=True)
        cols = st.columns(4)
        for i, rid in enumerate(top20):
            rid = int(rid)  # Bảo vệ 100%
            with cols[i % 4]:
                name = recipe_info[rid]['name']
                tags = ", ".join(recipe_info[rid]['tags'][:2])
                st.markdown(f"""
                <div class="recipe-card">
                    <p class="recipe-title">{name}</p>
                    <p style="margin:0.3rem 0 0; font-size:0.9rem; color:#666;"><code>{rid}</code></p>
                    <p style="margin:0.2rem 0 0; font-size:0.85rem; color:#FF6B6B;">Tags: {tags}</p>
                </div>
                """, unsafe_allow_html=True)

# ====================== FOOTER ======================
st.markdown("""
<div class="footer">
    <p><strong>NHÓM 8</strong> | Recipe Recommender System | Project 2025</p>
    <p><em>Đề xuất cá nhân hóa từ 872K đánh giá – Hybrid SVD + CBF + Tag Genome</em></p>
</div>
""", unsafe_allow_html=True)
