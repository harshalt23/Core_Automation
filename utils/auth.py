# from playwright.sync_api import sync_playwright

# def save_login_state():
#     with sync_playwright() as p:
#         browser = p.chromium.launch(headless=False)
#         context = browser.new_context()
#         page = context.new_page()

#         page.goto("https://core-dev.mma.com/core_v2/ui/",wait_until="domcontentloaded")

#         # Perform login
#         page.fill("#username", "")
#         page.fill("#password", "")
#         page.click("#login")


#         page.wait_for_timeout(3000)

#         # Save session
#         context.storage_state(path="storage_state.json")
#         print("Storage state saved successfully")

#         browser.close()
# if __name__ == "__main__":
#     save_login_state()
from playwright.sync_api import sync_playwright

BASE_URL = "https://core-dev.mma.com/core_v2/ui/"
STORAGE_FILE = "storage_state.json"


def save_login_state():
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
            channel="msedge",  # Use Edge since you are using it
        )

        context = browser.new_context()
        page = context.new_page()

        page.goto(BASE_URL)

        print("Login manually via SAS authentication...")
        print("Wait until you reach the Core dashboard.")

        input("After login is fully complete, press ENTER here...")

        context.storage_state(path=STORAGE_FILE)
        print("Storage state saved successfully!")

        browser.close()


if __name__ == "__main__":
    save_login_state()

    # To run and store the credentials into the json file type in terminal "python auth/save_login_state.py"
