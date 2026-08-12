from modules.analytical_plan.pages.analytical_plan import AnalyticalPlanPage
from test_data.UAP_test_data.analytical_plan_test_data import UAP_FILES
from playwright.sync_api import expect
import logging
import allure

logger = logging.getLogger(__name__)


@allure.title("Verify that the user can save the UAP with the spec")
@allure.description("This test verifies that the user can save the UAP with the spec")
@allure.severity(allure.severity_level.CRITICAL)
def test_save_ap_spec(authenticated_page):
    """Test saving UAP with spec."""
    ap_page = AnalyticalPlanPage(authenticated_page)

    with allure.step("Search for project"):
        ap_page.search_project("Core QA Only")
        logger.info("Successfully searched for project")
        assert authenticated_page.url, "Page should be loaded after project search"

    with allure.step("Open Create AP"):
        ap_page.open_create_ap()
        logger.info("Opened Create AP dialog")
        # Verify dialog elements are visible
        expect(authenticated_page.locator("text=Create AP")).to_be_visible(timeout=5000)

    with allure.step("Select databases"):
        ap_page.select_databases(
            "MP_ODS_ISG_RITEAID_US_STORE_5_COREDEV",
            "MP_ODS_ISG_RITEAID_US_DMA_1_COREDEV",
        )
        logger.info("Databases selected successfully")
        assert authenticated_page.url, (
            "Page should remain loaded after database selection"
        )

    with allure.step("Import UAP file"):
        file_path = UAP_FILES["UAP_with_ADS_and_Spec"]
        # file_path = os.path.abspath(
        #     r"C:\Users\Harshal.Tandulkar\Downloads\Latest AP\RITE_AID_UNIFIED AP_Q3 2024_RealativeDMA.xlsx"
        # )
        ap_page.import_uap_file(file_path)
        logger.info(f"Imported UAP file: {file_path}")
        assert authenticated_page.url, "Page should remain loaded after file import"



    with allure.step("Select latest version"):
        ap_page.click_latest_version()
        logger.info("Selected latest version")
        assert authenticated_page.url, (
            "Page should remain loaded after version selection"
        )

    with allure.step("Click through Next buttons"):
        ap_page.click_next_button()
        logger.info("Navigated through workflow")
        assert authenticated_page.url, "Page should remain loaded after navigation"

    with allure.step("Fill reporting period"):
        ap_page.reporting_period_tab("1/9/2022", "1/9/2022", "5/25/2025")
        logger.info("Reporting period configured successfully")
        assert authenticated_page.url, (
            "Page should remain loaded after reporting period configuration"
        )

    with allure.step("Save AP with Spec"):
        ap_page.click_save_ap_spec()
        logger.info("Successfully saved AP with Spec")
        assert authenticated_page.url, "Page should remain loaded after save operation"
        logger.info("Test test_save_ap_spec completed successfully")

    with allure.step("Final save confirmation"):
        ap_page._confirm_save_dialog()
        logger.info("Confirmed save operation")
        assert authenticated_page.url, "Page should remain loaded after confirming save"



@allure.title("Verify that the user can save the UAP")
@allure.description("This test verifies that the user can save the UAP by unchecking the constraints sheet checkbox")
@allure.severity(allure.severity_level.CRITICAL)

def test_save_ap(authenticated_page):
    """Test saving UAP without spec."""
    ap_page = AnalyticalPlanPage(authenticated_page)

    with allure.step("Search for project"):
        ap_page.search_project("Core QA Only")
        logger.info("Successfully searched for project")
        assert authenticated_page.url, "Page should be loaded after project search"

    with allure.step("Open Create AP"):
        ap_page.open_create_ap()
        logger.info("Opened Create AP dialog")
        expect(authenticated_page.locator("text=Create AP")).to_be_visible(timeout=5000)

    # with allure.step("Select databases"):
    #     ap_page.select_databases(
    #         "MP_ODS_ISG_RITEAID_US_STORE_5_COREDEV",
    #         "MP_ODS_ISG_RITEAID_US_DMA_1_COREDEV",
    #     )
    #     logger.info("Databases selected successfully")
    #     assert authenticated_page.url, (
    #         "Page should remain loaded after database selection"
    #     )
    with allure.step("Select databases"):
        file_path = UAP_FILES["single_db_UAP"]
        ap_page.select_single_database(file_path)
        logger.info("Single database selected successfully")



    with allure.step("Import UAP file"):
        file_path = UAP_FILES["UAP_with_ADS"]
        # file_path = os.path.abspath(
        #     r"C:\Users\Harshal.Tandulkar\Downloads\Latest AP\RITE_AID_UNIFIED AP_Q3 2024_RealativeDMA.xlsx"
        # )
        ap_page.import_uap_file(file_path)
        logger.info(f"Imported UAP file: {file_path}")
        assert authenticated_page.url, "Page should remain loaded after file import"    

    with allure.step("Unselect constraints checkbox"):
        ap_page.unselect_constraints_checkbox()
        logger.info("Unselected constraints checkbox")
        assert authenticated_page.url, (
            "Page should remain loaded after unchecking constraints"   
        )
       
    with allure.step("Get Hydro message text with version info"):
        ap_page.get_hydro_message_text()  


    with allure.step("Extract version of UAP from the Hydro message"):   
        message = ap_page.get_hydro_message_text()
        generated_version = message.split()[2].replace(":", "")
        logger.info(f"Extracted version from hydro message: {generated_version}")


    with allure.step("Select the generated version of UAP"):
        ap_page.click_generated_version(generated_version)
        logger.info(f"Selected generated version: {generated_version}")
          
    
   
    # with allure.step("Select latest version"):
    #     ap_page.click_latest_version()
    #     logger.info("Selected latest version")
       

    with allure.step("Click through Next buttons"):
        ap_page.click_next_button()
        logger.info("Navigated through workflow")
        assert authenticated_page.url, "Page should remain loaded after navigation"

    with allure.step("Click Next button on reporting period tab"):
        ap_page.Next_button_Reporting_period()
        logger.info("Clicked Next button on reporting period tab")
        assert authenticated_page.url, "Page should remain loaded after clicking Next"  

    with allure.step("Save AP"):
        ap_page.click_save_ap()
        logger.info("Successfully saved AP")

    assert authenticated_page.url, "Page should remain loaded after save operation"
    logger.info("Test test_save_ap completed successfully")

