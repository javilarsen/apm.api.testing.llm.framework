import pytest
import json
import csv
import os
from services.asset_template_client import AssetTemplateClient

@pytest.fixture
def asset_client():
    return AssetTemplateClient()

# Estructura en memoria para almacenar los resultados
test_results = {}

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Captura el resultado, duración y el motivo exacto del fallo de cada prueba.
    """
    outcome = yield
    report = outcome.get_result()

    nodeid = report.nodeid
    
    if nodeid not in test_results:
        test_results[nodeid] = {
            "test_name": item.name,
            "status": "PASSED",
            "failure_reason": "",
            "duration_seconds": 0.0
        }

    # Acumulamos el tiempo de ejecución (setup + call + teardown)
    test_results[nodeid]["duration_seconds"] += report.duration

    # Si hay un error o falla en cualquier fase
    if report.failed:
        test_results[nodeid]["status"] = "FAILED"
        
        # Extraemos el texto del error/traceback de pytest
        longrepr = getattr(report, "longreprtext", str(report.longrepr) if report.longrepr else "Error desconocido")
        
        # Limpiamos y compactamos los saltos de línea para que el CSV no se rompa en varias filas
        clean_reason = " | ".join([line.strip() for line in longrepr.splitlines() if line.strip()])
        test_results[nodeid]["failure_reason"] = clean_reason
        
    elif report.skipped and test_results[nodeid]["status"] != "FAILED":
        test_results[nodeid]["status"] = "SKIPPED"


def pytest_sessionfinish(session, exitstatus):
    """
    Genera los archivos CSV y JSON con las nuevas columnas al finalizar la sesión.
    """
    results_list = list(test_results.values())

    json_filepath = os.path.join(session.config.rootdir, "reporte_pruebas.json")
    csv_filepath = os.path.join(session.config.rootdir, "reporte_pruebas.csv")

    # Columnas organizadas incluyendo el motivo de la falla
    fieldnames = [ "test_name", "status", "failure_reason", "duration_seconds"]

    # 1. Guardar JSON
    try:
        with open(json_filepath, "w", encoding="utf-8") as f:
            json.dump(results_list, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"[ERROR] No se pudo generar el JSON: {e}")

    # 2. Guardar CSV
    try:
        with open(csv_filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results_list)
        
        print(f"\n\n[REPORTE ACTUALIZADO CON ÉXITO]\n - CSV: {csv_filepath}\n - JSON: {json_filepath}\n")
    except Exception as e:
        print(f"[ERROR] No se pudo generar el CSV: {e}")