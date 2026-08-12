from playwright.sync_api import Page
from modules.project_specs.pages.project_spec_locator import ProjectSpecLocator
import logging

logger = logging.getLogger(__name__)


class ProjectSpec:
    def __init__(self, page: Page):
        self.page = page
        self.locator = ProjectSpecLocator(page)

    def search_project(self, project_name: str):
        """Search for a project by name."""
        try:
            logger.info(f"Searching for project: {project_name}")
            self.locator.search_bar.fill(project_name)
            self.page.get_by_text(project_name, exact=True).click()
            logger.info(f"Successfully found and clicked project: {project_name}")
        except Exception as e:
            logger.error(f"Failed to search project {project_name}: {str(e)}")
            raise

    def click_project_spec(self):
        """Click on the Project Spec button."""
        try:
            logger.info("Clicking on the Project Spec button")
            self.locator.project_spec_button.click()
            logger.info("Successfully clicked on Project Spec button")
        except Exception as e:
            logger.error(f"Failed to click Project Spec button: {str(e)}")
            raise

    def model_key_selection(self, model_key_name: str):
        """Select a model key from the dropdown."""
        try:
            logger.info(f"Starting model key selection: {model_key_name}")
            # Wait for dropdown to be visible instead of fixed timeout
            self.locator.model_key_dropdown.wait_for(state="visible", timeout=20000)
            logger.info("Model key dropdown is visible")
            self.locator.model_key_dropdown.click()
            logger.info("Clicked on model key dropdown")
            # Wait for option to appear
            model_key_option = self.page.get_by_title(model_key_name)
            model_key_option.wait_for(state="visible", timeout=5000)
            model_key_option.click()
            logger.info(f"Successfully selected model key: {model_key_name}")
        except Exception as e:
            logger.error(f"Failed to select model key {model_key_name}: {str(e)}")
            raise

    def select_latest_spec(self):
        """Select the latest spec from the list."""
        try:
            logger.info("Selecting latest spec")
            self.locator.select_latest_spec_locator.wait_for(
                state="visible", timeout=10000
            )
            self.locator.select_latest_spec_locator.click()
            logger.info("Clicked on select latest spec button")
            self.locator.open_latest_spec_button.wait_for(state="visible", timeout=5000)
            self.locator.open_latest_spec_button.click()
            logger.info("Successfully opened latest spec")
        except Exception as e:
            logger.error(f"Failed to select latest spec: {str(e)}")
            raise

    def save_spec(self):
        """Save the spec with normal save option."""
        try:
            logger.info("Saving spec with normal save option")
            self.locator.save_button.click()
            logger.info("Clicked on save dropdown")
            self.locator.save_option.wait_for(state="visible", timeout=5000)
            self.locator.save_option.click()
            logger.info("Successfully saved spec")
        except Exception as e:
            logger.error(f"Failed to save spec: {str(e)}")
            raise

    def save_draft_spec(self):
        """Save the spec as draft."""
        try:
            logger.info("Saving spec as draft")
            self.locator.save_button.click()
            logger.info("Clicked on save dropdown")
            self.locator.save_as_draft_option.wait_for(state="visible", timeout=5000)
            self.locator.save_as_draft_option.click()
            logger.info("Successfully saved spec as draft")
        except Exception as e:
            logger.error(f"Failed to save spec as draft: {str(e)}")
            raise

    def save_and_run_spec(self):
        """Save the spec and run it."""
        try:
            logger.info("Saving spec and running")
            self.locator.save_button.click()
            logger.info("Clicked on save dropdown")
            self.locator.save_and_run_option.wait_for(state="visible", timeout=5000)
            self.locator.save_and_run_option.click()
            logger.info("Successfully saved and ran spec")
        except Exception as e:
            logger.error(f"Failed to save and run spec: {str(e)}")
            raise

    def click_import(self):
        """Click on the Import button."""
        try:
            logger.info("Clicking on Import button")
            self.locator.import_button.click()
            logger.info("Import button clicked successfully")
        except Exception as e:
            logger.error(f"Failed to click Import button: {str(e)}")
            raise

    def import_spec(self, file_path: str):
        """Import spec file and close file dialog."""
        try:
            logger.info(f"Importing spec file: {file_path}")
            self.locator.ok_button.click()
            logger.info("Clicked OK button to open file dialog")
            self.locator.file_input.set_input_files(file_path)
            logger.info(f"File set: {file_path}")
            # Use Playwright's keyboard method instead of pyautogui
            self.page.keyboard.press("Escape")
            logger.info("Pressed Escape key to close dialog")
            # Wait for file upload to complete
            self.locator.hydro_message.wait_for(state="visible", timeout=5000)
            logger.info("Spec file uploaded successfully")
        except Exception as e:
            logger.error(f"Failed to import spec file: {str(e)}")
            raise

    def select_ads(self, ads_name: str):
        """Select ADS from the dropdown."""
        try:
            logger.info(f"Selecting ADS: {ads_name}")
            self.locator.ads_dropdown.click()
            logger.info("Clicked on ADS dropdown")
            ads_option = self.page.get_by_text(ads_name, exact=True)
            ads_option.wait_for(state="visible", timeout=5000)
            ads_option.click()
            logger.info(f"ADS selected successfully: {ads_name}")
        except Exception as e:
            logger.error(f"Failed to select ADS {ads_name}: {str(e)}")
            raise

    def get_hydro_message(self, hydro_text: str):
        """Get hydro success message by text."""
        try:
            logger.info(f"Getting hydro message: {hydro_text}")
            message = self.locator.hydro_message.filter(has_text=hydro_text)
            message.wait_for(state="visible", timeout=6000)
            logger.info(f"Hydro message found: {hydro_text}")
            return message
        except Exception as e:
            logger.error(f"Failed to get hydro message: {str(e)}")
            raise

    def alias_name(self, alias_text: str = "Test_Spec"):
        """Set alias name for the spec."""
        try:
            logger.info(f"Setting alias name: {alias_text}")
            self.locator.alias_input.wait_for(state="visible", timeout=5000)
            self.locator.alias_input.fill(alias_text)
            logger.info(f"Alias name set successfully: {alias_text}")
        except Exception as e:
            logger.error(f"Failed to set alias name: {str(e)}")
            raise

    def select_exclude_zero_dependent(self):
        """Select Exclude Zero Dependent checkbox."""
        try:
            logger.info("Selecting Exclude Zero Dependent checkbox")
            self.locator.exclude_zero_dependent_checkbox.wait_for(
                state="visible", timeout=5000
            )
            self.locator.exclude_zero_dependent_checkbox.click()
            logger.info("Exclude Zero Dependent checkbox selected successfully")
        except Exception as e:
            logger.error(f"Failed to select Exclude Zero Dependent checkbox: {str(e)}")
            raise

    def select_include_randomization_level(self):
        """Select Include Randomization Level checkbox."""
        try:
            logger.info("Selecting Include Randomization Level checkbox")
            self.locator.include_randomization_checkbox.wait_for(
                state="visible", timeout=5000
            )
            self.locator.include_randomization_checkbox.click()
            logger.info("Include Randomization Level checkbox selected successfully")
        except Exception as e:
            logger.error(
                f"Failed to select Include Randomization Level checkbox: {str(e)}"
            )
            raise

    def select_borrow_transformation(self):
        """Select Borrow Transformation checkbox."""
        try:
            logger.info("Selecting Borrow Transformation checkbox")
            self.locator.borrow_transformation_checkbox.wait_for(
                state="visible", timeout=5000
            )
            self.locator.borrow_transformation_checkbox.click()
            logger.info("Borrow Transformation checkbox selected successfully")
        except Exception as e:
            logger.error(f"Failed to select Borrow Transformation checkbox: {str(e)}")
            raise

    def select_recalibration_to_national(self):
        """Select Recalibration to National checkbox."""
        try:
            logger.info("Selecting Recalibration to National checkbox")
            self.locator.recalibration_to_national_checkbox.wait_for(
                state="visible", timeout=5000
            )
            self.locator.recalibration_to_national_checkbox.click()
            logger.info("Recalibration to National checkbox selected successfully")
        except Exception as e:
            logger.error(
                f"Failed to select Recalibration to National checkbox: {str(e)}"
            )
            raise

    def select_base_settings(self):
        """Select Base Settings checkbox."""
        try:
            logger.info("Selecting Base Settings checkbox")
            self.locator.base_settings_checkbox.wait_for(state="visible", timeout=5000)
            self.locator.base_settings_checkbox.click()
            logger.info("Base Settings checkbox selected successfully")
        except Exception as e:
            logger.error(f"Failed to select Base Settings checkbox: {str(e)}")
            raise

    def select_include_intercept(self):
        """Select Include Intercept checkbox."""
        try:
            logger.info("Selecting Include Intercept checkbox")
            self.locator.include_intercept_checkbox.wait_for(
                state="visible", timeout=5000
            )
            self.locator.include_intercept_checkbox.click()
            logger.info("Include Intercept checkbox selected successfully")
        except Exception as e:
            logger.error(f"Failed to select Include Intercept checkbox: {str(e)}")
            raise

    def open_granular_spec(self):
        """Open the Granular Spec option."""
        try:
            logger.info("Clicking on Granular Spec button")
            self.locator.granular_spec_button.wait_for(state="visible", timeout=5000)
            self.locator.granular_spec_button.click()
            logger.info("Granular Spec button clicked successfully")
        except Exception as e:
            logger.error(f"Failed to open Granular Spec: {str(e)}")
            raise

    def generate_new_granular_spec(self):
        """Click Generate New button for granular spec."""
        try:
            logger.info("Clicking on Generate New button")
            self.locator.generate_new_button.wait_for(state="visible", timeout=5000)
            self.locator.generate_new_button.click()
            logger.info("Generate New button clicked successfully")
        except Exception as e:
            logger.error(f"Failed to generate new granular spec: {str(e)}")
            raise

    def select_global_option(self):
        """Select GLOBAL option for granular spec."""
        try:
            logger.info("Selecting GLOBAL option")
            self.locator.global_option.wait_for(state="visible", timeout=5000)
            self.locator.global_option.click()
            logger.info("GLOBAL option selected successfully")
        except Exception as e:
            logger.error(f"Failed to select GLOBAL option: {str(e)}")
            raise

    def select_ex_sea_option(self):
        """Select EX_SEA option for granular spec."""
        try:
            logger.info("Selecting EX_SEA option")
            self.locator.ex_sea_option.wait_for(state="visible", timeout=5000)
            self.locator.ex_sea_option.click()
            logger.info("EX_SEA option selected successfully")
        except Exception as e:
            logger.error(f"Failed to select EX_SEA option: {str(e)}")
            raise

    def select_override_option(self):
        """Select OVERRIDE option for granular spec."""
        try:
            logger.info("Selecting OVERRIDE option")
            self.locator.override_option.wait_for(state="visible", timeout=5000)
            self.locator.override_option.click()
            logger.info("OVERRIDE option selected successfully")
        except Exception as e:
            logger.error(f"Failed to select OVERRIDE option: {str(e)}")
            raise

    def granular_spec(self):
        """Execute complete granular spec generation workflow."""
        try:
            logger.info("Starting granular spec generation workflow")
            self.open_granular_spec()
            self.generate_new_granular_spec()
            self.select_global_option()
            self.select_ex_sea_option()
            self.select_override_option()
            logger.info("Granular spec generation completed successfully")
        except Exception as e:
            logger.error(f"Failed to complete granular spec workflow: {str(e)}")
            raise

    def click_button(self, button_text: str):
        """Click on a button by text."""
        try:
            logger.info(f"Clicking on button: {button_text}")
            button = self.page.get_by_text(button_text)
            button.wait_for(state="visible", timeout=5000)
            button.click()
            logger.info(f"Button '{button_text}' clicked successfully")
        except Exception as e:
            logger.error(f"Failed to click button '{button_text}': {str(e)}")
            raise
