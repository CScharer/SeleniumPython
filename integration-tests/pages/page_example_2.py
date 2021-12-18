from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from pages.page_base_v1 import PageBase


class PageExample2(PageBase):
    ALL_REPORTS_CHECKBOX = (By.CSS_SELECTOR, "[title='Toggle All Rows Selected']")
    BULK_DELETE_BUTTON = (By.CSS_SELECTOR, "[data-qa='ReportsView_ActionBar_BulkDeleteButton']")
    BULK_DOWNLOAD_BUTTON = (By.CSS_SELECTOR, "[data-qa='ReportsView_ActionBar_BulkDownloadButton']")
    BUSINESS_CYCLE_YEAR_SELECT = "BusinessCycleSelect"
    BUSINESS_CYCLE_YEAR_SELECTOR = (By.XPATH, f"//div[@data-qa='{BUSINESS_CYCLE_YEAR_SELECT}']")
    COLUMN_NAMES = ["", "Report Type", "Format", "Date Generated", "Status", ""]
    DOWNLOAD_BUTTON = (
        By.XPATH,
        "//button[@class='gk-button btn btn-outline-primary' and contains(text(), 'Download')]",
    )
    DOWNLOAD_LINK = (By.XPATH, "//a[contains(@href, 'https://document-service-reports-')]")
    DROPDOWN_REPORTS_TYPE = (By.CSS_SELECTOR, "[data-qa='ReportTypeFilterSelect--summary']")
    HEADING = "Reports"

    def __init__(self, driver):
        super().__init__(driver=driver)
        self.wait = WebDriverWait(self.driver, 30, 0.1, ignored_exceptions=ElementClickInterceptedException)

    def business_cycle_year_text(self):
        return self.wait_for_and_get_element((By.XPATH, "//span[@class='gk-select-box-text my-auto']")).text

    def click_bulk_delete_button(self):
        self.wait_for_and_get_element_is_clickable(self.BULK_DELETE_BUTTON).click()

    def click_bulk_download_button(self):
        self.wait_for_and_get_element_is_clickable(self.BULK_DOWNLOAD_BUTTON).click()

    def click_delete_button_report_page(self, report_id):
        self.click_menu_by_report_id(report_id)
        self.is_text_present("Delete")
        self.wait_for_and_get_element_is_clickable(
            (By.CSS_SELECTOR, f"[data-qa='ReportActionsDropdown-delete-{report_id}']")
        ).click()

    def click_download_button(self):
        self.wait_for_and_get_element_is_clickable(self.DOWNLOAD_BUTTON).click()

    def click_download_button_report_page(self, report_id):
        self.click_menu_by_report_id(report_id)
        self.is_text_present("Download")
        self.wait_for_and_get_element_is_clickable(
            (By.CSS_SELECTOR, f"[data-qa='ReportActionsDropdown-download-{report_id}']")
        ).click()

    def click_menu_by_report_id(self, report_id):
        self.wait_for_and_get_element_is_clickable(
            (By.CSS_SELECTOR, f"[data-qa='ReportActionsDropdown-{report_id}']")
        ).click()

    def columns(self):
        return self.driver.find_elements(By.CSS_SELECTOR, "[data-qa='ReportsTable_DataGrid--th']")

    def columns_count(self):
        return len(self.columns())

    def columns_validate_names(self):
        columns_actual = self.columns()
        columns_expected = self.COLUMN_NAMES
        msg: str = f"len(columns_expected):[{len(columns_expected)}] == len(columns):[{len(columns_actual)}]"
        assert len(columns_expected) == len(columns_actual), msg
        column_names_found = []
        for column_index in range(len(columns_expected)):
            column_names_found.append(columns_actual[column_index].text)
        assert column_names_found == columns_expected, f"column names match {columns_expected}"

    def dropdown_reports_type(self):
        return self.wait_for_and_get_element_is_clickable(self.DROPDOWN_REPORTS_TYPE)

    def find_checkbox_in_table_by_id(self, report_id):
        selector: str = f"//*[@data-qa='ReportActionsDropdown-{report_id}']/../..//*[@title='Toggle Row Selected']"
        return self.wait_for_and_get_element_is_clickable((By.XPATH, selector))

    def find_report_in_table_by_id(self, report_id):
        self.wait_for_and_get_element((By.ID, f"report-action-dropdown-{report_id}"))

    def get_active_column_sorting_order(self, column_name, keyword):
        active_column = self.wait.until(
            ec.visibility_of_element_located(
                (By.XPATH, f"//div[@title='Toggle SortBy'][.='{column_name}']//i[contains(@class,'{keyword}')]")
            )
        )
        active_column_attribute = active_column.get_attribute("name")
        if active_column_attribute == "arrow_drop_down":
            active_column_order = "Descending"
        elif active_column_attribute == "arrow_drop_up":
            active_column_order = "Ascending"
        else:
            raise Exception("Could not get sorting order")
        return column_name, active_column_order

    def get_download_url(self):
        return self.driver.find_element(*self.DOWNLOAD_LINK).get_attribute("href")

    def heading_text(self):
        return self.wait_for_and_get_element((By.XPATH, "//h2")).text

    def no_results_link(self):
        return self.wait_for_and_get_element((By.XPATH, "//div[@data-qa='no-results-text']/p")).text

    def no_results_text(self):
        return self.wait_for_and_get_element((By.XPATH, "//div[@data-qa='no-results-text']/h2")).text

    def rows(self):

        return self.driver.find_elements(By.CSS_SELECTOR, "[data-qa='ReportsTable_DataGrid--tr']")

    def rows_count(self):
        return len(self.rows()) - 1

    def select_business_cycle_year(self, year):
        self.wait_for_and_get_element_is_clickable(self.BUSINESS_CYCLE_YEAR_SELECTOR).click()
        business_cycle_year = (
            By.XPATH,
            f"//div[@data-qa='{self.BUSINESS_CYCLE_YEAR_SELECT}']//li[@role='menuitem'][.='{year}']",
        )
        self.wait_for_and_get_element_is_clickable(business_cycle_year).click()

    def _select_dropdown_report(self, report_type):
        self.dropdown_reports_type().click()
        CHECKBOX_OBJECT = (By.CSS_SELECTOR, f"[data-qa='reportTypeFilterOption-{report_type}']")
        return self.wait_for_and_get_element_is_clickable(CHECKBOX_OBJECT)

    def select_dropdown_report_checkbox_farm_and_field_proposal(self):
        self._select_dropdown_report("FarmAndFieldProposalReport").click()

    def select_dropdown_report_checkbox_harvest_map_book(self):
        self._select_dropdown_report("HarvestMapBookReport").click()

    def select_dropdown_report_checkbox_map_based_planting_plan(self):
        self._select_dropdown_report("MapBasedPlantingPlanReport").click()

    def select_dropdown_report_checkbox_operation_growing_season_report(self):
        self._select_dropdown_report("OperationGrowingSeason").click()

    def select_dropdown_report_checkbox_planted_map_book(self):
        self._select_dropdown_report("PlantedMapBook").click()

    def select_dropdown_report_checkbox_seed_placement_summary(self):
        self._select_dropdown_report("SeedPlacementReport").click()

    def sort_report_header(self, header_name):
        self.wait_for_and_get_element_is_clickable(
            (By.XPATH, f"//div[@title='Toggle SortBy'][.='{header_name}']")
        ).click()

    def toggle_all_reports_checkbox(self):
        self.wait_for_and_get_element_is_clickable(self.ALL_REPORTS_CHECKBOX).click()

    def toggle_checkbox_in_table_by_id(self, report_id):
        self.find_checkbox_in_table_by_id(report_id).click()

    def wait_for_download_button(self):
        self.wait_for_and_get_element(self.DOWNLOAD_BUTTON)

    def wait_for_report_column_to_update_after_sorting(self, column_name):
        self.wait_for_and_get_element((By.XPATH, f"//div[text() = '{column_name}']"))
