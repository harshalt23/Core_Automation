import logging
import allure
from modules.workflow.project_workflow import FullCoreWorkflow
logger=logging.getLogger(__name__)


class TestFullCoreWorkflow:
    @allure.title("Verify end-to-end workflow from Analytical plan to Analytic Dataset")
    @allure.description("This test verifies the complete workflow from creating an Analytical Plan to generating an Analytic Dataset.")
    @allure.severity(allure.severity_level.CRITICAL)

    def test_full_core_workflow(self,authenticated_page):
        workflow=FullCoreWorkflow(authenticated_page)
        # """Test the full core workflow from Analytical Plan to Analytic Dataset."""
        
        # workflow.execute_full_workflow( project_name="YTL 2026 June",
        #     ap_file_path=r"C:\Users\Harshal.Tandulkar\Downloads\Latest AP\RITE_AID_UNIFIED AP_Q3 2024_RealativeDMA.xlsx",
        #     reporting_period=("1/9/2022", "1/9/2022", "5/25/2025"),
        #     primary_db="MP_ODS_ISG_RITEAID_US_STORE_5_COREDEV",
        #     secondary_db="MP_ODS_ISG_RITEAID_US_DMA_1_COREDEV"
        # )

        workflow.run_uap_workflow( project_name="YTL 2026 June",
            ap_file_path=r"C:\Users\Harshal.Tandulkar\Downloads\Latest AP\RITE_AID_UNIFIED AP_Q3 2024_RealativeDMA.xlsx",       
            reporting_period=("1/9/2022", "1/9/2022", "5/25/2025"),
            primary_db="MP_ODS_ISG_RITEAID_US_STORE_5_COREDEV",
            secondary_db="MP_ODS_ISG_RITEAID_US_DMA_1_COREDEV"
        )

        workflow.run_ads_workflow() 
        
        workflow.run_project_spec_workflow()
     

