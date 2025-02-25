import booking.constants as const
from booking.booking_filtration import BookingFiltration
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from booking.booking_results import BookingReport
from prettytable import PrettyTable


class Booking(webdriver.Chrome):
    def __init__(self, driver_path=r"/Users/p/Proj/big_p/lib/python3.12/site-packages/selenium/", teardown=False):
        self.driver_path = driver_path
        self.teardown = teardown
        os.environ['PATH'] += self.driver_path
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        super(Booking, self).__init__(options=options)
        self.implicitly_wait(15)
        self.maximize_window()
    
    def __exit__(self, exc_type, exc, traceback):
        if self.teardown:
            self.quit()
        
    def land_first_page(self):
        self.get(const.BASE_URL)
        
    def change_currensy(self, currency=None):
        if currency is None:
         raise ValueError("Please specify a currency code (e.g., 'USD', 'EUR')")
    
        # Click the trigger to open the currency picker dropdown.
        currency_trigger = self.find_element(By.CSS_SELECTOR, 'button[data-testid="header-currency-picker-trigger"]')
        currency_trigger.click()
    
        # Wait for the currency selection buttons to become present.
        currency_buttons = WebDriverWait(self, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'button[data-testid="selection-item"]'))
        )
        #print(currency_buttons)
    
        # Iterate through each currency button to find the one that matches the desired currency.
        for btn in currency_buttons:
            # Get the text of the button (this may include both the currency name and code)
            button_text = btn.text.strip()
            if currency.upper() in button_text.upper():
                btn.click()
                print(f"Selected currency: {currency.upper()}")
                return

        # If no matching currency is found, raise an exception.
        raise Exception(f"Currency '{currency}' not found on the page.")
    
    
    def place_to_go(self, place_to_go=None):
        # Locate the destination input field by its 'name' attribute and clear any existing text.
        place = self.find_element(By.NAME, "ss")
        place.clear()
        
        # Send the desired destination text to the input field.
        place.send_keys(place_to_go)
        print(f"Selected destination: {place_to_go.upper()}")
        
        # Wait up to 10 seconds for the autocomplete results to load.
        # We're using a CSS selector to find all elements that have role="button".
        frst_rslt = WebDriverWait(self, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div[role='button']"))
        )
        
        # Initialize a flag to check if we have successfully clicked a matching result.
        clicked = False

        # Loop through each autocomplete result.
        for element in frst_rslt:
            # Compare the text in each element with the desired destination.
            # Using lower() to ensure the match is case-insensitive.
            if place_to_go.lower() in element.text.lower():
                # If the text matches, click the element.
                element.click()
                clicked = True
                break
            
         # If no matching result was found, print a message.
        if not clicked:
            print(f"Destination '{place_to_go}' not found in autocomplete results.")
            
    def choose_date(self, check_in, check_out):
        #print(check_in)
        #print(check_out)
        
        # Use CSS selectors to locate the specific check in date elements
        check_in_trigger = self.find_element(By.CSS_SELECTOR, f'span[data-date="{check_in}"]')
        check_in_trigger.click()
        
        # Use CSS selectors to locate the specific check out date elements
        check_out_trigger = self.find_element(By.CSS_SELECTOR, f'span[data-date="{check_out}"]')
        check_out_trigger.click()
        
    def occupancy(self, count=None):
        # Opens the dropdowm menu to select the amount of occupants (Adults, Children, Rooms)
        select_trigger = self.find_element(By.CSS_SELECTOR, 'button[data-testid="occupancy-config"]')
        select_trigger.click()
        
        while True:
            decrement_button = WebDriverWait(self, 10).until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "button.a83ed08757.c21c56c305.f38b6daa18.d691166b09.ab98298258.e91c91fa93")
                    ))
        
            decrement_button.click()
        
            adults_value_element = self.find_element(By.ID, "group_adults")
            # Should give the adults value
            adults_value = adults_value_element.get_attribute('value')
        
            if int(adults_value) == 1:
                break
            
        increase_button_element = WebDriverWait(self, 10).until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "button.a83ed08757.c21c56c305.f38b6daa18.d691166b09.ab98298258.bb803d8689.f4d78af12a")
            ))
        
        for i in range(count - 1):
            increase_button_element.click()
         
    def click_search(self):
        search_button = self.find_element(By.CSS_SELECTOR, 'button[type=submit]')
        search_button.click()
        
    def booking_filtration(self):
        filtration = BookingFiltration(driver=self)
        filtration.apply_star_rating(3, 4, 5)
        filtration.sort_by_lowest()
        
    def report_results(self):
        results = self.find_element(By.CSS_SELECTOR, 
                                    "div.bcbf33c5c3"
                                    )
        
        report = BookingReport(results)
        table = PrettyTable(
            field_names = ["Hotel Name", "Hotel Price", "Hotel Score"]
        )
        table.add_rows(report.pull_deal_box_attributes())
        print(table)
        

        
        