import streamlit as st
import pandas as pd
import datetime
import os
import pickle

# -------------------------------
# Constantes de precios
# -------------------------------

PRECIOS_FIJOS = {
    "CLIP": 27500,
    "OPEN": 11000,
    "SAM": 11000,
    "Team class": 54648
}

ESCALAS_TIEMPO = [
    ("Hasta 5 minutos", 5, 8863),
    ("De 5 a 10 minutos", 10, 17727),
    ("De 11 a 15 minutos", 15, 26590),
    ("De 16 a 20 minutos", 20, 35453),
]

PRECIO_EXTRA_MINUTO = 1845

# -------------------------------
# Carga / Guardado de datos
# -------------------------------

DATA_FILE = "video_data.pkl"

def cargar_datos():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "rb") as f:
            df = pickle.load(f)
            df["Fecha"] = pd.to_datetime(df["Fecha"], errors="coerce")
            return df
    else:
df_vacio = pd.DataFrame(columns=["Fecha", "Tipo de video", "Duración (min)", "Precio"])
df_vacio["Fecha"] = pd.to_datetime(df_vacio["Fecha"])
return df_vacio

def guardar_datos(df):
    with open(DATA_FILE, "wb") as f:
        pickle.dump(df, f)

# -------------------------------
# Cálculo de precio
# -------------------------------

def calcular_precio(tipo, duracion):
    if tipo in PRECIOS_FIJOS:
        return PRECIOS_FIJOS[tipo]
    for nombre, limite, precio_base in ESCALAS_TIEMPO:
        if tipo == nombre:
            if duracion <= limite:
                return precio_base
            else:
                extra_minutos = duracion - limite
                return precio_base + extra_minutos * PRECIO_EXTRA_MINUTO
    return 0  # fallback

# -------------------------------
# Interfaz de Streamlit
# -------------------------------

st.set_page_config(page_title="Seguimiento de Edición de Videos", layout="wide")
st.title("🎬 Seguimiento de Edición de Videos")

# Advertencia sobre almacenamiento temporal
st.warning("⚠️ Esta versión de la app no guarda datos permanentemente. Al cerrar o actualizar, los datos se perderán.")

# Cargar datos
df = cargar_datos()

# Sidebar: Resumen del mes actual
hoy = datetime.date.today()
mes_actual = hoy.strftime("%Y-%m")
df_mes_actual = df[df["Fecha"].dt.strftime("%Y-%m") == mes_actual]

with st.sidebar:
    st.header("📊 Resumen del mes actual")
    st.metric("Videos editados", len(df_mes_actual))
    st.metric("Total ganado (ARS)", f"${df_mes_actual['Precio'].sum():,.0f}")

# Formulario para ingresar un nuevo video
st.subheader("➕ Agregar nuevo video editado")

with st.form("video_form"):
    col1, col2, col3 = st.columns(3)
    with col1:
        fecha = st.date_input("Fecha de edición", value=hoy)
    with col2:
        tipo = st.selectbox("Tipo de video", list(PRECIOS_FIJOS.keys()) + [x[0] for x in ESCALAS_TIEMPO])
    with col3:
        duracion = st.number_input("Duración (en minutos)", min_value=1, step=1)

    submitted = st.form_submit_button("Agregar video")

    if submitted:
        precio = calcular_precio(tipo, duracion)
        nuevo = pd.DataFrame([{
            "Fecha": pd.to_datetime(fecha),
            "Tipo de video": tipo,
            "Duración (min)": duracion,
            "Precio": precio
        }])
        df = pd.concat([df, nuevo], ignore_index=True)
        guardar_datos(df)
        st.success(f"✅ Video agregado correctamente. Pago: ${precio:,.0f} ARS")

# Agrupar por mes
if not df.empty:
    df["Mes"] = df["Fecha"].dt.strftime("%Y-%m")
    meses = sorted(df["Mes"].unique(), reverse=True)

    # Pestañas por mes
    tabs = st.tabs(meses)

    for i, mes in enumerate(meses):
        with tabs[i]:
            st.subheader(f"📅 Videos del mes: {mes}")
            df_mes = df[df["Mes"] == mes].copy()
            df_mes = df_mes.sort_values("Fecha")
            df_mes["Fecha"] = df_mes["Fecha"].dt.date  # mostrar solo la fecha

            st.dataframe(df_mes[["Fecha", "Tipo de video", "Duración (min)", "Precio"]], use_container_width=True)
            st.markdown(f"### 💰 Total mensual: ${df_mes['Precio'].sum():,.0f} ARS")
else:
    st.info("No hay videos cargados aún.")
