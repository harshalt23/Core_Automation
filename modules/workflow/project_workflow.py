from Core_Automation.test_data.UAP_test_data.analytical_plan_test_data import UAP_FILES
from modules.home.pages.home import HomePage
from modules.analytical_plan.pages.analytical_plan import AnalyticalPlanPage
from modules.analytic_dataset.pages.analytic_dataset import AnalyticalDatasetPage
from modules.project_specs.pages.project_specs import ProjectSpec
import logging
import allure
from playwright.sync_api import Page
logger=logging.getLogger(__name__)

class FullCoreWorkflow:

    def __init__(self,page:Page):
        self.page=page
        self.home = HomePage(page)
        self.ap = AnalyticalPlanPage(page)
        self.ads =AnalyticalDatasetPage(page)
        self.ps = ProjectSpec(page)
    
        def run_uap_workflow(self,project_name:str,ap_file_path:str,reporting_period:tuple,primary_db:str,secondary_db:str):
           """Test saving UAP with spec."""
        try:
            with allure.step("Search for project"):
                self.ap.search_project("Core QA Only")
                logger.info("Successfully searched for project")
       
            with allure.step("Open Create AP"):
                self.ap.open_create_ap()
                logger.info("Opened Create AP dialog")
                # Verify dialog elements are visible
     

            with allure.step("Select databases"):
                self.ap .select_databases(
                "MP_ODS_ISG_RITEAID_US_STORE_5_COREDEV",
                "MP_ODS_ISG_RITEAID_US_DMA_1_COREDEV",
             )
                logger.info("Databases selected successfully")
       
        

            with allure.step("Import UAP file"):
                file_path = UAP_FILES["UAP_with_ADS_and_Spec"]
                # file_path = os.path.abspath(
                #     r"C:\Users\Harshal.Tandulkar\Downloads\Latest AP\RITE_AID_UNIFIED AP_Q3 2024_RealativeDMA.xlsx"
            # )
                self.ap.import_uap_file(file_path)
                logger.info(f"Imported UAP file: {file_path}")
        

            with allure.step("Select latest version"):
                self.ap.click_latest_version()
                logger.info("Selected latest version")
     

            with allure.step("Click through Next buttons"):
                self.ap.click_next_button()
                logger.info("Navigated through workflow")
     

            with allure.step("Fill reporting period"):
                self.ap.reporting_period_tab("1/9/2022", "1/9/2022", "5/25/2025")
                logger.info("Reporting period configured successfully")
      

            with allure.step("Save AP with Spec"):
                self.ap .click_save_ap_spec()
                logger.info("Successfully saved AP with Spec")
       
            with allure.step("Final save confirmation"):
                self.ap._confirm_save_dialog()
                logger.info("Confirmed save operation")
        except Exception as e:
            logger.error(f"Error during UAP workflow execution: {str(e)}")   
            raise        
       

    def run_ads_workflow(self):
        try:
            with allure.step("Creating Analytic Dataset with Spend Support template"):
                self.ads.spend_support_toggle()
                logger.info("Enabled Spend Support toggle for ADS")
            with allure.step("Selecting UAP in the ADS bulder to create AD"):   
                self.ads.select_uap()
                logger.info("Selected UAP for ADS")
            with allure.step("Entering input fields, selecting dates and model categories for ADS, and generating the dataset"):    
                self.ads.enter_input()
                logger.info("Entered input fields for ADS")
            with allure.step("Selecting start and end dates for ADS"):    
                self.ads.select_dates_from_calender()
                logger.info("Selected start and end dates for ADS")
            with allure.step("Selecting model categories and generating ADS"):    
                self.ads.select_model_category()
                logger.info("Selected model categories for ADS")
            with allure.step("Clicking on Generate button to create ADS"):    
                self.ads.click_on_generate()
                logger.info("Clicked on Generate button for ADS and Spend Support template")
         
        except Exception as e:
            logger.error(f"Error during ADS Creation:{str(e)}") 
            raise

    def run_spec_workflow(self):
        try:
          
            with allure.step("Searching the project in the search bar"):
                self.ps.search_project("YTL 2026 June")

            with allure.step("Clicking on the project spec"):
               self.ps.click_project_spec()

            with allure.step("Selecting the model key"):
                self.ps.model_key_selection("Demo_Key1")
            
            with allure.step("Selecting the latest spec by clicking the select latest spec button"):
                self.ps.select_latest_spec()

            with allure.step(f"Saving spec as Save and Run"):
                self.ps.save_and_run_spec()
                logger.info("Saved and ran the spec successfully")


        except Exception as e:
                logger.error(f"Error during Project Spec workflow execution: {str(e)}")   
                raise     





        




        