# --- Replace the previous st.markdown(f"""...""") CSS block with this safe version ---

# prepare dynamic background line safely (no f-string for the whole CSS)
if bg_img:
    background_line = 'background-image: url("data:image/jpg;base64,' + bg_img + '");'
else:
    background_line = ''

css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

:root{
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
}

body, .stApp {
  font-family: var(--font-family);
}

/* Background image + overlay for legibility */
.stApp {
    """ + background_line + """
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
    position: relative;
}
.app-overlay {
    position: fixed;
    inset: 0;
    background: rgba(255,255,255,0.74); /* slightly more opaque to ensure contrast */
    z-index: 0;
    pointer-events: none;
}

/* main header card */
.main-header {
    background: linear-gradient(90deg, var(--accent-1), var(--accent-2));
    padding: 1rem 1.25rem;
    border-radius: 12px;
    color: white;
    box-shadow: var(--shadow);
    margin-bottom: 1rem;
    position: relative;
    z-index: 2;
}
.main-header h1 {
    margin: 0;
    font-size: 1.9rem;
    font-weight: 700;
    letter-spacing: -0.3px;
}
.main-header p {
    margin: 4px 0 0 0;
    opacity: 0.95;
    font-size: 0.95rem;
}

/* Tab container: ensure tabs look like cards and content is inside */
.stTabs [role="tablist"] {
    z-index: 3;
}
.tab-card-wrapper {
    margin-top: 0.75rem;
    background: linear-gradient(180deg, rgba(255,255,255,0.98), rgba(247,247,247,0.98));
    border-radius: 12px;
    padding: 0.9rem;
    box-shadow: var(--shadow);
    border: 1px solid var(--card-border);
    position: relative;
    z-index: 2;
}

/* Section card (used for headings + text blocks) */
.card {
    background: var(--card-bg);
    border-radius: 12px;
    padding: 0.9rem;
    box-shadow: var(--shadow);
    border: 1px solid var(--card-border);
    margin-bottom: 0.9rem;
}

/* Stats grid - uniform cards */
.stat-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
  gap: 0.9rem;
}
.stat {
  background: linear-gradient(180deg, #fff, #fbfbfb);
  padding: 0.8rem;
  border-radius: 10px;
  border: 1px solid rgba(0,0,0,0.04);
  text-align: center;
}
.stat .label{ font-size:0.88rem; color:var(--muted); margin-bottom:6px; }
.stat .value{ font-size:1.45rem; font-weight:700; color:var(--accent-contrast); }

/* EDA image grid: images not in card, but layout controlled and captions inside card below */
.eda-grid {
  display: grid;
  gap: 0.75rem;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  align-items: start;
}
.eda-img-wrap {
  width: 100%;
  height: 220px; /* unified height */
  overflow: hidden;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(180deg, #fff, #f7f7f7);
  border: 1px solid rgba(0,0,0,0.03);
}
.eda-img-wrap img {
  width: 100%;
  height: 100%;
  object-fit: cover; /* ensures uniform crop */
  display: block;
}

/* caption card under images */
.caption-row {
  display: grid;
  gap: 0.5rem;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  margin-top: 0.5rem;
}
.caption {
  background: rgba(255,255,255,0.98);
  padding: 0.6rem;
  border-radius: 8px;
  border: 1px solid rgba(0,0,0,0.03);
  color: var(--muted);
  font-size: 0.92rem;
}

/* Recipe card + shimmer */
.recipe-grid {
  display: grid;
  gap: 0.9rem;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
}
.recipe-card {
  padding: 0.8rem;
  border-radius: 10px;
  border: 1px solid rgba(0,0,0,0.04);
  background: linear-gradient(180deg,#fff,#fbfbfb);
  transition: transform .22s ease, box-shadow .22s ease;
}
.recipe-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 22px 40px rgba(12,12,12,0.12);
}
.recipe-title{font-weight:700;color:var(--accent-contrast);margin-bottom:6px;}
.recipe-sub{color:var(--muted);font-size:0.88rem;}

/* footer */
.footer {
  margin-top: 1rem;
  padding: 1rem;
  text-align: center;
  color: var(--muted);
  font-size: 0.95rem;
  border-radius: 10px;
  border: 1px solid rgba(0,0,0,0.03);
  background: rgba(255,255,255,0.96);
}

/* Accessibility fallback for high contrast */
@media (prefers-contrast: more) {
  :root { --card-bg: #fff; --accent-contrast: #000; }
}

/* small screens tweak */
@media (max-width:640px) {
  .eda-img-wrap { height: 160px; }
}
</style>
"""

st.markdown(css, unsafe_allow_html=True)
