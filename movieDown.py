import os
from bs4 import BeautifulSoup
import requests
import webbrowser
import tkinter as tk
from tkinter import Entry, Label, Button, Listbox, Scrollbar

# Function to handle movie search
def search_movie():
    movie_name = movie_name_entry.get()
    if movie_name != "":
        x = movie_name.split()
        name = "+".join(x)
        result = requests.get("https://mycima.cloud/search/" + name)
        src = result.content
        soup = BeautifulSoup(src, "html.parser")
        movies_info = soup.find_all("div", {"class": "Thumb--GridItem"})

        if len(movies_info) > 0:
            return movies_info
    return None

def choose_movie():
    global movies_info
    movies_info = search_movie()
    if movies_info:
        movies_listbox.delete(0, tk.END)
        for index, movie_info in enumerate(movies_info):
            movies_listbox.insert(index, movie_info.text)

def on_select(event):
    selected_index = movies_listbox.curselection()
    if selected_index:
        chosen_movie = movies_info[selected_index[0]]
        link = get_download_link(chosen_movie)
        open_download_link(link)

def get_download_link(movie_info):
    link = movie_info.find("a").attrs['href']
    return link

def open_download_link(link):
    result = requests.get(link)
    src = result.content
    soup = BeautifulSoup(src, "html.parser")
    movies = soup.find_all("a", {"class": "hoverable activable"})
    global movies_links  # Define movies_links as a global variable
    movies_links = []

    for movie in movies:
        if "upbaam" in movie['href']:
            movies_links.append(movie['href'])

    quality_listbox.delete(0, tk.END)
    for index, movie_link in enumerate(movies_links):
        quality_listbox.insert(index, movie_link)

def on_quality_select():
    selected_index = quality_listbox.curselection()
    if selected_index:
        webbrowser.open(movies_links[selected_index[0]])

# Create GUI
root = tk.Tk()
root.title("Movie Downloader")
root.configure(bg="#f0f0f0")  # Set a background color

# Disable maximizing
root.resizable(False, False)

# Set the size of the window
root.geometry("800x500")  # Adjust the dimensions as needed

# Label and Entry for movie name
Label(root, text="Movie Name:", bg="#f0f0f0", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=10, sticky="w")
movie_name_entry = Entry(root, width=50, font=("Arial", 12))
movie_name_entry.grid(row=0, column=1, padx=10, pady=10)

# Search button
search_button = Button(root, text="Search", command=choose_movie, width=20, bg="#4CAF50", fg="white", font=("Arial", 10, "bold"))
search_button.grid(row=0, column=2, padx=10, pady=10)

# Listbox to display movie choices
movies_listbox = Listbox(root, font=("Arial", 12), width=80, height=10)
movies_listbox.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")
movies_scrollbar = Scrollbar(root)
movies_scrollbar.grid(row=1, column=2, sticky="ns")
movies_listbox.config(yscrollcommand=movies_scrollbar.set)
movies_scrollbar.config(command=movies_listbox.yview)
movies_listbox.bind('<<ListboxSelect>>', on_select)

# Listbox to display download links
quality_listbox = Listbox(root, font=("Arial", 12), width=80, height=5)
quality_listbox.grid(row=3, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")
quality_scrollbar = Scrollbar(root)
quality_scrollbar.grid(row=3, column=2, sticky="ns")
quality_listbox.config(yscrollcommand=quality_scrollbar.set)
quality_scrollbar.config(command=quality_listbox.yview)

# Download button
download_button = Button(root, text="Download Movie", command=on_quality_select, width=30, bg="#2196F3", fg="white", font=("Arial", 10, "bold"))
download_button.grid(row=5, column=0, columnspan=3, pady=10)

# Add a label for feedback
feedback_label = Label(root, text="", fg="red", bg="#f0f0f0", font=("Arial", 10))
feedback_label.grid(row=4, column=0, columnspan=3)

root.mainloop()
