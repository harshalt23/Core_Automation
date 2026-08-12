from playwright.sync_api import Page


class AnalyticalPlanLocator:
    """Page Object for Analytical Plan locators"""

    def __init__(self, page: Page):
        self.page = page

        # Main Navigation
        self.analytic_plan_tab = page.get_by_text("Analytic Plan", exact=True)
        self.search_box = page.get_by_role("textbox", name="Search")

        # Create AP Section
        self.chart_line_icon = page.locator(".fas.fa-chart-line").first
        self.create_ap_button = page.get_by_text("Create AP")

        # Database Selection
        self.select_primary_db = page.get_by_text("Select primary DB")
        self.select_secondary_db = page.get_by_text("Select secondary DB")

        # Import Template
        self.import_template_button = page.get_by_text("Import Template")
        self.file_input = page.locator("input[type='file']")


        self.upload_button = page.locator("div.saveblue.mg-r-5")

        #uncheck the constraint sheet using all Select all the worksheets checkbox
        self.uncheck_Select_worksheets_checkbox =page.get_by_text("Select all the Worksheets")

        # Constraint Sheet Checkbox
        self.constraint_sheet_checkbox = page.locator(
            "div:has-text('Constraint Sheet') i.fa-check-square"
        ).first
        self.constraint_sheet_text = page.get_by_text("Constraint Sheet")
        self.workbook_sheet_dropdown = page.locator(
            ".ap-select-workbooksheet > .v-align > .wd-20 > .fas"
        )
        #Hydro message locator in UAP
        self.hydro_message1 = page.get_by_role("alert").filter(has_text="UAP Version")
        self.hydro_message=page.get_by_text("UAP Version", exact=False)

        # Version Selection
        self.latest_version = page.locator(".rs-ap-table-wd-01.v-align").first

        #latest version locator with dynamic version number
        # self.feched_version_from_hydro_message=page.locator(f"div.wd-70:has-text('{version}')")

        # Next/Navigation Button
        self.next_button = page.get_by_text("Next")
        self.next_exact_button = page.get_by_text("Next", exact=True)
        self.chevron_right_button = page.locator(".fas.fa-chevron-right.pd-l-5")

        # Model Keys Selection
        self.select_model_keys = page.get_by_text("Select Model Keys")
        self.front_end_sales = page.get_by_text("Front_End_Sales", exact=True)
        self.riteaid_com = page.get_by_text("RiteAid_com", exact=True)
        self.pharmacy = page.get_by_text("Pharmacy", exact=True)
        self.immunization = page.get_by_text("Immunization", exact=True)
        self.front_end_transactions = page.get_by_text(
            "Front_End_Transactions", exact=True
        )
        self.riteaid_com_transactions = page.get_by_text(
            "RiteAid_com_Transactions", exact=True
        )

        # Date Pickers
        self.overflow_container = page.locator(".ov-flow")
        self.calendar_icon = page.locator(".far.fa-calendar-alt").first
        self.type_or_select_textbox_first = page.get_by_role(
            "textbox", name="Type or select"
        ).first
        self.type_or_select_textbox_second = page.get_by_role(
            "textbox", name="Type or select"
        ).nth(1)
        self.type_or_select_textbox_third = page.get_by_role(
            "textbox", name="Type or select"
        ).nth(2)

        # Reporting Period Fields
        self.enter_name_field = page.get_by_role("textbox", name="Enter Name")
        self.enter_tag_field = page.get_by_role("textbox", name="Enter Tag")
        self.select_start_date_field = page.get_by_role(
            "textbox", name="Select Start Date"
        )
        self.select_end_date_field = page.get_by_role("textbox", name="Select End Date")
        self.update_button = page.get_by_text("Update").first

        # Save Options
        self.save_dropdown_toggle = page.locator(
            "//i[@class='fas fa-angle-down pd-l-5']"
        )
        self.save_draft_option = page.locator("//div[text()='Save Draft']")
        self.save_ap_option = page.locator("//div[text()='Save AP']")
        self.save_ap_spec_option = page.get_by_text("Save AP & Spec")

        # Save Confirmation Dialog
        # self.save_confirmation_dialog = page.locator("div:has-text('Do you want to save this file permanently?')").first
        # page.locator('div').filter({ hasText: 'Do you want to save this file permanently?' }).first()
        self.confirm_save_button = page.locator(
            "div.saveblue.v-align", has_text="Save"
        ).first
        # self.confirm_save_button=page.get_by_text("Save", exact=True).first

        # Download
        self.download_button = page.locator(
            ".fas.fa-download.wb-fa-download.pd-10"
        ).first

        # Status
        self.draft_status = page.get_by_text("Draft")
