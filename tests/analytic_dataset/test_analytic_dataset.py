from modules.analytic_dataset.pages.analytic_dataset import AnalyticalDatasetPage
from playwright.sync_api import expect
import logging
import allure

logger = logging.getLogger(__name__)


@allure.title("Verify that the user can create an Analytic Dataset")
@allure.description(
    "This test verifies the complete flow of creating an Analytic Dataset with all required configurations"
)
@allure.severity(allure.severity_level.CRITICAL)
def test_create_analytic_dataset(authenticated_page):
    """Test creating an Analytic Dataset."""
    ads_page = AnalyticalDatasetPage(authenticated_page)

    with allure.step("Search for project"):
        ads_page.search_project("core")
        logger.info("Successfully searched for project")
        expect(authenticated_page.locator("text=Analytic Dataset")).to_be_visible(
            timeout=5000
        )

    with allure.step("Open ADS Builder"):
        ads_page.open_ads_builder()
        logger.info("Opened ADS Builder")
        expect(authenticated_page.locator("text=ADS Builder")).to_be_visible(
            timeout=5000
        )

    with allure.step("Select UAP file"):
        ads_page.select_uap()
        logger.info("Selected UAP file")
        expect(
            authenticated_page.locator("text=V_2978 RITE_AID_UNIFIED AP_Q3")
        ).to_be_visible(timeout=5000)

    with allure.step("Toggle spend support"):
        ads_page.spend_support_toggle()
        logger.info("Toggled spend support to No")
        expect(authenticated_page.locator("text=No")).to_be_visible(timeout=5000)

    with allure.step("Enter ADS details"):
        ads_page.enter_input()
        logger.info("Entered ADS name and description")
        ads_name = authenticated_page.get_by_role(
            "textbox", name="Max 15 characters..."
        )
        expect(ads_name).to_have_value("Test ADS", timeout=5000)

    with allure.step("Select dates from calendar"):
        ads_page.select_dates_from_cal()
        logger.info("Selected start and end dates")
        expect(authenticated_page.locator("text=1/9/2022")).to_be_visible(timeout=5000)

    with allure.step("Select model categories"):
        ads_page.select_model_cat()
        logger.info("Selected all required model categories")
        expect(
            authenticated_page.get_by_role("radio", name="Model Categories")
        ).to_be_checked(timeout=5000)

    with allure.step("Click Generate button"):
        ads_page.click_on_generate()
        logger.info("Clicked Generate button successfully")
        expect(authenticated_page.locator("text=Generate")).to_be_visible(timeout=5000)
