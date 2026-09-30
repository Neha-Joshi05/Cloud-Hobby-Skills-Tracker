"""
dashboard.py — Online Hobby & Skills Tracker
Community Sharing on Cloud
Dark + Light Theme | Gamified | Interactive
Run: python -m streamlit run dashboard.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import random
import sys
from datetime import datetime, timedelta

sys.path.insert(0, ".")
from simulation.user_simulator    import UserManager
from simulation.hobby_simulator   import (
    HobbyManager, HOBBY_CATEGORIES
)
from simulation.session_simulator import SessionManager
from simulation.community_simulator import CommunityManager
from src.streak_engine import StreakEngine
from src.badge_engine  import BadgeEngine, BADGES
from src.data_store    import DataStore
from src.auth          import AuthService
from src.analytics     import (
    get_theme, get_pt,
    create_activity_trend,
    create_hobby_radar,
    create_session_heatmap,
    create_progress_bars,
    create_hours_donut,
    create_category_polar,
    create_xp_gauge,
    create_session_mood,
    create_leaderboard_chart,
    create_focus_area_pie,
    PALETTE, CAT_COLORS,
)

# ── Page config ───────────────────────────────
st.set_page_config(
    page_title="SkillCloud — Hobby Tracker",
    page_icon="🌟",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Session state ─────────────────────────────
if "user_mgr" not in st.session_state:
    with st.spinner("☁️ Loading SkillCloud..."):
        st.session_state.user_mgr    = UserManager(30)
        st.session_state.hobby_mgr   = HobbyManager(
            st.session_state.user_mgr
        )
        st.session_state.session_mgr = SessionManager(
            st.session_state.hobby_mgr
        )
        st.session_state.community   = CommunityManager(
            st.session_state.user_mgr,
            st.session_state.hobby_mgr,
        )
        st.session_state.streak_eng  = StreakEngine()
        st.session_state.badge_eng   = BadgeEngine()
        st.session_state.data_store  = DataStore()
        st.session_state.auth        = AuthService()

if "theme"     not in st.session_state:
    st.session_state.theme     = "dark"
if "page"      not in st.session_state:
    st.session_state.page      = "dashboard"
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user"      not in st.session_state:
    st.session_state.user      = None

user_mgr    = st.session_state.user_mgr
hobby_mgr   = st.session_state.hobby_mgr
session_mgr = st.session_state.session_mgr
community   = st.session_state.community
streak_eng  = st.session_state.streak_eng
badge_eng   = st.session_state.badge_eng
data_store  = st.session_state.data_store
auth        = st.session_state.auth
theme       = st.session_state.theme
T           = get_theme(theme)

# ── CSS ───────────────────────────────────────
def inject_css(T, theme):
    bg = (
        "linear-gradient(135deg,#060410,#0a0818)"
        if theme == "dark"
        else "linear-gradient(135deg,#f5f0ff,#ede8ff)"
    )
    st.markdown(f"""
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;900&display=swap');
      *{{ font-family:'Inter',sans-serif !important; }}
      .stApp{{ background:{bg};color:{T['text']}; }}
      section[data-testid="stSidebar"]{{
        background:{T['card']} !important;
        border-right:1px solid {T['border']};
      }}
      [data-testid="stMetric"]{{
        background:{T['card']};
        border:1px solid {T['border']};
        border-radius:16px;padding:18px !important;
        position:relative;overflow:hidden;
      }}
      [data-testid="stMetric"]::before{{
        content:'';position:absolute;
        top:0;left:0;right:0;height:2px;
        background:linear-gradient(90deg,
          {T['accent']},{T['accent2']},{T['gold']}
        );
      }}
      [data-testid="stMetricValue"]{{
        font-size:1.8rem !important;
        font-weight:900 !important;
        color:{T['accent']} !important;
      }}
      [data-testid="stMetricLabel"]{{
        color:{T['muted']} !important;
        font-size:0.7rem !important;
        text-transform:uppercase;letter-spacing:1px;
      }}
      .hero-card{{
        background:{T['card']};
        border:1px solid {T['border']};
        border-radius:20px;padding:24px 28px;
        margin-bottom:18px;
        position:relative;overflow:hidden;
      }}
      .hero-card::before{{
        content:'';position:absolute;
        top:0;left:0;right:0;height:3px;
        background:linear-gradient(90deg,
          {T['accent']},{T['accent2']},
          {T['gold']},{T['accent']}
        );
        background-size:200% 100%;
        animation:shimmer 4s linear infinite;
      }}
      @keyframes shimmer{{
        0%{{background-position:0%}}
        100%{{background-position:200%}}
      }}
      .hobby-card{{
        background:{T['card']};
        border:1px solid {T['border']};
        border-radius:14px;padding:16px;
        margin:6px 0;
        transition:border-color 0.2s;
        position:relative;overflow:hidden;
      }}
      .hobby-card:hover{{border-color:{T['accent']};}}
      .post-card{{
        background:{T['card']};
        border:1px solid {T['border']};
        border-radius:14px;padding:16px;
        margin:8px 0;
        transition:border-color 0.2s;
      }}
      .post-card:hover{{border-color:{T['accent']};}}
      .badge-card{{
        background:{T['card']};
        border:1px solid {T['border']};
        border-radius:12px;padding:14px;
        text-align:center;margin:4px;
      }}
      .stat-row{{
        display:flex;justify-content:space-between;
        align-items:center;padding:7px 0;
        border-bottom:1px solid {T['border']};
        font-size:0.82rem;
      }}
      .stat-row:last-child{{border-bottom:none;}}
      .badge{{
        display:inline-block;padding:3px 10px;
        border-radius:20px;font-size:0.72rem;
        font-weight:700;
      }}
      .badge-purple{{
        background:rgba(167,139,250,0.15);
        color:{T['accent']};border:1px solid {T['accent']};
      }}
      .badge-green{{
        background:rgba(52,211,153,0.15);
        color:{T['green']};border:1px solid {T['green']};
      }}
      .badge-gold{{
        background:rgba(251,191,36,0.15);
        color:{T['gold']};border:1px solid {T['gold']};
      }}
      .badge-blue{{
        background:rgba(96,165,250,0.15);
        color:{T['accent2']};border:1px solid {T['accent2']};
      }}
      .section-title{{
        font-size:0.78rem;font-weight:700;
        color:{T['muted']};text-transform:uppercase;
        letter-spacing:1.2px;margin:12px 0 8px;
        padding-left:10px;
        border-left:3px solid {T['accent']};
      }}
      .live-dot{{
        display:inline-block;width:8px;height:8px;
        background:{T['green']};border-radius:50%;
        animation:pulse 1.5s infinite;
      }}
      @keyframes pulse{{
        0%,100%{{opacity:1}} 50%{{opacity:0.3}}
      }}
      .prog-bg{{
        background:{T['border']};border-radius:4px;
        height:6px;margin:4px 0;
      }}
      .prog-fill{{
        height:6px;border-radius:4px;
        background:linear-gradient(90deg,
          {T['accent']},{T['accent2']}
        );
      }}
      .stButton>button{{
        background:linear-gradient(135deg,
          {T['accent']},{T['accent2']}
        ) !important;
        color:{'#060410' if theme=='dark' else '#fff'} !important;
        border:none !important;border-radius:10px !important;
        font-weight:700 !important;
      }}
      .stTabs [data-baseweb="tab-list"]{{
        background:{T['card']};border-radius:12px;
        padding:4px;gap:4px;
      }}
      .stTabs [data-baseweb="tab"]{{
        color:{T['muted']} !important;
        font-weight:600;border-radius:8px !important;
      }}
      .stTabs [aria-selected="true"]{{
        background:linear-gradient(135deg,
          {T['accent']},{T['accent2']}
        ) !important;
        color:{'#060410' if theme=='dark' else '#fff'} !important;
      }}
    </style>
    """, unsafe_allow_html=True)

inject_css(T, theme)

# ════════════════════════════════════════════
# LOGIN PAGE
# ════════════════════════════════════════════
if not st.session_state.logged_in:
    st.markdown(f"""
    <div style='max-width:420px;margin:50px auto;
      background:{T['card']};border:1px solid {T['border']};
      border-radius:24px;padding:40px;
      position:relative;overflow:hidden'>
      <div style='position:absolute;top:0;left:0;
        right:0;height:3px;background:linear-gradient(
        90deg,{T['accent']},{T['accent2']},{T['gold']})'></div>
      <div style='text-align:center;margin-bottom:24px'>
        <div style='font-size:3rem'>🌟</div>
        <h1 style='font-size:1.6rem;font-weight:900;
          color:{T['accent']};margin:8px 0 4px'>
          SkillCloud
        </h1>
        <p style='color:{T['muted']};font-size:0.85rem'>
          Track Hobbies · Earn Badges · Share Progress
        </p>
      </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style='background:{T['bg']};
      border:1px solid {T['border']};
      border-radius:12px;padding:12px 16px;
      margin-bottom:20px;font-size:0.8rem'>
      <div style='color:{T['accent']};
        font-weight:700;margin-bottom:6px'>
        🔑 Demo Credentials
      </div>
      <div style='color:{T['muted']}'>
        neha@demo.com / demo123<br>
        rahul@demo.com / demo123<br>
        priya@demo.com / demo123
      </div>
    </div>
    """, unsafe_allow_html=True)

    email = st.text_input(
        "📧 Email",
        placeholder="your@email.com",
    )
    pwd   = st.text_input(
        "🔒 Password",
        type="password",
        placeholder="••••••••",
    )

    if st.button("Login →",
                 use_container_width=True):
        session, msg = auth.login(email, pwd)
        if session:
            st.session_state.user      = session
            st.session_state.logged_in = True
            st.success(f"Welcome, {session['name']}! 🌟")
            st.rerun()
        else:
            st.error(f"❌ {msg}")

    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

user = st.session_state.user

# ── Get user data ─────────────────────────────
all_sessions  = session_mgr.get_all()
user_sessions = [
    s for s in all_sessions
    if s.get("user_id","") == user.get("email","")
    or True  # show demo data
][:50]

all_hobbies   = hobby_mgr.get_all()
user_hobbies  = [
    h for h in all_hobbies
][:6]

all_posts     = community.get_feed(limit=30)
activity_df   = data_store.get_activity_df()
leaderboard   = user_mgr.get_leaderboard()
comm_stats    = community.get_stats()
platform_stats= data_store.get_platform_stats()

# Badges
earned_badges = badge_eng.evaluate(
    user, all_sessions, user_hobbies, all_posts
)
next_badges   = badge_eng.get_next_badges(
    user, all_sessions, user_hobbies
)

# ════════════════════════════════════════════
# SIDEBAR
# ════════════════════════════════════════════
with st.sidebar:
    st.markdown(f"""
    <div style='text-align:center;padding:16px 0 8px'>
      <div style='font-size:2.5rem'>🌟</div>
      <div style='font-size:1.1rem;font-weight:900;
        color:{T['accent']};margin-top:6px'>SkillCloud</div>
      <div style='color:{T['muted']};font-size:0.72rem'>
        Hobby & Skills Tracker
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style='text-align:center;margin-bottom:10px'>
      <span class='live-dot'></span>
      <span style='color:{T['green']};font-size:0.72rem;
        font-weight:700;margin-left:6px'>CLOUD SYNCED</span>
    </div>
    """, unsafe_allow_html=True)

    # User card
    st.markdown(f"""
    <div style='background:{T['bg']};
      border:1px solid {T['border']};
      border-radius:12px;padding:14px;
      margin-bottom:10px'>
      <div style='font-size:2rem;text-align:center'>
        {user['avatar']}
      </div>
      <div style='text-align:center;margin-top:6px'>
        <div style='color:{T['text']};font-weight:700'>
          {user['name']}
        </div>
        <div style='color:{T['muted']};font-size:0.75rem'>
          @{user['username']} • {user['city']}
        </div>
        <div style='color:{T['accent']};font-size:0.8rem;
          font-weight:700;margin-top:4px'>
          {user['level']}
        </div>
      </div>
      <div style='display:flex;
        justify-content:space-around;margin-top:10px'>
        <div style='text-align:center'>
          <div style='color:{T['accent']};font-weight:700'>
            {user['followers']}
          </div>
          <div style='color:{T['muted']};font-size:0.7rem'>
            Followers
          </div>
        </div>
        <div style='text-align:center'>
          <div style='color:{T['accent']};font-weight:700'>
            {user['following']}
          </div>
          <div style='color:{T['muted']};font-size:0.7rem'>
            Following
          </div>
        </div>
        <div style='text-align:center'>
          <div style='color:{T['gold']};font-weight:700'>
            {user['xp']}
          </div>
          <div style='color:{T['muted']};font-size:0.7rem'>
            XP
          </div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Theme toggle
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🌙 Dark",
                     use_container_width=True):
            st.session_state.theme = "dark"
            st.rerun()
    with c2:
        if st.button("☀️ Light",
                     use_container_width=True):
            st.session_state.theme = "light"
            st.rerun()

    st.markdown("---")

    # Navigation
    st.markdown(
        f'<div class="section-title">Navigation</div>',
        unsafe_allow_html=True,
    )
    pages = [
        ("🏠","Dashboard",   "dashboard"),
        ("🎯","My Hobbies",  "hobbies"),
        ("📝","Log Session", "log"),
        ("🏆","Achievements","badges"),
        ("🌐","Community",   "community"),
        ("📊","Analytics",   "analytics"),
        ("🏅","Leaderboard", "leaderboard"),
        ("⚙️","Profile",    "profile"),
    ]
    for icon, label, key in pages:
        is_active = st.session_state.page == key
        if st.sidebar.button(
            f"{icon} {label}",
            key=f"nav_{key}",
            use_container_width=True,
            type="primary"
            if is_active else "secondary",
        ):
            st.session_state.page = key
            st.rerun()

    st.markdown("---")

    # Streak display
    st.markdown(f"""
    <div style='background:{T['bg']};
      border:1px solid {T['border']};
      border-radius:12px;padding:12px;
      text-align:center;margin-bottom:8px'>
      <div style='font-size:1.8rem'>🔥</div>
      <div style='color:{T['gold']};font-weight:900;
        font-size:1.4rem'>
        {user['current_streak']} Days
      </div>
      <div style='color:{T['muted']};font-size:0.75rem'>
        Current Streak
      </div>
      <div style='color:{T['muted']};font-size:0.72rem;
        margin-top:4px'>
        Best: {user['longest_streak']} days
      </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🚪 Logout",
                 use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.user      = None
        st.rerun()

page = st.session_state.page

# ════════════════════════════════════════════
# PAGE: DASHBOARD
# ════════════════════════════════════════════
if page == "dashboard":
    now_str = datetime.now().strftime(
        "%d %b %Y | %H:%M:%S"
    )
    st.markdown(f"""
    <div class='hero-card'>
      <div style='display:flex;align-items:center;
        justify-content:space-between;
        flex-wrap:wrap;gap:12px'>
        <div>
          <h1 style='margin:0;font-size:1.8rem;
            font-weight:900;color:{T['text']}'>
            🌟 SkillCloud Dashboard
          </h1>
          <p style='color:{T['muted']};margin:6px 0 0;
            font-size:0.88rem'>
            Track Hobbies • Earn Badges •
            Share Progress • Cloud Synced
          </p>
        </div>
        <div style='text-align:right'>
          <span class='live-dot'></span>
          <span style='color:{T['green']};
            font-size:0.78rem;font-weight:700;
            margin-left:6px'>LIVE</span>
          <div style='color:{T['muted']};
            font-size:0.72rem;margin-top:4px'>
            {now_str}
          </div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # KPIs
    c1,c2,c3,c4,c5,c6 = st.columns(6)
    c1.metric("🔥 Streak",
              f"{user['current_streak']}d")
    c2.metric("⏱️ Total Hours",
              f"{user['total_hours']:.0f}h")
    c3.metric("📝 Sessions",
              user["total_sessions"])
    c4.metric("🌟 XP",
              f"{user['xp']:,}")
    c5.metric("🏆 Badges",
              len(earned_badges))
    c6.metric("🎯 Hobbies",
              len(user["hobbies"]))

    st.markdown("---")

    # Row 1
    col1, col2 = st.columns([2,1])
    with col1:
        fig = create_activity_trend(
            activity_df, theme
        )
        st.plotly_chart(
            fig, use_container_width=True
        )
    with col2:
        fig = create_xp_gauge(
            user["xp"],
            user["level"],
            theme,
        )
        st.plotly_chart(
            fig, use_container_width=True
        )

        # Next badges
        st.markdown(
            f'<div class="section-title">'
            f'🎯 Next Badges</div>',
            unsafe_allow_html=True,
        )
        for nb in next_badges[:3]:
            pct = nb["progress"]
            st.markdown(f"""
            <div style='background:{T['bg']};
              border:1px solid {T['border']};
              border-radius:10px;
              padding:10px 12px;margin:4px 0'>
              <div style='display:flex;
                justify-content:space-between;
                margin-bottom:4px'>
                <span style='color:{T['text']};
                  font-size:0.82rem;font-weight:600'>
                  {nb['emoji']} {nb['name']}
                </span>
                <span style='color:{nb['color']};
                  font-size:0.75rem;font-weight:700'>
                  {pct:.0f}%
                </span>
              </div>
              <div class='prog-bg'>
                <div class='prog-fill'
                  style='width:{pct:.0f}%;
                  background:{nb['color']}'></div>
              </div>
              <div style='color:{T['muted']};
                font-size:0.72rem;margin-top:3px'>
                {nb['left']} more {nb['metric']}
              </div>
            </div>
            """, unsafe_allow_html=True)

    # Row 2
    col1, col2 = st.columns(2)
    with col1:
        fig = create_session_heatmap(
            all_sessions,
            user.get("email",""),
            theme,
        )
        st.plotly_chart(
            fig, use_container_width=True
        )
    with col2:
        fig = create_hobby_radar(
            user_hobbies, theme
        )
        st.plotly_chart(
            fig, use_container_width=True
        )

    # Community preview
    st.markdown("---")
    st.markdown(
        f'<div class="section-title">'
        f'🌐 Community Feed Preview</div>',
        unsafe_allow_html=True,
    )
    for post in all_posts[:4]:
        st.markdown(f"""
        <div class='post-card'>
          <div style='display:flex;
            justify-content:space-between;
            margin-bottom:8px'>
            <div style='display:flex;
              align-items:center;gap:8px'>
              <span style='font-size:1.2rem'>
                {post['user_avatar']}
              </span>
              <div>
                <span style='color:{T['text']};
                  font-weight:700;font-size:0.85rem'>
                  {post['user_name']}
                </span>
                <span class='badge badge-purple'
                  style='margin-left:6px'>
                  {post['hobby']}
                </span>
              </div>
            </div>
            <span style='font-size:1.5rem'>
              {post['image_emoji']}
            </span>
          </div>
          <div style='color:{T['text']};
            font-size:0.85rem;
            line-height:1.5;margin-bottom:8px'>
            {post['content']}
          </div>
          <div style='display:flex;gap:16px;
            font-size:0.78rem;color:{T['muted']}'>
            <span>❤️ {post['likes']}</span>
            <span>💬 {post['comment_count']}</span>
            <span>👁️ {post['views']}</span>
          </div>
        </div>
        """, unsafe_allow_html=True)

# ════════════════════════════════════════════
# PAGE: MY HOBBIES
# ════════════════════════════════════════════
elif page == "hobbies":
    st.markdown(
        f"<h2 style='color:{T['text']}'>"
        f"🎯 My Hobbies & Skills</h2>",
        unsafe_allow_html=True,
    )

    # Add new hobby
    with st.expander("➕ Add New Hobby"):
        col1, col2, col3 = st.columns(3)
        with col1:
            new_cat = st.selectbox(
                "Category",
                list(HOBBY_CATEGORIES.keys()),
            )
        with col2:
            new_name = st.selectbox(
                "Hobby",
                HOBBY_CATEGORIES[new_cat],
            )
        with col3:
            st.markdown("<br>",
                        unsafe_allow_html=True)
            if st.button(
                "➕ Add Hobby",
                use_container_width=True,
            ):
                h = hobby_mgr.add_hobby(
                    user["email"],
                    new_name, new_cat,
                )
                user_hobbies.append(h.to_dict())
                st.success(
                    f"✅ {new_name} added!"
                )
                st.rerun()

    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        fig = create_progress_bars(
            user_hobbies, theme
        )
        st.plotly_chart(
            fig, use_container_width=True
        )
    with col2:
        fig = create_hours_donut(
            user_hobbies, theme
        )
        st.plotly_chart(
            fig, use_container_width=True
        )

    # Hobby cards
    st.markdown(
        f'<div class="section-title">'
        f'All Hobbies</div>',
        unsafe_allow_html=True,
    )
    cols = st.columns(3)
    for i, h in enumerate(user_hobbies):
        color = CAT_COLORS.get(
            h["category"], T["accent"]
        )
        with cols[i % 3]:
            pct = h["goal_progress"]
            st.markdown(f"""
            <div class='hobby-card'
              style='border-left:4px solid {color}'>
              <div style='display:flex;
                justify-content:space-between;
                margin-bottom:10px'>
                <div>
                  <span style='font-size:1.3rem'>
                    {h['emoji']}
                  </span>
                  <span style='color:{T['text']};
                    font-weight:700;
                    font-size:0.9rem;
                    margin-left:6px'>
                    {h['name']}
                  </span>
                </div>
                <span class='badge badge-purple'>
                  {h['category']}
                </span>
              </div>
              <div class='stat-row'>
                <span style='color:{T['muted']}'>
                  Skill Level
                </span>
                <span style='color:{color};
                  font-weight:600;font-size:0.8rem'>
                  {h['skill_level']}
                </span>
              </div>
              <div class='stat-row'>
                <span style='color:{T['muted']}'>
                  Target
                </span>
                <span style='color:{T['text']};
                  font-size:0.8rem'>
                  {h['target_level']}
                </span>
              </div>
              <div class='stat-row'>
                <span style='color:{T['muted']}'>
                  Hours
                </span>
                <span style='color:{T['accent2']};
                  font-weight:700'>
                  {h['total_hours']:.0f}h
                </span>
              </div>
              <div class='stat-row'>
                <span style='color:{T['muted']}'>
                  Sessions
                </span>
                <span style='color:{T['text']}'>
                  {h['sessions']}
                </span>
              </div>
              <div class='stat-row'>
                <span style='color:{T['muted']}'>
                  🔥 Streak
                </span>
                <span style='color:{T['gold']};
                  font-weight:700'>
                  {h['streak']} days
                </span>
              </div>
              <div style='margin-top:10px'>
                <div style='display:flex;
                  justify-content:space-between;
                  font-size:0.75rem;
                  color:{T['muted']};
                  margin-bottom:3px'>
                  <span>Goal: {h['goal'][:25]}</span>
                  <span style='color:{color}'>
                    {pct}%
                  </span>
                </div>
                <div class='prog-bg'>
                  <div class='prog-fill'
                    style='width:{pct}%;
                    background:{color}'>
                  </div>
                </div>
              </div>
            </div>
            """, unsafe_allow_html=True)

# ════════════════════════════════════════════
# PAGE: LOG SESSION
# ════════════════════════════════════════════
elif page == "log":
    st.markdown(
        f"<h2 style='color:{T['text']}'>"
        f"📝 Log Practice Session</h2>",
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)
    with col1:
        hobby_names = [
            h["name"] for h in user_hobbies
        ]
        sel_hobby = st.selectbox(
            "🎯 Select Hobby",
            hobby_names,
        )
        duration  = st.slider(
            "⏱️ Duration (minutes)",
            15, 180, 45, 15,
        )
        mood      = st.selectbox(
            "😊 How was your session?",
            ["😊 Great","🔥 On Fire",
             "😐 Okay","😓 Tough","😴 Tired"],
        )
        focus     = st.selectbox(
            "🎯 Focus Area",
            ["Basics","Technique","Speed",
             "Accuracy","Theory","Practice",
             "New Skill","Revision",
             "Performance"],
        )
        notes     = st.text_area(
            "📝 Notes",
            placeholder="What did you practice today?",
        )

        xp = duration * 2
        st.markdown(f"""
        <div style='background:{T['bg']};
          border:1px solid {T['border']};
          border-radius:12px;
          padding:14px;margin-top:8px'>
          <div style='display:flex;
            justify-content:space-between;
            margin-bottom:6px'>
            <span style='color:{T['muted']}'>
              XP to earn
            </span>
            <span style='color:{T['gold']};
              font-weight:900;font-size:1.1rem'>
              +{xp} XP
            </span>
          </div>
          <div style='display:flex;
            justify-content:space-between'>
            <span style='color:{T['muted']}'>
              Duration
            </span>
            <span style='color:{T['text']};
              font-weight:700'>
              {duration} min
              ({duration/60:.1f}h)
            </span>
          </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button(
            "💾 Log Session",
            use_container_width=True,
        ):
            sel_h = next(
                (h for h in user_hobbies
                 if h["name"] == sel_hobby),
                None,
            )
            if sel_h:
                s = session_mgr.log_session(
                    user["email"],
                    sel_h["hobby_id"],
                    sel_hobby,
                    duration, mood,
                    focus, notes or
                    "Great practice session!",
                )
                st.success(
                    f"✅ Session logged! "
                    f"+{s.xp_earned} XP earned!"
                )
                st.balloons()

    with col2:
        fig = create_session_mood(
            all_sessions,
            user.get("email",""),
            theme,
        )
        st.plotly_chart(
            fig, use_container_width=True
        )
        fig = create_focus_area_pie(
            all_sessions,
            user.get("email",""),
            theme,
        )
        st.plotly_chart(
            fig, use_container_width=True
        )

        # Recent sessions
        st.markdown(
            f'<div class="section-title">'
            f'Recent Sessions</div>',
            unsafe_allow_html=True,
        )
        for s in all_sessions[:5]:
            st.markdown(f"""
            <div style='background:{T['bg']};
              border:1px solid {T['border']};
              border-radius:10px;
              padding:10px 14px;margin:4px 0;
              font-size:0.82rem'>
              <div style='display:flex;
                justify-content:space-between'>
                <span style='color:{T['text']};
                  font-weight:600'>
                  🎯 {s.get('hobby_name','')}
                </span>
                <span style='color:{T['gold']};
                  font-weight:700'>
                  +{s.get('xp_earned',0)} XP
                </span>
              </div>
              <div style='color:{T['muted']};
                font-size:0.75rem;margin-top:3px'>
                {s.get('mood','')} •
                {s.get('duration_min',0)}min •
                {s.get('date','')}
              </div>
            </div>
            """, unsafe_allow_html=True)

# ════════════════════════════════════════════
# PAGE: BADGES / ACHIEVEMENTS
# ════════════════════════════════════════════
elif page == "badges":
    st.markdown(
        f"<h2 style='color:{T['text']}'>"
        f"🏆 Achievements & Badges</h2>",
        unsafe_allow_html=True,
    )

    c1,c2,c3,c4 = st.columns(4)
    c1.metric("🏆 Earned",   len(earned_badges))
    c2.metric("🎯 Available",len(BADGES))
    c3.metric("🌟 Total XP", f"{user['xp']:,}")
    c4.metric("🔥 Streak",
              f"{user['current_streak']}d")

    st.markdown("---")

    # Earned badges
    st.markdown(
        f'<div class="section-title">'
        f'✅ Earned Badges</div>',
        unsafe_allow_html=True,
    )
    if earned_badges:
        cols = st.columns(4)
        for i, b in enumerate(earned_badges):
            with cols[i % 4]:
                st.markdown(f"""
                <div class='badge-card'
                  style='border:1px solid {b['color']};
                  background:rgba(0,0,0,0.1)'>
                  <div style='font-size:2rem'>
                    {b['emoji']}
                  </div>
                  <div style='color:{b['color']};
                    font-weight:700;font-size:0.85rem;
                    margin:6px 0'>
                    {b['name']}
                  </div>
                  <div style='color:{T['muted']};
                    font-size:0.72rem'>
                    {b['desc']}
                  </div>
                  <div style='color:{T['gold']};
                    font-weight:700;margin-top:6px'>
                    +{b['xp']} XP
                  </div>
                </div>
                """, unsafe_allow_html=True)

    # Next badges progress
    st.markdown("---")
    st.markdown(
        f'<div class="section-title">'
        f'🎯 In Progress</div>',
        unsafe_allow_html=True,
    )
    for nb in next_badges:
        pct = nb["progress"]
        st.markdown(f"""
        <div style='background:{T['card']};
          border:1px solid {T['border']};
          border-radius:12px;
          padding:14px 18px;margin:6px 0'>
          <div style='display:flex;
            justify-content:space-between;
            align-items:center;margin-bottom:8px'>
            <div>
              <span style='font-size:1.3rem'>
                {nb['emoji']}
              </span>
              <span style='color:{T['text']};
                font-weight:700;margin-left:8px'>
                {nb['name']}
              </span>
            </div>
            <span style='color:{nb['color']};
              font-weight:900;font-size:1rem'>
              {pct:.0f}%
            </span>
          </div>
          <div class='prog-bg'>
            <div class='prog-fill'
              style='width:{pct:.0f}%;
              background:{nb['color']}'></div>
          </div>
          <div style='color:{T['muted']};
            font-size:0.78rem;margin-top:6px'>
            {nb['current']} / {nb['target']}
            {nb['metric']} •
            {nb['left']} more to go!
          </div>
        </div>
        """, unsafe_allow_html=True)

    # All badges catalog
    st.markdown("---")
    st.markdown(
        f'<div class="section-title">'
        f'📋 All Badges Catalog</div>',
        unsafe_allow_html=True,
    )
    cats = list(set(
        b["category"]
        for b in badge_eng.get_all_badges()
    ))
    for cat in cats:
        st.markdown(
            f"**{cat} Badges**"
        )
        cat_badges = [
            b for b in badge_eng.get_all_badges()
            if b["category"] == cat
        ]
        cols = st.columns(
            min(4, len(cat_badges))
        )
        for i, b in enumerate(cat_badges):
            is_earned = any(
                e["name"] == b["name"]
                for e in earned_badges
            )
            opacity = "1" if is_earned else "0.4"
            with cols[i % len(cols)]:
                st.markdown(f"""
                <div class='badge-card'
                  style='opacity:{opacity}'>
                  <div style='font-size:1.5rem'>
                    {b['emoji']}
                  </div>
                  <div style='color:{T['text']};
                    font-weight:600;
                    font-size:0.78rem;margin:4px 0'>
                    {b['name']}
                  </div>
                  <div style='color:{T['muted']};
                    font-size:0.68rem'>
                    {b['desc']}
                  </div>
                  {"<div style='color:#34d399;font-size:0.68rem;margin-top:4px'>✅ Earned!</div>" if is_earned else f"<div style='color:{T['muted']};font-size:0.68rem;margin-top:4px'>+{b['xp']} XP</div>"}
                </div>
                """, unsafe_allow_html=True)

# ════════════════════════════════════════════
# PAGE: COMMUNITY
# ════════════════════════════════════════════
elif page == "community":
    st.markdown(
        f"<h2 style='color:{T['text']}'>"
        f"🌐 Community Feed</h2>",
        unsafe_allow_html=True,
    )

    c1,c2,c3,c4 = st.columns(4)
    c1.metric("📝 Total Posts",
              comm_stats["total_posts"])
    c2.metric("❤️ Total Likes",
              comm_stats["total_likes"])
    c3.metric("💬 Comments",
              comm_stats["total_comments"])
    c4.metric("👁️ Views",
              comm_stats["total_views"])

    # Filters
    col1, col2 = st.columns([2,1])
    with col1:
        cat_filter = st.selectbox(
            "Filter by Category",
            ["All"] + list(
                HOBBY_CATEGORIES.keys()
            ),
        )
    with col2:
        sort_opt = st.selectbox(
            "Sort by",
            ["Latest","Most Liked",
             "Most Commented"],
        )

    # Post composer
    st.markdown(
        f'<div class="section-title">'
        f'✍️ Share Your Progress</div>',
        unsafe_allow_html=True,
    )
    col1, col2, col3 = st.columns([2,1,1])
    with col1:
        new_content = st.text_area(
            "What have you been working on?",
            placeholder="Share your progress...",
            height=80,
        )
    with col2:
        post_hobby = st.selectbox(
            "Hobby",
            user["hobbies"],
        )
    with col3:
        st.markdown("<br>",
                    unsafe_allow_html=True)
        if st.button(
            "📤 Share Post",
            use_container_width=True,
        ):
            if new_content:
                post = community.add_post(
                    type("obj", (), {
                        "user_id": user["email"],
                        "name":    user["name"],
                        "avatar":  user["avatar"],
                    })(),
                    post_hobby, new_content,
                )
                st.success("✅ Post shared!")
                st.rerun()
            else:
                st.error("Write something first!")

    st.markdown("---")

    # Feed
    posts = all_posts
    if cat_filter != "All":
        posts = [
            p for p in posts
            if any(
                h in p.get("hobby","")
                for h in HOBBY_CATEGORIES.get(
                    cat_filter, []
                )
            )
        ]

    for post in posts[:15]:
        with st.container():
            st.markdown(f"""
            <div class='post-card'>
              <div style='display:flex;
                justify-content:space-between;
                margin-bottom:10px'>
                <div style='display:flex;
                  align-items:center;gap:10px'>
                  <span style='font-size:1.5rem'>
                    {post['user_avatar']}
                  </span>
                  <div>
                    <span style='color:{T['text']};
                      font-weight:700'>
                      {post['user_name']}
                    </span><br>
                    <span class='badge badge-purple'>
                      {post['hobby']}
                    </span>
                  </div>
                </div>
                <div style='text-align:right'>
                  <span style='font-size:1.8rem'>
                    {post['image_emoji']}
                  </span>
                </div>
              </div>
              <p style='color:{T['text']};
                font-size:0.875rem;
                line-height:1.6;
                margin-bottom:12px'>
                {post['content']}
              </p>
              <div style='display:flex;
                gap:4px;margin-bottom:12px;
                flex-wrap:wrap'>
                {' '.join([f"<span style='background:{T['bg']};color:{T['muted']};padding:2px 8px;border-radius:10px;font-size:0.72rem'>#{t}</span>" for t in post.get('tags',[])])}
              </div>
              <div style='display:flex;
                gap:20px;font-size:0.82rem;
                color:{T['muted']}'>
                <span>❤️ {post['likes']} likes</span>
                <span>💬 {post['comment_count']} comments</span>
                <span>👁️ {post['views']} views</span>
              </div>
            </div>
            """, unsafe_allow_html=True)

            # Like & comment
            col1, col2 = st.columns([1,3])
            with col1:
                if st.button(
                    f"❤️ Like",
                    key=f"like_{post['post_id']}",
                ):
                    community.like_post(
                        post["post_id"]
                    )
                    st.rerun()
            with col2:
                comment = st.text_input(
                    "Add comment...",
                    key=f"cmt_{post['post_id']}",
                    label_visibility="collapsed",
                    placeholder="Write a comment...",
                )
                if comment and st.button(
                    "💬",
                    key=f"send_{post['post_id']}",
                ):
                    community.add_comment(
                        post["post_id"],
                        user["name"], comment,
                    )
                    st.rerun()

            # Comments
            if post.get("comments"):
                with st.expander(
                    f"💬 {post['comment_count']}"
                    f" comments"
                ):
                    for c in post["comments"][:3]:
                        st.markdown(f"""
                        <div style='padding:8px;
                          border-left:2px solid
                          {T['border']};
                          margin:4px 0;
                          font-size:0.8rem'>
                          <span style='color:{T['accent']};
                            font-weight:600'>
                            {c['avatar']} {c['user']}
                          </span>
                          <span style='color:{T['muted']};
                            font-size:0.7rem;
                            margin-left:6px'>
                            {c['time']}
                          </span><br>
                          <span style='color:{T['text']}'>
                            {c['text']}
                          </span>
                        </div>
                        """, unsafe_allow_html=True)

# ════════════════════════════════════════════
# PAGE: ANALYTICS
# ════════════════════════════════════════════
elif page == "analytics":
    st.markdown(
        f"<h2 style='color:{T['text']}'>"
        f"📊 Deep Analytics</h2>",
        unsafe_allow_html=True,
    )

    p = platform_stats
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("📝 Total Sessions",
              p.get("total_sessions",0))
    c2.metric("⏱️ Total Hours",
              f"{p.get('total_hours',0):.0f}h")
    c3.metric("📅 Avg Daily",
              p.get("avg_daily_sessions",0))
    c4.metric("📅 Peak Day",
              p.get("peak_day","N/A"))

    col1, col2 = st.columns(2)
    with col1:
        fig = create_activity_trend(
            activity_df, theme
        )
        st.plotly_chart(
            fig, use_container_width=True
        )
        fig = create_session_heatmap(
            all_sessions,
            user.get("email",""),
            theme,
        )
        st.plotly_chart(
            fig, use_container_width=True
        )
    with col2:
        fig = create_category_polar(
            user_hobbies, theme
        )
        st.plotly_chart(
            fig, use_container_width=True
        )
        fig = create_focus_area_pie(
            all_sessions,
            user.get("email",""),
            theme,
        )
        st.plotly_chart(
            fig, use_container_width=True
        )

    # Sessions table
    st.markdown(
        f'<div class="section-title">'
        f'Session History</div>',
        unsafe_allow_html=True,
    )
    df_sessions = pd.DataFrame(all_sessions[:50])
    if not df_sessions.empty:
        cols_show = [
            c for c in [
                "hobby_name","date",
                "duration_min","mood",
                "focus_area","xp_earned",
                "rating",
            ] if c in df_sessions.columns
        ]
        st.dataframe(
            df_sessions[cols_show],
            use_container_width=True,
            height=300,
        )
        csv = df_sessions.to_csv(index=False)
        st.download_button(
            "⬇️ Download Session Data (CSV)",
            csv,
            "sessions.csv",
            "text/csv",
        )

# ════════════════════════════════════════════
# PAGE: LEADERBOARD
# ════════════════════════════════════════════
elif page == "leaderboard":
    st.markdown(
        f"<h2 style='color:{T['text']}'>"
        f"🏅 Global Leaderboard</h2>",
        unsafe_allow_html=True,
    )

    fig = create_leaderboard_chart(
        leaderboard, theme
    )
    st.plotly_chart(fig, use_container_width=True)

    # Leaderboard table
    st.markdown(
        f'<div class="section-title">'
        f'Top Learners</div>',
        unsafe_allow_html=True,
    )
    for rank, u in enumerate(
        leaderboard, 1
    ):
        medal = (
            "🥇" if rank == 1
            else "🥈" if rank == 2
            else "🥉" if rank == 3
            else f"#{rank}"
        )
        bar_w = int(
            u["total_hours"] /
            max(leaderboard[0]["total_hours"],1)
            * 100
        )
        st.markdown(f"""
        <div style='background:{T['card']};
          border:1px solid {T['border']};
          border-radius:12px;
          padding:14px 18px;margin:5px 0;
          display:flex;align-items:center;
          gap:14px'>
          <span style='font-size:1.3rem;
            min-width:30px'>{medal}</span>
          <span style='font-size:1.3rem'>
            {u['avatar']}
          </span>
          <div style='flex:1'>
            <div style='display:flex;
              justify-content:space-between;
              margin-bottom:4px'>
              <span style='color:{T['text']};
                font-weight:700'>
                {u['name']}
              </span>
              <span style='color:{T['gold']};
                font-weight:700'>
                {u['total_hours']:.0f}h
              </span>
            </div>
            <div class='prog-bg'>
              <div class='prog-fill'
                style='width:{bar_w}%'></div>
            </div>
            <div style='display:flex;gap:12px;
              margin-top:4px;font-size:0.72rem;
              color:{T['muted']}'>
              <span>🔥 {u['current_streak']}d streak</span>
              <span>📝 {u['total_sessions']} sessions</span>
              <span>🌟 {u['xp']:,} XP</span>
              <span>{u['level']}</span>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

# ════════════════════════════════════════════
# PAGE: PROFILE
# ════════════════════════════════════════════
elif page == "profile":
    st.markdown(
        f"<h2 style='color:{T['text']}'>"
        f"⚙️ My Profile</h2>",
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns([1,2])
    with col1:
        st.markdown(f"""
        <div class='hobby-card'
          style='text-align:center'>
          <div style='font-size:4rem;
            margin-bottom:12px'>
            {user['avatar']}
          </div>
          <div style='color:{T['text']};
            font-size:1.2rem;font-weight:900'>
            {user['name']}
          </div>
          <div style='color:{T['muted']};
            font-size:0.82rem;margin:4px 0'>
            @{user['username']}
          </div>
          <div style='color:{T['accent']};
            font-weight:700;margin:6px 0'>
            {user['level']}
          </div>
          <div style='color:{T['muted']};
            font-size:0.82rem;
            line-height:1.5;margin-top:8px'>
            {user['bio']}
          </div>
          <div style='display:flex;
            justify-content:space-around;
            margin-top:16px'>
            <div>
              <div style='color:{T['accent']};
                font-weight:700'>
                {user['followers']}
              </div>
              <div style='color:{T['muted']};
                font-size:0.7rem'>Followers</div>
            </div>
            <div>
              <div style='color:{T['accent']};
                font-weight:700'>
                {user['following']}
              </div>
              <div style='color:{T['muted']};
                font-size:0.7rem'>Following</div>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        # Stats
        for label, val, color in [
            ("🌟 Total XP",
             f"{user['xp']:,}", T["gold"]),
            ("⏱️ Total Hours",
             f"{user['total_hours']:.1f}h",
             T["accent"]),
            ("📝 Total Sessions",
             user["total_sessions"],
             T["accent2"]),
            ("🔥 Current Streak",
             f"{user['current_streak']} days",
             T["gold"]),
            ("🏆 Longest Streak",
             f"{user['longest_streak']} days",
             T["orange"]),
            ("🏅 Badges Earned",
             len(earned_badges), T["green"]),
            ("🎯 Hobbies",
             len(user["hobbies"]), T["accent"]),
            ("📍 City", user["city"],
             T["muted"]),
        ]:
            st.markdown(f"""
            <div style='display:flex;
              justify-content:space-between;
              padding:9px 12px;
              background:{T['card']};
              border-radius:8px;margin:3px 0;
              border:1px solid {T['border']}'>
              <span style='color:{T['muted']};
                font-size:0.85rem'>{label}</span>
              <span style='color:{color};
                font-weight:700;
                font-size:0.85rem'>{val}</span>
            </div>
            """, unsafe_allow_html=True)

        # Hobbies
        st.markdown(
            f'<div class="section-title">'
            f'My Hobbies</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            " ".join([
                f"<span class='badge badge-purple'>"
                f"{h}</span>"
                for h in user["hobbies"]
            ]),
            unsafe_allow_html=True,
        )

# ── Footer ────────────────────────────────────
st.markdown("---")
st.markdown(f"""
<div style='text-align:center;
  color:{T['muted']};
  font-size:0.72rem;padding:8px 0'>
  🌟 SkillCloud — Hobby & Skills Tracker •
  Cloud-Synced Learning Platform •
  {datetime.now().strftime('%d %b %Y %H:%M:%S')}
</div>
""", unsafe_allow_html=True)