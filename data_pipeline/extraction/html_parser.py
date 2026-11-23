
import re
from bs4 import BeautifulSoup


def _clean(value):
    return re.sub(r"\s+", " ", value or "").strip()


def parse_html(content):
    soup = BeautifulSoup(content, "html.parser")
    for tag in soup(["script", "style", "noscript", "svg", "iframe", "form"]):
        tag.decompose()
    title_tag = soup.find("meta", attrs={"property": "og:title"})
    title = _clean(title_tag.get("content", "") if title_tag else "")
    if not title:
        heading = soup.find("h1") or soup.find("title")
        title = _clean(heading.get_text(" ", strip=True)) if heading else ""
    date = ""
    for props in ({"property": "article:published_time"}, {"itemprop": "datePublished"},
                  {"name": "date"}, {"name": "pubdate"}):
        tag = soup.find("meta", attrs=props)
        if tag and tag.get("content", ""):
            date = _clean(tag["content"])
            break
    if not date:
        tag = soup.find("time", datetime=True)
        date = tag.get("datetime", "") if tag else ""
    body = next((node for sel in ("article", "[itemprop='articleBody']", ".article-body",
                     ".entry-content", "main") if (node := soup.select_one(sel))), soup.body or soup)
    for tag in body(["nav", "footer", "aside", "header"]):
        tag.decompose()
    paragraphs = [_clean(p.get_text(" ", strip=True)) for p in body.find_all(["p", "h2", "h3", "li"])]
    paragraphs = [p for p in paragraphs if p]
    if not paragraphs:
        paragraphs = [_clean(body.get_text(" ", strip=True))]
    
    table_lines = []
    for tr in body.select("table tr"):
        cells = [_clean(cell.get_text(" ", strip=True)) for cell in tr.find_all(["th", "td"], recursive=False)]
        if len(cells) >= 2:
            table_lines.append("  ".join(cells))
    text = "\n".join(paragraphs + table_lines)
    return {"title": title, "published_date": date,
            "sections": [{"page_number": None, "kind": "html_content", "text": text}]}
