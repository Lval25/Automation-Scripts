from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re

# This file will include a class and instance methods 
# That will apply filtration to the results we recieved back

class BookingFiltration:
    def __init__(self, driver:WebDriver):
        self.driver = driver
        
    def apply_star_rating(self, *star_values):
        # Create an explicit wait instance using the driver associated with this class.
        wait = WebDriverWait(self.driver, 10)
        
        # Locate the star rating container using its data-filters-group attribute.
        star_box = wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, "div[data-filters-group='class']")
        ))
        
        # Find all individual star rating items within the container.
        # Each item has a data-filters-item attribute starting with "class:class=".
        star_items = star_box.find_elements(By.CSS_SELECTOR, "div[data-filters-item^='class:class=']")

        #print(len(star_items))
        
        # Loop over each desired star rating value provided as arguments.
        for star_value in star_values:
            # Convert the star value (number) to a string.
            star_value_str = str(star_value)
            # Flag to track if the desired rating was found.
            found = False
        
            for item in star_items:
                # Locate the label element that contains the visible rating text.
                label_element = item.find_element(By.CSS_SELECTOR, "label")
                label_text = label_element.text.strip()
            
                # Use a regex to check if the label starts with the given number followed by "star" or "stars"
                # The regex ^\s* ensures any leading spaces are ignored.
                pattern = rf"^\s*{star_value_str}\s+star(s)?\b"
                if re.search(pattern, label_text, flags=re.IGNORECASE):
                    # If a match is found, locate the corresponding input element and click it.
                    input_element = item.find_element(By.CSS_SELECTOR, "input")
                    input_element.click()
                    print(f"Selected rating: {star_value_str}")
                    found = True
                    break  # Break out of the inner loop once the option is selected.
            
                else:
                    # The else clause of the inner loop executes if no break occurred, i.e., if the star_value was not found.
                    print(f"Desired rating '{star_value}' not found among the available options.")
    
    def sort_by_lowest(self):
        # Find the let down menu that contains the lowest price checker
        lowest_menu = self.driver.find_element(By.CSS_SELECTOR, 'span[class="cac967781c"]')
        lowest_menu.click()
        
        # Find and click the lowest price button
        lowest_price = self.driver.find_element(By.CSS_SELECTOR, "button[data-id='price']")
        lowest_price.click()


     