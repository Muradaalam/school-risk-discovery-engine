
import re
from defusedxml import ElementTree as ET


def clean(value):
    return re.sub(r"\s+", " ", value or "").strip()


def tag_name(tag):
    return tag.rsplit("}", 1)[-1].lower()


def value_of(node):
    return clean(" ".join(node.itertext()))


def child(node, *names):
    names = set(names)
    for element in node:
        if tag_name(element.tag) in names:
            return element
    return None


def parse_xml(content):
    try:
        root = ET.fromstring(content)
    except ET.ParseError as error:
        raise ValueError(f"Invalid XML: {error}") from error
    sections = []
    items = [x for x in root.iter() if tag_name(x.tag) in ("item", "entry")]
    if items:
        for index, item in enumerate(items, 1):
            title = child(item, "title")
            summary = child(item, "description", "summary", "content", "encoded")
            date = child(item, "pubdate", "published", "updated", "date")
            link = child(item, "link")
            url = (link.attrib.get("href") or value_of(link)) if link is not None else ""
            sections.append({"page_number": index, "kind": "xml_entry",
                             "title": value_of(title) if title is not None else "",
                             "text": "\n".join(filter(None, [value_of(title) if title is not None else "",
                                                              value_of(summary) if summary is not None else ""])),
                             "published_date": value_of(date) if date is not None else "",
                             "entry_url": url})
    else:
        
        lines = [value_of(element) for element in root.iter() if len(element) == 0 and element.text]
        sections.append({"page_number": None, "kind": "xml_content", "text": "\n".join(lines)})
    title = child(root, "title")
    return {"title": value_of(title) if title is not None else "", "published_date": "", "sections": sections}
