from textwrap import dedent
from datetime import datetime
import urllib.parse
import re

def on_env(env, **kwargs):
    env.globals["current_year"] = datetime.now().year


x_intent = "https://twitter.com/intent/tweet"
fb_sharer = "https://www.facebook.com/sharer/sharer.php"
include = re.compile(r"blog/[1-9].*")

def on_page_markdown(markdown, **kwargs):
    page = kwargs['page']
    config = kwargs['config']
    if not include.match(page.url):
        return markdown

    page_url = config.site_url+page.url
    page_title = urllib.parse.quote(page.title+'\n')

    return markdown + dedent(f"""
    [:simple-x:]({x_intent}?text={page_title}&url={page_url}){{ .md-button .icon-only }}
    [:simple-facebook:]({fb_sharer}?u={page_url}){{ .md-button .icon-only }}
    """)
