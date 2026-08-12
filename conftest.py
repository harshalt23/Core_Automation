import os
import pytest
from playwright.sync_api import sync_playwright
import allure
import pytest_html
import base64
import platform
import shutil
from utils.logger_utils import setup_logger
from utils.folder_utils import create_report_folders
from utils.screenshot_utils import capture_screenshot
from utils.trace_utils import start_trace, stop_trace
from utils.config_reader import load_config

EDGE_PROFILE = os.path.join(os.getcwd(), "edge_profile")

# Create report folders
create_report_folders()

# Setup logger
logger = setup_logger()

# Provided the URL in the config.yaml then reading it through config_reader.py then calling it here to run
config = load_config()


def cleanup_parallel_profiles():
    """Remove worker-specific edge profiles (gw0, gw1, etc.)"""
    current_dir = os.getcwd()
    for folder in os.listdir(current_dir):
        folder_path = os.path.join(current_dir, folder)
        if os.path.isdir(folder_path) and folder.startswith("edge_profile_gw"):
            try:
                shutil.rmtree(folder_path)
                logger.info(f"Cleaned up parallel profile: {folder}")
            except Exception as e:
                logger.warning(f"Failed to cleanup {folder}: {e}")


# Environment details to be visible in the Allure report
@pytest.fixture(scope="session", autouse=True)
def environment_details():
    """Generate environment properties file for Allure reporting."""
    env_path = "reports/allure-results/environment.properties"

    try:
        os.makedirs("reports/allure-results", exist_ok=True)

        with open(env_path, "w") as f:
            f.write(f"Environment={config['env']}\n")
            f.write(f"BaseURL={config['base_url']}\n")
            f.write(f"Browser={config['browser']}\n")
            f.write(f"OperatingSystem={platform.system()}\n")
            f.write(f"OSVersion={platform.version()}\n")
            f.write(f"PythonVersion={platform.python_version()}\n")
        logger.info("Successfully generated environment.properties file")
    except Exception as e:
        logger.error(f"Failed to write environment.properties: {str(e)}")


# Launch browser and navigate to application
@pytest.fixture(scope="function")
def authenticated_page(request: pytest.FixtureRequest, worker_id):
    # Determine if running in parallel mode
    is_parallel = worker_id != "master"

    # Create unique browser profile per worker in parallel mode, use EDGE_PROFILE otherwise
    if is_parallel:
        edge_profile = os.path.join(os.getcwd(), f"edge_profile_{worker_id}")
        logger.info(f"Running in parallel mode with worker {worker_id}")
    else:
        edge_profile = EDGE_PROFILE

        # Clean up any leftover parallel profiles from previous runs
        cleanup_parallel_profiles()
        logger.info("Running in single test mode with EDGE_PROFILE")

    os.makedirs(edge_profile, exist_ok=True)

    with sync_playwright() as playwright:
        context = playwright.chromium.launch_persistent_context(
            user_data_dir=edge_profile, headless=False, channel="msedge", slow_mo=1000
        )
        logger.info("Starting Playwright trace")
        # Start Trace
        start_trace(context)

        page = context.new_page()
        logger.info("Maximizing the browser window")
        page.set_viewport_size({"width": 1366, "height": 768})
        logger.info("Opening the core application")
        page.goto(config["base_url"], wait_until="domcontentloaded")

        yield page

        # Stop Trace
        logger.info("Stopping Playwright trace")
        trace_path = stop_trace(context, request.node.name)

        allure.attach.file(
            trace_path,
            name="Playwright_Trace",
            attachment_type=allure.attachment_type.ZIP,
        )
        logger.info("Closing the browser")
        context.close()


# PYTEST HOOK --This is used to generate the report this hook is going to link with the Allure report.


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call":
        page = item.funcargs.get("authenticated_page")

        if page and not page.is_closed():
            try:
                screenshot_path = capture_screenshot(page, item.name)
                if report.failed:
                    screenshot_name = "Failure Screenshot"
                else:
                    screenshot_name = "Success Screenshot"

                allure.attach.file(
                    screenshot_path,
                    name=screenshot_name,
                    attachment_type=allure.attachment_type.PNG,
                )

                # Attach screenshot to HTML report (embedded)
                try:
                    with open(screenshot_path, "rb") as image_file:
                        encoded_image = base64.b64encode(image_file.read()).decode()
                    extras = getattr(report, "extras", [])
                    extras.append(pytest_html.extras.image(encoded_image))
                    report.extras = extras
                except Exception as e:
                    logger.error(
                        f"Failed to attach screenshot to HTML report: {str(e)}"
                    )
            except Exception as e:
                logger.error(f"Failed to capture screenshot: {str(e)}")

            if report.failed:
                log_file = "reports/logs/execution.log"
                if os.path.exists(log_file):
                    try:
                        allure.attach.file(
                            log_file,
                            name="Execution Logs",
                            attachment_type=allure.attachment_type.TEXT,
                        )
                    except Exception as e:
                        logger.error(f"Failed to attach execution log: {str(e)}")


# Cleanup parallel profiles after tests complete successfully
@pytest.hookimpl(tryfirst=True)
def pytest_sessionfinish(session, exitstatus):
    """Clean up worker-specific edge profiles after all tests complete and exit status is 0 (success)"""
    if exitstatus == 0:
        cleanup_parallel_profiles()
        logger.info("All tests passed. Cleaned up parallel profiles.")
