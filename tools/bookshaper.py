import os
import re
from bs4 import BeautifulSoup
from llm.prompt_manager import PromptManager
from llm.prompt_templates import PROMPT_TEMPLATES

def extract_chapters_from_html(html_path):
    """Extracts chapters from a structured HTML file into title/text dictionaries."""
    with open(html_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    chapters = []
    for i, div in enumerate(soup.find_all("div", class_="chapter")):
        header = div.find(["h1", "h2", "h3"])
        raw_title = header.get_text(strip=True) if header else f"Chapter {i + 1}"
        lower_title = raw_title.lower()

        if header:
            header.extract()  # remove title from the body text

        text = div.get_text("\n", strip=True)
        chapters.append({
            "title": raw_title,
            "chapter_title": lower_title,
            "text": text
        })
    return chapters

def rewrite_chapter(chapter, prompt_manager: PromptManager, template_name="AF.SatiricalRewrite", allow_expensive=True):
    """Uses a prompt template to rewrite a chapter."""
    print(f"\n🖋 Rewriting: {chapter['title']}")
    rewritten = prompt_manager.run_template(
        name=template_name,
        variables={"input": chapter["text"]},
        metadata={
            "chapter_title": chapter["chapter_title"],
            "source": "The Prince",
            "allow_expensive": allow_expensive
        }
    )
    return rewritten

def safe_filename(text):
    """Sanitize filename for filesystem."""
    return re.sub(r'[\\/*?:"<>|]', "-", text).replace(" ", "_")

def process_book(html_path, output_dir="rewritten_chapters", limit=1, allow_expensive=False, offset=0):
    """Main entrypoint: loads HTML, rewrites chapters, saves results."""
    os.makedirs(output_dir, exist_ok=True)
    chapters = extract_chapters_from_html(html_path)
    pm = PromptManager()

    for chapter in chapters[offset:offset + limit]:
        rewritten = rewrite_chapter(chapter, pm, allow_expensive=allow_expensive)
        filename = safe_filename(chapter["title"]) + ".txt"
        path = os.path.join(output_dir, filename)
        with open(path, "w", encoding="utf-8") as f:
            f.write(rewritten)
        print(f"✅ Saved: {path}")

if __name__ == "__main__":
    process_book("the_prince.html", limit=26, allow_expensive=True, offset=8)
