# def test_basic_launch(page):
#     page.goto("https://core-dev.mma.com/core_v2/ui/")
#     assert page.title() is not None


# def test_basic_launch(page):
#     page.goto("https://core-dev.mma.com/core_v2/ui/", wait_until="networkidle")

#     # Wait for something stable on the application (Navbar / Body / Logo)
#     page.wait_for_load_state("networkidle")

#     # Instead of relying on title() (your app may not have a static title)
#     assert page.url.startswith("https://core-dev.mma.com/core_v2/ui/")


# def test_basic_launch(page):
#     page.goto("https://core-dev.mma.com/core_v2/ui/", wait_until="domcontentloaded")

#     # Expect redirect to Microsoft login
#     page.wait_for_url("https://login.microsoftonline.com/**")

#     # Validate login page is shown
#     assert "login.microsoftonline.com" in page.url


# tests/sanity/test_basic_launch.py

# def test_basic_launch(page):
#     # Step 1: Open app
#     page.goto("https://core-dev.mma.com/core_v2/ui/", wait_until="load")

#     # Step 2: Allow time for Microsoft login + phone approval
#     # This keeps the browser open
#     page.wait_for_url(
#         "**/core_v2/ui/**",
#         timeout=180_000  # 3 minutes – plenty for phone approval
#     )

#     # Step 3: Final stability wait
#     page.wait_for_load_state("networkidle")

#     # Step 4: Assertion AFTER auth
#     assert "core_v2/ui" in page.url


# def test_basic_launch(page):
#     # Step 1: Launch app
#     page.goto("https://core-dev.mma.com/core_v2/ui/", wait_until="load")

#     # Step 2: You WILL land on Microsoft login — that's OK
#     print("Waiting for manual Microsoft authentication...")

#     # Step 3: Give human time (phone approval)
#     page.wait_for_timeout(120_000)  # 2 minutes hard wait

#     # Step 4: AFTER you approve on phone, Playwright will redirect automatically
#     page.wait_for_load_state("networkidle")

#     # Step 5: NOW assert (safe)
#     assert "core_v2/ui" in page.url


# print(">>> SCRIPT STARTED <<<")

# from playwright.sync_api import sync_playwright

# def test_first_login():
#     with sync_playwright() as p:
#         context = p.chromium.launch_persistent_context(
#             user_data_dir="C:/playwright-edge-profile",
#             channel="msedge",
#             headless=False,
#             slow_mo=1000
#         )

#         page = context.new_page()

#         print("Opening Core UI...")
#         page.goto("https://core-dev.mma.com/core_v2/ui/", wait_until="load")

#         print(" Login manually using Microsoft Authenticator")
#         print("You have 2 minutes...")

#         # Hard wait for manual authentication
#         page.wait_for_timeout(120_000)

#         print("Closing browser. Session should now be saved.")
#         context.close()


# below is working code

# from playwright.sync_api import sync_playwright

# print(">>> SCRIPT STARTED <<<")

# with sync_playwright() as p:
#     print("Opening CORE app...")

#     context = p.chromium.launch_persistent_context(
#         user_data_dir=r"C:\pw-edge-profile",
#         headless=False,
#         channel="msedge"
#     )

#     page = context.new_page()

#     page.goto("https://core-dev.mma.com/core_v2/ui/", wait_until="domcontentloaded")

#     print("Waiting for Azure SSO redirect to complete...")
#     page.wait_for_timeout(120_000)  # time for phone approval

#     print("Final URL:", page.url)

#     # URL-level validation
#     assert "core_v2/ui" in page.url

#     print("Waiting for CORE UI to render...")

#     #  UI-level wait (MUST be before Playwright closes)
#     page.wait_for_selector("body", timeout=120_000)

#     print("CORE app launched successfully")

#     input("Press ENTER to close browser...")

#     context.close()


def test_core_ui_launch(authenticated_page):
    page = authenticated_page

    # Assert CORE UI loaded
    assert "core_v2/ui" in page.url
