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
    
    # Sidebar con información
    st.sidebar.header("ℹ️ Información del Sistema")
    st.sidebar.markdown("""
    **Módulos disponibles:**
    - 📄 **Archivo Plano** - Procesamiento de caja y big pass
    - 🔜 Más módulos próximamente...
    
    **Archivos requeridos:**
    - 📁 **CAJA**: Archivo Excel con columna "DESCUADRES DE CAJA PARA DESCONTAR"
    - 📁 **BIG PASS**: Archivo Excel con columnas "Descontar", "Pagar", "PEOPLE", "N° Sap ", "Terminación"
    """)
    
    # Tabs principales
    tab1, tab2 = st.tabs(["📄 Generar Archivo Plano", "🏠 Inicio"])
    
    with tab1:
        generar_archivo_plano()
    
    with tab2:
        mostrar_inicio()

def mostrar_inicio():
    st.header("🏠 Bienvenido al Sistema de Liquidaciones")
    
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
        
        # Información de acceso directo
        st.info("👆 La funcionalidad principal está en la pestaña 'Generar Archivo Plano'")
    
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
    st.markdown("""
    Este módulo procesa los archivos de **CAJA** y **BIG PASS** para generar el archivo plano de liquidaciones.
    
    **📋 Columnas requeridas en los archivos:**
    
    **ARCHIVO CAJA:**
    - `SAP` - Número SAP del empleado
    - `Fecha Terminación. (Digite)` - Fecha de terminación
    - `DESCUADRES DE CAJA PARA DESCONTAR` - Valores a procesar
    
    **ARCHIVO BIG PASS:**
    - `N° Sap ` - Número SAP del empleado  
    - `Terminación` - Fecha de terminación
    - `Descontar` - Valores a descontar (concepto Z609)
    - `Pagar` - Valores a pagar (concepto Y602)
    - `PEOPLE` - Valores people (concepto Y608)
    """)
    
    # Upload de archivos
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📁 Archivo CAJA")
        archivo_caja = st.file_uploader(
            "Selecciona el archivo de caja (Excel)",
            type=['xlsx', 'xls'],
            key="caja",
            help="Archivo que contiene los descuadres de caja para procesar"
        )
        
        if archivo_caja:
            st.success(f"✅ Archivo cargado: {archivo_caja.name}")
            st.info(f"📊 Tamaño: {archivo_caja.size:,} bytes")
    
    with col2:
        st.subheader("📁 Archivo BIG PASS")
        archivo_big_pass = st.file_uploader(
            "Selecciona el archivo de big pass (Excel)",
            type=['xlsx', 'xls'],
            key="big_pass",
            help="Archivo que contiene datos de descontar, pagar y people"
        )
        
        if archivo_big_pass:
            st.success(f"✅ Archivo cargado: {archivo_big_pass.name}")
            st.info(f"📊 Tamaño: {archivo_big_pass.size:,} bytes")
    
    # Configuración adicional
    st.markdown("---")
    st.subheader("⚙️ Configuración de Procesamiento")
    
    col3, col4 = st.columns(2)
    
    with col3:
        formato_salida = st.selectbox(
            "📄 Formato de archivo de salida:",
            ["Excel (.xlsx)", "CSV (.csv)"],
            help="Selecciona el formato para el archivo de salida"
        )
        
        incluir_timestamp = st.checkbox(
            "🕒 Incluir timestamp en nombre del archivo",
            value=True,
            help="Agrega fecha y hora al nombre del archivo"
        )
    
    with col4:
        mostrar_estadisticas = st.checkbox(
            "📊 Mostrar estadísticas detalladas",
            value=True,
            help="Muestra resumen por concepto y totales"
        )
    
    # Botón de procesamiento
    st.markdown("---")
    if st.button("🚀 Procesar y Generar Archivo Plano", type="primary", use_container_width=True):
        if archivo_caja is not None and archivo_big_pass is not None:
            
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
                        
                        # Preparar archivo para descarga con hora colombiana
                        if PYTZ_AVAILABLE:
                            colombia_tz = pytz.timezone('America/Bogota')
                            timestamp = datetime.now(colombia_tz).strftime("_%Y%m%d_%H%M%S") if incluir_timestamp else ""
                        else:
                            # Fallback a hora local si pytz no está disponible
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
        
        else:
            st.error("⚠️ Por favor, sube ambos archivos (CAJA y BIG PASS) para continuar.")

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
