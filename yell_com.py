import tkinter as tk
from tkinter import filedialog
from selenium import webdriver
from bs4 import BeautifulSoup
import csv

data = []
obj = {}
countpage = 1

# Initialize the WebDriver
driver = webdriver.Chrome()

def scrape_data():
    global data
    global countpage
    global obj

    # Load the target website
    target_website = "https://www.yell.com/ucs/UcsSearchAction.do?keywords=pizza&location=uk&scrambleSeed=509559697&pageNum=" + str(countpage)
    driver.get(target_website)

    # Wait for a few seconds for the page to load
    import time
    time.sleep(5)

    # Now you can scrape the data as needed using BeautifulSoup or other methods
    # For example:
    while True:
        time.sleep(5)
        print(countpage)
        if target_website:
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            allResults = soup.find_all('div', {'class': 'row businessCapsule--mainRow'})
            print(len(allResults))

            try:
                dum_nextsite = soup.find("a", {"class": "btn btn-blue btn-fullWidth pagination--next"}).get('href')
                print((dum_nextsite))
                countpage = countpage + 1
                target_website = "https://www.yell.com" + (dum_nextsite)
            except:
                print("exception Here")
                target_website = None

            for i in range(0, len(allResults)):
                try:
                    obj["name"] = allResults[i].find("a", {"class": "businessCapsule--title"}).text
                except:
                    obj["name"] = None
                try:
                    obj["email"] = 'https://www.yell.com' + (
                            allResults[i].find("div", {"class": "col-sm-24 businessCapsule--ctas"}).find("a",
                                                                                                               {
                                                                                                                   "data-tracking": "LIST:CONTACT"}).get(
                                'href'))
                except:
                    obj["email"] = None
                try:
                    obj["address"] = 'https://www.yell.com/' + allResults[i].find("a", {
                        "class": "col-sm-24 businessCapsule--address businessCapsule--link"}).get('href')
                except:
                    obj["address"] = None
                try:
                    obj["website"] = (allResults[i].find("div", {"class": "col-sm-24 businessCapsule--ctas"}).find(
                        "a", {"data-tracking": "WL:CLOSED"}).get('href'))
                except:
                    obj["Website"] = None
                try:
                    dum = allResults[0].find("div", {"class": "expand--content trans-opacity expand--blockContent business--multiplePhonesWrapper"}).find(
                        'div', {'class': 'phoneOption'}).text.strip()
                    ls = dum.split('Tel')
                    obj["Phone"] = ls[1].strip()
                except:
                    obj["Phone"] = None
                data.append(obj)
                obj = {}
                print(data)

def browse_file():
    global FileName
    file_name = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    if file_name:
        file_name_entry.delete(0, tk.END)
        file_name_entry.insert(0, file_name)
        FileName = file_name

def start_scraping():
    global stop_event
    count_var.set("Count: 1")  # Initialize count_var
    scrape_data()

# Create the main window
window = tk.Tk()
window.title("YellowPages.com")
window.geometry("400x250")

# Create and place widgets for the input fields
file_name_label = tk.Label(window, text="File Name:")
file_name_label.pack()

file_name_entry = tk.Entry(window)
file_name_entry.pack()

browse_button = tk.Button(window, text="Browse", command=browse_file)
browse_button.pack()

start_button = tk.Button(window, text="Start Scraping", command=start_scraping)
start_button.pack()

# Create a label to display countpage
count_var = tk.StringVar()
count_label = tk.Label(window, textvariable=count_var)
count_label.pack()

# Bind the window close event to the on_closing function
window.protocol("WM_DELETE_WINDOW", window.quit)

# Start the Tkinter event loop
window.mainloop()
