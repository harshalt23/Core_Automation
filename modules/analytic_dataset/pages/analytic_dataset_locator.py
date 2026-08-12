import re
from playwright.sync_api import Page


class AnalyticDatasetLocator:
    """Page Object for Analytic Dataset locators"""

    def __init__(self, page: Page):
        self.page = page

        # Main Navigation & Search
        self.search_box = page.get_by_role("textbox", name="Search")
        self.core_qa_only = page.get_by_text("Core QA Only")
        self.analytic_dataset_section = (
            page.locator("div").filter(has_text=re.compile(r"^Analytic Dataset$")).first
        )

        # Expand/Collapse
        self.expand_all_button = page.get_by_text("Expand All")
        self.collapse_all_button = page.get_by_text("Collapse All")

        # ADS Options
        self.ads_builder = page.get_by_text("ADS Builder").nth(1)
        self.ads_archive = page.get_by_text("ADS Archive").nth(1)

        # UAP Selection
        self.uap_selector = page.get_by_text("V_2978 RITE_AID_UNIFIED AP_Q3")

        # Spend Support Toggle
        self.spend_support_no = page.get_by_text("No", exact=True)

        # Input Fields
        self.ads_name_field = page.get_by_role("textbox", name="Max 15 characters...")
        self.description_field = page.get_by_role("textbox", name="Description...")

        # Date Fields
        self.start_date_field = page.get_by_role("textbox").nth(3)
        self.end_date_field = page.get_by_role("textbox").nth(4)

        # Model Categories
        self.model_categories_radio = page.get_by_role("radio", name="Model Categories")

        # Dropdown Fields
        self.dropdown_value_container = page.locator(".dd__value-container")
        self.dropdown_indicator_separator = page.locator(
            ".dd__control.css-yk16xz-control > .dd__indicators > .dd__indicator-separator"
        )

        # Category Options
        self.model_category_option = page.get_by_text("ModelCategory-1", exact=True)
        self.demo_category_option = page.get_by_text("DemoCategory1", exact=True)
        self.demo_category_filter = (
            page.locator("div").filter(has_text=re.compile(r"^DemoCategory1$")).nth(1)
        )
        self.category1_option = page.get_by_text("Category1", exact=True)

        # Checkbox
        self.category_checkbox = page.get_by_role("checkbox").first

        # Action Buttons
        self.generate_button = page.get_by_text("Generate")
