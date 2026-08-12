from playwright.sync_api import Page


class HomePage:
    def __init__(self, page: Page):
        self.page = page

    def wait_for_home_to_load(self):
        self.page.locator("input[placeholder='Search']").wait_for(
            state="visible", timeout=15000
        )

    def search_project(self, project_name: str):
        project_name = project_name.strip()

        search = self.page.locator("input[placeholder='Search']")
        search.fill("")
        search.fill(project_name)

        # Allow debounce filtering to complete
        self.page.wait_for_timeout(10000)

    def expand_project(self, project_name):
        project = self.page.locator(f"text={project_name}").first
        project.wait_for(state="visible", timeout=10000)

        plus_icon = project.locator(
            "xpath=preceding::i[contains(@class,'fa-plus-square')]"
        ).first

        if plus_icon.is_visible():
            plus_icon.click()
