import os
import time
import logging
from datetime import datetime
import pytest
from selenium import webdriver

# Configuración del Sistema de Logging
os.makedirs("Reports", exist_ok=True)
logging.basicConfig(
    filename="Reports/execution.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# Diccionario global para almacenar resultados para el reporte HTML
test_resultados = []

@pytest.fixture
def setup_driver(request):
    """Fixture que configura el navegador Chrome, registra logs y gestiona capturas ante fallos"""
    test_name = request.node.name
    logging.info(f"--- INICIO de la prueba: {test_name} ---")
    
    driver = webdriver.Chrome()
    driver.get("https://www.saucedemo.com")
    logging.info("Navegador abierto y dirigido a https://www.saucedemo.com")
    
    yield driver
    
    # Si la prueba falló, capturamos pantalla
    if request.node.rep_call.failed:
        os.makedirs("Evidence", exist_ok=True)
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        nombre_limpio = test_name.replace("[", "_").replace("]", "")
        ruta_img = f"Evidence/{nombre_limpio}_{timestamp}.png"
        driver.save_screenshot(ruta_img)
        logging.error(f"Fallo detectado en '{test_name}'. Captura guardada en: {ruta_img}")
        request.node.screenshot_path = ruta_img
    else:
        logging.info(f"Prueba '{test_name}' finalizada con ÉXITO.")
        request.node.screenshot_path = None

    driver.quit()
    logging.info(f"--- FIN de la prueba: {test_name} ---\n")

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook para capturar el resultado y duración de cada test"""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)
    
    if rep.when == "call":
        duracion = getattr(rep, "duration", 0.0)
        estado = "PASSED" if rep.passed else "FAILED"
        
        # Guardamos datos para el reporte HTML final
        test_resultados.append({
            "name": item.name,
            "status": estado,
            "duration": round(duracion, 2),
            "error": str(rep.longrepr) if rep.failed else ""
        })

def pytest_sessionfinish(session, exitstatus):
    """Genera automáticamente un reporte HTML detallado al finalizar todas las pruebas"""
    html_content = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Reporte de Ejecución - Automatización QA</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; background-color: #f4f6f9; color: #333; }}
            h1 {{ color: #2c3e50; }}
            .summary {{ background: #fff; padding: 15px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-bottom: 20px; }}
            table {{ width: 100%; border-collapse: collapse; background: #fff; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
            th, td {{ padding: 12px 15px; text-align: left; border-bottom: 1px solid #ddd; }}
            th {{ background-color: #34495e; color: #fff; }}
            .passed {{ color: #27ae60; font-weight: bold; }}
            .failed {{ color: #c0392b; font-weight: bold; }}
        </style>
    </head>
    <body>
        <h1>Reporte de Pruebas Automatizadas (UI & API)</h1>
        <div class="summary">
            <p><strong>Fecha y Hora de Ejecución:</strong> {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
            <p><strong>Total de Pruebas Ejecutadas:</strong> {len(test_resultados)}</p>
        </div>
        <table>
            <tr>
                <th>Nombre del Test</th>
                <th>Estado</th>
                <th>Duración (s)</th>
            </tr>
    """
    
    for t in test_resultados:
        clase_estado = "passed" if t["status"] == "PASSED" else "failed"
        html_content += f"""
            <tr>
                <td>{t["name"]}</td>
                <td class="{clase_estado}">{t["status"]}</td>
                <td>{t["duration"]}s</td>
            </tr>
        """
        
    html_content += """
        </table>
    </body>
    </html>
    """
    
    ruta_reporte = "Reports/reporte_ejecucion.html"
    with open(ruta_reporte, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"\n[INFO] Reporte HTML generado exitosamente en: {ruta_reporte}")
    print("[INFO] Sistema de logging activo en: Reports/execution.log")