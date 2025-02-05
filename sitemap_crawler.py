import requests
from bs4 import BeautifulSoup as Soup
import pandas as pd
import hashlib


# Pass the headers you want to retrieve from the xml such as ["loc", "lastmod"]
def parse_sitemap( url,headers):
    resp = requests.get(url)
    # we didn't get a valid response, bail
    if (200 != resp.status_code):
        return False

    # BeautifulSoup to parse the document
    soup = Soup(resp.content, "html.parser")

    # find all the <url> tags in the document
    urls = soup.findAll('url')
    sitemaps = soup.findAll('sitemap')
    new_list = [] + headers
    panda_out_total = pd.DataFrame([], columns=new_list)


    if not urls and not sitemaps:
        return False

    # Recursive call to the the function if sitemap contains sitemaps
    if sitemaps:
        for u in sitemaps:
            test = u.find('loc').string
            panda_recursive = parse_sitemap(test, headers)
            panda_out_total = pd.concat([panda_out_total, panda_recursive], ignore_index=True)

    out = []

    # Extract the keys we want
    for u in urls:
        values = []
        for head in headers:
            loc = None
            loc = u.find(head)
            if not loc:
                loc = "None"
            else:
                loc = loc.string
            values.append(loc)
        out.append(values)
    
    # Create a dataframe
    panda_out = pd.DataFrame(out, columns= new_list)

    # If recursive then merge recursive dataframe
    if not panda_out_total.empty:
        panda_out = pd.concat([panda_out, panda_out_total], ignore_index=True)

    #returns the dataframe
    return panda_out

def main():
    print(parse_sitemap("https://menlovc.com/sitemap_index.xml", ["loc"]))
    #parse_sitemap("https://menlovc.com/sitemap_index.xml", ["loc"]).to_csv("menlo_links.csv")

if __name__ == "__main__":
    main()

