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
    
    # Título principal
    st.title("📊 Sistema de Liquidaciones de Nómina")
    st.markdown("---")
    
    # Sidebar con carga de archivos
    configurar_sidebar()
    
    # Tabs principales
    tab1, tab2 = st.tabs(["📄 Generar Archivo Plano", "🏠 Inicio"])
    
    with tab1:
        generar_archivo_plano()
    
    with tab2:
        mostrar_inicio()

def configurar_sidebar():
    """Configura el sidebar con la carga de archivos y información del sistema"""
    st.sidebar.header("📁 Cargar Archivos")
    
    # Upload de archivos en el sidebar
    archivo_caja = st.sidebar.file_uploader(
        "📊 Archivo CAJA (Excel)",
        type=['xlsx', 'xls'],
        key="sidebar_caja",
        help="Archivo que contiene descuadres de caja para descontar"
    )
    
    if archivo_caja:
        st.sidebar.success(f"✅ CAJA: {archivo_caja.name}")
        st.sidebar.caption(f"📊 Tamaño: {archivo_caja.size:,} bytes")
    
    archivo_big_pass = st.sidebar.file_uploader(
        "🎫 Archivo BIG PASS (Excel)",
        type=['xlsx', 'xls'],
        key="sidebar_big_pass",
        help="Archivo que contiene datos de descontar, pagar y people"
    )
    
    if archivo_big_pass:
        st.sidebar.success(f"✅ BIG PASS: {archivo_big_pass.name}")
        st.sidebar.caption(f"📊 Tamaño: {archivo_big_pass.size:,} bytes")
    
    # Guardar archivos en session_state para usar en otras funciones
    st.session_state.archivo_caja = archivo_caja
    st.session_state.archivo_big_pass = archivo_big_pass
    
    st.sidebar.markdown("---")
    
    # Información del sistema
    st.sidebar.header("ℹ️ Información del Sistema")
    st.sidebar.markdown("""
    **Módulos disponibles:**
    - 📄 **Archivo Plano** - Procesamiento de caja y big pass
    - 🔜 Más módulos próximamente...
    """)
    
    # Expandir información sobre columnas requeridas
    with st.sidebar.expander("📋 Columnas Requeridas", expanded=False):
        st.markdown("""
        **ARCHIVO CAJA:**
        • `SAP` - Número SAP del empleado
        • `Fecha Terminación. (Digite)` - Fecha de terminación
        • `DESCUADRES DE CAJA PARA DESCONTAR` - Valores a procesar
        
        **ARCHIVO BIG PASS:**
        • `N° Sap ` - Número SAP del empleado
        • `Terminación` - Fecha de terminación
        • `Descontar` - Valores a descontar (Z609)
        • `Pagar` - Valores a pagar (Y602)
        • `PEOPLE` - Valores people (Y608)
        """)
    
    # Estado de archivos
    st.sidebar.markdown("### 📊 Estado de Archivos")
    col1, col2 = st.sidebar.columns(2)
    with col1:
        caja_status = "✅" if archivo_caja else "⏳"
        st.markdown(f"**CAJA:** {caja_status}")
    with col2:
        big_pass_status = "✅" if archivo_big_pass else "⏳"
        st.markdown(f"**BIG PASS:** {big_pass_status}")
    
    # Botón de procesamiento prominente en sidebar
    if archivo_caja and archivo_big_pass:
        st.sidebar.markdown("---")
        if st.sidebar.button("🚀 PROCESAR ARCHIVOS", type="primary", use_container_width=True):
            st.session_state.procesar_archivos = True
        st.sidebar.success("✅ Ambos archivos cargados - Listo para procesar")
    else:
        st.sidebar.markdown("---")
        st.sidebar.warning("⚠️ Carga ambos archivos para continuar")

def mostrar_inicio():
    st.header("🏠 Bienvenido al Sistema de Liquidaciones")
    
    # Verificar estado de archivos
    archivo_caja = getattr(st.session_state, 'archivo_caja', None)
    archivo_big_pass = getattr(st.session_state, 'archivo_big_pass', None)
    
    if archivo_caja and archivo_big_pass:
        st.success("✅ Ambos archivos están cargados. Ve a la pestaña 'Generar Archivo Plano' para procesarlos.")
    elif archivo_caja or archivo_big_pass:
        st.warning("⚠️ Solo un archivo está cargado. Carga el archivo faltante en el panel lateral.")
    else:
        st.info("📁 Carga los archivos CAJA y BIG PASS en el panel lateral para comenzar.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📋 Funciones Principales")
        st.markdown("""
        ### 1. 📄 Generación de Archivo Plano
        - Procesa archivos de **CAJA** y **BIG PASS**
        - Genera conceptos: Z498, Z609, Y602, Y608
        - Exporta en formato Excel o CSV
        
        ### 2. 🔜 Próximamente
        - Validación de datos
        - Reportes avanzados
        - Más procesadores
        """)
        
        # Guía rápida
        st.info("💡 **Guía rápida:** Carga ambos archivos en el panel lateral y haz clic en 'PROCESAR ARCHIVOS'")
    
    with col2:
        st.subheader("📊 Conceptos Procesados")
        conceptos_data = {
            'Concepto': ['Z498', 'Z609', 'Y602', 'Y608'],
            'Descripción': ['CAJA - Descuadres', 'BIG PASS - Descontar', 'BIG PASS - Pagar', 'BIG PASS - People'],
            'Tipo': ['Descuento', 'Descuento', 'Pago', 'Pago'],
            'Archivo': ['CAJA', 'BIG PASS', 'BIG PASS', 'BIG PASS']
        }
        df_conceptos = pd.DataFrame(conceptos_data)
        st.dataframe(df_conceptos, use_container_width=True)
        
        # Métricas
        st.subheader("📈 Estadísticas")
        col2_1, col2_2 = st.columns(2)
        with col2_1:
            st.metric("Conceptos", "4", "Activos")
        with col2_2:
            st.metric("Módulos", "1", "Disponible")

def generar_archivo_plano():
    st.header("📄 Generación de Archivo Plano")
    
    # Obtener archivos del session_state
    archivo_caja = getattr(st.session_state, 'archivo_caja', None)
    archivo_big_pass = getattr(st.session_state, 'archivo_big_pass', None)
    
    # Verificar si se debe procesar
    procesar = getattr(st.session_state, 'procesar_archivos', False)
    if procesar:
        st.session_state.procesar_archivos = False  # Reset flag
        if archivo_caja and archivo_big_pass:
            ejecutar_procesamiento(archivo_caja, archivo_big_pass)
            return
    
    # Mostrar estado de archivos
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📁 Estado de Archivos CAJA")
        if archivo_caja:
            st.success(f"✅ Archivo cargado: {archivo_caja.name}")
            st.info(f"📊 Tamaño: {archivo_caja.size:,} bytes")
            
            # Preview del archivo
            with st.expander("👀 Vista previa CAJA"):
                try:
                    df_preview = pd.read_excel(archivo_caja, nrows=5)
                    st.dataframe(df_preview, use_container_width=True)
                    st.caption(f"Mostrando primeras 5 filas de {len(pd.read_excel(archivo_caja)):,} registros totales")
                except Exception as e:
                    st.error(f"Error al leer archivo: {e}")
        else:
            st.warning("⚠️ No hay archivo CAJA cargado")
            st.info("👈 Carga el archivo en el panel lateral")
    
    with col2:
        st.subheader("📁 Estado de Archivos BIG PASS")
        if archivo_big_pass:
            st.success(f"✅ Archivo cargado: {archivo_big_pass.name}")
            st.info(f"📊 Tamaño: {archivo_big_pass.size:,} bytes")
            
            # Preview del archivo
            with st.expander("👀 Vista previa BIG PASS"):
                try:
                    df_preview = pd.read_excel(archivo_big_pass, nrows=5)
                    st.dataframe(df_preview, use_container_width=True)
                    st.caption(f"Mostrando primeras 5 filas de {len(pd.read_excel(archivo_big_pass)):,} registros totales")
                except Exception as e:
                    st.error(f"Error al leer archivo: {e}")
        else:
            st.warning("⚠️ No hay archivo BIG PASS cargado")
            st.info("👈 Carga el archivo en el panel lateral")
    
    st.markdown("---")
    
    # Descripción del proceso
    st.subheader("📋 Descripción del Proceso")
    st.markdown("""
    Este módulo procesa los archivos de **CAJA** y **BIG PASS** para generar el archivo plano de liquidaciones.
    
    **🔄 Proceso automático:**
    1. **CAJA** → Genera registros con concepto **Z498** (Descuadres de caja)
    2. **BIG PASS** → Genera registros con conceptos:
       - **Z609** (Descontar)
       - **Y602** (Pagar) 
       - **Y608** (People)
    3. **Consolidación** → Unifica todos los registros en un archivo plano
    4. **Exportación** → Genera archivo Excel o CSV para descarga
    """)
    
    # Configuración de salida
    st.subheader("⚙️ Configuración de Salida")
    col3, col4 = st.columns(2)
    
    with col3:
        formato_salida = st.selectbox(
            "📄 Formato de archivo:",
            ["Excel (.xlsx)", "CSV (.csv)"],
            help="Selecciona el formato para el archivo de salida"
        )
        
    with col4:
        incluir_timestamp = st.checkbox(
            "🕒 Incluir timestamp en nombre",
            value=True,
            help="Agrega fecha y hora al nombre del archivo"
        )
    
    mostrar_estadisticas = st.checkbox(
        "📊 Mostrar estadísticas detalladas",
        value=True,
        help="Muestra resumen por concepto y totales"
    )
    
    # Botón principal de procesamiento
    st.markdown("---")
    if archivo_caja and archivo_big_pass:
        if st.button("🚀 Procesar y Generar Archivo Plano", type="primary", use_container_width=True):
            ejecutar_procesamiento(archivo_caja, archivo_big_pass, formato_salida, incluir_timestamp, mostrar_estadisticas)
    else:
        st.error("⚠️ Por favor, carga ambos archivos en el panel lateral para continuar.")
        if not archivo_caja:
            st.warning("📁 Falta archivo CAJA")
        if not archivo_big_pass:
            st.warning("🎫 Falta archivo BIG PASS")

def ejecutar_procesamiento(archivo_caja, archivo_big_pass, formato_salida="Excel (.xlsx)", incluir_timestamp=True, mostrar_estadisticas=True):
    """Ejecuta el procesamiento de los archivos"""
    
    # Crear archivos temporales
    with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp_caja:
        tmp_caja.write(archivo_caja.getvalue())
        ruta_caja = tmp_caja.name
    
    with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp_big_pass:
        tmp_big_pass.write(archivo_big_pass.getvalue())
        ruta_big_pass = tmp_big_pass.name
    
    try:
        with st.spinner("⏳ Procesando archivos... Por favor espera."):
            # Llamar a la función del módulo archivo_plano con rutas temporales
            df_resultado, estadisticas = procesar_con_archivo_plano(ruta_caja, ruta_big_pass)
            
            if df_resultado is not None and not df_resultado.empty:
                st.success("✅ ¡Procesamiento completado exitosamente!")
                
                # Mostrar estadísticas si está habilitado
                if mostrar_estadisticas:
                    mostrar_resumen_procesamiento(estadisticas)
                
                # Preparar archivo para descarga
                timestamp = datetime.now().strftime("_%Y%m%d_%H%M%S") if incluir_timestamp else ""
                
                if formato_salida == "Excel (.xlsx)":
                    output = io.BytesIO()
                    df_resultado.to_excel(output, index=False, engine='openpyxl')
                    output.seek(0)
                    
                    nombre_archivo = f"archivo_plano{timestamp}.xlsx"
                    
                    st.download_button(
                        label="📥 Descargar Archivo Excel",
                        data=output.getvalue(),
                        file_name=nombre_archivo,
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True
                    )
                else:
                    csv_data = df_resultado.to_csv(index=False, encoding='utf-8-sig', sep=';')
                    nombre_archivo = f"archivo_plano{timestamp}.csv"
                    
                    st.download_button(
                        label="📥 Descargar Archivo CSV",
                        data=csv_data,
                        file_name=nombre_archivo,
                        mime="text/csv",
                        use_container_width=True
                    )
                
                # Mostrar preview del resultado
                with st.expander("👀 Vista previa del archivo generado", expanded=True):
                    st.dataframe(df_resultado.head(10), use_container_width=True)
                    if len(df_resultado) > 10:
                        st.caption(f"Mostrando primeras 10 filas de {len(df_resultado):,} registros totales")
            
            else:
                st.error("❌ No se generaron datos. Verifica que los archivos contengan información válida.")
    
    except Exception as e:
        st.error(f"❌ Error durante el procesamiento: {str(e)}")
        st.markdown("**Posibles causas:**")
        st.markdown("- Formato incorrecto de archivos")
        st.markdown("- Columnas faltantes en los archivos")
        st.markdown("- Datos corruptos")
    
    finally:
        # Limpiar archivos temporales
        try:
            os.unlink(ruta_caja)
            os.unlink(ruta_big_pass)
        except:
            pass

def procesar_con_archivo_plano(ruta_caja, ruta_big_pass):
    """
    Función adaptada del código original para trabajar con Streamlit
    """
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
    st.subheader("📊 Resumen del Procesamiento")
    
    # Métricas principales
    col1, col2, col3, col4 = st.columns(4)
    
    conceptos_info = {
        'caja': {'nombre': 'CAJA (Z498)', 'color': 'red'},
        'descontar': {'nombre': 'Descontar (Z609)', 'color': 'orange'},
        'pagar': {'nombre': 'Pagar (Y602)', 'color': 'green'},
        'people': {'nombre': 'People (Y608)', 'color': 'blue'}
    }
    
    columnas = [col1, col2, col3, col4]
    for i, (key, data) in enumerate(conceptos_info.items()):
        with columnas[i]:
            st.metric(
                label=data['nombre'],
                value=f"{estadisticas[key]['registros']:,}",
                delta=f"${estadisticas[key]['total']:,}"
            )
    
    # Tabla detallada
    st.subheader("📋 Detalle por Concepto")
    resumen_data = []
    total_registros = 0
    total_valor = 0
    
    for key, info in conceptos_info.items():
        registros = estadisticas[key]['registros']
        valor = estadisticas[key]['total']
        total_registros += registros
        total_valor += valor
        
        resumen_data.append({
            'Concepto': info['nombre'],
            'Registros': f"{registros:,}",
            'Valor Total': f"${valor:,}",
            'Promedio': f"${valor/registros:,.0f}" if registros > 0 else "$0"
        })
    
    # Agregar total
    resumen_data.append({
        'Concepto': '**TOTAL**',
        'Registros': f"**{total_registros:,}**",
        'Valor Total': f"**${total_valor:,}**",
        'Promedio': f"**${total_valor/total_registros:,.0f}**" if total_registros > 0 else "**$0**"
    })
    
    df_resumen = pd.DataFrame(resumen_data)
    st.dataframe(df_resumen, use_container_width=True, hide_index=True)

if __name__ == "__main__":
    main()
