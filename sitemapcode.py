import datetime
import random
import sys
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
from xml.etree.ElementTree import Element, SubElement, ElementTree, tostring
from xml.dom.minidom import parseString
import tkinter.ttk as ttk

def pretty_xml(element):
    rough_string = tostring(element, 'utf-8')
    reparsed = parseString(rough_string)
    return reparsed.toprettyxml(indent="\t")

def generate_sitemap_from_links(links, start_date_str, limit_per_sitemap, sitemap_name, progress_var):
    start_date = datetime.datetime.strptime(start_date_str, "%d/%m/%Y").date()
    today = datetime.date.today()

    days_difference = (today - start_date).days + 1
    links_per_day, remainder = divmod(len(links), days_difference)

    sitemap_counter = 1
    links_counter = 0
    current_sitemap_links = []
    current_date = start_date

    links_for_current_day = links_per_day + remainder

    total_links = len(links)
    for idx, link in enumerate(links):
        hour = random.randint(0, 23)
        minute = random.randint(0, 59)
        second = random.randint(0, 59)
        current_datetime = datetime.datetime.combine(current_date, datetime.time(hour, minute, second))
        current_sitemap_links.append((link.strip(), current_datetime.isoformat()))

        links_for_current_day -= 1
        if links_for_current_day == 0:
            current_date += datetime.timedelta(days=1)
            links_for_current_day = links_per_day

        links_counter += 1
        if links_counter == limit_per_sitemap:
            save_to_xml(current_sitemap_links, f"{sitemap_name}{sitemap_counter}.xml")
            links_counter = 0
            current_sitemap_links = []
            sitemap_counter += 1

        progress_var.set((idx + 1) / total_links * 100)

    if current_sitemap_links:
        save_to_xml(current_sitemap_links, f"{sitemap_name}{sitemap_counter}.xml")

def save_to_xml(links, filename):
    urlset = Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
    for link, lastmod in links:
        url = SubElement(urlset, "url")
        loc = SubElement(url, "loc")
        loc.text = link
        lm = SubElement(url, "lastmod")
        lm.text = lastmod

    with open(filename, "w", encoding="utf-8") as f:
        f.write(pretty_xml(urlset))

def start_generation():
    file_path = filedialog.askopenfilename(title="Pilih file link.txt", filetypes=[("Text files", "*.txt")])
    if not file_path:
        return

    with open(file_path, "r", encoding="utf-8") as file:
        all_links = file.readlines()

    start_date_input = simpledialog.askstring("Input", "Masukkan tanggal mulai (dd/mm/yyyy):")
    if not start_date_input:
        return

    limit = simpledialog.askinteger("Input", "Berapa link maksimal per sitemap?")
    if not limit:
        return

    sitemap_name = simpledialog.askstring("Input", "Nama sitemap (tanpa .xml):")
    if not sitemap_name:
        return

    generate_sitemap_from_links(all_links, start_date_input, limit, sitemap_name, progress_var)
    messagebox.showinfo("Info", "Sitemap berhasil digenerate!")

app = tk.Tk()
app.title("Sitemap Generator")

frame = tk.Frame(app)
frame.pack(pady=20)

btn = tk.Button(frame, text="Generate Sitemap", command=start_generation)
btn.pack()

progress_var = tk.DoubleVar()
progress = ttk.Progressbar(frame, orient="horizontal", length=300, variable=progress_var, mode="determinate")
progress.pack(pady=20)

app.mainloop()
