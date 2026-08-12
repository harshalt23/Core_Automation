from playwright.sync_api import Page
from modules.analytical_plan.pages.analytical_plan_locator import AnalyticalPlanLocator
import logging

logger = logging.getLogger(__name__)


class AnalyticalPlanPage:
    """Page Object for Analytical Plan module"""

    def __init__(self, page: Page):
        self.page = page
        self.locator = AnalyticalPlanLocator(page)

    def open_analytic_plan(self):
        """Open the Analytical Plan tab."""
        try:
            logger.info("Opening Analytic Plan tab")
            self.locator.analytic_plan_tab.wait_for(state="visible", timeout=5000)
            self.locator.analytic_plan_tab.click()
            logger.info("Successfully opened Analytic Plan tab")
        except Exception as e:
            logger.error(f"Failed to open Analytic Plan tab: {str(e)}")
            raise

    def search_project(self, project_name: str):
        """Search for a project by name."""
        try:
            logger.info(f"Searching for project: {project_name}")
            # self.locator.search_box.wait_for(state="visible", timeout=5000)
            self.locator.search_box.fill(project_name)
            project_option = self.page.get_by_text(project_name, exact=True)
            project_option.wait_for(state="visible", timeout=5000)
            project_option.click()
            logger.info(f"Successfully found and clicked project: {project_name}")
        except Exception as e:
            logger.error(f"Failed to search project {project_name}: {str(e)}")
            raise

    def open_create_ap(self):
        """Open Create Analytical Plan dialog."""
        try:
            logger.info("Opening Create AP dialog")
            self.locator.chart_line_icon.wait_for(state="visible", timeout=5000)
            self.locator.chart_line_icon.click()
            self.locator.create_ap_button.wait_for(state="visible", timeout=5000)
            self.locator.create_ap_button.click()
            logger.info("Successfully opened Create AP dialog")
        except Exception as e:
            logger.error(f"Failed to open Create AP dialog: {str(e)}")
            raise

    def select_databases(self, primary_db: str, secondary_db: str):
        """Select primary and secondary databases."""
        try:
            logger.info(
                f"Selecting databases - Primary: {primary_db}, Secondary: {secondary_db}"
            )
            self.locator.select_primary_db.wait_for(state="visible", timeout=5000)
            self.locator.select_primary_db.click()
            logger.info("Clicked on Select Primary DB")
            primary_option = self.page.get_by_text(primary_db, exact=True)
            primary_option.wait_for(state="visible", timeout=5000)
            primary_option.click()
            logger.info(f"Selected primary database: {primary_db}")

            self.locator.select_secondary_db.wait_for(state="visible", timeout=5000)
            self.locator.select_secondary_db.click()
            logger.info("Clicked on Select Secondary DB")
            secondary_option = self.page.get_by_text(secondary_db, exact=True)
            secondary_option.wait_for(state="visible", timeout=5000)
            secondary_option.click()
            logger.info(f"Selected secondary database: {secondary_db}")
        except Exception as e:
            logger.error(f"Failed to select databases: {str(e)}")
            raise

    def select_single_database(self, database: str):  
        """Select a single database when only one is required."""
        try:
            logger.info(f"Selecting single database: {database}")
            self.locator.select_primary_db.wait_for(state="visible", timeout=5000)
            self.locator.select_primary_db.click()
            logger.info("Clicked on Select Primary DB")
            db_option = self.page.get_by_text(database, exact=True)
            db_option.wait_for(state="visible", timeout=5000)
            db_option.click()
            logger.info(f"Selected database: {database}")
        except Exception as e:
            logger.error(f"Failed to select database: {str(e)}")
            raise  

    def import_uap_file(self, file_path: str):
        """Import UAP file."""
        try:
            logger.info(f"Importing UAP file: {file_path}")
            self.locator.import_template_button.wait_for(state="visible", timeout=5000)
            self.locator.import_template_button.click()
            logger.info("Clicked Import Template button")
            self.locator.file_input.wait_for(state="attached", timeout=5000)
            self.locator.file_input.set_input_files(file_path)
            logger.info(f"File set: {file_path}")
            self.locator.upload_button.wait_for(state="visible", timeout=5000)
            self.locator.upload_button.click()
            logger.info("Clicked upload button")
            self.page.wait_for_load_state("networkidle")
            logger.info("UAP file uploaded successfully")
        except Exception as e:
            logger.error(f"Failed to import UAP file: {str(e)}")
            raise

    def unselect_constraints_checkbox(self):
        """Uncheck the Constraint Sheet checkbox."""
        try:
            logger.info("Unchecking Constraint Sheet checkbox")
            self.locator.uncheck_Select_worksheets_checkbox.wait_for(
                state="visible", timeout=5000
            )
            self.locator.uncheck_Select_worksheets_checkbox.click()
            logger.info("Constraint Sheet checkbox unchecked")
            self.page.wait_for_load_state("networkidle")
            # self.locator.constraint_sheet_text.wait_for(state="visible", timeout=5000)
            # self.locator.constraint_sheet_text.click()
            # self.locator.workbook_sheet_dropdown.wait_for(state="visible", timeout=5000)
            # self.locator.workbook_sheet_dropdown.click()
            # logger.info("Successfully unselected constraints")
        except Exception as e:
            logger.error(f"Failed to unselect constraints checkbox: {str(e)}")
            raise

    def get_hydro_message_text(self):
        """Get the hydro message as text"""
        try:
            
            message_locator = self.locator.hydro_message

            message_locator.wait_for(state="attached", timeout=100000)

            message_text = message_locator.inner_text()

            logger.info(f"Hydro message text: {message_text}")

            print(f"Hydro message text:{message_text}")

            return message_text
        
        except Exception as e:
            logger.error(f"Failed to get hydro message text: {str(e)}")
            raise


    def get_hydro_message_uap(self, hydro_text: str):
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

    def click_generated_version(self, version: str):
        """Click on the generated version of UAP."""
        try:
            logger.info(f"Clicking on generated version: {version}")
            version_generated = self.page.locator(f"div.wd-70:not(.ps-relative):has-text('{version}')") # this is the dynamic locator for the generated version based on the version number extracted from the hydro message
            version_generated.wait_for(state="visible", timeout=5000) #Dynamic locators should be created inside methods using self.page
            version_generated.click()
            logger.info(f"Successfully clicked on generated version: {version}")
        except Exception as e:
            logger.error(f"Failed to click generated version: {str(e)}")
            raise       

    def click_latest_version(self):
        """Select the latest version of the file."""
        try:
            logger.info("Clicking on latest version")
            self.locator.latest_version.wait_for(state="visible", timeout=5000)
            self.locator.latest_version.click()
            logger.info("Successfully selected latest version")
        except Exception as e:
            logger.error(f"Failed to click latest version: {str(e)}")
            raise

    # def click_next_button(self):
    #     """Click through all Next buttons in the workflow."""
    #     try:
    #         logger.info("Starting to click Next buttons")
    #         next_buttons = [
    #             logger.info("Clicking on the Next button present in DataSource"),
    #             self.locator.next_button,
    #             logger.info("Clicking on the Next button present in the Models"),
    #             self.locator.next_button,
    #             logger.info("Clicking on the Next button present in the Dependent"),
    #             self.locator.chevron_right_button,
    #             logger.info("Clicking on the Next button present in the Variables"),
    #             self.locator.next_exact_button,
    #             logger.info("Clicking on the Next button present in the Relative Geo"),
    #             self.locator.next_button,
    #             logger.info("Clicking on the Next button present in the Buckets"),
    #             self.locator.next_button,
    #             logger.info("Clicking on the Next button present in the Reporting Period"),
    #             self.locator.next_button]
            
    #         for i, button in enumerate(next_buttons):
    #             button.wait_for(state="visible", timeout=5000)
    #             button.click()
    #             logger.info(f"Clicked Next button {i + 1}/7")
    #         logger.info("Successfully clicked through all Next buttons")
    #     except Exception as e:
    #         logger.error(f"Failed to click Next buttons: {str(e)}")
    #         raise
    def click_next_button(self):
        """Click through all Next buttons in the workflow."""
        try:
            logger.info("Starting to click Next buttons")

            steps = [
                ("DataSource", self.locator.next_button),
                ("Models", self.locator.next_button),
                ("Dependent", self.locator.chevron_right_button),
                ("Variables", self.locator.next_exact_button),
                ("Relative Geo", self.locator.next_button),
                ("Buckets", self.locator.next_button),
                ("Reporting Period", self.locator.next_button)
                ]

            for i, (step_name, button) in enumerate(steps):
                logger.info(f"Clicking on the Next button present in {step_name}")

                button.wait_for(state="visible", timeout=5000)
                button.click()

                logger.info(f"Clicked Next button {i + 1}/8")

            logger.info("Successfully clicked through all Next buttons")

        except Exception as e:
            logger.error(f"Failed to click Next buttons: {str(e)}")
            raise

    def reporting_period_tab(
        self, trans_date: str, model_start_date: str, model_end_date: str
    ):
        """Fill reporting period tab with model keys and dates."""
        try:
            logger.info("Starting reporting period tab configuration")

            # Select Model Keys
            logger.info("Selecting model keys")
            self.locator.select_model_keys.wait_for(state="visible", timeout=5000)
            self.locator.select_model_keys.click()
            self.locator.front_end_sales.wait_for(state="visible", timeout=5000)
            self.locator.front_end_sales.click()
            self.locator.riteaid_com.wait_for(state="visible", timeout=5000)
            self.locator.riteaid_com.click()
            self.locator.pharmacy.wait_for(state="visible", timeout=5000)
            self.locator.pharmacy.click()
            self.locator.immunization.wait_for(state="visible", timeout=5000)
            self.locator.immunization.click()
            self.locator.front_end_transactions.wait_for(state="visible", timeout=5000)
            self.locator.front_end_transactions.click()
            self.locator.riteaid_com_transactions.wait_for(
                state="visible", timeout=5000
            )
            self.locator.riteaid_com_transactions.click()

            # Fill Date Fields
            self.locator.overflow_container.wait_for(state="visible", timeout=5000)
            self.locator.overflow_container.click()
            self.locator.calendar_icon.wait_for(state="visible", timeout=5000)
            self.locator.calendar_icon.click()

            # Transaction Date
            trans_textbox = self.locator.type_or_select_textbox_first
            trans_textbox.wait_for(state="visible", timeout=5000)
            trans_textbox.click()
            trans_textbox.fill(trans_date)
            trans_textbox.click()
            trans_textbox.press("Enter")
            logger.info(f"Set transaction date: {trans_date}")

            # Model Start Date
            start_textbox = self.locator.type_or_select_textbox_second
            start_textbox.wait_for(state="visible", timeout=5000)
            start_textbox.click()
            start_textbox.fill(model_start_date)
            logger.info(f"Set model start date: {model_start_date}")

            # Model End Date
            end_textbox = self.locator.type_or_select_textbox_third
            end_textbox.wait_for(state="visible", timeout=5000)
            end_textbox.click()
            end_textbox.fill(model_end_date)
            end_textbox.press("Enter")
            logger.info(f"Set model end date: {model_end_date}")

            # Fill Name and Tag
            self.locator.enter_name_field.wait_for(state="visible", timeout=5000)
            self.locator.enter_name_field.click()
            self.locator.enter_name_field.fill("FY 2022")
            self.locator.enter_tag_field.wait_for(state="visible", timeout=5000)
            self.locator.enter_tag_field.click()
            self.locator.enter_tag_field.fill("FY")

            # Fill Start/End Dates
            self.locator.select_start_date_field.wait_for(state="visible", timeout=5000)
            self.locator.select_start_date_field.click()
            self.locator.select_start_date_field.fill(model_start_date)
            self.locator.select_end_date_field.wait_for(state="visible", timeout=5000)
            self.locator.select_end_date_field.click()
            self.locator.select_end_date_field.fill(model_end_date)

            self.locator.update_button.click()
            self.locator.next_button.click()
            logger.info("Successfully completed reporting period tab")
        except Exception as e:
            logger.error(f"Failed to fill reporting period tab: {str(e)}")
            raise
    def Next_button_Reporting_period(self):
        """Click on Next button on reporting period tab."""
        try:
            logger.info("Clicking Next button on reporting period tab")
            self.locator.next_button.wait_for(state="visible", timeout=5000)
            self.locator.next_button.click()
            logger.info("Successfully clicked Next button on reporting period tab")
        except Exception as e:
            logger.error(f"Failed to click Next button: {str(e)}")
            raise    

    def click_save_draft(self):
        """Save the analytical plan as draft."""
        try:
            logger.info("Clicking Save Draft")
            self.locator.save_dropdown_toggle.wait_for(state="visible", timeout=5000)
            self.locator.save_dropdown_toggle.click()
            self.locator.save_draft_option.wait_for(state="visible", timeout=5000)
            self.locator.save_draft_option.click()
            logger.info("Successfully saved as draft")
        except Exception as e:
            logger.error(f"Failed to save draft: {str(e)}")
            raise

    def click_save_ap(self):
        """Save the analytical plan."""
        try:
            logger.info("Clicking Save AP")
            self.locator.save_dropdown_toggle.click()
            self.locator.save_ap_option.wait_for(state="visible", timeout=5000)
            self.locator.save_ap_option.click()
            logger.info("Clicked Save AP option")
            self._confirm_save_dialog()
            logger.info("Successfully saved AP")
        except Exception as e:
            logger.error(f"Failed to save AP: {str(e)}")
            raise

    def click_save_ap_spec(self):
        """Save analytical plan and spec."""
        try:
            logger.info("Clicking Save AP & Spec")
            self.locator.save_dropdown_toggle.wait_for(state="visible", timeout=5000)
            self.locator.save_dropdown_toggle.click()
            # self.locator.save_ap_spec_option.wait_for(state="visible", timeout=5000)
            self.locator.save_ap_spec_option.click()
            logger.info("Clicked Save AP & Spec option")
            self._confirm_save_dialog()
            logger.info("Successfully saved AP & Spec")
        except Exception as e:
            logger.error(f"Failed to save AP & Spec: {str(e)}")
            raise

    def _confirm_save_dialog(self):
        """Confirm save in the popup dialog."""
        try:
            logger.info("Confirming save dialog")
            # dialog = self.locator.save_confirmation_dialog
            # dialog.wait_for(state="visible", timeout=10000)
            self.locator.confirm_save_button.click(force=True)
            logger.info("Save confirmed")
        except Exception as e:
            logger.error(f"Failed to confirm save dialog: {str(e)}")
            raise

    def download_uap(self):
        """Download the UAP file."""
        try:
            logger.info("Clicking download button")
            self.locator.download_button.wait_for(state="visible", timeout=5000)
            self.locator.download_button.click()
            logger.info("Successfully initiated UAP download")
        except Exception as e:
            logger.error(f"Failed to download UAP: {str(e)}")
            raise

    def get_status(self):
        """Get the status of the UAP."""
        try:
            logger.info("Getting UAP status")
            status = self.locator.draft_status
            status.wait_for(state="visible", timeout=5000)
            logger.info("Successfully retrieved UAP status")
            return status
        except Exception as e:
            logger.error(f"Failed to get status: {str(e)}")
            raise
