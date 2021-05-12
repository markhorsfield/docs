#!/usr/bin/env python3
'''
Edits html NVIDIA doc pdf HTML files to enable a more user-friendly experience.
'''
from bs4 import BeautifulSoup
import os
from os import path

def rewrite_urls(soup, product):
    '''
    Modifies all links on a page to become local anchors

    soup - BeautifulSoup object to modify
    product - The product string of the PDF being modified. Must match the content directory name, e.g., cumulus-linux-42

    Returns a modified BeautifulSoup object
    '''
    for link in soup.find_all("a"):
        href = link.get("href")

        if not href:
            continue

        path_parts = href.split("/")

        if len(path_parts) < 2:
            continue

        if product not in path_parts:
            continue

        if path_parts[len(path_parts) - 1] == "#":
            anchor = "#" + path_parts[len(path_parts) - 2]
        else:
            anchor = path_parts[len(path_parts) - 1]

        link["href"] = anchor

    return soup

def expand_details(soup):
    '''
    Expands all "summary" sections of an HTML page

    soup - BeautifulSoup object to modify

    Returns BeautifulSoup object
    '''
    for div in soup.find_all("div", {"class": "expand-content"}):
        div["style"] = ""

    return soup

def get_folder_list():
    '''
    Get a list of generated Hugo folders that have a pdf file to modify.
    Assumes that Hugo docs are built into public/networking-ethernet-software

    Returns a list of paths rooted at the repo url
    '''
    path_list = []
    base_dir = "public/networking-ethernet-software"
    for folder in os.listdir(base_dir):
        if path.exists(base_dir + "/" + folder + "/pdf/index.html"):
            path_list.append(base_dir + "/" + folder + "/pdf/index.html")

    return path_list

def get_product(path):
    '''
    Determine the product component of a path to a PDF HTML page.

    path - the string path to the PDF file.

    Returns a string of just the component.
    '''
    start_index = len("public/networking-ethernet-software/")
    path = path[start_index:path.find("/pdf")]

    return path

def main():
    """
    Main function to modify static HTML files
    """

    for path in get_folder_list():
        with open(path, "r") as in_file:
            soup = BeautifulSoup(in_file, 'html.parser')

        product = get_product(path)
        print("Modifying " + path)
        soup = rewrite_urls(soup, product)
        soup = expand_details(soup)

        with open(path, "w") as in_file:
            in_file.write(str(soup))

if __name__ == "__main__":
    main()



