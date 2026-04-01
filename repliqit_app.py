import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Repliq.it Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

/* Sidebar */
[data-testid="stSidebar"] {
    background: #F2EDE4;
    border-right: 1px solid #D8D2C8;
}
[data-testid="stSidebar"] .stRadio label {
    font-size: 0.88rem;
    color: #3D5A4C;
    font-weight: 500;
}

/* Metric cards */
[data-testid="metric-container"] {
    background: #F2EDE4;
    border: 1px solid #D8D2C8;
    border-radius: 10px;
    padding: 1rem;
}
[data-testid="stMetricValue"] { color: #1A1A18 !important; font-weight: 600; }
[data-testid="stMetricLabel"] { color: #8A8278 !important; font-size: 0.8rem; }
[data-testid="stMetricDelta"] { font-size: 0.78rem; }

/* Headers */
h1 { color: #1A1A18 !important; font-weight: 600 !important; }
h2 { color: #1A1A18 !important; font-weight: 500 !important; }
h3 { color: #3D5A4C !important; font-weight: 500 !important; }

/* Buttons */
.stButton > button {
    background: #3D5A4C;
    color: #F2EDE4;
    border: none;
    border-radius: 100px;
    font-size: 0.85rem;
    font-weight: 500;
    padding: 0.4rem 1.2rem;
    transition: opacity 0.15s;
}
.stButton > button:hover { opacity: 0.8; background: #3D5A4C; color: #F2EDE4; }

/* Tabs */
.stTabs [data-baseweb="tab-list"] { gap: 4px; background: #F2EDE4; border-radius: 8px; padding: 4px; }
.stTabs [data-baseweb="tab"] { border-radius: 6px; font-size: 0.85rem; font-weight: 500; color: #8A8278; }
.stTabs [aria-selected="true"] { background: #3D5A4C !important; color: #F2EDE4 !important; }

/* Dataframe */
[data-testid="stDataFrame"] { border: 1px solid #D8D2C8; border-radius: 10px; }

/* Selectbox / Input */
.stSelectbox > div > div { border-color: #D8D2C8 !important; border-radius: 8px; }
.stTextInput > div > div { border-color: #D8D2C8 !important; border-radius: 8px; }
.stTextArea > div > div { border-color: #D8D2C8 !important; border-radius: 8px; }

div[data-testid="stStatusWidget"] { display: none; }

/* Status badges */
.badge {
    display: inline-block;
    padding: 2px 10px;
    border-radius: 100px;
    font-size: 0.75rem;
    font-weight: 500;
}
.badge-new       { background:#EAF3DE; color:#3B6D11; }
.badge-follow    { background:#FAEEDA; color:#854F0B; }
.badge-booked    { background:#E1F5EE; color:#0F6E56; }
.badge-lost      { background:#FCEBEB; color:#A32D2D; }
.badge-confirmed { background:#E1F5EE; color:#0F6E56; }
.badge-pending   { background:#FAEEDA; color:#854F0B; }
.badge-noshow    { background:#FCEBEB; color:#A32D2D; }
</style>
""", unsafe_allow_html=True)

# ── Session state — sample data ────────────────────────────────────────────────
def init_data():
    if "leads" not in st.session_state:
        names   = ["Priya Sharma","Ravi Kumar","Ananya Iyer","Meera Nair","Karthik R",
                   "Divya Menon","Suresh Bhat","Lakshmi T","Arjun Pillai","Nisha Patel"]
        types   = ["Salon","Coaching Center","Clinic","Salon","Coaching Center",
                   "Clinic","Salon","Clinic","Coaching Center","Salon"]
        sources = ["Instagram","WhatsApp","Website","Instagram","WhatsApp",
                   "Instagram","Website","WhatsApp","Instagram","Website"]
        statuses= ["New","Follow-up","Booked","New","Booked",
                   "Lost","Follow-up","Booked","New","Booked"]
        st.session_state.leads = pd.DataFrame({
            "Name":     names,
            "Business": types,
            "Source":   sources,
            "Status":   statuses,
            "Date":     [(datetime.today() - timedelta(days=random.randint(0,14))).strftime("%d %b %Y") for _ in range(10)],
            "Reply (s)": [random.randint(8, 55) for _ in range(10)],
            "Notes":    [""] * 10,
        })

    if "appointments" not in st.session_state:
        clients = ["Priya Sharma","Ravi Kumar","Ananya Iyer","Meera Nair","Karthik R","Divya Menon"]
        statuses2 = ["Confirmed","Confirmed","Pending","No-show","Confirmed","Pending"]
        st.session_state.appointments = pd.DataFrame({
            "Client":   clients,
            "Date":     [(datetime.today() + timedelta(days=random.randint(-3,7))).strftime("%d %b %Y") for _ in range(6)],
            "Time":     ["10:00 AM","11:30 AM","02:00 PM","09:00 AM","03:30 PM","05:00 PM"],
            "Type":     ["Consultation","Follow-up","Consultation","Consultation","Follow-up","Consultation"],
            "Status":   statuses2,
            "Reminder": ["Sent","Sent","Pending","Sent","Pending","Pending"],
        })

    if "weekly" not in st.session_state:
        days = [(datetime.today() - timedelta(days=6-i)).strftime("%a %d") for i in range(7)]
        st.session_state.weekly = pd.DataFrame({
            "Day":         days,
            "Leads":       [3,5,2,7,4,6,3],
            "Booked":      [2,3,1,5,3,4,2],
            "No-shows":    [0,1,0,1,0,0,1],
            "Revenue (₹)": [4500,7200,2800,9500,6100,8400,4200],
        })

init_data()

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🌿 Repliq.it")
    st.markdown("<p style='color:#8A8278;font-size:0.8rem;margin-top:-0.5rem;margin-bottom:1.5rem;'>Revenue Recovery Dashboard</p>", unsafe_allow_html=True)

    page = st.radio("Navigation", ["Overview", "Leads", "Appointments", "Add Lead", "Reports"], label_visibility="collapsed")

    st.markdown("---")
    st.markdown("<p style='color:#8A8278;font-size:0.78rem;'>Business</p>", unsafe_allow_html=True)
    biz_type = st.selectbox("Type", ["Salon","Coaching Center","Clinic"], label_visibility="collapsed")
    st.markdown("<p style='color:#8A8278;font-size:0.78rem;margin-top:0.5rem;'>Owner</p>", unsafe_allow_html=True)
    st.markdown("<p style='color:#1A1A18;font-size:0.9rem;font-weight:500;'>Gokul N</p>", unsafe_allow_html=True)
    st.markdown("<p style='color:#8A8278;font-size:0.78rem;'>hello@repliq.it</p>", unsafe_allow_html=True)

# ── Helpers ────────────────────────────────────────────────────────────────────
STATUS_COLORS = {
    "New":"badge-new","Follow-up":"badge-follow","Booked":"badge-booked",
    "Lost":"badge-lost","Confirmed":"badge-confirmed","Pending":"badge-pending","No-show":"badge-noshow",
}

def badge(text):
    cls = STATUS_COLORS.get(text, "badge-new")
    return f'<span class="badge {cls}">{text}</span>'

SAGE   = "#3D5A4C"
SAND   = "#F2EDE4"
MUTED  = "#8A8278"
LINE   = "#D8D2C8"
INK    = "#1A1A18"

def sage_chart_theme():
    return dict(
        plot_bgcolor=SAND, paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter", color=INK, size=12),
        xaxis=dict(gridcolor=LINE, linecolor=LINE, tickfont=dict(color=MUTED)),
        yaxis=dict(gridcolor=LINE, linecolor=LINE, tickfont=dict(color=MUTED)),
        margin=dict(l=0,r=0,t=20,b=0),
    )

# ── OVERVIEW ──────────────────────────────────────────────────────────────────
if page == "Overview":
    st.markdown("## Overview")
    st.markdown(f"<p style='color:{MUTED};font-size:0.9rem;margin-top:-0.5rem;'>Today, {datetime.today().strftime('%A %d %B %Y')}</p>", unsafe_allow_html=True)

    st.markdown("---")

    c1,c2,c3,c4 = st.columns(4)
    total_leads  = len(st.session_state.leads)
    booked       = len(st.session_state.leads[st.session_state.leads.Status=="Booked"])
    no_shows     = len(st.session_state.appointments[st.session_state.appointments.Status=="No-show"])
    avg_reply    = int(st.session_state.leads["Reply (s)"].mean())
    c1.metric("Total Leads", total_leads,       "+3 this week")
    c2.metric("Appointments Booked", booked,    "+2 this week")
    c3.metric("No-shows", no_shows,             "-1 vs last week")
    c4.metric("Avg Reply Time", f"{avg_reply}s","↓ 8s faster")

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns([2,1])

    with col1:
        st.markdown(f"<h3 style='color:{SAGE};'>Weekly lead & booking trend</h3>", unsafe_allow_html=True)
        wk = st.session_state.weekly
        fig = go.Figure()
        fig.add_bar(x=wk.Day, y=wk.Leads,  name="Leads",  marker_color=LINE)
        fig.add_bar(x=wk.Day, y=wk.Booked, name="Booked", marker_color=SAGE)
        fig.update_layout(**sage_chart_theme(), barmode="group", height=240,
                          legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown(f"<h3 style='color:{SAGE};'>Lead sources</h3>", unsafe_allow_html=True)
        src = st.session_state.leads.Source.value_counts().reset_index()
        src.columns = ["Source","Count"]
        fig2 = px.pie(src, names="Source", values="Count",
                      color_discrete_sequence=[SAGE,"#6B8F7E","#A8C5B8",LINE],
                      hole=0.55)
        fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)", showlegend=True,
                           legend=dict(font=dict(size=11,color=INK)),
                           margin=dict(l=0,r=0,t=10,b=0), height=240)
        fig2.update_traces(textinfo="percent", textfont_size=11)
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col3, col4 = st.columns(2)

    with col3:
        st.markdown(f"<h3 style='color:{SAGE};'>Recent leads</h3>", unsafe_allow_html=True)
        recent = st.session_state.leads[["Name","Source","Status","Reply (s)"]].head(5).copy()
        st.dataframe(recent, use_container_width=True, hide_index=True)

    with col4:
        st.markdown(f"<h3 style='color:{SAGE};'>Upcoming appointments</h3>", unsafe_allow_html=True)
        upcoming = st.session_state.appointments[["Client","Date","Time","Status"]].head(5)
        st.dataframe(upcoming, use_container_width=True, hide_index=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='color:{SAGE};'>Revenue this week</h3>", unsafe_allow_html=True)
    fig3 = px.area(st.session_state.weekly, x="Day", y="Revenue (₹)",
                   color_discrete_sequence=[SAGE])
    fig3.update_traces(fill="tozeroy", line_color=SAGE, fillcolor="rgba(61,90,76,0.12)")
    fig3.update_layout(**sage_chart_theme(), height=200)
    st.plotly_chart(fig3, use_container_width=True)

# ── LEADS ─────────────────────────────────────────────────────────────────────
elif page == "Leads":
    st.markdown("## Lead tracker")
    st.markdown(f"<p style='color:{MUTED};font-size:0.9rem;margin-top:-0.5rem;'>All inbound enquiries</p>", unsafe_allow_html=True)
    st.markdown("---")

    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        status_filter = st.selectbox("Filter by status", ["All","New","Follow-up","Booked","Lost"])
    with col_f2:
        source_filter = st.selectbox("Filter by source", ["All","Instagram","WhatsApp","Website"])
    with col_f3:
        biz_filter = st.selectbox("Filter by business", ["All","Salon","Coaching Center","Clinic"])

    df = st.session_state.leads.copy()
    if status_filter != "All": df = df[df.Status == status_filter]
    if source_filter != "All": df = df[df.Source == source_filter]
    if biz_filter    != "All": df = df[df.Business == biz_filter]

    st.markdown("<br>", unsafe_allow_html=True)

    # Render as styled table
    rows_html = ""
    for _, r in df.iterrows():
        rows_html += f"""
        <tr style='border-bottom:1px solid {LINE};'>
          <td style='padding:10px 8px;font-size:0.88rem;font-weight:500;color:{INK};'>{r['Name']}</td>
          <td style='padding:10px 8px;font-size:0.85rem;color:{MUTED};'>{r['Business']}</td>
          <td style='padding:10px 8px;font-size:0.85rem;color:{MUTED};'>{r['Source']}</td>
          <td style='padding:10px 8px;'>{badge(r['Status'])}</td>
          <td style='padding:10px 8px;font-size:0.85rem;color:{MUTED};'>{r['Date']}</td>
          <td style='padding:10px 8px;font-size:0.85rem;color:{SAGE};font-weight:500;'>{r['Reply (s)']}s</td>
        </tr>"""

    st.markdown(f"""
    <table style='width:100%;border-collapse:collapse;background:{SAND};border:1px solid {LINE};border-radius:10px;overflow:hidden;'>
      <thead>
        <tr style='background:{LINE};'>
          <th style='padding:10px 8px;text-align:left;font-size:0.78rem;font-weight:500;color:{MUTED};letter-spacing:.05em;text-transform:uppercase;'>Name</th>
          <th style='padding:10px 8px;text-align:left;font-size:0.78rem;font-weight:500;color:{MUTED};letter-spacing:.05em;text-transform:uppercase;'>Business</th>
          <th style='padding:10px 8px;text-align:left;font-size:0.78rem;font-weight:500;color:{MUTED};letter-spacing:.05em;text-transform:uppercase;'>Source</th>
          <th style='padding:10px 8px;text-align:left;font-size:0.78rem;font-weight:500;color:{MUTED};letter-spacing:.05em;text-transform:uppercase;'>Status</th>
          <th style='padding:10px 8px;text-align:left;font-size:0.78rem;font-weight:500;color:{MUTED};letter-spacing:.05em;text-transform:uppercase;'>Date</th>
          <th style='padding:10px 8px;text-align:left;font-size:0.78rem;font-weight:500;color:{MUTED};letter-spacing:.05em;text-transform:uppercase;'>Reply Time</th>
        </tr>
      </thead>
      <tbody>{rows_html}</tbody>
    </table>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    c1,c2,c3 = st.columns(3)
    c1.metric("Total shown", len(df))
    c2.metric("Avg reply", f"{int(df['Reply (s)'].mean())}s" if len(df) else "—")
    c3.metric("Conversion rate", f"{int(len(df[df.Status=='Booked'])/len(df)*100)}%" if len(df) else "—")

# ── APPOINTMENTS ──────────────────────────────────────────────────────────────
elif page == "Appointments":
    st.markdown("## Appointments")
    st.markdown(f"<p style='color:{MUTED};font-size:0.9rem;margin-top:-0.5rem;'>Manage bookings and reminders</p>", unsafe_allow_html=True)
    st.markdown("---")

    tab1, tab2 = st.tabs(["All appointments", "Send reminder"])

    with tab1:
        status_f = st.selectbox("Filter by status", ["All","Confirmed","Pending","No-show"])
        appts = st.session_state.appointments.copy()
        if status_f != "All": appts = appts[appts.Status == status_f]

        rows_html = ""
        for _, r in appts.iterrows():
            rows_html += f"""
            <tr style='border-bottom:1px solid {LINE};'>
              <td style='padding:10px 8px;font-size:0.88rem;font-weight:500;color:{INK};'>{r['Client']}</td>
              <td style='padding:10px 8px;font-size:0.85rem;color:{MUTED};'>{r['Date']}</td>
              <td style='padding:10px 8px;font-size:0.85rem;color:{MUTED};'>{r['Time']}</td>
              <td style='padding:10px 8px;font-size:0.85rem;color:{MUTED};'>{r['Type']}</td>
              <td style='padding:10px 8px;'>{badge(r['Status'])}</td>
              <td style='padding:10px 8px;'>{badge(r['Reminder'])}</td>
            </tr>"""

        st.markdown(f"""
        <table style='width:100%;border-collapse:collapse;background:{SAND};border:1px solid {LINE};border-radius:10px;overflow:hidden;'>
          <thead>
            <tr style='background:{LINE};'>
              {''.join(f"<th style='padding:10px 8px;text-align:left;font-size:0.78rem;font-weight:500;color:{MUTED};letter-spacing:.05em;text-transform:uppercase;'>{h}</th>" for h in ['Client','Date','Time','Type','Status','Reminder'])}
            </tr>
          </thead>
          <tbody>{rows_html}</tbody>
        </table>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        c1,c2,c3 = st.columns(3)
        all_a = st.session_state.appointments
        c1.metric("Confirmed", len(all_a[all_a.Status=="Confirmed"]))
        c2.metric("Pending",   len(all_a[all_a.Status=="Pending"]))
        c3.metric("No-shows",  len(all_a[all_a.Status=="No-show"]))

    with tab2:
        st.markdown(f"<h3 style='color:{SAGE};'>Send appointment reminder</h3>", unsafe_allow_html=True)
        clients_list = st.session_state.appointments["Client"].tolist()
        selected_client = st.selectbox("Select client", clients_list)
        msg = st.text_area("Message", f"Hi! Just a reminder about your upcoming appointment with us. Please confirm your attendance or let us know if you'd like to reschedule. — Repliq.it")
        if st.button("Send Reminder"):
            idx = st.session_state.appointments[st.session_state.appointments.Client == selected_client].index[0]
            st.session_state.appointments.at[idx, "Reminder"] = "Sent"
            st.success(f"Reminder sent to {selected_client}!")

# ── ADD LEAD ──────────────────────────────────────────────────────────────────
elif page == "Add Lead":
    st.markdown("## Add new lead")
    st.markdown(f"<p style='color:{MUTED};font-size:0.9rem;margin-top:-0.5rem;'>Log a new inbound enquiry</p>", unsafe_allow_html=True)
    st.markdown("---")

    with st.form("add_lead_form"):
        c1, c2 = st.columns(2)
        with c1:
            name     = st.text_input("Full name *")
            source   = st.selectbox("Source", ["Instagram","WhatsApp","Website","Referral","Walk-in"])
            reply_s  = st.number_input("Reply time (seconds)", min_value=0, max_value=300, value=25)
        with c2:
            business = st.selectbox("Business type", ["Salon","Coaching Center","Clinic","Other"])
            status   = st.selectbox("Status", ["New","Follow-up","Booked","Lost"])

        notes = st.text_area("Notes", placeholder="e.g. Interested in monthly package, follow up Friday...")
        submitted = st.form_submit_button("Add Lead")

        if submitted:
            if not name:
                st.error("Please enter a name.")
            else:
                new_row = {
                    "Name":     name,
                    "Business": business,
                    "Source":   source,
                    "Status":   status,
                    "Date":     datetime.today().strftime("%d %b %Y"),
                    "Reply (s)": reply_s,
                    "Notes":    notes,
                }
                st.session_state.leads = pd.concat(
                    [st.session_state.leads, pd.DataFrame([new_row])],
                    ignore_index=True
                )
                st.success(f"Lead '{name}' added successfully!")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='color:{SAGE};'>Recent additions</h3>", unsafe_allow_html=True)
    st.dataframe(st.session_state.leads.tail(5)[["Name","Business","Source","Status","Date"]], use_container_width=True, hide_index=True)

# ── REPORTS ───────────────────────────────────────────────────────────────────
elif page == "Reports":
    st.markdown("## Reports")
    st.markdown(f"<p style='color:{MUTED};font-size:0.9rem;margin-top:-0.5rem;'>Revenue recovery performance</p>", unsafe_allow_html=True)
    st.markdown("---")

    wk = st.session_state.weekly
    leads_df = st.session_state.leads
    appts_df = st.session_state.appointments

    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Total Revenue (week)", f"₹{wk['Revenue (₹)'].sum():,}")
    c2.metric("Leads this week",      wk["Leads"].sum())
    c3.metric("Bookings",             wk["Booked"].sum())
    c4.metric("No-show rate",         f"{int(appts_df[appts_df.Status=='No-show'].shape[0]/len(appts_df)*100)}%")

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"<h3 style='color:{SAGE};'>Revenue by day</h3>", unsafe_allow_html=True)
        fig = px.bar(wk, x="Day", y="Revenue (₹)", color_discrete_sequence=[SAGE])
        fig.update_layout(**sage_chart_theme(), height=220)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown(f"<h3 style='color:{SAGE};'>Lead status breakdown</h3>", unsafe_allow_html=True)
        status_counts = leads_df.Status.value_counts().reset_index()
        status_counts.columns = ["Status","Count"]
        fig2 = px.bar(status_counts, x="Status", y="Count",
                      color_discrete_sequence=[SAGE,"#6B8F7E","#A8C5B8",LINE,"#8A8278"])
        fig2.update_layout(**sage_chart_theme(), height=220)
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col3, col4 = st.columns(2)

    with col3:
        st.markdown(f"<h3 style='color:{SAGE};'>No-shows vs bookings</h3>", unsafe_allow_html=True)
        fig3 = go.Figure()
        fig3.add_scatter(x=wk.Day, y=wk.Booked,   name="Booked",   line=dict(color=SAGE,  width=2), mode="lines+markers")
        fig3.add_scatter(x=wk.Day, y=wk["No-shows"], name="No-shows", line=dict(color="#C1511F",width=2), mode="lines+markers")
        fig3.update_layout(**sage_chart_theme(), height=220,
                           legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))
        st.plotly_chart(fig3, use_container_width=True)

    with col4:
        st.markdown(f"<h3 style='color:{SAGE};'>Leads by business type</h3>", unsafe_allow_html=True)
        biz_counts = leads_df.Business.value_counts().reset_index()
        biz_counts.columns = ["Business","Count"]
        fig4 = px.pie(biz_counts, names="Business", values="Count",
                      color_discrete_sequence=[SAGE,"#6B8F7E","#A8C5B8"], hole=0.5)
        fig4.update_layout(paper_bgcolor="rgba(0,0,0,0)", margin=dict(l=0,r=0,t=10,b=0), height=220,
                           legend=dict(font=dict(size=11,color=INK)))
        st.plotly_chart(fig4, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='color:{SAGE};'>Weekly summary table</h3>", unsafe_allow_html=True)
    st.dataframe(wk, use_container_width=True, hide_index=True)
