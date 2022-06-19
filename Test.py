from html2image import Html2Image

hti = Html2Image(custom_flags=['--no-sandbox'])
hti.browser_executable = "/usr/bin/google-chrome"
html = """<h1> An interesting title </h1> This page will be red"""
css = "body {background: red;}"

file = hti.screenshot(html_str=html, css_str=css, save_as='red_page.png')