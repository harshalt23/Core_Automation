from modules.analytic_dataset.pages.analytic_dataset_locator import (
    AnalyticDatasetLocator,
)
from playwright.sync_api import Page
import logging

logger = logging.getLogger(__name__)


class AnalyticalDatasetPage:
    """Page Object for Analytic Dataset module"""

    def __init__(self, page: Page):
        self.page = page
        self.locator = AnalyticDatasetLocator(page)

    def open_analytic_dataset(self):
        """Open the Analytic Dataset section."""
        try:
            logger.info("Opening Analytic Dataset section")
            self.locator.search_box.wait_for(state="visible", timeout=5000)
            self.locator.search_box.click()
            self.locator.search_box.fill("core")
            self.locator.core_qa_only.wait_for(state="visible", timeout=5000)
            self.locator.core_qa_only.click()
            self.locator.analytic_dataset_section.wait_for(
                state="visible", timeout=5000
            )
            self.locator.analytic_dataset_section.click()
            self.locator.expand_all_button.wait_for(state="visible", timeout=5000)
            self.locator.expand_all_button.click()
            self.locator.collapse_all_button.wait_for(state="visible", timeout=5000)
            self.locator.collapse_all_button.click()
            self.locator.expand_all_button.wait_for(state="visible", timeout=5000)
            self.locator.expand_all_button.click()
            self.locator.ads_builder.wait_for(state="visible", timeout=5000)
            self.locator.ads_builder.click()
            self.locator.ads_archive.wait_for(state="visible", timeout=5000)
            self.locator.ads_archive.click()
            self.locator.collapse_all_button.wait_for(state="visible", timeout=5000)
            self.locator.collapse_all_button.click()
            self.locator.expand_all_button.wait_for(state="visible", timeout=5000)
            self.locator.expand_all_button.click()
            logger.info("Successfully opened Analytic Dataset section")
        except Exception as e:
            logger.error(f"Failed to open Analytic Dataset: {str(e)}")
            raise

    def search_project(self, project_name: str):
        """Search for a project by name."""
        try:
            logger.info(f"Searching for project: {project_name}")
            self.locator.search_box.wait_for(state="visible", timeout=5000)
            self.locator.search_box.fill(project_name)
            self.locator.core_qa_only.wait_for(state="visible", timeout=5000)
            self.locator.core_qa_only.click()
            self.page.wait_for_timeout(3000)
            analytic_dataset_text = self.page.get_by_text(
                "Analytic Dataset", exact=True
            ).first
            analytic_dataset_text.wait_for(state="visible", timeout=5000)
            analytic_dataset_text.click()
            logger.info(f"Successfully found and clicked project: {project_name}")
        except Exception as e:
            logger.error(f"Failed to search project {project_name}: {str(e)}")
            raise

    def open_ads_builder(self):
        """Open ADS Builder."""
        try:
            logger.info("Opening ADS Builder")
            self.locator.ads_builder.wait_for(state="visible", timeout=5000)
            self.locator.ads_builder.click()
            logger.info("Successfully opened ADS Builder")
        except Exception as e:
            logger.error(f"Failed to open ADS Builder: {str(e)}")
            raise

    def select_uap(self):
        """Select UAP file."""
        try:
            logger.info("Selecting UAP file")
            self.locator.uap_selector.wait_for(state="visible", timeout=5000)
            self.locator.uap_selector.click()
            logger.info("Successfully selected UAP file")
        except Exception as e:
            logger.error(f"Failed to select UAP: {str(e)}")
            raise

    def spend_support_toggle(self):
        """Toggle spend support to No."""
        try:
            logger.info("Toggling spend support to No")
            self.locator.spend_support_no.wait_for(state="visible", timeout=5000)
            self.locator.spend_support_no.click()
            logger.info("Successfully toggled spend support")
        except Exception as e:
            logger.error(f"Failed to toggle spend support: {str(e)}")
            raise

    def enter_input(self):
        """Enter ADS name and description."""
        try:
            logger.info("Entering ADS details")
            self.locator.ads_name_field.wait_for(state="visible", timeout=5000)
            self.locator.ads_name_field.click()
            self.locator.ads_name_field.fill("Automation_ADS")
            logger.info("Entered ADS name")

            self.locator.description_field.wait_for(state="visible", timeout=5000)
            self.locator.description_field.click()
            self.locator.description_field.fill("ADS created by Automation")
            logger.info("Entered ADS description")
        except Exception as e:
            logger.error(f"Failed to enter ADS details: {str(e)}")
            raise

    def select_dates_from_calender(self):
        """Select start and end dates."""
        try:
            logger.info("Selecting dates from calendar")
            self.locator.start_date_field.wait_for(state="visible", timeout=5000)
            self.locator.start_date_field.click()
            self.locator.start_date_field.fill("1/9/2022")
            logger.info("Set start date: 1/9/2022")

            self.locator.end_date_field.wait_for(state="visible", timeout=5000)
            self.locator.end_date_field.click()
            self.locator.end_date_field.fill("5/25/2025")
            logger.info("Set end date: 5/25/2025")
        except Exception as e:
            logger.error(f"Failed to select dates: {str(e)}")
            raise

    def select_model_category(self):
        """Select model categories and options."""
        try:
            logger.info("Selecting model categories")
            self.locator.model_categories_radio.wait_for(state="visible", timeout=5000)
            self.locator.model_categories_radio.check()
            logger.info("Checked Model Categories radio")

            self.locator.dropdown_value_container.wait_for(
                state="visible", timeout=5000
            )
            self.locator.dropdown_value_container.click()
            self.locator.model_category_option.wait_for(state="visible", timeout=5000)
            self.locator.model_category_option.click()
            logger.info("Selected ModelCategory-1")

            self.locator.dropdown_indicator_separator.wait_for(
                state="visible", timeout=5000
            )
            self.locator.dropdown_indicator_separator.click()
            self.locator.demo_category_option.wait_for(state="visible", timeout=5000)
            self.locator.demo_category_option.click()
            logger.info("Selected DemoCategory1")

            self.locator.demo_category_filter.wait_for(state="visible", timeout=5000)
            self.locator.demo_category_filter.click()
            self.locator.category1_option.wait_for(state="visible", timeout=5000)
            self.locator.category1_option.click()
            logger.info("Selected Category1")

            self.locator.category_checkbox.wait_for(state="visible", timeout=5000)
            self.locator.category_checkbox.check()
            logger.info("Checked category checkbox")
        except Exception as e:
            logger.error(f"Failed to select model categories: {str(e)}")
            raise

    def click_on_generate(self):
        """Click the Generate button."""
        try:
            logger.info("Clicking Generate button")
            self.locator.generate_button.wait_for(state="visible", timeout=5000)
            self.locator.generate_button.click()
            logger.info("Successfully clicked Generate button")
        except Exception as e:
            logger.error(f"Failed to click Generate button: {str(e)}")
            raise
