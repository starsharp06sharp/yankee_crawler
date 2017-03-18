#!/usr/bin/env python3
import os
import re
import sys
import requests
from htmldom import htmldom
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader(sys.path[0]))
template = env.get_template('template.html')


def load_request_list(path):
    with open(path) as f:
        return [line.strip() for line in f.readlines()]


def get_title_and_slides(html_doc):
    title = html_doc.find('title').text()
    slides = []

    for dl in html_doc.find('#eData').children('dl'):
        dd_list = dl.children('dd')
        if dd_list.length() != 7:
            print('warning when get %s' % title)
        slides.append({
            'img_src': dd_list[0].text(),
            'description': dd_list[4].text()
        })

    return title, slides

if __name__ == '__main__':
    list_file_name = sys.argv[1]
    count = 1
    for url in load_request_list(list_file_name):
        r = requests.get(url)
        print(r.status_code)
        html_doc = htmldom.HtmlDom().createDom(r.content.decode('gb18030'))

        title, slides = get_title_and_slides(html_doc)
        output_name = '%s_%02d' % (list_file_name, count)
        with open('./out/%s.html' % output_name, 'w') as f:
            f.write(template.render(
                title=title,
                slides=slides
            ))
        count += 1
