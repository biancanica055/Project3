from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd
import tkinter as tk
from PIL import Image, ImageTk


# The script starts by importing necessary libraries, including Selenium for web scraping, time for adding delays,
# pandas for data manipulation, tkinter for creating the GUI, and Pillow (PIL) for working with images.


def scrape_data(search_term):
    """
    This function takes a search term as an input.
    It initializes a Chrome WebDriver using Selenium and navigates to the Carrefour website.
    It enters the search term in the search bar and clicks the search button.
    The script then iterates through up to 10 search result pages, extracting product names from each page.
    The extracted product names are stored in a list called products.
    The data is saved to an Excel file named "data.xlsx" using pandas.
    The function also updates a label in the Tkinter GUI to indicate that the data has been scraped and saved.
    The Chrome browser is closed after the scraping is complete.
    :param search_term: The product term to search for on the Carrefour website.
    :return: None
    """

    # Open the browser
    browser = webdriver.Chrome()
    browser.get('https://carrefour.ro/')  # Navigates the browser to the Carrefour website.
    browser.maximize_window()

    # Enter the search term and perform the search
    input_search = browser.find_element(By.ID,
                                        'search')  # Locates the search input field on the website using its HTML ID.
    search_button = browser.find_element(By.XPATH,
                                         "//img[@src='https://cdn-static.carrefour.ro/unified/assets/images/dist"
                                         "/icons/search.svg']")  # Locates the search button using its XPATH.
    input_search.send_keys(search_term)  # Enters the provided search term into the search input field.
    sleep(1)
    search_button.click()  # Clicks the search button to initiate the search.

    products = []  # Creating an empty list for storing the products
    next_button_available = True  # Flag to track the availability of the "Next" button for pagination.

    for i in range(10):  # Scrape data from up to 10 pages
        print('Scraping page', i + 1)
        product_elements = browser.find_elements(By.XPATH,
                                                 "//li/div/div/div/div/a")  # Finds all product elements on
        # the current page by their XPATH

        # Extract product data and add to the list
        for product in product_elements:
            products.append(product.text)

        try:  # try-except block to handle situations where the "Next" button is not found(one page of results)
            if next_button_available:
                # Attempts to click the "Next" button if it's available. If not, it breaks out of the loop.
                wait = WebDriverWait(browser, 10)
                next_page = wait.until(EC.element_to_be_clickable(
                    (By.XPATH, "//*[@id='maincontent']/div[3]/div[1]/div[2]/div[3]/div[1]/div/ul/li[5]")))
                next_page.click()
                sleep(2)
            else:
                break  # Exit the loop if the "Next" button is no longer available
        except:
            next_button_available = False  # Set the flag to False if the "Next" button is not found

    # Save the scraped data to Excel
    data = pd.DataFrame({"Products": products})  # After scraping data from multiple pages,
    # the script creates a pandas DataFrame named data with a column named "Products."
    data.to_excel("data.xlsx", index=False)  # Saves the DataFrame to an Excel file named "data.xlsx."

    # Close the browser
    browser.quit()

    result_label.config(text="Data scraped and saved to data.xlsx")  # Updates a result label in the Tkinter GUI to
    # indicate that the data has been scraped and saved to "data.xlsx."
    root.destroy()  # Closes the Tkinter GUI


root = tk.Tk()
root.title("Searching engine")  # The name of the GUI window
root.geometry("840x490")  # Tkinter GUI window dimensions


def sh_button():
    """
     Callback function for the Tkinter GUI 'Search' button.
    Retrieves the search term entered in the keyword_entry widget
    and initiates a data scraping process using the scrape_data function.

    :return: None
    """
    search_term = keyword_entry.get()  # It retrieves the search term entered in
    # the keyword_entry widget
    scrape_data(search_term)  # Calls the scrape_data() function with the search term


# Load and resize the background image
image = Image.open("C:/Users/Bianca/Desktop/bg2.jpg")  # It loads an image using the method from the Pillow (PIL)
# library.
bg_width, bg_height = root.winfo_screenwidth(), root.winfo_screenheight()
image = image.resize((bg_width, bg_height), Image.LANCZOS)
background_image = ImageTk.PhotoImage(image)

# Create a label for the background image and place it in the frame
background_label = tk.Label(root, image=background_image)
background_label.place(relwidth=1, relheight=1)

# Create a frame for other widgets
frame = tk.Frame(root)
frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

# Other widgets
keyword_label = tk.Label(frame, text="Enter the product you want to search for:", font=("Helvetica", 14), bg="white")
keyword_label.pack()

keyword_entry = tk.Entry(frame, font=("Helvetica", 12), bd=2, relief=tk.GROOVE)
keyword_entry.pack(pady=10)

sr_button = tk.Button(frame, text="Search", font=("Helvetica", 12), bg="blue", fg="white", relief=tk.RAISED,
                      command=sh_button)
sr_button.pack(pady=10)

result_label = tk.Label(frame, text="", font=("Helvetica", 12))
result_label.pack()

root.mainloop()  # Initiates the main event loop for the Tkinter application
