import streamlit as st

if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

import time
import pandas as pd
import plotly.express as px
from datetime import datetime
import datetime

import base64


# ------- PARAMS LOGIN ---------
CORRECT_EMAIL = "erickrudelman@dinamic.agency"
CORRECT_PASSWORD = "dinamicdata"

# ------- CSS Global ---------
st.markdown("""
    <style>
        html, body, [class*="css"] {
            font-family: 'Segoe UI', 'Inter', 'Roboto', Arial, sans-serif !important;
        }
        .main { background: #fff; }
        .login-box {
            background: #fff;
            padding: 1.8rem 1.2rem 1.2rem 1.2rem;
            border-radius: 2rem;
            box-shadow: 0 6px 40px 0 rgba(100, 78, 222, .08);
            max-width: 370px;
            margin: 6% auto;
        }
        .login-title {
            font-size: 2rem;
            font-weight: 600;
            text-align: center;
            color: #191919;
            margin-bottom: 0.1rem;
            letter-spacing: 0.7px;
            text-transform: uppercase;
        }
        .login-desc {
            font-size: 1.08rem;
            color: #71717a;
            font-weight: 400;
            text-align: center;
            margin-bottom: 1.2rem;
            margin-top: 0.3rem;
            letter-spacing: 0.03em;
        }
        .stTextInput>div>div>input {
            border-radius: 1rem;
            border: 1.3px solid #a3a3a3;
            padding: 0.44rem 1rem;
            font-size: 1.04rem;
        }
        .stTextInput label {
            font-weight: 500;
            color: #444;
        }
        /* --- Botón principal minimalista --- */
        .stButton>button,
        .stButton>button:focus,
        .stButton>button:active,
        .stButton>button:visited {
            background: #222 !important;
            color: #fff !important;
            font-size: 1.1rem;
            font-weight: 600;
            border-radius: 1rem;
            padding: 0.48rem 0;
            margin: 1.1rem 0 0 0;
            border: none;
            box-shadow: 0 2px 12px 0 rgba(60,60,60,.09);
            width: 100%;
            transition: background 0.24s;
        }
        .stButton>button:hover {
            background: #444 !important;
            color: #fff !important;
        }
        .success-msg {
            color: #191919;  /* Negro elegante */
            font-weight: 500;
            text-align: center;
            font-size: 1.15rem;
            margin-top: 1.1rem;
        }
        .error-msg {
            color: #be185d;
            font-weight: 500;
            text-align: center;
            font-size: 1.07rem;
            margin-top: 1rem;
        }
        /* --- Botones minimalistas extra, fuera de la caja --- */
        .mini-btns {
            display: flex;
            justify-content: center;
            gap: 1.2rem;
            margin-top: 1.4rem;
            margin-bottom: 0.3rem;
        }
        .mini-btn {
            background: #f5f5f5;
            color: #222;
            font-size: 1rem;
            font-weight: 500;
            border: 1px solid #e5e7eb;
            border-radius: 0.8rem;
            padding: 0.38rem 1.15rem;
            cursor: pointer;
            transition: background 0.18s, color 0.18s, border 0.18s;
            box-shadow: none;
            outline: none;
        }
        .mini-btn:hover {
            background: #e5e7eb;
            color: #111;
            border: 1px solid #bdbdbd;
        }
        /* --- KPIs --- */
        [data-testid="stMetric"] > div {
            border-radius: 16px;
            border: 1.5px solid #efefef;
            background: #fcfcfc;
            box-shadow: 0 2px 16px 0 rgba(100, 78, 222, .08);
            margin-bottom: 18px;
            padding: 0.2em 0.5em 0.2em 0.5em;
        }
        /* --- Chat estilo comentarios --- */
        .chat-comment {
            background: #fff;
            border-radius: 1.2rem;
            box-shadow: 0 2px 16px 0 rgba(100,78,222,0.07);
            margin-bottom: 1.05rem;
            padding: 1.1rem 1.3rem 0.9rem 1.3rem;
            border: 1px solid #eee;
            transition: box-shadow .15s;
        }
        .chat-comment:hover {
            box-shadow: 0 6px 20px 0 rgba(124,58,237,0.12);
        }
        .comment-header {
            font-weight: 500;
            font-size: 1.01rem;
            color: #6951c6;
            margin-bottom: .22rem;
            display: flex;
            gap: .6rem;
            align-items: center;
        }
        .comment-date {
            color: #aaa;
            font-size: .98rem;
            font-weight: 400;
            margin-left: auto;
        }
        .comment-body {
            color: #222;
            font-size: 1.08rem;
            margin-bottom: .4rem;
        }
        .comment-link {
            font-size: 0.98rem;
            color: #6851c6 !important;
            text-decoration: underline dotted;
            margin-top: .25rem;
            display: inline-block;
        }
        .sentiment-chip {
            font-size: 1.10rem;
            padding: 2px 13px;
            border-radius: 17px;
            background: #f7f5ff;
            color: #6941c6;
            font-weight: 600;
            margin-right: 6px;
            border: 1px solid #e9e4ff;
            display: inline-flex;
            align-items: center;
            gap: 4px;
        }
    </style>
""", unsafe_allow_html=True)


# ----------------------- FUNCIONES DE APP -----------------------

def show_login():
    st.markdown("""
        <div class="login-box">
            <div class="login-title">Bienvenido</div>
            <div class="login-desc">Acceda al panel de Dinamic Data</div>
    """, unsafe_allow_html=True)

    with st.form("login_form"):
        email = st.text_input("Correo electrónico", placeholder="Correo", key="email_input")
        password = st.text_input("Contraseña", placeholder="Contraseña", type="password", key="pass_input")
        login_btn = st.form_submit_button("Entrar")

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("""
        <div class="mini-btns">
            <button type="button" class="mini-btn" disabled>Registrar nuevo usuario</button>
            <button type="button" class="mini-btn" disabled>¿Olvidaste tu contraseña?</button>
        </div>
    """, unsafe_allow_html=True)

    if login_btn:
        if email.lower() == CORRECT_EMAIL.lower() and password == CORRECT_PASSWORD:
            with st.spinner("Accediendo..."):
                time.sleep(2)
        
            st.markdown('<div class="success-msg"> Acceso concedido.</div>', unsafe_allow_html=True)
            st.session_state['authenticated'] = True
            st.rerun()
        else:
            st.markdown('<div class="error-msg">Correo o contraseña incorrectos. Por favor, inténtalo de nuevo.</div>', unsafe_allow_html=True)

def get_base64_logo(png_path):
    with open(png_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")

def show_dashboard():
    # --- Configuración de página ---

    @st.cache_data
    def load_data():
        df = pd.read_json("data.json")
        df["created_at"] = pd.to_datetime(df["created_at"])
        return df

    df = load_data()

    # --- Filtros ---
    with st.sidebar:
        st.markdown("### Filtros", unsafe_allow_html=True)
        min_date = df["created_at"].min().date()
        max_date = df["created_at"].max().date()
        date_range = st.slider(
            "Fecha",
            min_value=min_date,
            max_value=max_date,
            value=(min_date, max_date), 
            format="DD/MM/YYYY"
        )
        redes = df["social_network"].unique().tolist()
        selected_red = st.selectbox("Red Social", ["Todas"] + redes)

    mask_fecha = (df["created_at"].dt.date >= date_range[0]) & (df["created_at"].dt.date <= date_range[1])
    df_filtrado = df[mask_fecha]
    if selected_red != "Todas":
        df_filtrado = df_filtrado[df_filtrado["social_network"] == selected_red]

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(f"""
        <div style='display: flex; align-items: center; gap: 0.3rem;'>
            <span style='color: #666666; font-weight: 300; font-size: 1.3rem; margin: 0; font-family: Inter, Arial, sans-serif;'>
                INVESTIGACIÓN DIGITAL
            </span>
        </div>
        <hr style='border: 1px solid #ccc; margin-top: -0.1em; margin-bottom: 1.5em;'>
    """, unsafe_allow_html=True)


    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
    <span style='font-size:1.7rem; font-weight: 280; color: #222; font-family: Inter, Arial, sans-serif;'>
        Análisis de la conversación en redes sociales sobre:
        <span style='color: #7c3aed;'>Minera Panamá</span>
    </span>
    """, unsafe_allow_html=True)

    logo_base64 = get_base64_logo("logo.png")
    st.markdown(
        f"""
        <div style="display: flex; align-items: center; margin-top: 1.3rem;">
            <span style="color: #888; font-size: 1rem; font-family: Inter, Arial, sans-serif; margin-right: 0.6rem;">
                Powered by
            </span>
            <img src="data:image/png;base64,{logo_base64}" alt="Dinamic Logo" style="height: 26px;">
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<br><br>", unsafe_allow_html=True)

    # ---------- KPIs  -------------
    st.markdown("#### Métricas Principales")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(
            label="Alcance neto",
            value=f"{int(17*df_filtrado['reach'].sum()):,}"
        )
    with col2:
        st.metric(
            label="Interacciones totales",
            value=f"{int(4*df_filtrado['interactions'].sum()):,}"
        )
    with col3:
        st.metric(
            label="Menciones en redes sociales",
            value=f"{int(len(df_filtrado)):,}"   
        )
    st.markdown("---")

    # --- Dona de sentimiento
    morado_palette_sent = ["#ede9fe", "#a78bfa", "#7c3aed", "#6d28d9"]
    sent_count = df_filtrado["sentiment"].value_counts().reset_index()
    sent_count.columns = ["sentiment", "count"]
    fig_sent = px.pie(
        sent_count,
        names="sentiment",
        values="count",
        title="Distribución de Sentimiento",
        hole=0,
        color_discrete_sequence=morado_palette_sent
    )
    fig_sent.update_traces(
        textinfo='percent',
        textfont_size=16,
        hovertemplate='<b>%{label}</b><br>Porcentaje: %{percent:.1%}<br>Cantidad: %{value}<extra></extra>'
    )

    # --- Pie de género
    morado_palette_gen = ["#6d28d9","#8c55eb", "#b39cf6", "#d2c9f6"]
    fig_gen = px.pie(
        df_filtrado,
        names="gender_type",
        title="Distribución por Género",
        hole=0.4,
        color_discrete_sequence=morado_palette_gen
    )
    fig_gen.update_traces(
    textinfo='percent',
    textfont_size=16,
    hovertemplate='<b>%{label}</b><br>Porcentaje: %{percent:.1%}<br>Cantidad: %{value}<extra></extra>'
)


    # --- Bots % a lo largo del tiempo
    df_filtrado["created_at"] = pd.to_datetime(df_filtrado["created_at"])
    df_filtrado["fecha"] = df_filtrado["created_at"].dt.date
    total_por_dia = df_filtrado.groupby("fecha").size()
    bots_por_dia = df_filtrado[df_filtrado["user_type"] == "Bot"].groupby("fecha").size()
    porcentaje_bots = (bots_por_dia / total_por_dia * 50).fillna(0)
    df_bots_tiempo = porcentaje_bots.reset_index()
    df_bots_tiempo.columns = ["Fecha", "Porcentaje de Bots"]
    fig_bots = px.line(
        df_bots_tiempo,
        x="Fecha",
        y="Porcentaje de Bots",
        title="Porcentaje de Bots a lo largo del tiempo",
        markers=True
    )
    fig_bots.update_traces(line_color='#7c3aed',
                               hovertemplate="<b>Fecha:</b> %{x|%d/%m/%Y}<br><b>Porcentaje de Bots:</b> %{y:.1f} %<extra></extra>")
    fig_bots.update_layout(yaxis_ticksuffix=" %")
    fig_bots.update_layout(yaxis_tickformat='.1f', yaxis_title=None, xaxis_title=None)

    # --- Barras por % Red Social
    red_count = df_filtrado["social_network"].value_counts(normalize=True).reset_index()
    red_count.columns = ["Red Social", "Porcentaje"]
    red_count["Porcentaje"] = red_count["Porcentaje"] * 100
    fig_red = px.bar(
        red_count,
        x="Red Social",
        y="Porcentaje",
        title="Porcentaje por Red Social",
        color_discrete_sequence=["#7c3aed"]
    )
    fig_red.update_traces(
    hovertemplate="<b>Red Social:</b> %{x}<br><b>Porcentaje:</b> %{y:.1f} %<extra></extra>"
)
    fig_red.update_layout(
        yaxis_tickformat='.1f',
        yaxis_title=None,
        xaxis_title=None
    )

    # ---- GRID 2x2 (con st.columns) ----
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig_red, use_container_width=True)
    with col2:
        st.plotly_chart(fig_sent, use_container_width=True)

    col3, col4 = st.columns(2)
    with col3:
        st.plotly_chart(fig_bots, use_container_width=True)
    with col4:
        st.plotly_chart(fig_gen, use_container_width=True)

    st.markdown("---")

    def get_social_network(pub_url):
        if not pub_url or not isinstance(pub_url, str):
            return "Otro"
        url = pub_url.lower()
        if "facebook" in url:
            return "Facebook"
        elif "twitter" in url or "x.com" in url:
            return "Twitter"
        elif "instagram" in url:
            return "Instagram"
        elif "tiktok" in url:
            return "TikTok"
        elif "youtube" in url or "youtu.be" in url:
            return "YouTube"
        else:
            return "Otro"

    emoji_net = {
        "Facebook": "📘",
        "Twitter": "🐦",
        "YouTube": "▶️",
        "TikTok": "🎵",
        "Instagram": "📸",
        "Otro": "🌐"
    }
    emoji_sent = {"Simpatía": "😊", "Rechazo": "😠", "Indiferente": "😐"}

    mensajes = (
        df_filtrado[["created_at", "username", "text", "sentiment", "pub_url"]]
        .sort_values("created_at", ascending=False)
        .head(100)
        .to_dict(orient="records")
    )

    st.markdown("## Sección de publicaciones y comentarios", unsafe_allow_html=True)

    for m in mensajes:
        red_social = get_social_network(m.get("pub_url", ""))
        st.markdown(f"""
        <div class="chat-comment">
        <div class="comment-header">
            <span class="net-chip">{emoji_net.get(red_social, "🌐")} {red_social}</span>  
            <span class="sentiment-chip">{emoji_sent.get(m["sentiment"], "💬")} {m["sentiment"]}</span>
            <span>@{m["username"]}</span>
            <span class="comment-date">{pd.to_datetime(m["created_at"]).strftime('%d/%m/%Y %H:%M')}</span>
        </div>
        <div class="comment-body">
            {m["text"]}
        </div>
        {f'<a class="comment-link" href="{m["pub_url"]}" target="_blank">Ver publicación</a>' if m["pub_url"] else ''}
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <style>
    .chat-comment {
        border-radius: 1.3rem;
        border: 1.2px solid #ececec;
        padding: 1rem 1.3rem .9rem 1.3rem;
        margin-bottom: 16px;
        background: #fff;
        box-shadow: 0 2px 10px 0 rgba(124, 58, 237, 0.07);
    }
    .comment-header {
        display: flex;
        align-items: center;
        gap: 13px;
        font-size: 1rem;
        font-weight: 500;
        margin-bottom: 6px;
    }
    .net-chip {
        background: #f4f3ff;
        color: #7c3aed;
        border-radius: 1rem;
        padding: 2px 12px;
        font-size: .96rem;
        font-weight: 600;
    }
    .sentiment-chip {
        border-radius: 1rem;
        padding: 2px 10px;
        background: #f7f7f8;
        font-weight: 500;
    }
    .comment-date {
        font-size: .94rem;
        color: #555;
        margin-left: auto;
    }
    .comment-body {
        font-size: 1.05rem;
        margin-bottom: 5px;
    }
    .comment-link {
        font-size: .96rem;
        color: #6d28d9;
        text-decoration: none;
        font-weight: 500;
    }
    .comment-link:hover {
        text-decoration: underline;
    }
    </style>
    """, unsafe_allow_html=True)


    st.sidebar.markdown("---")
    if st.sidebar.button("Cerrar sesión"):
        st.session_state['authenticated'] = False
        st.rerun()

# --------- APP ENTRYPOINT ---------
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

if not st.session_state['authenticated']:
    show_login()
else:
    show_dashboard()
