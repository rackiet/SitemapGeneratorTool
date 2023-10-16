import datetime
import random
from xml.etree.ElementTree import Element, SubElement, ElementTree, tostring
from xml.dom.minidom import parseString
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog

def pretty_xml(element):
    """Return a pretty-printed XML string for the Element."""
    rough_string = tostring(element, 'utf-8')
    reparsed = parseString(rough_string)
    return reparsed.toprettyxml(indent="\t")

def generate_sitemap_from_links(links, start_date_str, limit_per_sitemap, sitemap_name):
    start_date = datetime.datetime.strptime(start_date_str, "%d/%m/%Y").date()
    today = datetime.date.today()

    days_difference = (today - start_date).days + 1
    links_per_day, remainder = divmod(len(links), days_difference)

    sitemap_counter = 1
    links_counter = 0
    current_sitemap_links = []
    current_date = start_date
    links_for_current_day = links_per_day + remainder

    for link in links:
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

    with open(filename, "w") as f:
        f.write(pretty_xml(urlset))

def load_links():
    filepath = filedialog.askopenfilename(title="Open link.txt", filetypes=[("Text files", "*.txt")])
    with open(filepath, 'r') as file:
        return file.readlines()

def generate_sitemap():
    links = load_links()
    start_date_input = simpledialog.askstring("Input", "Masukkan tanggal mulai (dd/mm/yyyy):")
    limit = simpledialog.askinteger("Input", "Berapa link maksimal per sitemap?")
    sitemap_name = simpledialog.askstring("Input", "Nama sitemap (tanpa .xml):")

    generate_sitemap_from_links(links, start_date_input, limit, sitemap_name)
    messagebox.showinfo("Success", "Sitemap has been generated!")

def main():
    root = tk.Tk()
    root.title("Sitemap Generator")
    
    frame = tk.Frame(root)
    frame.pack(padx=10, pady=10)

    load_btn = tk.Button(frame, text="Generate Sitemap", command=generate_sitemap)
    load_btn.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    main()
