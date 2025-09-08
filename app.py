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
    # Configuración de la página
    st.set_page_config(
        page_title="Nómina 2025 | Jerónimo Martins",
        page_icon="💼",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # CSS mínimo y limpio
    st.markdown("""
    <style>
        .stApp {
            max-width: 1200px;
            margin: 0 auto;
        }
        
        /* Ocultar elementos innecesarios */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        /* Hero section simple */
        .hero-container {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 3rem 2rem;
            border-radius: 15px;
            margin-bottom: 2rem;
            color: white;
            text-align: center;
        }
        
        .hero-title {
            font-size: 3rem;
            margin-bottom: 0.5rem;
            font-weight: bold;
        }
        
        .hero-subtitle {
            font-size: 1.8rem;
            color: #90EE90;
            margin-bottom: 0.5rem;
        }
        
        @media (max-width: 768px) {
            .hero-title { font-size: 2rem; }
            .hero-subtitle { font-size: 1.2rem; }
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Inicializar session_state
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

def mostrar_landing_page():
    """Landing page limpia y funcional"""
    
    # Hero section
    st.markdown("""
    <div class="hero-container">
        <div class="hero-title">💼 Liquidaciones de Nómina</div>
        <div class="hero-subtitle">Nómina 2025</div>
        <div style="font-size: 1.1rem; margin-bottom: 1rem;">Jerónimo Martins Colombia</div>
        <div style="font-size: 1.2rem;">Sistema automatizado para el procesamiento de archivos de liquidación SAP</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Botón principal
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 **INICIAR PROCESAMIENTO**", type="primary", use_container_width=True):
            st.session_state.pagina_actual = 'archivo_plano'
            st.rerun()
        
        st.markdown("""
        <div style='text-align: center; margin-top: 1rem;'>
            <small>✨ Procesa CAJA y BIG PASS en segundos</small>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Características principales
    st.markdown("## 🌟 Características del Sistema")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        ### ⚡ Ultra Rápido
        - Procesamiento en segundos
        - Algoritmos optimizados  
        - Interfaz responsiva
        - Sin interrupciones
        """)
    
    with col2:
        st.markdown("""
        ### 🎯 Conceptos SAP
        - **Z498** - Descuadres de Caja
        - **Z609** - Valores a Descontar
        - **Y602** - Valores a Pagar
        - **Y608** - Valores People
        """)
    
    with col3:
        st.markdown("""
        ### 📊 Resultados Pro
        - Estadísticas detalladas
        - Vista previa instantánea
        - Múltiples formatos
        - Descarga inmediata
        """)
    
    st.markdown("---")
    
    # Proceso paso a paso
    st.markdown("## 📋 Proceso Simplificado")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        #### 1️⃣ Cargar
        📁 Sube tus archivos CAJA y BIG PASS
        """)
    
    with col2:
        st.markdown("""
        #### 2️⃣ Configurar  
        ⚙️ Elige formato y opciones
        """)
    
    with col3:
        st.markdown("""
        #### 3️⃣ Procesar
        🚀 Sistema genera conceptos SAP
        """)
    
    with col4:
        st.markdown("""
        #### 4️⃣ Descargar
        📥 Obtén tu archivo listo
        """)
    
    st.markdown("---")
    
    # Información técnica
    with st.expander("📝 **Información Técnica Detallada**"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **📊 Archivo CAJA**
            
            Columnas requeridas:
            - `SAP` - Número SAP del empleado
            - `Fecha Terminación. (Digite)` - Fecha de terminación  
            - `DESCUADRES DE CAJA PARA DESCONTAR` - Valores
            
            Formato: Excel (.xlsx, .xls)  
            Concepto generado: Z498
            """)
        
        with col2:
            st.markdown("""
            **🎫 Archivo BIG PASS**
            
            Columnas requeridas:
            - `N° Sap ` - Número SAP del empleado
            - `Terminación` - Fecha de terminación
            - `Descontar`, `Pagar`, `PEOPLE` - Valores
            
            Formato: Excel (.xlsx, .xls)  
            Conceptos generados: Z609, Y602, Y608
            """)
    
    # Métricas del sistema
    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📊 Conceptos SAP", "4", "Automatizados")
    
    with col2:
        st.metric("📁 Formatos", "2", "Excel y CSV")
    
    with col3:
        st.metric("⚡ Velocidad", "Ultra", "Procesamiento rápido")
    
    with col4:
        st.metric("🔄 Versión", "1.0", "Estable")
    
    # Call to action final
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("### 🎯 ¿Listo para la experiencia más rápida?")
        if st.button("▶️ **COMENZAR AHORA**", type="primary", use_container_width=True):
            st.session_state.pagina_actual = 'archivo_plano'
            st.rerun()
    
    # Footer simple
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; padding: 2rem; border-radius: 10px; margin-top: 2rem;'>
        <h4 style='color: #667eea;'>📊 Nómina 2025</h4>
        <h5 style='color: #28a745;'>Jerónimo Martins Colombia</h5>
        <p>Creado por <strong>Jeysshon</strong></p>
        <small>Sistema optimizado para máximo rendimiento</small>
    </div>
    """, unsafe_allow_html=True)

def mostrar_pagina_archivo_plano():
    """Página de procesamiento limpia"""
    
    # Header
    col1, col2 = st.columns([1, 5])
    with col1:
        if st.button("⬅️ Inicio"):
            st.session_state.pagina_actual = 'inicio'
            st.rerun()
    
    with col2:
        st.markdown("# 📄 Procesador de Archivo Plano")
    
    st.markdown("**Procesamiento automatizado optimizado para máxima velocidad**")
    
    # Estado de archivos
    archivo_caja = st.session_state.get('archivo_caja')
    archivo_big_pass = st.session_state.get('archivo_big_pass')
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        caja_status = "✅ Completado" if archivo_caja else "📁 Pendiente"
        st.metric("Paso 1: CAJA", caja_status)
    
    with col2:
        big_pass_status = "✅ Completado" if archivo_big_pass else "📁 Pendiente"
        st.metric("Paso 2: BIG PASS", big_pass_status)
    
    with col3:
        ready_status = "🚀 Listo" if (archivo_caja and archivo_big_pass) else "⏳ Esperando"
        st.metric("Paso 3: Procesar", ready_status)
    
    st.markdown("---")
    
    # Carga de archivos
    st.markdown("## 📁 Carga de Archivos")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 Archivo CAJA")
        archivo_caja = st.file_uploader(
            "Selecciona archivo CAJA",
            type=['xlsx', 'xls'],
            key="caja_uploader",
            help="Archivo Excel con descuadres de caja"
        )
        
        if archivo_caja:
            st.session_state.archivo_caja = archivo_caja
            st.success(f"✅ **{archivo_caja.name}**")
            st.caption(f"📏 Tamaño: {archivo_caja.size:,} bytes")
            
            with st.expander("👀 Vista previa"):
                try:
                    df_preview = pd.read_excel(archivo_caja, nrows=3)
                    st.dataframe(df_preview, use_container_width=True)
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.info("📁 Archivo CAJA pendiente")
    
    with col2:
        st.markdown("### 🎫 Archivo BIG PASS")
        archivo_big_pass = st.file_uploader(
            "Selecciona archivo BIG PASS",
            type=['xlsx', 'xls'],
            key="big_pass_uploader",
            help="Archivo Excel con datos de descontar, pagar y people"
        )
        
        if archivo_big_pass:
            st.session_state.archivo_big_pass = archivo_big_pass
            st.success(f"✅ **{archivo_big_pass.name}**")
            st.caption(f"📏 Tamaño: {archivo_big_pass.size:,} bytes")
            
            with st.expander("👀 Vista previa"):
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
    
    # Configuración
    st.markdown("## ⚙️ Configuración")
    
    col1, col2 = st.columns(2)
    
    with col1:
        formato_salida = st.selectbox(
            "📄 Formato de salida:",
            ["Excel (.xlsx)", "CSV (.csv)"]
        )
        
        incluir_timestamp = st.checkbox(
            "🕒 Timestamp en nombre",
            value=True
        )
    
    with col2:
        mostrar_estadisticas = st.checkbox(
            "📊 Estadísticas detalladas",
            value=True
        )
        
        mostrar_preview = st.checkbox(
            "👀 Vista previa resultado",
            value=True
        )
    
    st.markdown("---")
    
    # Procesamiento
    st.markdown("## 🚀 Procesamiento")
    
    if st.button("⚡ **PROCESAR ARCHIVOS AHORA**", type="primary", use_container_width=True):
        ejecutar_procesamiento(archivo_caja, archivo_big_pass, formato_salida, incluir_timestamp, mostrar_estadisticas, mostrar_preview)

def ejecutar_procesamiento(archivo_caja, archivo_big_pass, formato_salida, incluir_timestamp, mostrar_estadisticas, mostrar_preview):
    """Procesamiento optimizado"""
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        status_text.text("⏳ Inicializando...")
        progress_bar.progress(10)
        
        # Crear archivos temporales
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
            status_text.text("✅ Completado!")
            progress_bar.progress(100)
            
            # Limpiar progress
            progress_bar.empty()
            status_text.empty()
            
            st.success("🎉 **¡Procesamiento completado exitosamente!**")
            
            # Estadísticas
            if mostrar_estadisticas:
                st.markdown("### 📊 Estadísticas")
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("📊 CAJA (Z498)", f"{estadisticas['caja']['registros']:,}", f"${estadisticas['caja']['total']:,}")
                
                with col2:
                    st.metric("⬇️ Descontar (Z609)", f"{estadisticas['descontar']['registros']:,}", f"${estadisticas['descontar']['total']:,}")
                
                with col3:
                    st.metric("⬆️ Pagar (Y602)", f"{estadisticas['pagar']['registros']:,}", f"${estadisticas['pagar']['total']:,}")
                
                with col4:
                    st.metric("👥 People (Y608)", f"{estadisticas['people']['registros']:,}", f"${estadisticas['people']['total']:,}")
            
            # Preview
            if mostrar_preview:
                st.markdown("### 👀 Vista Previa")
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.dataframe(df_resultado.head(8), use_container_width=True)
                with col2:
                    st.metric("📊 Total", f"{len(df_resultado):,}")
                    st.metric("🎯 Conceptos", len(df_resultado['CONCEPTO'].unique()))
            
            # Descarga
            st.markdown("### 📥 Descarga")
            
            timestamp = datetime.now().strftime("_%Y%m%d_%H%M%S") if incluir_timestamp else ""
            
            col1, col2 = st.columns(2)
            
            if formato_salida == "Excel (.xlsx)":
                output = io.BytesIO()
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

def procesar_con_archivo_plano(ruta_caja, ruta_big_pass):
    """Función de procesamiento - FORMATO DE FECHA CORREGIDO"""
    try:
        todos_los_registros = []
        estadisticas = {
            'caja': {'registros': 0, 'total': 0},
            'descontar': {'registros': 0, 'total': 0},
            'pagar': {'registros': 0, 'total': 0},
            'people': {'registros': 0, 'total': 0}
        }
        
        # Procesar CAJA
        df_caja = pd.read_excel(ruta_caja)
        columna_descuadres = 'DESCUADRES DE CAJA PARA DESCONTAR'
        
        if columna_descuadres in df_caja.columns:
            mask = (df_caja[columna_descuadres].notna()) & \
                   (pd.to_numeric(df_caja[columna_descuadres], errors='coerce') > 0)
            df_caja_filtrado = df_caja[mask]
            
            for _, row in df_caja_filtrado.iterrows():
                fecha_str = ''
                if 'Fecha Terminación. (Digite)' in row and pd.notna(row['Fecha Terminación. (Digite)']):
                    fecha_dt = pd.to_datetime(row['Fecha Terminación. (Digite)'], errors='coerce')
                    if pd.notna(fecha_dt):
                        fecha_str = fecha_dt.strftime('%d.%m.%Y')  # CAMBIADO: puntos en lugar de barras
                
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
        
        # Procesar BIG PASS
        df_big_pass = pd.read_excel(ruta_big_pass)
        
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
                            fecha_str = fecha_dt.strftime('%d.%m.%Y')  # CAMBIADO: puntos en lugar de barras
                    
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
        
        # Crear DataFrame final
        if todos_los_registros:
            df_final = pd.DataFrame(todos_los_registros)
            return df_final, estadisticas
        else:
            return None, estadisticas
    
    except Exception as e:
        st.error(f"Error en procesamiento: {str(e)}")
        return None, None

if __name__ == "__main__":
    main()
