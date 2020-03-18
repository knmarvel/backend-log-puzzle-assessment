#!/usr/bin/env python2
"""
Logpuzzle exercise

Copyright 2010 Google Inc.
Licensed under the Apache License, Version 2.0
http://www.apache.org/licenses/LICENSE-2.0

Google's Python Class
http://code.google.com/edu/languages/google-python-class/

Given an apache logfile, find the puzzle urls and download the images.

Here's what a puzzle url looks like:
10.254.254.28 - - [06/Aug/2007:00:13:48 -0700]
"GET /~foo/puzzle-bar-aaab.jpg HTTP/1.0" 302 528 "-"
 "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.6)
 Gecko/20070725 Firefox/2.0.0.6"

"""

import os
import re
import sys
import urllib
import shutil
import argparse


def read_urls(filename):
    """Returns a list of the puzzle urls from the given log file,
    extracting the hostname from the filename itself.
    Screens out duplicate urls and returns the urls sorted into
    increasing order."""
    # +++your code here+++
    with open(filename, "r") as apache_list:
        url_list = apache_list.read().split("\n")
    host_list = [extract_host_name(url)for url in url_list if "GET " in url]
    host_list = filter(lambda url: "puzzle" in url,
                       host_list)

    host_list = list(set(host_list))

    second_word = re.findall("puzzle\/.-....-(....).jpg", host_list[0])

    host_dict = {}
    if second_word:
        for url in host_list:
            sorted_word = re.findall(r'puzzle\/.-....-(....).jpg', url)
            host_dict[url] = sorted_word
    else:
        for url in host_list:
            sorted_word = re.findall(r'puzzle\/.-(....).jpg', url)
            host_dict[url] = sorted_word

    sorted_host_list = sorted(host_dict.items(), key=lambda x: x[1])
    sorted_host_list = [host_tuple[0] for host_tuple in sorted_host_list]
    completed_url_list = add_prefixes(filename, sorted_host_list)

    return completed_url_list


def extract_host_name(url):
    """returns the host name from a given url"""
    host = re.findall(r'GET (\S+) HTTP', url)
    return host[0]


def add_prefixes(filename, host_list):
    """adds server prefixes to the urls in host_list"""
    server_name = "https://" + re.findall(r'\S+\_(\S+)', filename)[0]
    completed_url_list = [server_name + host for host in host_list]
    return completed_url_list


def download_images(img_urls, dest_dir):
    """Given the urls already in the correct order, downloads
    each image into the given directory.
    Gives the images local filenames img0, img1, and so on.
    Creates an index.html in the directory
    with an img tag to show each local image file.
    Creates the directory if necessary.
    """
    create_new_directory(dest_dir)
    index_html = "<html> \n <body> \n"
    for url in img_urls:
        index_html += "<img src='" + url + "'/>"
        save_pics(url, img_urls.index(url), dest_dir)
    index_html += "\n </body> \n </html>"
    with open(dest_dir + "/index.html", "w") as index_html_file:
        index_html_file.write(index_html)


def create_new_directory(dest_dir):
    """If the destination directory does not already exist,
    creates the destination directory."""
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)


def save_pics(url, num, dest_dir):
    """Given an url, a number, and a destination directory,
    downloads the image available at the url to the test directory
    with a filename in a format that includes 'img' and the number"""
    print("Retrieving and saving " + url)
    img_dest = dest_dir + "/img" + str(num)
    urllib.urlretrieve(url, img_dest)


def create_parser():
    """Create an argument parser object"""
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--todir',  help='destination directory for downloaded images')
    parser.add_argument('logfile', help='apache logfile to extract urls from')

    return parser


def main(args):
    """Parse args, scan for urls, get images from urls"""
    parser = create_parser()

    if not args:
        parser.print_usage()
        sys.exit(1)

    parsed_args = parser.parse_args(args)

    img_urls = read_urls(parsed_args.logfile)

    if parsed_args.todir:
        download_images(img_urls, parsed_args.todir)
    else:
        print('\n'.join(img_urls))


if __name__ == '__main__':
    main(sys.argv[1:])
