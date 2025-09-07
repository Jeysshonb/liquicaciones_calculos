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
    
    # Inicializar session_state para navegación
    if 'pagina_actual' not in st.session_state:
        st.session_state.pagina_actual = 'inicio'
    
    # Inicializar archivos
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
    """Landing page principal - sin sidebar"""
    
    # Hero section
    st.markdown("""
    <div style='text-align: center; padding: 3rem 0;'>
        <h1 style='color: #1f77b4; font-size: 4rem; margin-bottom: 1rem;'>
            💼 Liquidaciones de Nómina
        </h1>
        <p style='font-size: 1.4rem; color: #666; margin-bottom: 3rem;'>
            Sistema automatizado para el procesamiento de archivos de liquidación SAP
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Botón principal prominente
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 **GENERAR ARCHIVO PLANO**", type="primary", use_container_width=True):
            st.session_state.pagina_actual = 'archivo_plano'
            st.rerun()
        
        st.markdown("<div style='text-align: center; margin-top: 1rem;'>", unsafe_allow_html=True)
        st.caption("Procesa tus archivos CAJA y BIG PASS automáticamente")
        st.markdown("</div>", unsafe_allow_html=True)
    
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
    
    # Información técnica
    st.markdown("---")
    st.markdown("## 📝 Información Técnica")
    
    info_col1, info_col2 = st.columns(2)
    
    with info_col1:
        st.markdown("""
        ### 📊 **Archivo CAJA** (Requerido)
        
        **Columnas necesarias:**
        - `SAP` - Número SAP del empleado
        - `Fecha Terminación. (Digite)` - Fecha de terminación
        - `DESCUADRES DE CAJA PARA DESCONTAR` - Valores a procesar
        
        **Formato:** Excel (.xlsx, .xls)  
        **Concepto generado:** Z498
        """)
    
    with info_col2:
        st.markdown("""
        ### 🎫 **Archivo BIG PASS** (Requerido)
        
        **Columnas necesarias:**
        - `N° Sap ` - Número SAP del empleado
        - `Terminación` - Fecha de terminación
        - `Descontar`, `Pagar`, `PEOPLE` - Valores correspondientes
        
        **Formato:** Excel (.xlsx, .xls)  
        **Conceptos generados:** Z609, Y602, Y608
        """)
    
    # Footer con estadísticas
    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📊 Conceptos SAP", "4", "Z498, Z609, Y602, Y608")
    with col2:
        st.metric("📁 Formatos Salida", "2", "Excel y CSV")
    with col3:
        st.metric("⚡ Velocidad", "Rápido", "Procesamiento automático")
    with col4:
        st.metric("🔄 Versión", "1.0", "Nómina 2025")
    
    # Call to action final
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("### 🎯 ¿Listo para comenzar?")
        if st.button("▶️ **COMENZAR PROCESAMIENTO**", type="primary", use_container_width=True):
            st.session_state.pagina_actual = 'archivo_plano'
            st.rerun()
    
    # Footer con créditos
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; padding: 2rem 0; color: #666; background-color: #f8f9fa; border-radius: 10px; margin-top: 2rem;'>
        <h4 style='color: #1f77b4; margin-bottom: 0.5rem;'>📊 Nómina 2025</h4>
        <p style='margin: 0; font-size: 0.9rem;'>Creado por <strong>Jeysshon</strong></p>
    </div>
    """, unsafe_allow_html=True)

def mostrar_pagina_archivo_plano():
    """Página dedicada al procesamiento de archivos"""
    
    # Header con navegación
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("⬅️ Volver al Inicio"):
            st.session_state.pagina_actual = 'inicio'
            st.rerun()
    
    with col2:
        st.markdown("# 📄 Generar Archivo Plano")
    
    st.markdown("Procesamiento automático de archivos CAJA y BIG PASS para liquidaciones de nómina")
    st.markdown("---")
    
    # === SECCIÓN 1: CARGA DE ARCHIVOS ===
    st.markdown("## 📁 Paso 1: Cargar Archivos")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 Archivo CAJA")
        archivo_caja = st.file_uploader(
            "Selecciona el archivo CAJA (Excel)",
            type=['xlsx', 'xls'],
            key="caja_uploader",
            help="Archivo que contiene descuadres de caja"
        )
        
        if archivo_caja:
            st.session_state.archivo_caja = archivo_caja
            st.success(f"✅ **{archivo_caja.name}**")
            st.caption(f"📏 Tamaño: {archivo_caja.size:,} bytes")
            
            # Vista previa
            with st.expander("👀 Vista previa CAJA"):
                try:
                    df_preview = pd.read_excel(archivo_caja, nrows=5)
                    st.dataframe(df_preview, use_container_width=True)
                    total_rows = len(pd.read_excel(archivo_caja))
                    st.caption(f"📊 Total de registros: {total_rows:,}")
                except Exception as e:
                    st.error(f"Error al leer archivo: {e}")
        else:
            st.info("📁 Selecciona el archivo CAJA para continuar")
    
    with col2:
        st.markdown("### 🎫 Archivo BIG PASS")
        archivo_big_pass = st.file_uploader(
            "Selecciona el archivo BIG PASS (Excel)",
            type=['xlsx', 'xls'],
            key="big_pass_uploader",
            help="Archivo que contiene datos de descontar, pagar y people"
        )
        
        if archivo_big_pass:
            st.session_state.archivo_big_pass = archivo_big_pass
            st.success(f"✅ **{archivo_big_pass.name}**")
            st.caption(f"📏 Tamaño: {archivo_big_pass.size:,} bytes")
            
            # Vista previa
            with st.expander("👀 Vista previa BIG PASS"):
                try:
                    df_preview = pd.read_excel(archivo_big_pass, nrows=5)
                    st.dataframe(df_preview, use_container_width=True)
                    total_rows = len(pd.read_excel(archivo_big_pass))
                    st.caption(f"📊 Total de registros: {total_rows:,}")
                except Exception as e:
                    st.error(f"Error al leer archivo: {e}")
        else:
            st.info("📁 Selecciona el archivo BIG PASS para continuar")
    
    # Estado de archivos
    st.markdown("### 📊 Estado de Archivos")
    
    status_col1, status_col2, status_col3 = st.columns(3)
    
    with status_col1:
        caja_status = "✅ Cargado" if archivo_caja else "⏳ Pendiente"
        st.metric("📊 CAJA", caja_status)
    
    with status_col2:
        big_pass_status = "✅ Cargado" if archivo_big_pass else "⏳ Pendiente"
        st.metric("🎫 BIG PASS", big_pass_status)
    
    with status_col3:
        if archivo_caja and archivo_big_pass:
            st.metric("🎯 Estado", "✅ Listo", "Para procesar")
        else:
            st.metric("🎯 Estado", "⏳ Esperando", "Archivos faltantes")
    
    # Solo continuar si ambos archivos están cargados
    if not archivo_caja or not archivo_big_pass:
        st.warning("⚠️ **Carga ambos archivos para continuar al siguiente paso**")
        return
    
    st.markdown("---")
    
    # === SECCIÓN 2: CONFIGURACIÓN ===
    st.markdown("## ⚙️ Paso 2: Configuración del Procesamiento")
    
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
    
    # Información del proceso
    with st.expander("ℹ️ ¿Qué hará el procesamiento?", expanded=False):
        st.markdown("""
        **El sistema procesará automáticamente:**
        
        1. **📊 Archivo CAJA** → Genera registros con concepto **Z498** (Descuadres de caja)
        2. **🎫 Archivo BIG PASS** → Genera registros con conceptos:
           - **Z609** (Descontar)
           - **Y602** (Pagar)  
           - **Y608** (People)
        3. **🔄 Consolidación** → Unifica todos los registros en un DataFrame
        4. **📁 Exportación** → Genera archivo en el formato seleccionado
        5. **📊 Estadísticas** → Muestra resumen de registros procesados
        """)
    
    st.markdown("---")
    
    # === SECCIÓN 3: PROCESAMIENTO ===
    st.markdown("## 🚀 Paso 3: Ejecutar Procesamiento")
    
    # Botón principal
    if st.button("🎯 **PROCESAR ARCHIVOS Y GENERAR PLANO**", type="primary", use_container_width=True):
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
                st.markdown("## 📥 Descargar Archivo Generado")
                
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
                        st.caption(f"📊 {len(df_resultado):,} registros procesados")
                        st.caption(f"📅 Generado: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
                
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
                        st.caption(f"📊 {len(df_resultado):,} registros procesados")
                        st.caption(f"📅 Generado: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
                
                # Botón para procesar más archivos
                st.markdown("---")
                if st.button("🔄 **Procesar Otros Archivos**", use_container_width=True):
                    # Limpiar archivos de session_state
                    st.session_state.archivo_caja = None
                    st.session_state.archivo_big_pass = None
                    st.rerun()
            
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
