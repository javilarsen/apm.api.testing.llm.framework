import pytest
import json
import csv
import os
from services.asset_template_client import AssetTemplateClient

@pytest.fixture
def asset_client():
    return AssetTemplateClient()

# Structure in memory to store test results
test_results = {}

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Catch the result, duration time and the failure reason of each test.
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

    # Accumulate the execution time (setup + call + teardown) for the test.
    test_results[nodeid]["duration_seconds"] += report.duration

    # If there is an error or failure in any phase
    if report.failed:
        test_results[nodeid]["status"] = "FAILED"
        
        # Extract the error/traceback text from pytest
        longrepr = getattr(report, "longreprtext", str(report.longrepr) if report.longrepr else "Error desconocido")
        
        # Clean and compact line breaks so that the CSV does not break into multiple rows
        clean_reason = " | ".join([line.strip() for line in longrepr.splitlines() if line.strip()])
        test_results[nodeid]["failure_reason"] = clean_reason
        
    elif report.skipped and test_results[nodeid]["status"] != "FAILED":
        test_results[nodeid]["status"] = "SKIPPED"


def pytest_sessionfinish(session, exitstatus):
    """
    Generate CSV and JSON files with the new columns at the end of the session.
    """
    results_list = list(test_results.values())

    json_filepath = os.path.join(session.config.rootdir, "test_document.json")
    csv_filepath = os.path.join(session.config.rootdir, "test_document.csv")

    # Organized columns including the failure reason
    fieldnames = [ "test_name", "status", "failure_reason", "duration_seconds"]

    # 1. Save JSON
    try:
        with open(json_filepath, "w", encoding="utf-8") as f:
            json.dump(results_list, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"[ERROR] Could not generate JSON: {e}")

    # 2. Save CSV
    try:
        with open(csv_filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results_list)
        
        print(f"\n\n[REPORT UPDATED SUCCESSFULLY]\n - CSV: {csv_filepath}\n - JSON: {json_filepath}\n")
    except Exception as e:
        print(f"[ERROR] Could not generate CSV: {e}")