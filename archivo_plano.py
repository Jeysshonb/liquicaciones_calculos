import pandas as pd
import os
from datetime import datetime

def procesar_todo_simple():
    """
    Procesador simple que funciona sin errores
    """
    print("=== PROCESADOR SIMPLE - CAJA + BIG PASS ===")
    print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    
    ruta_salida = r"C:\Users\jjbustos\OneDrive - Grupo Jerónimo Martins\Documents\liquidacion_validacion_nomina\archivos_salida"
    os.makedirs(ruta_salida, exist_ok=True)
    
    # Lista para todos los registros
    todos_los_registros = []
    
    # ============ PROCESAR CAJA ============
    print("PROCESANDO ARCHIVO CAJA...")
    try:
        archivo_caja = r"C:\Users\jjbustos\OneDrive - Grupo Jerónimo Martins\Documents\liquidacion_validacion_nomina\archivos_busqueda_planos\PAZ Y SALVOS PQT_08 JULIO 2025_caja.xlsx"
        df_caja = pd.read_excel(archivo_caja)
        
        # Filtrar descuadres de caja > 0
        columna_descuadres = 'DESCUADRES DE CAJA PARA DESCONTAR'
        df_caja_filtrado = df_caja[
            (df_caja[columna_descuadres].notna()) & 
            (pd.to_numeric(df_caja[columna_descuadres], errors='coerce') > 0)
        ]
        
        print(f"Registros CAJA procesados: {len(df_caja_filtrado)}")
        
        # Agregar registros de caja
        for _, row in df_caja_filtrado.iterrows():
            fecha_str = ''
            if pd.notna(row['Fecha Terminación. (Digite)']):
                fecha_dt = pd.to_datetime(row['Fecha Terminación. (Digite)'], errors='coerce')
                if pd.notna(fecha_dt):
                    fecha_str = fecha_dt.strftime('%d.%m.%Y')  # CAMBIADO: puntos en lugar de barras
            
            registro = {
                'SAP': row['SAP'],
                'FECHA': fecha_str,
                'CONCEPTO': 'Z498',
                'VALOR': int(pd.to_numeric(row[columna_descuadres], errors='coerce'))
            }
            todos_los_registros.append(registro)
            
    except Exception as e:
        print(f"Error procesando CAJA: {e}")
    
    # ============ PROCESAR BIG PASS ============
    print("\nPROCESANDO ARCHIVO BIG PASS...")
    try:
        archivo_big_pass = r"C:\Users\jjbustos\OneDrive - Grupo Jerónimo Martins\Documents\liquidacion_validacion_nomina\archivos_busqueda_planos\PAZ Y SALVOS PQT_08_Julio 2025_big_pass.xlsx"
        df_big_pass = pd.read_excel(archivo_big_pass)
        
        print(f"Columnas Big Pass: {list(df_big_pass.columns)}")
        
        # Procesar DESCONTAR
        df_descontar = df_big_pass[
            (df_big_pass['Descontar'].notna()) & 
            (pd.to_numeric(df_big_pass['Descontar'], errors='coerce') > 0)
        ]
        print(f"Registros DESCONTAR procesados: {len(df_descontar)}")
        
        for _, row in df_descontar.iterrows():
            fecha_str = ''
            if pd.notna(row['Terminación']):
                fecha_dt = pd.to_datetime(row['Terminación'], errors='coerce')
                if pd.notna(fecha_dt):
                    fecha_str = fecha_dt.strftime('%d.%m.%Y')  # CAMBIADO: puntos en lugar de barras
            
            registro = {
                'SAP': str(row['N° Sap ']).strip(),
                'FECHA': fecha_str,
                'CONCEPTO': 'Z609',
                'VALOR': int(pd.to_numeric(row['Descontar'], errors='coerce'))
            }
            todos_los_registros.append(registro)
        
        # Procesar PAGAR
        print("\nAnalizando columna PAGAR:")
        valores_pagar = df_big_pass['Pagar'].value_counts()
        print(f"Valores únicos en Pagar: {valores_pagar.head(10)}")
        
        valores_numericos = pd.to_numeric(df_big_pass['Pagar'], errors='coerce')
        print(f"Valores > 0: {(valores_numericos > 0).sum()}")
        print(f"Valores = 0: {(valores_numericos == 0).sum()}")
        print(f"Valores NaN: {valores_numericos.isna().sum()}")
        
        df_pagar = df_big_pass[
            (df_big_pass['Pagar'].notna()) & 
            (pd.to_numeric(df_big_pass['Pagar'], errors='coerce') > 0)
        ]
        print(f"Registros PAGAR procesados: {len(df_pagar)}")
        
        for _, row in df_pagar.iterrows():
            fecha_str = ''
            if pd.notna(row['Terminación']):
                fecha_dt = pd.to_datetime(row['Terminación'], errors='coerce')
                if pd.notna(fecha_dt):
                    fecha_str = fecha_dt.strftime('%d.%m.%Y')  # CAMBIADO: puntos en lugar de barras
            
            valor_pagar = pd.to_numeric(row['Pagar'], errors='coerce')
            if valor_pagar > 0:
                registro = {
                    'SAP': str(row['N° Sap ']).strip(),
                    'FECHA': fecha_str,
                    'CONCEPTO': 'Y602',
                    'VALOR': int(valor_pagar)
                }
                todos_los_registros.append(registro)
            
    except Exception as e:
        print(f"Error procesando BIG PASS: {e}")
    
    # ============ PROCESAR PEOPLE SEPARADAMENTE ============
    print("\n=== PROCESANDO PEOPLE POR SEPARADO ===")
    try:
        archivo_big_pass = r"C:\Users\jjbustos\OneDrive - Grupo Jerónimo Martins\Documents\liquidacion_validacion_nomina\archivos_busqueda_planos\PAZ Y SALVOS PQT_08_Julio 2025_big_pass.xlsx"
        df_people_check = pd.read_excel(archivo_big_pass)
        
        print("--- PROCESANDO PEOPLE ---")
        print("Iniciando procesamiento de columna PEOPLE...")
        
        if 'PEOPLE' not in df_people_check.columns:
            print("ERROR: Columna PEOPLE no encontrada")
        else:
            print("Columna PEOPLE encontrada correctamente")
            
            valores_people = df_people_check['PEOPLE'].value_counts()
            print(f"Valores únicos en PEOPLE:")
            print(valores_people.head(10))
            
            valores_numericos_people = pd.to_numeric(df_people_check['PEOPLE'], errors='coerce')
            print(f"Valores > 0: {(valores_numericos_people > 0).sum()}")
            print(f"Valores = 0: {(valores_numericos_people == 0).sum()}")
            print(f"Valores NaN: {valores_numericos_people.isna().sum()}")
            
            df_people = df_people_check[
                (df_people_check['PEOPLE'].notna()) & 
                (pd.to_numeric(df_people_check['PEOPLE'], errors='coerce') > 0)
            ]
            print(f"Registros PEOPLE filtrados: {len(df_people)}")
            
            registros_people_agregados = 0
            for _, row in df_people.iterrows():
                fecha_str = ''
                if pd.notna(row['Terminación']):
                    # Primero convertir a string y limpiar
                    fecha_raw = str(row['Terminación']).strip()
                    print(f"DEBUG PEOPLE - Fecha raw: {fecha_raw}, tipo: {type(row['Terminación'])}")
                    
                    fecha_dt = pd.to_datetime(row['Terminación'], errors='coerce')
                    if pd.notna(fecha_dt):
                        fecha_str = fecha_dt.strftime('%d.%m.%Y')  # CAMBIADO: puntos en lugar de barras
                        print(f"DEBUG PEOPLE - Fecha convertida: {fecha_str}")
                
                valor_people = pd.to_numeric(row['PEOPLE'], errors='coerce')
                if valor_people > 0:
                    registro = {
                        'SAP': str(row['N° Sap ']).strip(),
                        'FECHA': fecha_str,
                        'CONCEPTO': 'Y608',
                        'VALOR': int(valor_people)
                    }
                    todos_los_registros.append(registro)
                    registros_people_agregados += 1
            
            print(f"Registros PEOPLE agregados al archivo: {registros_people_agregados}")
        
        print("Procesamiento de PEOPLE completado.")
        
    except Exception as e:
        print(f"Error procesando PEOPLE por separado: {e}")
    
    # ============ CREAR ARCHIVO FINAL ============
    if not todos_los_registros:
        print("No hay registros para procesar")
        return
    
    df_final = pd.DataFrame(todos_los_registros)
    print(f"\nTOTAL REGISTROS: {len(df_final)}")
    print(f"Columnas: {list(df_final.columns)}")
    
    # Contar por concepto
    conceptos = df_final['CONCEPTO'].value_counts()
    print("\nRESUMEN POR CONCEPTO:")
    for concepto, cantidad in conceptos.items():
        suma = df_final[df_final['CONCEPTO'] == concepto]['VALOR'].sum()
        nombre = {
            'Z498': 'CAJA',
            'Z609': 'BIG PASS - Descontar', 
            'Y602': 'BIG PASS - Pagar',
            'Y608': 'BIG PASS - People'
        }.get(concepto, concepto)
        print(f"{concepto} ({nombre}): {cantidad} registros, ${suma:,}")
    
    # Guardar archivo
    archivo_salida = os.path.join(ruta_salida, "archivo_plano.xlsx")
    try:
        df_final.to_excel(archivo_salida, index=False)
        print(f"\nARCHIVO CREADO: {archivo_salida}")
        print(f"Tamaño: {os.path.getsize(archivo_salida)} bytes")
    except:
        archivo_csv = os.path.join(ruta_salida, "archivo_plano.csv")
        df_final.to_csv(archivo_csv, index=False, encoding='utf-8-sig', sep=';')
        print(f"\nARCHIVO CREADO: {archivo_csv}")
    
    # Mostrar muestra
    print(f"\nMUESTRA DE DATOS:")
    print(df_final.head(10).to_string(index=False))
    
    print("\n" + "="*60)
    print("PROCESAMIENTO COMPLETADO")

# Ejecutar
if __name__ == "__main__":
    procesar_todo_simple()
