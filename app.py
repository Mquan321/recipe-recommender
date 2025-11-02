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

# --- CSS: Professional, accessible, cards as layers, tab styling + image optimization ---
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
  --glass-blur: 8px;
  --card-radius: 16px;
  --shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
  --shadow-hover: 0 12px 32px rgba(0, 0, 0, 0.18);
  --transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}}

* {{
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}}

/* Background with improved contrast */
.stApp {{
    {f'background-image: url("data:image/jpg;base64,{bg_img}");' if bg_img else ''}
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}}

.app-overlay {{
    position: fixed;
    inset: 0;
    background: linear-gradient(135deg, rgba(255,255,255,0.75) 0%, rgba(245,247,250,0.8) 100%);
    z-index: 0;
    pointer-events: none;
}}

/* Main container */
.reportview-container .main {{
    padding: 2rem 1.5rem;
    position: relative;
    z-index: 1;
}}

/* Header card - Professional gradient */
.main-header {{
    background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
    padding: 2rem 1.5rem;
    border-radius: var(--card-radius);
    text-align: center;
    box-shadow: var(--shadow);
    color: white;
    z-index: 2;
    position: relative;
    margin-bottom: 1.75rem;
    border: 1px solid rgba(255,255,255,0.2);
}}
.main-header h1 {{
    margin: 0;
    font-size: 2.5rem;
    font-weight: 800;
    letter-spacing: -1.2px;
    text-shadow: 0 2px 12px rgba(0,0,0,0.15);
}}
.main-header .subtitle {{
    font-size: 1.05rem;
    margin-top: 0.5rem;
    color: rgba(255,255,255,0.95);
    font-weight: 500;
    letter-spacing: 0.3px;
}}

/* TABS STYLING - Professional card-based tabs */
.stTabs {{
    background: var(--card-bg);
    border-radius: var(--card-radius);
    padding: 0.5rem;
    box-shadow: var(--shadow);
    border: 1px solid var(--card-border);
    position: relative;
    z-index: 2;
    margin-bottom: 1.5rem;
}}

.stTabs [data-baseweb="tab-list"] {{
    gap: 0.5rem;
    background: transparent;
    padding: 0.5rem;
}}

.stTabs [data-baseweb="tab"] {{
    height: auto;
    background: linear-gradient(135deg, rgba(255,255,255,0.6), rgba(248,250,252,0.6));
    border-radius: 12px;
    padding: 0.85rem 2rem;
    font-size: 1rem;
    font-weight: 600;
    color: var(--muted);
    border: 2px solid transparent;
    transition: var(--transition);
    letter-spacing: 0.3px;
}}

.stTabs [data-baseweb="tab"]:hover {{
    background: linear-gradient(135deg, rgba(255,255,255,0.9), rgba(248,250,252,0.9));
    color: var(--accent-contrast);
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}}

.stTabs [data-baseweb="tab"][aria-selected="true"] {{
    background: linear-gradient(135deg, var(--accent-1), var(--accent-2));
    color: white;
    border-color: rgba(255,255,255,0.3);
    box-shadow: 0 6px 20px rgba(255,107,107,0.35);
}}

.stTabs [data-baseweb="tab-panel"] {{
    padding: 1.5rem 0.5rem 0.5rem 0.5rem;
}}

/* Section headers with card background */
.section-header {{
    background: linear-gradient(135deg, rgba(102,126,234,0.08), rgba(118,75,162,0.08));
    padding: 1.25rem 1.5rem;
    border-radius: 12px;
    margin: 1.75rem 0 1.25rem 0;
    border-left: 4px solid var(--accent-1);
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}}

.section-header h2 {{
    margin: 0;
    font-size: 1.75rem;
    font-weight: 700;
    color: var(--accent-contrast);
    letter-spacing: -0.5px;
}}

.section-header h3 {{
    margin: 0;
    font-size: 1.4rem;
    font-weight: 700;
    color: var(--accent-contrast);
    letter-spacing: -0.3px;
}}

/* Generic card */
.card {{
    background: var(--card-bg);
    border-radius: var(--card-radius);
    padding: 1.5rem;
    box-shadow: var(--shadow);
    border: 1px solid var(--card-border);
    position: relative;
    z-index: 2;
    margin-bottom: 1.25rem;
    transition: var(--transition);
}}

.card:hover {{
    box-shadow: var(--shadow-hover);
    transform: translateY(-2px);
}}

/* Stats grid - Enhanced design */
.stat-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1.25rem;
    margin: 1.5rem 0;
}}

.stat {{
    background: linear-gradient(135deg, rgba(255,255,255,0.98), rgba(250,252,255,0.98));
    border-radius: 14px;
    padding: 1.5rem 1.25rem;
    text-align: center;
    border: 2px solid rgba(102,126,234,0.12);
    transition: var(--transition);
    position: relative;
    overflow: hidden;
}}

.stat::before {{
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: linear-gradient(90deg, var(--accent-1), var(--accent-2));
    opacity: 0;
    transition: opacity 0.3s ease;
}}

.stat:hover {{
    transform: translateY(-4px);
    box-shadow: 0 12px 28px rgba(102,126,234,0.2);
    border-color: var(--accent-1);
}}

.stat:hover::before {{
    opacity: 1;
}}

.stat .label {{
    font-size: 0.95rem;
    color: var(--muted);
    margin-bottom: 0.65rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.8px;
}}

.stat .value {{
    font-size: 2rem;
    font-weight: 800;
    background: linear-gradient(135deg, var(--accent-1), var(--accent-2));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: -1px;
}}

/* EDA Image cards - Optimized layout */
.eda-container {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(450px, 1fr));
    gap: 1.5rem;
    margin: 1.5rem 0;
}}

.eda-card {{
    background: var(--card-bg);
    border-radius: var(--card-radius);
    padding: 1.25rem;
    box-shadow: var(--shadow);
    border: 1px solid var(--card-border);
    transition: var(--transition);
    overflow: hidden;
}}

.eda-card:hover {{
    transform: translateY(-4px);
    box-shadow: var(--shadow-hover);
    border-color: rgba(102,126,234,0.3);
}}

.eda-card img {{
    width: 100%;
    height: auto;
    border-radius: 10px;
    display: block;
    margin-bottom: 1rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}}

.eda-caption {{
    background: linear-gradient(135deg, rgba(102,126,234,0.05), rgba(118,75,162,0.05));
    padding: 0.85rem 1.1rem;
    border-radius: 8px;
    font-size: 0.92rem;
    color: var(--muted);
    font-weight: 500;
    line-height: 1.6;
    border-left: 3px solid var(--accent-1);
}}

.eda-caption strong {{
    color: var(--accent-contrast);
    font-weight: 700;
}}

/* Recipe card + shimmer effect */
.recipe-card {{
    background: linear-gradient(135deg, rgba(255,255,255,0.98), rgba(250,252,255,0.98));
    padding: 1.25rem;
    border-radius: 14px;
    border: 2px solid rgba(102,126,234,0.12);
    transition: var(--transition);
    min-height: 160px;
    overflow: hidden;
    position: relative;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}}

.recipe-card:hover {{
    transform: translateY(-6px);
    box-shadow: 0 20px 40px rgba(102,126,234,0.2);
    border-color: var(--accent-1);
}}

.recipe-card::after {{
    content: "";
    position: absolute;
    inset: 0;
    background: linear-gradient(120deg, transparent 0%, rgba(255,255,255,0.2) 40%, rgba(255,255,255,0.3) 50%, rgba(255,255,255,0.2) 60%, transparent 100%);
    transform: translateX(-120%);
    transition: transform 0.8s ease;
    pointer-events: none;
    border-radius: 14px;
    opacity: 0;
}}

.recipe-card:hover::after {{
    transform: translateX(120%);
    opacity: 1;
}}

.recipe-title {{
    font-weight: 700;
    color: var(--accent-contrast);
    margin-bottom: 0.5rem;
    font-size: 1.05rem;
    line-height: 1.4;
    letter-spacing: -0.2px;
}}

.recipe-sub {{
    color: var(--muted-light);
    font-size: 0.88rem;
    line-height: 1.5;
    font-weight: 500;
}}

.recipe-sub code {{
    background: rgba(102,126,234,0.1);
    padding: 0.2rem 0.5rem;
    border-radius: 4px;
    color: var(--muted);
    font-size: 0.82rem;
    font-weight: 600;
}}

/* Divider */
.divider {{
    border: none;
    height: 2px;
    background: linear-gradient(90deg, transparent, rgba(102,126,234,0.2), transparent);
    margin: 1.5rem 0;
}}

/* Footer */
.footer {{
    text-align: center;
    margin-top: 2.5rem;
    padding: 1.5rem;
    color: var(--muted);
    font-size: 0.95rem;
    border-radius: var(--card-radius);
    background: var(--card-bg);
    border: 1px solid var(--card-border);
    box-shadow: var(--shadow);
    z-index: 2;
}}

.footer strong {{
    color: var(--accent-contrast);
    font-weight: 700;
}}

/* Responsive adjustments */
@media (max-width: 768px) {{
    .eda-container {{
        grid-template-columns: 1fr;
    }}
    
    .stat-grid {{
        grid-template-columns: repeat(2, 1fr);
    }}
    
    .main-header h1 {{
        font-size: 1.8rem;
    }}
}}

/* High contrast mode support */
@media (prefers-contrast: more) {{
    :root {{
        --card-bg: #ffffff;
        --card-border: #000000;
        --accent-contrast: #000000;
        --muted: #333333;
    }}
}}

/* Streamlit element overrides */
.stSelectbox, .stButton {{
    z-index: 2;
    position: relative;
}}

div[data-testid="stImage"] {{
    border-radius: 10px;
    overflow: hidden;
}}

</style>
""", unsafe_allow_html=True)

# overlay element
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
    <h1>🍳 NHÓM 8 - Recipe Recommender System</h1>
    <div class="subtitle">Personalized recommendations from 872K ratings</div>
</div>
""", unsafe_allow_html=True)

# === 2 TABS ===
tab1, tab2 = st.tabs(["📊 Data & EDA", "🤖 Model & Recommendation"])

with tab1:
    # Section header
    st.markdown("""
    <div class="section-header">
        <h2>📈 Tổng quan Dữ liệu</h2>
    </div>
    """, unsafe_allow_html=True)

    # stat grid
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

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    # EDA Section
    st.markdown("""
    <div class="section-header">
        <h3>🔍 Phân tích Dữ liệu (EDA)</h3>
    </div>
    """, unsafe_allow_html=True)

    # EDA images with optimized card layout
    eda_images = [
        (ASSETS / "eda_rating_distribution.png", "**Phân bố điểm đánh giá**: Hầu hết người dùng chấm 4-5 sao, cho thấy chất lượng công thức tốt."),
        (ASSETS / "eda_Ratings_per_Recipe.png", "**Số lượt đánh giá mỗi công thức**: Phân bố lệch phải với một số công thức rất phổ biến."),
        (ASSETS / "eda_Average Rating vs Number of Ingredients.png", "**Số nguyên liệu vs Rating**: Mối quan hệ giữa độ phức tạp và đánh giá của người dùng."),
        (ASSETS / "eda_Word Cloud for Ingredients.png", "**Từ khóa nguyên liệu phổ biến**: Các nguyên liệu được sử dụng nhiều nhất trong dataset."),
        (ASSETS / "eda_Word Cloud for Tags.png", "**Từ khóa thẻ (tags)**: Phân loại công thức theo các đặc điểm và danh mục phổ biến."),
    ]

    st.markdown('<div class="eda-container">', unsafe_allow_html=True)
    for img_path, caption in eda_images:
        if img_path.exists():
            img_b64 = get_base64_image(img_path)
            st.markdown(f"""
            <div class="eda-card">
                <img src="data:image/png;base64,{img_b64}" alt="{caption}">
                <div class="eda-caption">{caption}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="eda-card">
                <div class="eda-caption">⚠️ Missing image: {img_path.name}</div>
            </div>
            """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # EDA Video charts with auto-loop
    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown("""
    <div class="section-header">
        <h3>🎬 Phân tích Động (Dynamic Charts)</h3>
    </div>
    """, unsafe_allow_html=True)

    eda_videos = [
        (ASSETS / "eda_top_popular_recipes.mp4", "**Top Popular Recipes Animation**: Trực quan hóa động các công thức phổ biến nhất theo số lượt đánh giá và rating trung bình. Biểu đồ racing bar chart cho thấy sự cạnh tranh và thay đổi thứ hạng của các món ăn được yêu thích nhất."),
        (ASSETS / "eda_Time vs Rating Correlation.mp4", "**Time vs Rating Correlation**: Phân tích mối tương quan giữa thời gian nấu và điểm đánh giá theo thời gian. Animation thể hiện xu hướng thay đổi sở thích của người dùng qua các giai đoạn khác nhau."),
    ]

    # Use same grid as images but center the 2 videos
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="eda-container" style="grid-template-columns: repeat(2, 1fr);">', unsafe_allow_html=True)
        for video_path, caption in eda_videos:
            if video_path.exists():
                video_b64 = get_base64_image(video_path)
                st.markdown(f"""
                <div class="eda-card">
                    <video width="100%" style="border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.06);" autoplay loop muted playsinline>
                        <source src="data:video/mp4;base64,{video_b64}" type="video/mp4">
                        Your browser does not support the video tag.
                    </video>
                    <div class="eda-caption">{caption}</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="eda-card">
                    <div class="eda-caption">⚠️ Missing video: {video_path.name}</div>
                </div>
                """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)


with tab2:
    st.markdown("""
    <div class="section-header">
        <h2>⚙️ Chọn Model & User</h2>
    </div>
    """, unsafe_allow_html=True)

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

    if st.button("🎯 Recommend Top-20 Recipes", type="primary", use_container_width=True):
        top20 = recs[model_key][user_id]

        st.markdown("""
        <div class="section-header">
            <h3>📊 Hiệu suất Model</h3>
        </div>
        """, unsafe_allow_html=True)

        if model_key == 'fast':
            rmse, r2 = "0.9471", "0.0869"
            p20, r20, ndcg20, map20 = "0.0030", "0.0600", "0.0259", "0.0170"
        else:
            rmse, r2 = "0.9467", "0.0878"
            p20, r20, ndcg20, map20 = "0.0020", "0.0400", "0.0141", "0.0067"

        colm1, colm2 = st.columns([1, 2])
        with colm1:
            st.markdown("""
            <div style='background: linear-gradient(135deg, rgba(102,126,234,0.08), rgba(118,75,162,0.08)); 
                        padding: 1.25rem; border-radius: 12px; border-left: 4px solid var(--accent-1);'>
                <h4 style='margin: 0 0 1rem 0; color: var(--accent-contrast); font-size: 1.1rem; font-weight: 700;'>Regression Metrics</h4>
                <div style='display: grid; gap: 0.75rem;'>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
                <div class='stat' style='margin: 0;'>
                    <div class='label'>RMSE</div>
                    <div class='value'>{rmse}</div>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
                <div class='stat' style='margin: 0;'>
                    <div class='label'>R²</div>
                    <div class='value'>{r2}</div>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown("</div></div>", unsafe_allow_html=True)
        
        with colm2:
            st.markdown("""
            <div style='background: linear-gradient(135deg, rgba(255,107,107,0.08), rgba(255,142,83,0.08)); 
                        padding: 1.25rem; border-radius: 12px; border-left: 4px solid var(--accent-2);'>
                <h4 style='margin: 0 0 1rem 0; color: var(--accent-contrast); font-size: 1.1rem; font-weight: 700;'>Ranking Metrics @ K=20</h4>
                <div style='display: grid; grid-template-columns: repeat(4, 1fr); gap: 0.75rem;'>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
                <div class='stat' style='margin: 0;'>
                    <div class='label'>P@20</div>
                    <div class='value'>{p20}</div>
                </div>
                <div class='stat' style='margin: 0;'>
                    <div class='label'>R@20</div>
                    <div class='value'>{r20}</div>
                </div>
                <div class='stat' style='margin: 0;'>
                    <div class='label'>nDCG@20</div>
                    <div class='value'>{ndcg20}</div>
                </div>
                <div class='stat' style='margin: 0;'>
                    <div class='label'>mAP@20</div>
                    <div class='value'>{map20}</div>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown("</div></div>", unsafe_allow_html=True)

        st.markdown("""
        <div class="section-header" style="margin-top: 2rem;">
            <h3>🍽️ Top-20 Recipe Đề Xuất</h3>
        </div>
        """, unsafe_allow_html=True)

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

# footer
st.markdown("""
<div class='footer'>
    <p><strong>NHÓM 8</strong> | Recipe Recommender System | Project 2025</p>
    <p><em>Đề xuất cá nhân hóa từ 872K đánh giá – Hybrid SVD + CBF</em></p>
</div>
""", unsafe_allow_html=True)
