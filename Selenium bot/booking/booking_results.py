# This fiel is going to include a method that will parse
# The pecefic data hat we need from each one of the deal boxes

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
import re

class BookingReport:
    def __init__(self, boxes_selection_element:WebElement):
        self.boxes_selection_elemnet = boxes_selection_element
        self.deal_boxes = self.pull_deal_boxes()
        
    def pull_deal_boxes(self):
        return self.boxes_selection_elemnet.find_elements(
                                        By.CSS_SELECTOR, "div[data-testid='property-card']")
    
    def pull_deal_box_attributes(self):
        collection = []
        for deal_box in self.deal_boxes:
            # Title extraction (as before)
            title_element = deal_box.find_element(By.CSS_SELECTOR, 'div[data-testid="title"]')
            hotel_name = title_element.get_attribute('innerHTML').strip()
            
            # Price extraction
            price_element = deal_box.find_element(By.CSS_SELECTOR, "span[data-testid='price-and-discounted-price']")
            hotel_price = price_element.get_attribute('innerHTML').strip()
            
            # Score extraction: target the outer container that holds the score info
            score_container = deal_box.find_element(By.CSS_SELECTOR, 'div.a3b8729ab1.d86cee9b25')
            score_text = score_container.text.strip()  # This might return "Scored 6.6 6.6"
            
            # Use regex to extract the first occurrence of a floating point number
            match = re.search(r'(\d+\.\d+)', score_text)
            hotel_score = match.group(1) if match else "N/A"
            
            collection.append([hotel_name, hotel_price, hotel_score])
        return collection

