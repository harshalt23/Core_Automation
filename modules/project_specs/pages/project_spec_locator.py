from playwright.sync_api import Page


class ProjectSpecLocator:
    """Page Object for Project Spec locators"""

    def __init__(self, page: Page):
        self.page = page

        # Search and Navigation
        self.search_bar = page.get_by_role("textbox", name="Search")
        self.project_spec_button = page.get_by_text("Project Specs").first

        # Model Key Dropdown
        # NOTE: Using generic SVG selector - consider updating to:
        # - page.locator("button[aria-label*='model']") if available
        # - page.locator("[data-testid='model-key-dropdown']") if available
        self.model_key_dropdown = page.locator("svg").first

        # Save Options
        self.save_button = page.get_by_role("button", name=" Save")
        self.save_option = page.locator("div.dropdown-item", has_text="Save")
        self.save_as_draft_option = page.get_by_text("Save As Draft")
        self.save_and_run_option = page.get_by_text("Save And Run")

        # Import/Export
        self.import_button = page.get_by_text("Import")
        self.file_input = page.locator("input[type='file']")
        self.ok_button = page.get_by_text("Ok", exact=True)

        # ADS Selection
        self.ads_dropdown = page.locator("svg").nth(1)

        # Messages
        self.hydro_message = page.locator("div.alert.alert-hydro-msg")

        # Input Fields
        self.alias_input = page.locator("input.pd-l-7").first

        # Checkbox Options
        self.exclude_zero_dependent_checkbox = page.get_by_text(
            "Exclude Zero Dependent"
        )
        self.include_randomization_checkbox = page.get_by_text(
            "Include Randomization Level"
        )
        self.borrow_transformation_checkbox = page.get_by_text("Borrow Transformation")
        self.recalibration_to_national_checkbox = page.get_by_text(
            "Recalibration to National"
        )
        self.base_settings_checkbox = page.get_by_text("Base Settings")
        self.include_intercept_checkbox = page.get_by_text("Include Intercept")

        # Granular Spec
        self.granular_spec_button = page.get_by_text("Granular Spec")
        self.generate_new_button = page.get_by_text("Generate New")
        self.global_option = page.get_by_text("GLOBAL").first
        self.ex_sea_option = page.get_by_text("EX_SEA")
        self.override_option = page.get_by_text("OVERRIDE")

        # Latest Spec
        self.open_latest_spec_button = page.get_by_text("Open Latest Spec")
        self.select_latest_spec_locator = page.locator(
            "button.saveblue.btn.btn-secondary"
        )
