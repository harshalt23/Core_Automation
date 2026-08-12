import datetime


def capture_screenshot(page, test_name):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot_path = f"reports/screenshots/{test_name}_{timestamp}.png"
    page.screenshot(path=screenshot_path)
    return screenshot_path
