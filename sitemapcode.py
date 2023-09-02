import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from tqdm import tqdm

def validate_date(date_str):
    try:
        return datetime.strptime(date_str, '%d-%m-%Y').date()
    except ValueError:
        return None

def url_generator(links, start_date, end_date, priority, changefreq):
    current_day = start_date
    link_count = 0
    
    while current_day <= end_date:
        for link in links:
            for minute in range(0, 59):
                url_data = {
                    'loc': link.strip(),
                    'lastmod': current_day.strftime('%Y-%m-%d') + f"T{minute:02d}:00:00Z",
                    'changefreq': changefreq,
                    'priority': str(priority)
                }
                
                yield url_data

                link_count += 1
                if link_count >= 500:
                    return

        current_day += timedelta(days=1)

def create_sitemap_chunk(url_gen, filename):
    urlset = ET.Element('urlset', xmlns='http://www.sitemaps.org/schemas/sitemap/0.9')

    for url_data in url_gen:
        url = ET.SubElement(urlset, 'url')
        for key, value in url_data.items():
            elem = ET.SubElement(url, key)
            elem.text = value
    
    tree = ET.ElementTree(urlset)
    tree.write(filename, xml_declaration=True, encoding='utf-8')

def main():
    # Input and validate start and end dates
    while True:
        start_date_str = input("Enter the start date (DD-MM-YYYY): ")
        end_date_str = input("Enter the end date (DD-MM-YYYY): ")
        
        start_date = validate_date(start_date_str)
        end_date = validate_date(end_date_str)
        
        if start_date and end_date:
            break
        else:
            print("Invalid date format. Please try again.")
    
    # Input priority and changefreq
    priority = float(input("Enter priority (e.g., 1.0): "))
    changefreq = input("Enter changefreq (e.g., always, hourly, daily): ")

    # Read website list from file
    with open('listwebsite.txt', 'r') as f:
        links = f.readlines()

    sitemap_index = 1
    total_links = len(links)

    print(f"Generating sitemaps for {total_links} links...")

    with tqdm(total=total_links) as pbar:
        while links:
            chunk_links = links[:500]
            links = links[500:]

            url_gen = url_generator(chunk_links, start_date, end_date, priority, changefreq)
            filename = f'sitemap{sitemap_index}.xml'

            create_sitemap_chunk(url_gen, filename)
            pbar.update(len(chunk_links))

            print(f"Sitemap chunk saved to {filename}")
            sitemap_index += 1

if __name__ == '__main__':
    main()
