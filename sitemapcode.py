import datetime
import random
import re
from xml.etree.ElementTree import Element, SubElement, ElementTree, tostring
from xml.dom.minidom import parseString
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

def clean_subdomain(link):
    """
    Clean the subdomain of a given link by keeping only alphanumeric characters and hyphens.
    """
    match = re.match(r"https?://(.*?)\.(.*)", link)
    if match:
        subdomain = re.sub(r"[^a-zA-Z0-9-]", "", match.group(1))  # Only allow alphanumeric characters and hyphens
        domain_and_path = match.group(2)
        cleaned_link = f"https://{subdomain}.{domain_and_path}"
        return cleaned_link
    return link  # if there's no match, return the link as it is

def pretty_xml(element):
    """Return a pretty-printed XML string for the Element."""
    rough_string = tostring(element, 'utf-8')
    reparsed = parseString(rough_string)
    return reparsed.toprettyxml(indent="\t")

def generate_sitemap_from_links(links, start_date_str, limit_per_sitemap, sitemap_name):
    links = [clean_subdomain(link.strip()) for link in links]

    start_date = datetime.datetime.strptime(start_date_str, "%d/%m/%Y").date()
    today = datetime.date.today()

    days_difference = (today - start_date).days + 1  # Inclusive end date
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
        # Update the format here to be compliant with sitemap specs
        formatted_datetime = current_datetime.strftime("%Y-%m-%dT%H:%M:%S+00:00")
        current_sitemap_links.append((link, formatted_datetime))

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

    with open(filename, "w", encoding="utf-8") as f:
        f.write(pretty_xml(urlset))

def gui_generate_sitemap():
    def on_generate():
        with open(file_path_var.get(), "r", encoding="utf-8") as file:
            all_links = file.readlines()

        start_date_input = start_date_var.get()
        limit = int(limit_var.get())
        sitemap_name = sitemap_name_var.get()

        generate_sitemap_from_links(all_links, start_date_input, limit, sitemap_name)
        messagebox.showinfo("Success", "Sitemaps generated successfully!")

    root = tk.Tk()
    root.title("Sitemap Generator")

    frame = ttk.Frame(root, padding="10")
    frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    ttk.Label(frame, text="Link File Path:").grid(row=0, column=0, sticky=tk.W, pady=(0, 10))
    file_path_var = tk.StringVar()
    ttk.Entry(frame, textvariable=file_path_var).grid(row=0, column=1, pady=(0, 10), sticky=(tk.W, tk.E))
    ttk.Button(frame, text="Browse", command=lambda: file_path_var.set(filedialog.askopenfilename())).grid(row=0, column=2, pady=(0, 10))

    ttk.Label(frame, text="Start Date (dd/mm/yyyy):").grid(row=1, column=0, sticky=tk.W, pady=10)
    start_date_var = tk.StringVar()
    ttk.Entry(frame, textvariable=start_date_var).grid(row=1, column=1, columnspan=2, pady=10, sticky=(tk.W, tk.E))

    ttk.Label(frame, text="Max Links per Sitemap:").grid(row=2, column=0, sticky=tk.W, pady=10)
    limit_var = tk.StringVar()
    ttk.Entry(frame, textvariable=limit_var).grid(row=2, column=1, columnspan=2, pady=10, sticky=(tk.W, tk.E))

    ttk.Label(frame, text="Sitemap Name:").grid(row=3, column=0, sticky=tk.W, pady=10)
    sitemap_name_var = tk.StringVar()
    ttk.Entry(frame, textvariable=sitemap_name_var).grid(row=3, column=1, columnspan=2, pady=10, sticky=(tk.W, tk.E))

    ttk.Button(frame, text="Generate Sitemaps", command=on_generate).grid(row=4, column=0, columnspan=3, pady=20)

    frame.columnconfigure(1, weight=1)
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    root.mainloop()

if __name__ == "__main__":
    gui_generate_sitemap()
