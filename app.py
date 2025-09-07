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
        page_title="Liquidaciones Nómina",
        page_icon="📊",
        layout="wide"
    )
    
    # Inicializar session_state
    if 'archivo_caja' not in st.session_state:
        st.session_state.archivo_caja = None
    if 'archivo_big_pass' not in st.session_state:
        st.session_state.archivo_big_pass = None
    
    # Sidebar
    configurar_sidebar()
    
    # Navegación principal
    st.title("📊 Sistema de Liquidaciones de Nómina")
    
    # Menú de navegación horizontal
    tab1, tab2 = st.tabs(["🏠 Inicio", "📄 Generar Archivo Plano"])
    
    with tab1:
        mostrar_inicio()
    
    with tab2:
        generar_archivo_plano()

def configurar_sidebar():
    """Sidebar simplificado con solo carga de archivos"""
    st.sidebar.header("📁 Cargar Archivos")
    
    # Upload de archivos
    archivo_caja = st.sidebar.file_uploader(
        "📊 Archivo CAJA",
        type=['xlsx', 'xls'],
        key="sidebar_caja",
        help="Archivo Excel con datos de caja"
    )
    
    archivo_big_pass = st.sidebar.file_uploader(
        "🎫 Archivo BIG PASS",
        type=['xlsx', 'xls'],
        key="sidebar_big_pass",
        help="Archivo Excel con datos de big pass"
    )
    
    # Actualizar session_state
    st.session_state.archivo_caja = archivo_caja
    st.session_state.archivo_big_pass = archivo_big_pass
    
    # Estado de archivos
    st.sidebar.markdown("### 📊 Estado")
    col1, col2 = st.sidebar.columns(2)
    with col1:
        caja_status = "✅" if archivo_caja else "⏳"
        st.markdown(f"**CAJA:** {caja_status}")
    with col2:
        big_pass_status = "✅" if archivo_big_pass else "⏳"
        st.markdown(f"**BIG PASS:** {big_pass_status}")
    
    if archivo_caja and archivo_big_pass:
        st.sidebar.success("✅ Listos para procesar")
    else:
        st.sidebar.info("📁 Carga ambos archivos")

def mostrar_inicio():
    """Página de inicio tipo landing page"""
    
    # Hero section
    st.markdown("""
    <div style='text-align: center; padding: 2rem 0;'>
        <h1 style='color: #1f77b4; font-size: 3rem; margin-bottom: 1rem;'>
            💼 Liquidaciones de Nómina
        </h1>
        <p style='font-size: 1.2rem; color: #666; margin-bottom: 2rem;'>
            Sistema automatizado para el procesamiento de archivos de liquidación
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Estado de archivos - prominente
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        archivo_caja = st.session_state.archivo_caja
        archivo_big_pass = st.session_state.archivo_big_pass
        
        if archivo_caja and archivo_big_pass:
            st.success("🎉 **¡Archivos listos!** Puedes procesar las liquidaciones", icon="✅")
            if st.button("🚀 **IR A GENERAR ARCHIVO PLANO**", type="primary", use_container_width=True):
                st.switch_page("📄 Generar Archivo Plano")
        elif archivo_caja or archivo_big_pass:
            st.warning("⚠️ **Falta un archivo** - Carga el archivo restante en el panel lateral", icon="📁")
        else:
            st.info("📁 **Comienza cargando los archivos** en el panel lateral", icon="👈")
    
    st.markdown("---")
    
    # Características principales
    st.markdown("## 🌟 Características del Sistema")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        ### 📊 **Procesamiento Automático**
        
        ✅ Lectura automática de archivos Excel  
        ✅ Validación de datos  
        ✅ Generación de conceptos SAP  
        ✅ Exportación en múltiples formatos  
        """)
    
    with col2:
        st.markdown("""
        ### 🎯 **Conceptos Procesados**
        
        **Z498** - Descuadres de Caja  
        **Z609** - Valores a Descontar  
        **Y602** - Valores a Pagar  
        **Y608** - Valores People  
        """)
    
    with col3:
        st.markdown("""
        ### 📈 **Resultados**
        
        📄 Archivo plano consolidado  
        📊 Estadísticas detalladas  
        💾 Descarga inmediata  
        🔍 Vista previa de resultados  
        """)
    
    # Instrucciones
    st.markdown("---")
    st.markdown("## 📋 Cómo usar el sistema")
    
    steps_col1, steps_col2 = st.columns(2)
    
    with steps_col1:
        st.markdown("""
        ### 🚀 **Pasos para generar liquidaciones:**
        
        **1.** 📁 Carga el archivo **CAJA** en el panel lateral  
        **2.** 🎫 Carga el archivo **BIG PASS** en el panel lateral  
        **3.** 📄 Ve a la pestaña **"Generar Archivo Plano"**  
        **4.** ⚙️ Configura las opciones de salida  
        **5.** 🚀 Haz clic en **"Procesar"**  
        **6.** 📥 Descarga tu archivo generado  
        """)
    
    with steps_col2:
        st.markdown("""
        ### 📝 **Columnas requeridas en archivos:**
        
        **📊 Archivo CAJA:**
        - `SAP` - Número SAP del empleado
        - `Fecha Terminación. (Digite)` - Fecha de terminación
        - `DESCUADRES DE CAJA PARA DESCONTAR` - Valores
        
        **🎫 Archivo BIG PASS:**
        - `N° Sap ` - Número SAP del empleado
        - `Terminación` - Fecha de terminación
        - `Descontar`, `Pagar`, `PEOPLE` - Valores
        """)
    
    # Footer con estadísticas
    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📊 Conceptos", "4", "SAP")
    with col2:
        st.metric("📁 Formatos", "2", "Excel/CSV")
    with col3:
        st.metric("⚡ Módulos", "1", "Activo")
    with col4:
        st.metric("🔄 Versión", "1.0", "Estable")

def generar_archivo_plano():
    """Página dedicada solo al procesamiento"""
    
    # Header
    st.markdown("# 📄 Generar Archivo Plano")
    st.markdown("Procesamiento automático de archivos CAJA y BIG PASS para liquidaciones de nómina")
    
    # Verificar archivos
    archivo_caja = st.session_state.archivo_caja
    archivo_big_pass = st.session_state.archivo_big_pass
    
    if not archivo_caja or not archivo_big_pass:
        st.error("⚠️ **Faltan archivos** - Ve al panel lateral y carga ambos archivos para continuar")
        
        missing = []
        if not archivo_caja:
            missing.append("📊 Archivo CAJA")
        if not archivo_big_pass:
            missing.append("🎫 Archivo BIG PASS")
        
        st.warning(f"**Archivos faltantes:** {', '.join(missing)}")
        return
    
    # === SECCIÓN 1: ESTADO DE ARCHIVOS ===
    st.markdown("## 📁 Archivos Cargados")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 CAJA")
        st.success(f"✅ **{archivo_caja.name}**")
        st.caption(f"📏 Tamaño: {archivo_caja.size:,} bytes")
        
        # Vista previa
        with st.expander("👀 Vista previa"):
            try:
                df_preview = pd.read_excel(archivo_caja, nrows=3)
                st.dataframe(df_preview, use_container_width=True)
                total_rows = len(pd.read_excel(archivo_caja))
                st.caption(f"📊 Total de registros: {total_rows:,}")
            except Exception as e:
                st.error(f"Error: {e}")
    
    with col2:
        st.markdown("### 🎫 BIG PASS")
        st.success(f"✅ **{archivo_big_pass.name}**")
        st.caption(f"📏 Tamaño: {archivo_big_pass.size:,} bytes")
        
        # Vista previa
        with st.expander("👀 Vista previa"):
            try:
                df_preview = pd.read_excel(archivo_big_pass, nrows=3)
                st.dataframe(df_preview, use_container_width=True)
                total_rows = len(pd.read_excel(archivo_big_pass))
                st.caption(f"📊 Total de registros: {total_rows:,}")
            except Exception as e:
                st.error(f"Error: {e}")
    
    st.markdown("---")
    
    # === SECCIÓN 2: CONFIGURACIÓN ===
    st.markdown("## ⚙️ Configuración del Procesamiento")
    
    config_col1, config_col2 = st.columns(2)
    
    with config_col1:
        st.markdown("### 📄 Formato de Salida")
        formato_salida = st.selectbox(
            "Tipo de archivo:",
            ["Excel (.xlsx)", "CSV (.csv)"],
            help="Formato del archivo a generar"
        )
        
        incluir_timestamp = st.checkbox(
            "🕒 Incluir fecha/hora en nombre",
            value=True,
            help="Agrega timestamp al nombre del archivo"
        )
    
    with config_col2:
        st.markdown("### 📊 Opciones de Reporte")
        mostrar_estadisticas = st.checkbox(
            "📈 Mostrar estadísticas detalladas",
            value=True,
            help="Incluye resumen por concepto"
        )
        
        mostrar_preview = st.checkbox(
            "👀 Vista previa del resultado",
            value=True,
            help="Muestra las primeras filas del archivo generado"
        )
    
    st.markdown("---")
    
    # === SECCIÓN 3: PROCESAMIENTO ===
    st.markdown("## 🚀 Procesamiento")
    
    # Descripción del proceso
    with st.expander("ℹ️ ¿Qué hace el procesamiento?", expanded=False):
        st.markdown("""
        **El sistema procesará automáticamente:**
        
        1. **📊 Archivo CAJA** → Genera registros con concepto **Z498** (Descuadres de caja)
        2. **🎫 Archivo BIG PASS** → Genera registros con conceptos:
           - **Z609** (Descontar)
           - **Y602** (Pagar)
           - **Y608** (People)
        3. **🔄 Consolidación** → Unifica todos los registros
        4. **📁 Exportación** → Genera archivo en el formato seleccionado
        """)
    
    # Botón principal
    st.markdown("### 🎯 Ejecutar Procesamiento")
    
    if st.button("🚀 **PROCESAR ARCHIVOS Y GENERAR PLANO**", type="primary", use_container_width=True):
        ejecutar_procesamiento(archivo_caja, archivo_big_pass, formato_salida, incluir_timestamp, mostrar_estadisticas, mostrar_preview)

def ejecutar_procesamiento(archivo_caja, archivo_big_pass, formato_salida, incluir_timestamp, mostrar_estadisticas, mostrar_preview):
    """Ejecuta el procesamiento con mejor organización visual"""
    
    # Crear archivos temporales
    with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp_caja:
        tmp_caja.write(archivo_caja.getvalue())
        ruta_caja = tmp_caja.name
    
    with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp_big_pass:
        tmp_big_pass.write(archivo_big_pass.getvalue())
        ruta_big_pass = tmp_big_pass.name
    
    try:
        with st.spinner("⏳ Procesando archivos... Por favor espera."):
            df_resultado, estadisticas = procesar_con_archivo_plano(ruta_caja, ruta_big_pass)
            
            if df_resultado is not None and not df_resultado.empty:
                
                # === RESULTADO EXITOSO ===
                st.success("🎉 **¡Procesamiento completado exitosamente!**")
                
                # Mostrar estadísticas
                if mostrar_estadisticas:
                    st.markdown("---")
                    mostrar_resumen_procesamiento(estadisticas)
                
                # Vista previa del resultado
                if mostrar_preview:
                    st.markdown("---")
                    st.markdown("## 👀 Vista Previa del Resultado")
                    
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.dataframe(df_resultado.head(10), use_container_width=True)
                    with col2:
                        st.metric("📊 Total Registros", f"{len(df_resultado):,}")
                        st.metric("📋 Conceptos", len(df_resultado['CONCEPTO'].unique()))
                    
                    if len(df_resultado) > 10:
                        st.caption(f"Mostrando primeras 10 filas de {len(df_resultado):,} registros totales")
                
                # === DESCARGA ===
                st.markdown("---")
                st.markdown("## 📥 Descargar Archivo")
                
                # Preparar archivo para descarga
                timestamp = datetime.now().strftime("_%Y%m%d_%H%M%S") if incluir_timestamp else ""
                
                download_col1, download_col2 = st.columns(2)
                
                if formato_salida == "Excel (.xlsx)":
                    output = io.BytesIO()
                    df_resultado.to_excel(output, index=False, engine='openpyxl')
                    output.seek(0)
                    
                    nombre_archivo = f"archivo_plano{timestamp}.xlsx"
                    
                    with download_col1:
                        st.download_button(
                            label="📥 **Descargar Archivo Excel**",
                            data=output.getvalue(),
                            file_name=nombre_archivo,
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                            use_container_width=True,
                            type="primary"
                        )
                    
                    with download_col2:
                        st.info(f"📁 **Archivo:** {nombre_archivo}")
                        st.caption(f"📊 {len(df_resultado):,} registros")
                
                else:
                    csv_data = df_resultado.to_csv(index=False, encoding='utf-8-sig', sep=';')
                    nombre_archivo = f"archivo_plano{timestamp}.csv"
                    
                    with download_col1:
                        st.download_button(
                            label="📥 **Descargar Archivo CSV**",
                            data=csv_data,
                            file_name=nombre_archivo,
                            mime="text/csv",
                            use_container_width=True,
                            type="primary"
                        )
                    
                    with download_col2:
                        st.info(f"📁 **Archivo:** {nombre_archivo}")
                        st.caption(f"📊 {len(df_resultado):,} registros")
            
            else:
                st.error("❌ **No se generaron datos**")
                st.warning("Verifica que los archivos contengan información válida en las columnas requeridas")
    
    except Exception as e:
        st.error(f"❌ **Error durante el procesamiento:** {str(e)}")
        
        with st.expander("🔍 Información de depuración"):
            st.markdown("**Posibles causas:**")
            st.markdown("- Formato incorrecto de archivos")
            st.markdown("- Columnas faltantes en los archivos") 
            st.markdown("- Datos corruptos o formato de fecha incorrecto")
            st.code(str(e))
    
    finally:
        # Limpiar archivos temporales
        try:
            os.unlink(ruta_caja)
            os.unlink(ruta_big_pass)
        except:
            pass

def procesar_con_archivo_plano(ruta_caja, ruta_big_pass):
    """Función de procesamiento - sin cambios en la lógica"""
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
            df_caja_filtrado = df_caja[
                (df_caja[columna_descuadres].notna()) & 
                (pd.to_numeric(df_caja[columna_descuadres], errors='coerce') > 0)
            ]
            
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
        
        # Procesar BIG PASS
        df_big_pass = pd.read_excel(ruta_big_pass)
        
        # DESCONTAR (Z609)
        if 'Descontar' in df_big_pass.columns:
            df_descontar = df_big_pass[
                (df_big_pass['Descontar'].notna()) & 
                (pd.to_numeric(df_big_pass['Descontar'], errors='coerce') > 0)
            ]
            
            for _, row in df_descontar.iterrows():
                fecha_str = ''
                if 'Terminación' in row and pd.notna(row['Terminación']):
                    fecha_dt = pd.to_datetime(row['Terminación'], errors='coerce')
                    if pd.notna(fecha_dt):
                        fecha_str = fecha_dt.strftime('%d/%m/%Y')
                
                valor = int(pd.to_numeric(row['Descontar'], errors='coerce'))
                registro = {
                    'SAP': str(row['N° Sap ']).strip() if 'N° Sap ' in row else '',
                    'FECHA': fecha_str,
                    'CONCEPTO': 'Z609',
                    'VALOR': valor
                }
                todos_los_registros.append(registro)
                estadisticas['descontar']['registros'] += 1
                estadisticas['descontar']['total'] += valor
        
        # PAGAR (Y602)
        if 'Pagar' in df_big_pass.columns:
            df_pagar = df_big_pass[
                (df_big_pass['Pagar'].notna()) & 
                (pd.to_numeric(df_big_pass['Pagar'], errors='coerce') > 0)
            ]
            
            for _, row in df_pagar.iterrows():
                fecha_str = ''
                if 'Terminación' in row and pd.notna(row['Terminación']):
                    fecha_dt = pd.to_datetime(row['Terminación'], errors='coerce')
                    if pd.notna(fecha_dt):
                        fecha_str = fecha_dt.strftime('%d/%m/%Y')
                
                valor = int(pd.to_numeric(row['Pagar'], errors='coerce'))
                registro = {
                    'SAP': str(row['N° Sap ']).strip() if 'N° Sap ' in row else '',
                    'FECHA': fecha_str,
                    'CONCEPTO': 'Y602',
                    'VALOR': valor
                }
                todos_los_registros.append(registro)
                estadisticas['pagar']['registros'] += 1
                estadisticas['pagar']['total'] += valor
        
        # PEOPLE (Y608)
        if 'PEOPLE' in df_big_pass.columns:
            df_people = df_big_pass[
                (df_big_pass['PEOPLE'].notna()) & 
                (pd.to_numeric(df_big_pass['PEOPLE'], errors='coerce') > 0)
            ]
            
            for _, row in df_people.iterrows():
                fecha_str = ''
                if 'Terminación' in row and pd.notna(row['Terminación']):
                    fecha_dt = pd.to_datetime(row['Terminación'], errors='coerce')
                    if pd.notna(fecha_dt):
                        fecha_str = fecha_dt.strftime('%d/%m/%Y')
                
                valor = int(pd.to_numeric(row['PEOPLE'], errors='coerce'))
                registro = {
                    'SAP': str(row['N° Sap ']).strip() if 'N° Sap ' in row else '',
                    'FECHA': fecha_str,
                    'CONCEPTO': 'Y608',
                    'VALOR': valor
                }
                todos_los_registros.append(registro)
                estadisticas['people']['registros'] += 1
                estadisticas['people']['total'] += valor
        
        # Crear DataFrame final
        if todos_los_registros:
            df_final = pd.DataFrame(todos_los_registros)
            return df_final, estadisticas
        else:
            return None, estadisticas
    
    except Exception as e:
        st.error(f"Error en procesamiento: {str(e)}")
        return None, None

def mostrar_resumen_procesamiento(estadisticas):
    """Resumen de estadísticas mejorado visualmente"""
    st.markdown("## 📊 Resumen del Procesamiento")
    
    # Métricas principales
    col1, col2, col3, col4 = st.columns(4)
    
    conceptos_info = {
        'caja': {'nombre': 'CAJA (Z498)', 'emoji': '📊'},
        'descontar': {'nombre': 'Descontar (Z609)', 'emoji': '⬇️'},
        'pagar': {'nombre': 'Pagar (Y602)', 'emoji': '⬆️'},
        'people': {'nombre': 'People (Y608)', 'emoji': '👥'}
    }
    
    columnas = [col1, col2, col3, col4]
    for i, (key, data) in enumerate(conceptos_info.items()):
        with columnas[i]:
            st.metric(
                label=f"{data['emoji']} {data['nombre']}",
                value=f"{estadisticas[key]['registros']:,}",
                delta=f"${estadisticas[key]['total']:,}"
            )
    
    # Tabla detallada
    st.markdown("### 📋 Detalle por Concepto")
    resumen_data = []
    total_registros = 0
    total_valor = 0
    
    for key, info in conceptos_info.items():
        registros = estadisticas[key]['registros']
        valor = estadisticas[key]['total']
        total_registros += registros
        total_valor += valor
        
        resumen_data.append({
            'Concepto': f"{info['emoji']} {info['nombre']}",
            'Registros': f"{registros:,}",
            'Valor Total': f"${valor:,}",
            'Promedio': f"${valor/registros:,.0f}" if registros > 0 else "$0"
        })
    
    # Agregar total
    resumen_data.append({
        'Concepto': '🎯 **TOTAL GENERAL**',
        'Registros': f"**{total_registros:,}**",
        'Valor Total': f"**${total_valor:,}**",
        'Promedio': f"**${total_valor/total_registros:,.0f}**" if total_registros > 0 else "**$0**"
    })
    
    df_resumen = pd.DataFrame(resumen_data)
    st.dataframe(df_resumen, use_container_width=True, hide_index=True)

if __name__ == "__main__":
    main()
