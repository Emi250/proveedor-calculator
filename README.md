# 🎬 Video Editor Tracker

Una app en Streamlit para registrar los videos que editás, calcular automáticamente el pago por cada uno y llevar un seguimiento mensual de tus ingresos en pesos argentinos.

## 🚀 Cómo usar

1. Cloná este repositorio o descargalo como ZIP.
2. Instalá las dependencias:

```
pip install -r requirements.txt
```

3. Ejecutá la app:

```
streamlit run app.py
```

Los datos se guardan automáticamente en un archivo local `video_data.pkl`.

## 🛠 Funcionalidades

- Formulario para cargar fecha, tipo de video y duración.
- Cálculo automático del pago según reglas preestablecidas.
- Pestañas por mes con resumen mensual.
- Sidebar con estadísticas del mes actual.