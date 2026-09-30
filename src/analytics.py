"""
analytics.py
Charts for Hobby & Skills Tracker Dashboard.
Dark + Light theme support.
"""

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
import random

THEMES = {
    "dark": {
        "bg":        "#080610",
        "card":      "#0f0d1e",
        "border":    "#1e1a38",
        "text":      "#e8e0f8",
        "muted":     "#7868a8",
        "accent":    "#a78bfa",
        "accent2":   "#60a5fa",
        "gold":      "#fbbf24",
        "red":       "#f87171",
        "green":     "#34d399",
        "pink":      "#f472b6",
        "orange":    "#fb923c",
        "paper_bg":  "rgba(0,0,0,0)",
        "plot_bg":   "rgba(8,6,16,0.95)",
        "grid":      "#1e1a38",
        "font_color":"#c4b8e8",
    },
    "light": {
        "bg":        "#f5f0ff",
        "card":      "#ffffff",
        "border":    "#e0d8f8",
        "text":      "#1a0840",
        "muted":     "#6a5898",
        "accent":    "#7c3aed",
        "accent2":   "#2563eb",
        "gold":      "#d97706",
        "red":       "#dc2626",
        "green":     "#059669",
        "pink":      "#db2777",
        "orange":    "#ea580c",
        "paper_bg":  "rgba(255,255,255,0)",
        "plot_bg":   "rgba(245,240,255,0.95)",
        "grid":      "#e0d8f8",
        "font_color":"#2a1460",
    },
}

PALETTE = [
    "#a78bfa","#60a5fa","#fbbf24",
    "#f87171","#34d399","#f472b6",
    "#fb923c","#38bdf8","#a3e635",
    "#e879f9",
]

CAT_COLORS = {
    "Music":      "#a78bfa",
    "Art":        "#f472b6",
    "Technology": "#60a5fa",
    "Fitness":    "#34d399",
    "Mind":       "#fbbf24",
    "Creative":   "#fb923c",
}


def get_theme(name="dark"):
    return THEMES.get(name, THEMES["dark"])


def get_pt(theme="dark"):
    t = get_theme(theme)
    return dict(
        template=(
            "plotly_dark"
            if theme == "dark"
            else "plotly_white"
        ),
        paper_bgcolor=t["paper_bg"],
        plot_bgcolor=t["plot_bg"],
        font=dict(
            family="Inter, sans-serif",
            color=t["font_color"],
            size=12,
        ),
    )


def create_activity_trend(activity_df,
                          theme="dark"):
    """Line chart: 30-day activity trend."""
    t  = get_theme(theme)
    PT = get_pt(theme)

    if activity_df.empty:
        return go.Figure()

    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        row_heights=[0.65, 0.35],
        vertical_spacing=0.08,
    )

    fig.add_trace(go.Scatter(
        x=activity_df["date"],
        y=activity_df["sessions"],
        mode="lines",
        name="Sessions",
        line=dict(
            color=t["accent"], width=2.5
        ),
        fill="tozeroy",
        fillcolor="rgba(167,139,250,0.1)",
    ), row=1, col=1)

    fig.add_trace(go.Scatter(
        x=activity_df["date"],
        y=activity_df["hours"],
        mode="lines",
        name="Hours",
        line=dict(
            color=t["green"],
            width=1.5, dash="dot",
        ),
    ), row=1, col=1)

    fig.add_trace(go.Bar(
        x=activity_df["date"],
        y=activity_df["xp_earned"],
        name="XP Earned",
        marker=dict(
            color=t["gold"], opacity=0.7
        ),
    ), row=2, col=1)

    fig.update_layout(
        **PT,
        title=dict(
            text="📈 30-Day Activity Trend",
            font=dict(
                color=t["text"], size=14
            ),
        ),
        height=400,
        xaxis2=dict(
            gridcolor=t["grid"],
            color=t["muted"],
        ),
        yaxis=dict(
            title="Sessions",
            gridcolor=t["grid"],
            color=t["muted"],
        ),
        yaxis2=dict(
            title="XP",
            gridcolor=t["grid"],
            color=t["muted"],
        ),
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            font=dict(color=t["muted"]),
            orientation="h", y=1.05,
        ),
        margin=dict(t=60,b=20,l=20,r=20),
        hovermode="x unified",
    )
    return fig


def create_hobby_radar(hobbies, theme="dark"):
    """Radar chart: hobby skill levels."""
    t  = get_theme(theme)
    PT = get_pt(theme)

    if not hobbies:
        return go.Figure()

    skill_map = {
        "Absolute Beginner": 10,
        "Beginner":          20,
        "Elementary":        35,
        "Pre-Intermediate":  45,
        "Intermediate":      60,
        "Upper-Intermediate":72,
        "Advanced":          85,
        "Expert":            95,
        "Master":            100,
    }

    names  = [h["name"][:10] for h in hobbies[:6]]
    values = [
        skill_map.get(h["skill_level"], 50)
        for h in hobbies[:6]
    ]

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values + [values[0]],
        theta=names + [names[0]],
        fill="toself",
        fillcolor="rgba(167,139,250,0.15)",
        line=dict(color=t["accent"], width=2),
        name="Skill Level",
    ))

    fig.update_layout(
        **PT,
        polar=dict(
            bgcolor=t["card"],
            radialaxis=dict(
                range=[0,100],
                gridcolor=t["border"],
                color=t["muted"],
            ),
            angularaxis=dict(
                gridcolor=t["border"],
                color=t["text"],
            ),
        ),
        title=dict(
            text="🎯 Skill Level Radar",
            font=dict(
                color=t["text"], size=14
            ),
        ),
        height=340,
        showlegend=False,
        margin=dict(t=50,b=20,l=20,r=20),
    )
    return fig


def create_session_heatmap(sessions,
                           user_id,
                           theme="dark"):
    """GitHub-style activity heatmap."""
    t  = get_theme(theme)
    PT = get_pt(theme)

    from datetime import datetime, timedelta

    weeks  = 12
    days   = weeks * 7
    dates  = []
    values = []
    texts  = []

    session_map = {}
    for s in sessions:
        if s.get("user_id") == user_id:
            d = s.get("date","")
            session_map[d] = (
                session_map.get(d, 0) +
                s.get("duration_min", 0)
            )

    for i in range(days-1, -1, -1):
        date = (
            datetime.now() -
            timedelta(days=i)
        ).strftime("%Y-%m-%d")
        mins = session_map.get(date, 0)
        dates.append(date)
        values.append(mins)
        texts.append(
            f"{date}<br>{mins} min"
        )

    # Reshape into weeks x days
    week_labels = []
    day_labels  = ["Mon","Tue","Wed",
                   "Thu","Fri","Sat","Sun"]
    z_data      = []

    for w in range(weeks):
        row = []
        for d in range(7):
            idx = w * 7 + d
            if idx < len(values):
                row.append(values[idx])
            else:
                row.append(0)
        z_data.append(row)

    fig = go.Figure(go.Heatmap(
        z=z_data,
        x=day_labels,
        y=[f"W{i+1}" for i in range(weeks)],
        colorscale=[
            [0.0, t["card"]],
            [0.3, "rgba(167,139,250,0.3)"],
            [0.7, t["accent"]],
            [1.0, "#7c3aed"],
        ],
        showscale=False,
        xgap=3, ygap=3,
        hovertemplate=(
            "Week: %{y}<br>"
            "Day: %{x}<br>"
            "Minutes: %{z}"
            "<extra></extra>"
        ),
    ))

    fig.update_layout(
        **PT,
        title=dict(
            text="🔥 Activity Heatmap "
                 "(12 Weeks)",
            font=dict(
                color=t["text"], size=14
            ),
        ),
        height=280,
        xaxis=dict(color=t["text"]),
        yaxis=dict(color=t["muted"]),
        margin=dict(t=50,b=20,l=40,r=20),
    )
    return fig


def create_progress_bars(hobbies,
                         theme="dark"):
    """Horizontal bars: goal progress."""
    t  = get_theme(theme)
    PT = get_pt(theme)

    if not hobbies:
        return go.Figure()

    names  = [h["name"][:15] for h in hobbies]
    progrs = [h["goal_progress"] for h in hobbies]
    colors = [
        CAT_COLORS.get(h["category"],
                       t["accent"])
        for h in hobbies
    ]

    fig = go.Figure(go.Bar(
        x=progrs,
        y=names,
        orientation="h",
        marker=dict(
            color=colors,
            line=dict(
                color=t["card"], width=1
            ),
        ),
        text=[f"{p}%" for p in progrs],
        textposition="outside",
        textfont=dict(
            color=t["text"], size=11
        ),
        hovertemplate=(
            "<b>%{y}</b><br>"
            "Progress: %{x}%"
            "<extra></extra>"
        ),
    ))

    fig.update_layout(
        **PT,
        title=dict(
            text="🎯 Goal Progress",
            font=dict(
                color=t["text"], size=14
            ),
        ),
        height=max(200, len(hobbies)*45),
        xaxis=dict(
            range=[0,120],
            gridcolor=t["grid"],
            color=t["muted"],
            title="Progress (%)",
        ),
        yaxis=dict(color=t["text"]),
        margin=dict(t=50,b=20,l=20,r=60),
    )
    return fig


def create_hours_donut(hobbies, theme="dark"):
    """Donut: hours by hobby."""
    t  = get_theme(theme)
    PT = get_pt(theme)

    if not hobbies:
        return go.Figure()

    labels = [h["name"][:12] for h in hobbies]
    values = [h["total_hours"] for h in hobbies]
    colors = [
        CAT_COLORS.get(h["category"],
                       t["accent"])
        for h in hobbies
    ]

    fig = go.Figure(go.Pie(
        labels=labels,
        values=values,
        hole=0.6,
        marker=dict(
            colors=colors,
            line=dict(
                color=t["card"], width=2
            ),
        ),
        textinfo="label+percent",
        textfont=dict(
            size=11, color=t["text"]
        ),
    ))

    total = sum(values)
    fig.add_annotation(
        text=f"<b>{total:.0f}h</b><br>Total",
        x=0.5, y=0.5, showarrow=False,
        font=dict(size=14, color=t["accent"]),
    )

    fig.update_layout(
        **PT,
        title=dict(
            text="⏱️ Hours by Hobby",
            font=dict(
                color=t["text"], size=14
            ),
        ),
        height=300,
        showlegend=False,
        margin=dict(t=50,b=10,l=10,r=10),
    )
    return fig


def create_category_polar(hobbies,
                          theme="dark"):
    """Polar chart: category distribution."""
    t  = get_theme(theme)
    PT = get_pt(theme)

    if not hobbies:
        return go.Figure()

    from collections import Counter
    cats   = Counter(
        h["category"] for h in hobbies
    )
    labels = list(cats.keys())
    values = list(cats.values())
    colors = [
        CAT_COLORS.get(c, t["accent"])
        for c in labels
    ]

    fig = go.Figure(go.Barpolar(
        r=values,
        theta=labels,
        marker=dict(
            color=colors,
            line=dict(
                color=t["card"], width=1
            ),
        ),
        opacity=0.85,
    ))

    fig.update_layout(
        **PT,
        title=dict(
            text="🌐 Hobby Categories",
            font=dict(
                color=t["text"], size=14
            ),
        ),
        polar=dict(
            bgcolor=t["card"],
            radialaxis=dict(
                gridcolor=t["border"],
                color=t["muted"],
            ),
            angularaxis=dict(
                gridcolor=t["border"],
                color=t["text"],
            ),
        ),
        height=320,
        showlegend=False,
        margin=dict(t=50,b=20,l=20,r=20),
    )
    return fig


def create_xp_gauge(xp, level, theme="dark"):
    """Gauge: XP progress to next level."""
    t  = get_theme(theme)
    PT = get_pt(theme)

    level_xp = {
        "🌱 Beginner":      1000,
        "📈 Intermediate":  2500,
        "⭐ Advanced":      5000,
        "🏆 Expert":        10000,
    }

    max_xp = level_xp.get(level, 5000)
    pct    = round(min(xp/max_xp*100, 100), 1)
    color  = (
        t["gold"]   if pct >= 75
        else t["accent"] if pct >= 40
        else t["accent2"]
    )

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=xp,
        title=dict(
            text=f"XP Progress — {level}",
            font=dict(
                color=t["muted"], size=12
            ),
        ),
        number=dict(
            suffix=" XP",
            font=dict(size=22, color=color),
        ),
        gauge=dict(
            axis=dict(
                range=[0, max_xp],
                tickcolor=t["muted"],
            ),
            bar=dict(
                color=color, thickness=0.25
            ),
            bgcolor=t["card"],
            bordercolor=t["border"],
            steps=[
                dict(range=[0, max_xp*0.33],
                     color="rgba(96,165,250,0.1)"),
                dict(range=[max_xp*0.33,
                            max_xp*0.66],
                     color="rgba(167,139,250,0.1)"),
                dict(range=[max_xp*0.66, max_xp],
                     color="rgba(251,191,36,0.1)"),
            ],
        ),
    ))

    fig.update_layout(
        **PT,
        height=220,
        margin=dict(t=50,b=10,l=20,r=20),
    )
    return fig


def create_session_mood(sessions,
                        user_id,
                        theme="dark"):
    """Bar: session mood distribution."""
    t  = get_theme(theme)
    PT = get_pt(theme)

    user_sessions = [
        s for s in sessions
        if s.get("user_id") == user_id
    ]
    if not user_sessions:
        return go.Figure()

    from collections import Counter
    moods  = Counter(
        s.get("mood","") for s in user_sessions
    )
    labels = list(moods.keys())
    values = list(moods.values())
    colors = [
        t["green"], t["accent2"],
        t["red"],   t["gold"], t["accent"],
    ][:len(labels)]

    fig = go.Figure(go.Bar(
        x=labels, y=values,
        marker=dict(
            color=colors,
            line=dict(
                color=t["card"], width=1
            ),
        ),
        text=values,
        textposition="outside",
        textfont=dict(
            color=t["text"], size=11
        ),
    ))

    fig.update_layout(
        **PT,
        title=dict(
            text="😊 Session Mood Tracker",
            font=dict(
                color=t["text"], size=14
            ),
        ),
        height=260,
        xaxis=dict(color=t["text"]),
        yaxis=dict(
            title="Sessions",
            gridcolor=t["grid"],
            color=t["muted"],
        ),
        margin=dict(t=50,b=20,l=20,r=20),
    )
    return fig


def create_leaderboard_chart(users,
                             theme="dark"):
    """Horizontal bar: top users leaderboard."""
    t  = get_theme(theme)
    PT = get_pt(theme)

    if not users:
        return go.Figure()

    top    = users[:8]
    names  = [u["name"][:15] for u in top]
    hours  = [u["total_hours"]  for u in top]
    colors = PALETTE[:len(names)]

    fig = go.Figure(go.Bar(
        x=hours, y=names,
        orientation="h",
        marker=dict(
            color=colors,
            line=dict(
                color=t["card"], width=1
            ),
        ),
        text=[f"{h:.0f}h" for h in hours],
        textposition="outside",
        textfont=dict(
            color=t["text"], size=11
        ),
        hovertemplate=(
            "<b>%{y}</b><br>"
            "Hours: %{x:.1f}"
            "<extra></extra>"
        ),
    ))

    fig.update_layout(
        **PT,
        title=dict(
            text="🏆 Leaderboard — Top Learners",
            font=dict(
                color=t["text"], size=14
            ),
        ),
        height=340,
        xaxis=dict(
            title="Total Hours",
            gridcolor=t["grid"],
            color=t["muted"],
        ),
        yaxis=dict(color=t["text"]),
        margin=dict(t=50,b=20,l=20,r=60),
    )
    return fig


def create_focus_area_pie(sessions,
                          user_id,
                          theme="dark"):
    """Pie: focus area distribution."""
    t  = get_theme(theme)
    PT = get_pt(theme)

    user_sessions = [
        s for s in sessions
        if s.get("user_id") == user_id
    ]
    if not user_sessions:
        return go.Figure()

    from collections import Counter
    focus  = Counter(
        s.get("focus_area","")
        for s in user_sessions
    )

    fig = go.Figure(go.Pie(
        labels=list(focus.keys()),
        values=list(focus.values()),
        hole=0.5,
        marker=dict(
            colors=PALETTE[:len(focus)],
            line=dict(
                color=t["card"], width=2
            ),
        ),
        textinfo="label+percent",
        textfont=dict(
            size=10, color=t["text"]
        ),
    ))

    fig.update_layout(
        **PT,
        title=dict(
            text="🎯 Focus Areas",
            font=dict(
                color=t["text"], size=14
            ),
        ),
        height=280,
        showlegend=False,
        margin=dict(t=50,b=10,l=10,r=10),
    )
    return fig