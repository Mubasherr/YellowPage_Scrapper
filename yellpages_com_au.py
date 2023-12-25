import tkinter as tk
from tkinter import filedialog
from bs4 import BeautifulSoup
import pandas as pd
import threading
import queue
from selenium import webdriver
import time

data = []
obj = {}
FileName = ''
update_interval = 100
stop_event = threading.Event()  

def scrape_data(what, where, file_name, update_queue, count_var,flg1):
            
    global data
    global FileName
    flg = flg1
    if(flg):
        driver=webdriver.Chrome()
        target_website = 'https://www.yellowpages.com.au/find/{what}/{where}'
        driver.get(target_website)
        time.sleep(30)
        flg=False
    
    print(target_website)
    FileName = file_name
    countpage = 1
    flag = True

    while flag:
        if target_website:
            try:
                soup = BeautifulSoup(driver.page_source,'html.parser')
                allResults = soup.find_all('div',{"class":['Box__Div-sc-dws99b-0 iOfhmk MuiPaper-root MuiCard-root TopOfList MuiPaper-elevation1 MuiPaper-rounded','Box__Div-sc-dws99b-0 iOfhmk MuiPaper-root MuiCard-root PaidListing MuiPaper-elevation1 MuiPaper-rounded']})
                try:
                    target_website = soup.find("a",{"class","MuiButtonBase-root MuiButton-root MuiButton-outlined MuiButton-fullWidth"}).get("href")
                    target_website = "https://www.yellowpages.com.au"+target_website
                except:
                    print("exception Here")
                    target_website = None

                for i in range(0, len(allResults)):
                    obj = {}
                    try:
                        obj["name"] =  allResults[i].find("a",{"class":"MuiTypography-root MuiLink-root MuiLink-underlineNone MuiTypography-colorPrimary"}).text
                    except:
                        obj["name"] = None
                    try:
                        obj["address"] = (allResults[i].find("div",{"class":"Box__Div-sc-dws99b-0 bvRSwt"})).find("p").text
                    except:
                        obj["address"] = None
                    try:
                        obj["website"] = allResults[i].find("a",{"class":"MuiButtonBase-root MuiButton-root MuiButton-text ButtonWebsite MuiButton-textSecondary MuiButton-fullWidth"}).get("href")
                    except:
                        obj["Website"] = None
                    try:
                        phone = allResults[i].find("a",{"class":"MuiButtonBase-root MuiButton-root MuiButton-text ButtonPhone MuiButton-textPrimary MuiButton-fullWidth"}).get("href")
                        ls = phone.split(':')
                        obj["Phone"] = ls[1].strip()
                    except:
                        obj["Phone"] = None
                    data.append(obj)
                    
                    print(data)
                    
                    update_queue.put("update")  # Signal the main thread to update the GUI
            except:
                if len(data) != 0:
                    df = pd.DataFrame(data)
                    df.to_excel(FileName + '.xlsx', index=False)
                    print("Your file has been saved")
                    flag = False
                    break
        else:
            df = pd.DataFrame(data)
            df.to_excel(FileName + '.xlsx', index=False)
            print("Your file has been saved")
            print("Completed")
            count_var.set("Data is Completely Scraped...") 
            flag = False
            break

def browse_file():
    global FileName
    file_name = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
    if file_name:
        file_name_entry.delete(0, tk.END)
        file_name_entry.insert(0, file_name)
        FileName = file_name

def start_scraping():
    
    what = what_entry.get()
    where = where_entry.get()
    file_name = file_name_entry.get()

    if what and where and file_name:
        count_var.set("Count: 1")  # Initialize count_var
        update_queue = queue.Queue()
        flag=True
        threading.Thread(target=scrape_data, args=(what, where, file_name, update_queue, count_var,flag), daemon=False).start()
        window.after(update_interval, check_update, update_queue)
    else:
        print('Please fill in all fields.')

def check_update(update_queue):
    try:
        while True:
            message = update_queue.get_nowait()
            if message == "update":
                window.after(0, update_gui)
            elif message == "completed":
                window.after(0, on_scraping_complete)
            else:
                break
    except queue.Empty:
        window.after(update_interval, check_update, update_queue)

def on_scraping_complete():
    global data
    global FileName

    if len(data) != 0:
        df = pd.DataFrame(data)
        df.to_excel(FileName + '.xlsx', index=False)
        print("Your file has been saved")

def update_gui():
    # Placeholder for any additional GUI updates
    pass

def on_closing():
    global data
    global FileName
    global stop_event
    global driver

    if len(data) != 0:
        df = pd.DataFrame(data)
        df.to_excel(FileName + '.xlsx', index=False)
        print("Your file has been saved")

    stop_event.set()  # Set the event to stop the thread
      # Close the WebDriver
    window.destroy()


# Create the main window
window = tk.Tk()
window.title("YellowPages.com.au")
window.geometry("400x250")

# Create and place widgets for the input fields
what_label = tk.Label(window, text="What:")
what_label.pack()

what_entry = tk.Entry(window)
what_entry.pack()

where_label = tk.Label(window, text="Where:")
where_label.pack()

where_entry = tk.Entry(window)
where_entry.pack()

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
window.protocol("WM_DELETE_WINDOW", on_closing)

# Start the Tkinter event loop
window.mainloop()
