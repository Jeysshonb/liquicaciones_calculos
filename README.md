# 📊 Sistema de Liquidaciones de Nómina

Sistema web desarrollado en Streamlit para el procesamiento automático de archivos de liquidaciones de nómina, específicamente para la generación de archivos planos con conceptos SAP.

## 🚀 Características

- **Procesamiento de Archivos**: Maneja archivos de CAJA y BIG PASS en formato Excel
- **Generación de Conceptos SAP**: Crea automáticamente conceptos Z498, Z609, Y602, Y608
- **Interfaz Web Intuitiva**: Desarrollado con Streamlit para facilidad de uso
- **Múltiples Formatos de Salida**: Exporta en Excel (.xlsx) o CSV (.csv)
- **Vista Previa de Datos**: Permite revisar los datos antes de la descarga
- **Estadísticas Detalladas**: Muestra resúmenes por concepto y totales

## 📋 Conceptos Procesados

| Concepto | Descripción | Archivo Origen | Tipo |
|----------|-------------|----------------|------|
| Z498 | CAJA - Descuadres de caja | CAJA | Descuento |
| Z609 | BIG PASS - Valores a descontar | BIG PASS | Descuento |
| Y602 | BIG PASS - Valores a pagar | BIG PASS | Pago |
| Y608 | BIG PASS - People | BIG PASS | Pago |

## 🛠️ Instalación

### Prerrequisitos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Instalación Local

1. **Clonar el repositorio**:
```bash
git clone https://github.com/tu-usuario/liquidaciones-nomina.git
cd liquidaciones-nomina
```

2. **Instalar dependencias**:
```bash
pip install -r requirements.txt
```

3. **Ejecutar la aplicación**:
```bash
streamlit run app.py
```

4. **Abrir en el navegador**:
La aplicación se abrirá automáticamente en `http://localhost:8501`

## 🌐 Deployment en Streamlit Cloud

1. **Fork este repositorio** en tu cuenta de GitHub
2. **Conectar con Streamlit Cloud**:
   - Visita [share.streamlit.io](https://share.streamlit.io)
   - Conecta tu cuenta de GitHub
   - Selecciona este repositorio
   - Especifica `app.py` como archivo principal
3. **Deploy automático**: La aplicación se desplegará automáticamente

## 📁 Estructura del Proyecto

```
liquidaciones-nomina/
│
├── app.py                 # Aplicación principal de Streamlit
├── archivo_plano.py       # Módulo de procesamiento de archivos
├── requirements.txt       # Dependencias del proyecto
└── README.md             # Documentación del proyecto
```

## 🔧 Uso

### 1. Subir Archivos
- **Archivo CAJA**: Debe contener la columna "DESCUADRES DE CAJA PARA DESCONTAR"
- **Archivo BIG PASS**: Debe contener las columnas "Descontar", "Pagar", "PEOPLE"

### 2. Configurar Opciones
- Seleccionar formato de salida (Excel o CSV)
- Elegir si incluir timestamp en el nombre del archivo
- Activar/desactivar vista previa y estadísticas

### 3. Procesar y Descargar
- Hacer clic en "Procesar y Generar Archivo Plano"
- Revisar las estadísticas y vista previa
- Descargar el archivo generado

## 📊 Formato de Salida

El archivo generado contiene las siguientes columnas:

| Columna | Descripción | Ejemplo |
|---------|-------------|---------|
| SAP | Número SAP del empleado | 12345678 |
| FECHA | Fecha de terminación | 31/07/2025 |
| CONCEPTO | Código de concepto SAP | Z498 |
| VALOR | Valor a procesar | 50000 |

## 🔍 Validaciones

El sistema incluye las siguientes validaciones:
- ✅ Verificación de columnas requeridas en los archivos
- ✅ Validación de formatos de fecha
- ✅ Filtrado de valores mayores a cero
- ✅ Conversión automática de tipos de datos
- ✅ Manejo de errores y datos faltantes

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Para contribuir:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Próximas Características

- [ ] Validación avanzada de datos
- [ ] Reportes gráficos
- [ ] Procesamiento por lotes
- [ ] Integración con APIs
- [ ] Más formatos de archivo
- [ ] Plantillas personalizables

## 📞 Soporte

Si tienes preguntas o necesitas ayuda:
- Crear un [Issue](https://github.com/tu-usuario/liquidaciones-nomina/issues) en GitHub
- Revisar la documentación en este README

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

---

**Desarrollado con ❤️ usando Streamlit**
