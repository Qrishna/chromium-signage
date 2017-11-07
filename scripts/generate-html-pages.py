#!/usr/bin/env python3

import glob

images = glob.glob("images/*.jp*g")
webpages = "html/"

# def sanitize_file_names_array(strings_array):
#     return ["".join(e for e in strings_array[x] if e.isalnum()) for x in range(0, len(strings_array)) ]

def sanitize_file_name(string):
    return "".join(e for e in string if e.isalnum())

for image in images:
    print(image)
    if "/" in image:
        splitted_names = image.split("/")
        size = len(splitted_names)
        html_file_name = sanitize_file_name(splitted_names[size-1]).strip(".jp*g") + ".html"
    else:
        html_file_name = sanitize_file_name(image.strip("")).strip(".jp*g") + ".html"

    data = """<!DOCTYPE html>
<html>
<head>
<style>
body, html {
    height: 100%;
    margin: 0;
}

.bg {
    /* The image used */ """ + \
           "\n\tbackground-image: url(\""+ "../"+image + "\");""""
    /* Full height */
    height: 100%;

    /* Center and scale the image nicely */
    background-position: center;
    background-repeat: no-repeat;
    background-size: cover;
}
</style>
</head>
<body>

<div class="bg"></div>

</body>"""
    fp = open (webpages + html_file_name, "w+")
    fp.write(data)
    fp.close()
