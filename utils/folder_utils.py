import os


def create_report_folders():
    os.makedirs("reports/screenshots", exist_ok=True)
    os.makedirs("reports/traces", exist_ok=True)
    os.makedirs("reports/logs", exist_ok=True)
    # os.makedirs("reports/videos", exist_ok=True)
