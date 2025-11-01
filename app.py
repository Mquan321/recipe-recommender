# app.py (REPLACE your file with this)
import streamlit as st
import pickle
from pathlib import Path
import base64

st.set_page_config(page_title="NHÓM 8- Recipe Recommender", page_icon="🍳", layout="wide")

ASSETS = Path("assets")

def get_base64_image(image_path):
    if not Path(image_path).exists():
        return ""
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

bg_b64 = get_base64_image(ASSETS / "bg_food.jpg")

# ============== CSS (accessible, controlled cards and fake tabs) ==============
st.markdown(f"""
<style>
:root {{
  --card-radius: 14px;
  --accent-1: #FF6B6B;
  --accent-2: #FF8E53;
  --text: #222;
  --muted: #6b6b6b;
  --card-bg: rgba(255,255,255,0.96);
  --glass: rgba(255,255,255,0.84);
  --shadow: 0 10px 30px rgba(12,12,12,0.08);
  --tab-height: 48px;
  font-family: -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial;
}}

/* Page background */
.stApp {{
    background-image: url("data:image/jpg;base64,{bg_b64}");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}}
/* Soft overlay to improve contrast */
.app-overlay {{
    position: absolute; inset: 0; z-index: 0;
    background: linear-gradient(rgba(255,255,255,0.66), rgba(255,255,255,0.66));
    pointer-events: none;
}}

/* Outer container card that will contain the fake-tabs and content */
.outer-card {{
  background: var(--card-bg);
  border-radius: var(--card-radius);
  padding: 1rem;
  box-shadow: var(--shadow);
  border: 1px solid rgba(0,0,0,0.04);
  margin-bottom: 1rem;
  position: relative;
  z-index: 2;
}}

/* Fake tabs (radio look) */
.fake-tabs {{
  display:flex;
  gap:8px;
  align-items:center;
  margin-bottom:10px;
}}
.fake-tab {{
  height: var(--tab-height);
  padding: 0 18px;
  border-radius: 10px;
  display:flex;
  align-items:center;
  justify-content:center;
  cursor: pointer;
  font-weight:600;
  color:var(--muted);
  background: linear-gradient(180deg, rgba(255,255,255,0.98), rgba(248,248,248,0.98));
  border: 1px solid rgba(0,0,0,0.03);
  transition: all .22s ease;
}
.fake-tab.selected {{
  color: white;
  background: linear-gradient(90deg, var(--accent-1), var(--accent-2));
  box-shadow: 0 8px 20px rgba(255,107,107,0.15);
  transform: translateY(-2px);
}

/* Heading inside card */
.card-heading {{
  font-size:1.25rem;
  font-weight:700;
  color:var(--text);
  margin-bottom:6px;
}}
.card-subhead {{
  color:var(--muted);
  margin-bottom:10px;
}}

/* stat grid */
.stat-grid {{
  display:grid;
  grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
  gap:12px;
}}
.stat {{
  background: linear-gradient(180deg, rgba(255,255,255,0.99), rgba(250,250,250,0.99));
  padding:10px;
  border-radius:10px;
  border:1px solid rgba(0,0,0,0.03);
  text-align:center;
}}
.stat .label {{ color:var(--muted); font-size:0.9rem; }}
.stat .value {{ font-size:1.35rem; font-weight:700; color:var(--text); }}

/* EDA image grid: use HTML images for precise layout */
.eda-grid {{
  display:grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap:12px;
  margin-top:8px;
}}
.eda-item img {{
  width:100%;
  height:220px;
  object-fit:cover;
  border-radius:10px;
  display:block;
  border:1px solid rgba(0,0,0,0.04);
}}
.eda-caption {{
  background: rgba(255,255,255,0.95);
  padding:8px;
  border-radius:8px;
  margin-top:6px;
  color:var(--muted);
  font-size:0.9rem;
  border:1px solid rgba(0,0,0,0.03);
}}

/* Recipe grid and recipe card */
.recipe-grid {{
  display:grid;
  grid-template-columns: repeat(4, 1fr);
  gap:12px;
  margin-top:12px;
}}
@media (max-width: 1000px) {{
  .recipe-grid {{ grid-template-columns: repeat(2, 1fr); }}
}}
@media (max-width: 600px) {{
  .recipe-grid {{ grid-template-columns: 1fr; }}
}}
.recipe-card {{
  background: linear-gradient(180deg, rgba(255,255,255,0.98), rgba(250,250,250,0.98));
  padding:12px;
  border-radius:10px;
  min-height:120px;
  display:flex; flex-direction:column;
  justify-content:flex-start;
  border:1px solid rgba(0,0,0,0.03);
  transition: transform .22s ease, box-shadow .22s ease;
  position:relative;
}}
.recipe-card:hover {{
  transform: translateY(-6px);
  box-shadow: 0 20px 40px rgba(12,12,12,0.12);
}}
.recipe-title {{ font-weight:700; color:var(--text); margin-bottom:6px; }}
.recipe-meta {{ color:var(--muted); font-size:0.88rem; }}

/* footer */
.footer {{
  text-align:center;
  color:var(--muted);
  margin-top:10px;
  font-size:0.95rem;
}}

/* accessibility: high contrast fallback */
@media (prefers-contrast: more) {{
  :root {{ --card-bg: #fff; --text: #000; --muted:#333; }}
}}
</style>
""", unsafe_allow_html=True)

# overlay to increase contrast
st.markdown('<div class="app-overlay"></div>', unsafe_allow_html=True)

# ============== load data (cached) =================
@st.cache_resource
def load_data():
    try:
        with open('recommendations.pkl', 'rb') as f:
            recs = pickle.load(f)
    except Exception:
        recs = {"fast": {}, "best": {}}
    try:
        with open('light_recipe_info.pkl', 'rb') as f:
            info = pickle.load(f)
    except Exception:
        info = {}
    return recs, info

recs, recipe_info = load_data()

# ============== Header (outside outer card) ==============
st.markdown(f"""
<div class="outer-card">
  <div style="display:flex;justify-content:space-between;align-items:center;gap:10px;flex-wrap:wrap">
    <div>
      <div style="font-size:1.6rem;font-weight:700;color:var(--text)">NHÓM 8 - Recipe Recommender System</div>
      <div style="color:var(--muted);margin-top:4px">Personalized recommendations from 872,021 ratings</div>
    </div>
    <div style="min-width:220px;text-align:right;color:var(--muted);font-size:0.95rem">
      Project 2025 · Hybrid SVD + CBF
    </div>
  </div>

  <div style="height:12px"></div>

  <!-- fake tabs -->
  <div class="fake-tabs" id="fakeTabs">
    <div class="fake-tab selected" id="tab0">Data &amp; EDA</div>
    <div class="fake-tab" id="tab1">Model &amp; Recommendation</div>
  </div>
</div>
""", unsafe_allow_html=True)

# We'll implement actual tab switching via a Streamlit radio (so we can style nicely)
tab = st.radio("", ("Data & EDA", "Model & Recommendation"), horizontal=True)
st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

# ---------------- Tab: Data & EDA ----------------
if tab == "Data & EDA":
    st.markdown('<div class="outer-card">', unsafe_allow_html=True)
    st.markdown('<div class="card-heading">Tổng quan Dữ liệu</div>', unsafe_allow_html=True)
    st.markdown('<div class="card-subhead">Các chỉ số tóm tắt của bộ dữ liệu (số liệu đã tiền xử lý)</div>', unsafe_allow_html=True)

    # stat grid using HTML so it won't create stray streamlit boxes
    st.markdown("""
    <div class="stat-grid" style="margin-top:8px;">
      <div class="stat"><div class="label">Tổng Ratings</div><div class="value">872,021</div></div>
      <div class="stat"><div class="label">Số User (≥5)</div><div class="value">23,086</div></div>
      <div class="stat"><div class="label">Tổng Recipes</div><div class="value">231,637</div></div>
      <div class="stat"><div class="label">Rating TB</div><div class="value">4.41</div></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<hr style="margin:14px 0;border:none;border-top:1px solid rgba(0,0,0,0.05)">', unsafe_allow_html=True)

    # EDA heading (in card)
    st.markdown('<div class="card-heading">Phân tích Dữ liệu (EDA)</div>', unsafe_allow_html=True)
    st.markdown('<div class="card-subhead">Các biểu đồ chính — bố cục ảnh được điều chỉnh đều, caption nằm trong card nhỏ bên dưới ảnh.</div>', unsafe_allow_html=True)

    # list of eda images with captions (adjust to whatever exists)
    eda_items = [
        ("assets/eda_rating_distribution.png", "Phân bố điểm đánh giá: Hầu hết chấm 4-5 sao."),
        ("assets/eda_Ratings_per_Recipe.png", "Số lượt đánh giá mỗi công thức: phân bố lệch phải."),
        ("assets/eda_Average Rating vs Number of Ingredients.png", "Số nguyên liệu vs Rating trung bình."),
        ("assets/eda_Word Cloud for Ingredients.png", "Từ khóa nguyên liệu phổ biến."),
        ("assets/eda_Word Cloud for Tags.png", "Từ khóa thẻ (tags).")
    ]

    # render grid with HTML images to avoid streamlit image boxes (keeps layout clean)
    eda_html = ['<div class="eda-grid">']
    for img_path, caption in eda_items:
        if Path(img_path).exists():
            eda_html.append(f'''
              <div class="eda-item">
                <img src="{img_path}" alt="{caption}">
                <div class="eda-caption">{caption}</div>
              </div>
            ''')
    eda_html.append('</div>')
    st.markdown("".join(eda_html), unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)  # close outer-card

# ---------------- Tab: Model & Recommendation ----------------
else:
    st.markdown('<div class="outer-card">', unsafe_allow_html=True)
    st.markdown('<div class="card-heading">Model & Recommendation</div>', unsafe_allow_html=True)
    st.markdown('<div class="card-subhead">Chọn model và user để sinh Top-20 đề xuất. Metrics & ranking nằm trong cùng card để đọc liền mạch.</div>', unsafe_allow_html=True)

    left, right = st.columns([2, 1])
    with left:
        model_choice = st.selectbox("Chọn Model", ["Hybrid Simple (α=0.9 SVD)", "Hybrid CBF (α=0.7 SVD + 0.3 CBF)"])
        model_key = 'fast' if "Simple" in model_choice else 'best'
        try:
            user_list = sorted([str(x) for x in recs[model_key].keys()])
        except Exception:
            user_list = ["user_1", "user_2"]
        user_id = st.selectbox("Chọn User ID", user_list)
    with right:
        st.write("")  # space
        if st.button("Recommend Top-20", use_container_width=True):
            pass

    # On button click show metrics and recipes
    if st.button("Run Recommendation", key="run_rec"):
        top20 = recs.get(model_key, {}).get(user_id, [])
        # metrics block
        st.markdown("""
        <div style="margin-top:8px;">
          <div class="stat-grid">
            <div class="stat"><div class="label">RMSE</div><div class="value">0.947</div></div>
            <div class="stat"><div class="label">R²</div><div class="value">0.087</div></div>
            <div class="stat"><div class="label">P@20</div><div class="value">0.003</div></div>
            <div class="stat"><div class="label">R@20</div><div class="value">0.060</div></div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div style="height:10px"></div>', unsafe_allow_html=True)
        st.markdown('<div class="card-heading">Top-20 Recipe Đề Xuất</div>', unsafe_allow_html=True)

        if not top20:
            st.info("Không có đề xuất cho user này.")
        else:
            # recipe grid
            html = ['<div class="recipe-grid">']
            for rid in top20:
                info = recipe_info.get(rid, {})
                name = info.get('name', f"Recipe {rid}")
                tags = ", ".join(info.get('tags', [])[:2])
                html.append(f'''
                  <div class="recipe-card">
                    <div class="recipe-title">{name}</div>
                    <div class="recipe-meta"><code style="color:var(--muted)">{rid}</code> · Tags: {tags}</div>
                  </div>
                ''')
            html.append('</div>')
            st.markdown("".join(html), unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)  # close outer-card

# Footer
st.markdown("""
<div style="margin-top:12px">
  <div class="outer-card" style="padding:12px;text-align:center;">
    <div style="font-weight:700">NHÓM 8 — Recipe Recommender System</div>
    <div style="color:var(--muted);margin-top:6px">Đề xuất cá nhân hóa từ 872K đánh giá · Hybrid SVD + CBF · Project 2025</div>
  </div>
</div>
""", unsafe_allow_html=True)
