# ✨ Entrega Final — Automatización de Testing (SauceDemo)

## 🎯 ¿Cuál es el propósito del proyecto?
La idea de este proyecto es automatizar las pruebas de **SauceDemo** usando **Page Object Model (POM)** para probar que todo funcione bien y sin errores. Incluye pruebas de login parametrizadas con datos externos (`usuarios.json`), validación del inventario, agregado al carrito y pruebas de API, dejando registro de todo con logs, capturas y reporte HTML.

## 🛠️ ¿Cuáles son las tecnologías utilizadas?
* **Python 3:** Lenguaje principal del proyecto.
* **Pytest:** Framework para organizar y correr las pruebas.
* **Selenium WebDriver:** Para automatizar las acciones en el navegador.
* **POM (Page Object Model):** Para tener separadas las páginas (`Utils/`) de los tests (`Test/`) y que el código sea más ordenado
* **Reportes y logs:** Reporte en HTML (`Reports/reporte_ejecucion.html`) y log de ejecución (`Reports/execution.log`)
* **Evidencias:** Capturas guardadas en la carpeta `Evidence/`
* **Git y GitHub:** Para el control de versiones y la entrega del repo.

## 📁 ¿Cómo es la estructura del proyecto?
* **`Test/`**: Están los archivos de prueba (`test_login.py`, `test_inventory.py`, `test_cart.py`, `test_api.py`) y `conftest.py`
* **`Utils/`**: Están las clases de cada página (`login_page.py` e `inventory_page.py`) con sus selectores y acciones
* **`Reports/`**: Acá se guardan `reporte_ejecucion.html` y `execution.log`
* **`Evidence/`**: Acá quedan las capturas de pantalla de evidencia
* **`pytest.ini`**: Configura `pytest` y tiene `pythonpath = .` para que encuentre `Utils/` sin dramas de rutas.
* **`usuarios.json`**: Tiene los datos de usuarios para las pruebas de login
* **`README.md`**: Este archivo con toda la explicación del proyecto.

## 📦 ¿Cómo instalar las dependencias?
1. Abrír la carpeta principal del proyecto en VS Coder
2. Abrír la terminal ahí mismor
3. Instalár lo necesario con `pip`:
   ```bash
   pip install pytest selenium pytest-html requests

## ▶️ ¿Cómo ejecutar las pruebas?
Asegurate de estar parado en la carpeta raíz del proyecto en mi caso " (Proyecto-Final -automatizacion-testing-Juarez_Victoria)"

Corrér este comando en la terminal:
  ```bash
 ## python -m pytest -v ##


📊 ¿Cómo interpretar los reportes generados?

En la terminal: Te muestra cada test con PASSED si salió todo bien o FAILED si falló algo, más el resumen final
Reporte HTML (Reports/reporte_ejecucion.html): Lo abrís en el navegador y ves el detalle visual de cómo salieron las pruebas
Log (Reports/execution.log): Te sirve para ver el paso a paso de lo que fue pasando y revisar si hubo algún error
Evidencias (Evidence/): Ahí están las imágenes de respaldo de la ejecución

