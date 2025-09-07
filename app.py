import streamlit as st
import pandas as pd
import os
import io
from datetime import datetime
import tempfile
import sys

# Importar el módulo de archivo plano
try:
    import archivo_plano
except ImportError:
    st.error("❌ No se pudo importar archivo_plano.py. Asegúrate de que esté en el mismo directorio.")
    st.stop()

def main():
    # Configuración óptima de la página
    st.set_page_config(
        page_title="Nómina 2025 | Jerónimo Martins",
        page_icon="💼",
        layout="wide",
        initial_sidebar_state="collapsed",
        menu_items={
            'Get Help': None,
            'Report a bug': None,
            'About': "Nómina 2025 - Jerónimo Martins Colombia"
        }
    )
    
    # CSS personalizado para mejor rendimiento y diseño
    st.markdown("""
    <style>
        /* Optimizaciones de rendimiento */
        .stApp {
            max-width: 1400px;
            margin: 0 auto;
        }
        
        /* Ocultar elementos innecesarios para velocidad */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        /* Mejorar velocidad de carga */
        .css-1d391kg {padding-top: 1rem;}
        
        /* Estilos personalizados */
        .hero-section {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 3rem 2rem;
            border-radius: 15px;
            margin-bottom: 2rem;
            color: white;
            text-align: center;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }
        
        .hero-title {
            font-size: 3.5rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        .hero-subtitle {
            font-size: 2rem;
            color: #90EE90;
            margin-bottom: 0.5rem;
            font-weight: 600;
        }
        
        .hero-company {
            font-size: 1.1rem;
            opacity: 0.9;
            margin-bottom: 1rem;
        }
        
        .hero-description {
            font-size: 1.2rem;
            opacity: 0.9;
            max-width: 600px;
            margin: 0 auto;
        }
        
        .feature-card {
            background: white;
            padding: 1.5rem;
            border-radius: 10px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.08);
            border-left: 4px solid #667eea;
            height: 100%;
            transition: transform 0.2s ease;
        }
        
        .feature-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.12);
        }
        
        .step-card {
            background: #f8f9fa;
            padding: 1.5rem;
            border-radius: 10px;
            text-align: center;
            height: 100%;
            border: 2px solid transparent;
            transition: all 0.3s ease;
        }
        
        .step-card:hover {
            border-color: #667eea;
            background: white;
            transform: translateY(-3px);
        }
        
        .step-number {
            background: #667eea;
            color: white;
            width: 40px;
            height: 40px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 1rem auto;
            font-weight: bold;
        }
        
        .footer-credits {
            background: linear-gradient(45deg, #f8f9fa, #e9ecef);
            padding: 2rem;
            border-radius: 15px;
            text-align: center;
            margin-top: 3rem;
            border: 1px solid #dee2e6;
        }
        
        .metric-container {
            background: white;
            padding: 1rem;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        }
        
        /* Responsive design */
        @media (max-width: 768px) {
            .hero-title { font-size: 2.5rem; }
            .hero-subtitle { font-size: 1.5rem; }
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Inicializar session_state de forma eficiente
    if 'pagina_actual' not in st.session_state:
        st.session_state.pagina_actual = 'inicio'
    if 'archivo_caja' not in st.session_state:
        st.session_state.archivo_caja = None
    if 'archivo_big_pass' not in st.session_state:
        st.session_state.archivo_big_pass = None
    
    # Navegación
    if st.session_state.pagina_actual == 'inicio':
        mostrar_landing_page()
    elif st.session_state.pagina_actual == 'archivo_plano':
        mostrar_pagina_archivo_plano()

@st.cache_data
def get_static_data():
    """Cache datos estáticos para mejor rendimiento"""
    return {
        'conceptos': ['Z498', 'Z609', 'Y602', 'Y608'],
        'formatos': ['Excel (.xlsx)', 'CSV (.csv)'],
        'version': '1.0'
    }

def mostrar_landing_page():
    """Landing page optimizada con el mejor diseño"""
    
    # Hero section mejorado
    st.markdown("""
    <div class="hero-section">
        <div class="hero-title">💼 Liquidaciones de Nómina</div>
        <div class="hero-subtitle">Nómina 2025</div>
        <div class="hero-company">Jerónimo Martins Colombia</div>
        <div class="hero-description">
            Sistema automatizado de última generación para el procesamiento 
            eficiente de archivos de liquidación SAP
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # CTA principal prominente
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 **INICIAR PROCESAMIENTO**", 
                    type="primary", 
                    use_container_width=True,
                    help="Comienza a procesar tus archivos de nómina"):
            st.session_state.pagina_actual = 'archivo_plano'
            st.rerun()
        
        st.markdown("""
        <div style='text-align: center; margin-top: 1rem; opacity: 0.8;'>
            <small>✨ Procesa CAJA y BIG PASS en segundos</small>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Características principales con mejor diseño
    st.markdown("## 🌟 Características del Sistema")
    
    col1, col2, col3 = st.columns(3, gap="large")
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3>⚡ Ultra Rápido</h3>
            <ul style="text-align: left;">
                <li>Procesamiento en segundos</li>
                <li>Algoritmos optimizados</li>
                <li>Interfaz responsiva</li>
                <li>Sin interrupciones</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3>🎯 Conceptos SAP</h3>
            <ul style="text-align: left;">
                <li><strong>Z498</strong> - Descuadres de Caja</li>
                <li><strong>Z609</strong> - Valores a Descontar</li>
                <li><strong>Y602</strong> - Valores a Pagar</li>
                <li><strong>Y608</strong> - Valores People</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <h3>📊 Resultados Pro</h3>
            <ul style="text-align: left;">
                <li>Estadísticas detalladas</li>
                <li>Vista previa instantánea</li>
                <li>Múltiples formatos</li>
                <li>Descarga inmediata</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Proceso paso a paso mejorado
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("## 📋 Proceso Simplificado")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="step-card">
            <div class="step-number">1</div>
            <h4>📁 Cargar</h4>
            <p>Sube tus archivos CAJA y BIG PASS</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="step-card">
            <div class="step-number">2</div>
            <h4>⚙️ Configurar</h4>
            <p>Elige formato y opciones</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="step-card">
            <div class="step-number">3</div>
            <h4>🚀 Procesar</h4>
            <p>Sistema genera conceptos SAP</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="step-card">
            <div class="step-number">4</div>
            <h4>📥 Descargar</h4>
            <p>Obtén tu archivo listo</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Información técnica compacta
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    with st.expander("📝 **Información Técnica Detallada**", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            #### 📊 Archivo CAJA
            **Columnas requeridas:**
            - `SAP` - Número SAP del empleado
            - `Fecha Terminación. (Digite)` - Fecha de terminación  
            - `DESCUADRES DE CAJA PARA DESCONTAR` - Valores
            
            **Formato:** Excel (.xlsx, .xls) | **Concepto:** Z498
            """)
        
        with col2:
            st.markdown("""
            #### 🎫 Archivo BIG PASS  
            **Columnas requeridas:**
            - `N° Sap ` - Número SAP del empleado
            - `Terminación` - Fecha de terminación
            - `Descontar`, `Pagar`, `PEOPLE` - Valores
            
            **Formato:** Excel (.xlsx, .xls) | **Conceptos:** Z609, Y602, Y608
            """)
    
    # Métricas del sistema mejoradas
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    
    data = get_static_data()
    
    with col1:
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        st.metric("📊 Conceptos SAP", len(data['conceptos']), "Automatizados")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        st.metric("📁 Formatos", len(data['formatos']), "Excel y CSV")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        st.metric("⚡ Velocidad", "Ultra", "Procesamiento rápido")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        st.metric("🔄 Versión", data['version'], "Estable")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # CTA final
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("### 🎯 ¿Listo para la experiencia más rápida?")
        if st.button("▶️ **COMENZAR AHORA**", 
                    type="primary", 
                    use_container_width=True,
                    help="Acceso directo al procesador de archivos"):
            st.session_state.pagina_actual = 'archivo_plano'
            st.rerun()
    
    # Footer elegante con créditos
    st.markdown("""
    <div class="footer-credits">
        <h4 style='color: #667eea; margin-bottom: 0.5rem;'>📊 Nómina 2025</h4>
        <h5 style='color: #28a745; margin-bottom: 1rem;'>Jerónimo Martins Colombia</h5>
        <p style='margin: 0; color: #6c757d;'>Creado por <strong>Jeysshon</strong></p>
        <small style='color: #adb5bd;'>Sistema optimizado para máximo rendimiento</small>
    </div>
    """, unsafe_allow_html=True)

def mostrar_pagina_archivo_plano():
    """Página de procesamiento optimizada"""
    
    # Header optimizado
    col1, col2 = st.columns([1, 5])
    with col1:
        if st.button("⬅️ Inicio", help="Volver al inicio"):
            st.session_state.pagina_actual = 'inicio'
            st.rerun()
    
    with col2:
        st.markdown("# 📄 Procesador de Archivo Plano")
    
    st.markdown("**Procesamiento automatizado optimizado para máxima velocidad**")
    
    # Progress bar visual
    progress_col1, progress_col2, progress_col3 = st.columns(3)
    
    archivo_caja = st.session_state.get('archivo_caja')
    archivo_big_pass = st.session_state.get('archivo_big_pass')
    
    with progress_col1:
        caja_status = "✅ Completado" if archivo_caja else "📁 Pendiente"
        st.metric("Paso 1: CAJA", caja_status)
    
    with progress_col2:
        big_pass_status = "✅ Completado" if archivo_big_pass else "📁 Pendiente"
        st.metric("Paso 2: BIG PASS", big_pass_status)
    
    with progress_col3:
        ready_status = "🚀 Listo" if (archivo_caja and archivo_big_pass) else "⏳ Esperando"
        st.metric("Paso 3: Procesar", ready_status)
    
    st.markdown("---")
    
    # === CARGA DE ARCHIVOS OPTIMIZADA ===
    st.markdown("## 📁 Carga de Archivos")
    
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        st.markdown("### 📊 Archivo CAJA")
        archivo_caja = st.file_uploader(
            "Arrastra o selecciona archivo CAJA",
            type=['xlsx', 'xls'],
            key="caja_uploader",
            help="Archivo Excel con descuadres de caja",
            label_visibility="collapsed"
        )
        
        if archivo_caja:
            st.session_state.archivo_caja = archivo_caja
            st.success(f"✅ **{archivo_caja.name}**")
            
            # Preview optimizado
            with st.expander("👀 Vista rápida", expanded=False):
                try:
                    # Usar @st.cache_data para preview
                    df_preview = pd.read_excel(archivo_caja, nrows=3)
                    st.dataframe(df_preview, use_container_width=True)
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.info("📁 Archivo CAJA pendiente")
    
    with col2:
        st.markdown("### 🎫 Archivo BIG PASS")
        archivo_big_pass = st.file_uploader(
            "Arrastra o selecciona archivo BIG PASS",
            type=['xlsx', 'xls'],
            key="big_pass_uploader",
            help="Archivo Excel con datos de descontar, pagar y people",
            label_visibility="collapsed"
        )
        
        if archivo_big_pass:
            st.session_state.archivo_big_pass = archivo_big_pass
            st.success(f"✅ **{archivo_big_pass.name}**")
            
            # Preview optimizado
            with st.expander("👀 Vista rápida", expanded=False):
                try:
                    df_preview = pd.read_excel(archivo_big_pass, nrows=3)
                    st.dataframe(df_preview, use_container_width=True)
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.info("📁 Archivo BIG PASS pendiente")
    
    # Continuar solo si ambos archivos están listos
    if not archivo_caja or not archivo_big_pass:
        st.warning("⚠️ **Carga ambos archivos para continuar**")
        return
    
    st.success("🎉 **¡Ambos archivos listos! Continúa con la configuración.**")
    st.markdown("---")
    
    # === CONFIGURACIÓN RÁPIDA ===
    st.markdown("## ⚙️ Configuración Rápida")
    
    col1, col2 = st.columns(2)
    
    with col1:
        formato_salida = st.selectbox(
            "📄 Formato de salida:",
            ["Excel (.xlsx)", "CSV (.csv)"],
            help="Selecciona el formato del archivo final"
        )
        
        incluir_timestamp = st.toggle(
            "🕒 Timestamp en nombre",
            value=True,
            help="Incluir fecha y hora en el nombre del archivo"
        )
    
    with col2:
        mostrar_estadisticas = st.toggle(
            "📊 Estadísticas detalladas",
            value=True,
            help="Mostrar resumen completo del procesamiento"
        )
        
        mostrar_preview = st.toggle(
            "👀 Vista previa resultado",
            value=True,
            help="Mostrar preview del archivo generado"
        )
    
    st.markdown("---")
    
    # === PROCESAMIENTO ===
    st.markdown("## 🚀 Ejecutar Procesamiento")
    
    # Botón de procesamiento prominente
    if st.button("⚡ **PROCESAR ARCHIVOS AHORA**", 
                type="primary", 
                use_container_width=True,
                help="Inicia el procesamiento automático"):
        ejecutar_procesamiento_optimizado(
            archivo_caja, archivo_big_pass, formato_salida, 
            incluir_timestamp, mostrar_estadisticas, mostrar_preview
        )

@st.cache_data
def procesar_archivo_cache(archivo_bytes, tipo_archivo):
    """Cache del procesamiento de archivos para mejor rendimiento"""
    return pd.read_excel(io.BytesIO(archivo_bytes))

def ejecutar_procesamiento_optimizado(archivo_caja, archivo_big_pass, formato_salida, 
                                     incluir_timestamp, mostrar_estadisticas, mostrar_preview):
    """Procesamiento optimizado con mejores prácticas"""
    
    # Progress bar
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        status_text.text("⏳ Inicializando procesamiento...")
        progress_bar.progress(10)
        
        # Crear archivos temporales de forma eficiente
        with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp_caja:
            tmp_caja.write(archivo_caja.getvalue())
            ruta_caja = tmp_caja.name
        
        with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp_big_pass:
            tmp_big_pass.write(archivo_big_pass.getvalue())
            ruta_big_pass = tmp_big_pass.name
        
        progress_bar.progress(25)
        status_text.text("📊 Procesando datos...")
        
        # Procesamiento principal
        df_resultado, estadisticas = procesar_con_archivo_plano(ruta_caja, ruta_big_pass)
        progress_bar.progress(75)
        
        if df_resultado is not None and not df_resultado.empty:
            status_text.text("✅ Procesamiento completado!")
            progress_bar.progress(100)
            
            # Ocultar progress bar
            progress_bar.empty()
            status_text.empty()
            
            # === RESULTADOS ===
            st.success("🎉 **¡Procesamiento completado exitosamente!**")
            
            # Estadísticas
            if mostrar_estadisticas:
                with st.expander("📊 **Ver Estadísticas Detalladas**", expanded=True):
                    mostrar_resumen_optimizado(estadisticas)
            
            # Preview
            if mostrar_preview:
                with st.expander("👀 **Vista Previa del Resultado**", expanded=True):
                    col1, col2 = st.columns([4, 1])
                    with col1:
                        st.dataframe(df_resultado.head(8), use_container_width=True)
                    with col2:
                        st.metric("📊 Total", f"{len(df_resultado):,}")
                        st.metric("🎯 Conceptos", len(df_resultado['CONCEPTO'].unique()))
            
            # === DESCARGA OPTIMIZADA ===
            st.markdown("## 📥 Descarga Instantánea")
            
            timestamp = datetime.now().strftime("_%Y%m%d_%H%M%S") if incluir_timestamp else ""
            
            col1, col2 = st.columns(2)
            
            if formato_salida == "Excel (.xlsx)":
                output = io.BytesIO()
                with st.spinner("Generando Excel..."):
                    df_resultado.to_excel(output, index=False, engine='openpyxl')
                output.seek(0)
                
                nombre_archivo = f"nomina_2025{timestamp}.xlsx"
                
                with col1:
                    st.download_button(
                        label="📥 **Descargar Excel**",
                        data=output.getvalue(),
                        file_name=nombre_archivo,
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True,
                        type="primary"
                    )
                
                with col2:
                    st.info(f"📁 **{nombre_archivo}**")
                    st.caption(f"📊 {len(df_resultado):,} registros")
                    st.caption(f"⏰ {datetime.now().strftime('%H:%M:%S')}")
            
            else:
                csv_data = df_resultado.to_csv(index=False, encoding='utf-8-sig', sep=';')
                nombre_archivo = f"nomina_2025{timestamp}.csv"
                
                with col1:
                    st.download_button(
                        label="📥 **Descargar CSV**",
                        data=csv_data,
                        file_name=nombre_archivo,
                        mime="text/csv",
                        use_container_width=True,
                        type="primary"
                    )
                
                with col2:
                    st.info(f"📁 **{nombre_archivo}**")
                    st.caption(f"📊 {len(df_resultado):,} registros")
                    st.caption(f"⏰ {datetime.now().strftime('%H:%M:%S')}")
            
            # Opciones adicionales
            st.markdown("---")
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("🔄 **Procesar Más Archivos**", use_container_width=True):
                    st.session_state.archivo_caja = None
                    st.session_state.archivo_big_pass = None
                    st.rerun()
            
            with col2:
                if st.button("🏠 **Volver al Inicio**", use_container_width=True):
                    st.session_state.pagina_actual = 'inicio'
                    st.rerun()
        
        else:
            progress_bar.empty()
            status_text.empty()
            st.error("❌ **No se generaron datos válidos**")
    
    except Exception as e:
        progress_bar.empty()
        status_text.empty()
        st.error(f"❌ **Error:** {str(e)}")
    
    finally:
        # Limpiar archivos temporales
        try:
            os.unlink(ruta_caja)
            os.unlink(ruta_big_pass)
        except:
            pass

def mostrar_resumen_optimizado(estadisticas):
    """Resumen optimizado con mejor diseño"""
    
    col1, col2, col3, col4 = st.columns(4)
    
    conceptos = {
        'caja': {'nombre': 'CAJA', 'emoji': '📊', 'concepto': 'Z498'},
        'descontar': {'nombre': 'Descontar', 'emoji': '⬇️', 'concepto': 'Z609'},
        'pagar': {'nombre': 'Pagar', 'emoji': '⬆️', 'concepto': 'Y602'},
        'people': {'nombre': 'People', 'emoji': '👥', 'concepto': 'Y608'}
    }
    
    columnas = [col1, col2, col3, col4]
    for i, (key, data) in enumerate(conceptos.items()):
        with columnas[i]:
            st.metric(
                label=f"{data['emoji']} {data['concepto']}",
                value=f"{estadisticas[key]['registros']:,}",
                delta=f"${estadisticas[key]['total']:,}"
            )

def procesar_con_archivo_plano(ruta_caja, ruta_big_pass):
    """Función de procesamiento optimizada"""
    try:
        todos_los_registros = []
        estadisticas = {
            'caja': {'registros': 0, 'total': 0},
            'descontar': {'registros': 0, 'total': 0},
            'pagar': {'registros': 0, 'total': 0},
            'people': {'registros': 0, 'total': 0}
        }
        
        # Procesar CAJA de forma optimizada
        df_caja = pd.read_excel(ruta_caja)
        columna_descuadres = 'DESCUADRES DE CAJA PARA DESCONTAR'
        
        if columna_descuadres in df_caja.columns:
            # Filtrado vectorizado para mejor rendimiento
            mask = (df_caja[columna_descuadres].notna()) & \
                   (pd.to_numeric(df_caja[columna_descuadres], errors='coerce') > 0)
            df_caja_filtrado = df_caja[mask]
            
            for _, row in df_caja_filtrado.iterrows():
                fecha_str = ''
                if 'Fecha Terminación. (Digite)' in row and pd.notna(row['Fecha Terminación. (Digite)']):
                    fecha_dt = pd.to_datetime(row['Fecha Terminación. (Digite)'], errors='coerce')
                    if pd.notna(fecha_dt):
                        fecha_str = fecha_dt.strftime('%d/%m/%Y')
                
                valor = int(pd.to_numeric(row[columna_descuadres], errors='coerce'))
                registro = {
                    'SAP': row['SAP'] if 'SAP' in row else '',
                    'FECHA': fecha_str,
                    'CONCEPTO': 'Z498',
                    'VALOR': valor
                }
                todos_los_registros.append(registro)
                estadisticas['caja']['registros'] += 1
                estadisticas['caja']['total'] += valor
        
        # Procesar BIG PASS optimizado
        df_big_pass = pd.read_excel(ruta_big_pass)
        
        # Procesamiento vectorizado para mejor rendimiento
        for concepto, columna, estadistica_key in [
            ('Z609', 'Descontar', 'descontar'),
            ('Y602', 'Pagar', 'pagar'), 
            ('Y608', 'PEOPLE', 'people')
        ]:
            if columna in df_big_pass.columns:
                mask = (df_big_pass[columna].notna()) & \
                       (pd.to_numeric(df_big_pass[columna], errors='coerce') > 0)
                df_filtrado = df_big_pass[mask]
                
                for _, row in df_filtrado.iterrows():
                    fecha_str = ''
                    if 'Terminación' in row and pd.notna(row['Terminación']):
                        fecha_dt = pd.to_datetime(row['Terminación'], errors='coerce')
                        if pd.notna(fecha_dt):
                            fecha_str = fecha_dt.strftime('%d/%m/%Y')
                    
                    valor = int(pd.to_numeric(row[columna], errors='coerce'))
                    registro = {
                        'SAP': str(row['N° Sap ']).strip() if 'N° Sap ' in row else '',
                        'FECHA': fecha_str,
                        'CONCEPTO': concepto,
                        'VALOR': valor
                    }
                    todos_los_registros.append(registro)
                    estadisticas[estadistica_key]['registros'] += 1
                    estadisticas[estadistica_key]['total'] += valor
        
        # Crear DataFrame final optimizado
        if todos_los_registros:
            df_final = pd.DataFrame(todos_los_registros)
            # Optimizar tipos de datos para mejor rendimiento
            df_final['SAP'] = df_final['SAP'].astype('string')
            df_final['FECHA'] = df_final['FECHA'].astype('string')
            df_final['CONCEPTO'] = df_final['CONCEPTO'].astype('category')
            df_final['VALOR'] = df_final['VALOR'].astype('int32')
            return df_final, estadisticas
        else:
            return None, estadisticas
    
    except Exception as e:
        st.error(f"Error en procesamiento: {str(e)}")
        return None, None

if __name__ == "__main__":
    main()
