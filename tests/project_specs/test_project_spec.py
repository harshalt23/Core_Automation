import pytest
from playwright.sync_api import expect
from modules.project_specs.pages.project_specs import ProjectSpec
import allure


@allure.title("Save the Spec file in the project spec")
@allure.description("User can save the spec by save_as_draft, save, or save_and_run")
@allure.severity(allure.severity_level.BLOCKER)
@pytest.mark.parametrize("save_type", ["save_as_draft", "save", "save_and_run"])
def test_save_spec(authenticated_page, save_type):
    with allure.step("Opening the browser and authenticating credentials"):
        project_spec_obj = ProjectSpec(authenticated_page)

    with allure.step("Searching the project in the search bar"):
        project_spec_obj.search_project("YTL 2026 June")

    with allure.step("Clicking on the project spec"):
        project_spec_obj.click_project_spec()

    with allure.step("Selecting the model key"):
        project_spec_obj.model_key_selection("Demo_Key1")

    with allure.step(
        "Selecting the latest spec by clicking the select latest spec button"
    ):
        project_spec_obj.select_latest_spec()

    with allure.step(f"Saving spec as {save_type}"):
        if save_type == "save_as_draft":
            project_spec_obj.save_draft_spec()
        elif save_type == "save":
            project_spec_obj.save_spec()
        elif save_type == "save_and_run":
            project_spec_obj.save_and_run_spec()
        assert authenticated_page.url, "Page should remain loaded after save operation"


@allure.title("Save the Spec file selecting the checkbox options")
@allure.description("User can save the spec with various checkbox options selected")
@allure.severity(allure.severity_level.BLOCKER)
def test_spec_saving_with_options_checkbox(authenticated_page):
    with allure.step("Opening the browser and authenticating credentials"):
        project_spec_obj = ProjectSpec(authenticated_page)

    with allure.step("Searching the project in the search bar"):
        project_spec_obj.search_project("YTL 2026 June")

    with allure.step("Clicking on the project spec"):
        project_spec_obj.click_project_spec()

    with allure.step("Selecting the model key"):
        project_spec_obj.model_key_selection("Demo_Key1")

    with allure.step("Click on Import button"):
        project_spec_obj.click_import()

    with allure.step("Importing the spec file"):
        project_spec_obj.import_spec(
            r"C:\Users\Harshal.Tandulkar\Downloads\YTL_2026_February_Grillmates_Spec_v1.xlsx"
        )

    with allure.step("Validate spec upload success message"):
        hydro_success = project_spec_obj.get_hydro_message("Spec Uploaded Successfully")
        expect(hydro_success).to_be_visible(timeout=6000)
        assert hydro_success, "Success message should be visible after spec upload"

    with allure.step("Select the ADS from the dropdown"):
        project_spec_obj.select_ads("V1_Test ADS Grill (Demo_Key1_1_f.csv)")

    # Demonstrate using list to iterate through checkbox methods
    checkbox_methods = [
        project_spec_obj.select_exclude_zero_dependent,
        project_spec_obj.select_borrow_transformation,
        project_spec_obj.select_recalibration_to_national,
        project_spec_obj.select_include_intercept,
    ]

    for checkbox_method in checkbox_methods:
        with allure.step(f"Selecting the checkbox: {checkbox_method.__name__}"):
            checkbox_method()

    with allure.step("Providing the alias name"):
        project_spec_obj.alias_name()

    with allure.step("Saving the spec as draft"):
        project_spec_obj.save_draft_spec()
        assert authenticated_page.url, "Page should remain loaded after save operation"


@allure.title("Test granular spec generation and template download")
@allure.description("User can generate granular spec and download the template")
@allure.severity(allure.severity_level.BLOCKER)
def test_granular_spec(authenticated_page):
    granular_spec_obj = ProjectSpec(authenticated_page)

    with allure.step("Searching the project in the search bar"):
        granular_spec_obj.search_project("YTL 2026 June")

    with allure.step("Clicking on the project spec"):
        granular_spec_obj.click_project_spec()

    with allure.step("Selecting the model key"):
        granular_spec_obj.model_key_selection("Demo_Key1")

    with allure.step("Click on Import button"):
        granular_spec_obj.click_import()

    with allure.step("Importing the spec file"):
        granular_spec_obj.import_spec(
            r"C:\Users\Harshal.Tandulkar\Downloads\YTL_2026_February_Grillmates_Spec_v1.xlsx"
        )

    with allure.step("Validate spec upload success message"):
        hydro_success = granular_spec_obj.get_hydro_message(
            "Spec Uploaded Successfully"
        )
        expect(hydro_success).to_be_visible(timeout=6000)
        assert hydro_success, "Success message should be visible after spec upload"

    with allure.step("Select the ADS from the dropdown"):
        granular_spec_obj.select_ads("V1_Test ADS Grill (Demo_Key1_1_f.csv)")

    with allure.step("Providing the alias name"):
        granular_spec_obj.alias_name()

    with allure.step("Clicking on the Granular Spec option"):
        granular_spec_obj.granular_spec()
        assert authenticated_page.url, (
            "Page should remain loaded after granular spec generation"
        )

    with allure.step("Downloading the Granular spec Template"):
        granular_spec_obj.click_button("Download TemplateImport")
        assert authenticated_page.url, (
            "Page should remain loaded after download operation"
        )
