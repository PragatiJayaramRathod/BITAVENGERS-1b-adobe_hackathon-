import fitz  
import json
import os
from pathlib import Path
from datetime import datetime

def load_input_files(input_dir):
    persona = (Path(input_dir) / "persona.txt").read_text(encoding="utf-8").strip()
    job = (Path(input_dir) / "job.txt").read_text(encoding="utf-8").strip()
    docs = [f for f in Path(input_dir).glob("*.pdf") if f.is_file()]
    return persona, job, docs

def extract_sections(doc, persona, job):
    sections = []
    prev_size, prev_flags = 10, 0
    for page_num in range(len(doc)):
        page = doc[page_num]
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if "lines" not in block:
                continue
            for line in block["lines"]:
                for span in line["spans"]:
                    heading_level = is_heading(span, prev_size, prev_flags)
                    if heading_level:
                        text = span["text"].strip()
                        relevance = calculate_relevance(text, persona, job)
                        sections.append({
                            "document": doc.name,
                            "page_number": page_num + 1,
                            "section_title": text,
                            "importance_rank": relevance
                        })
                        prev_size, prev_flags = span["size"], span["flags"]
    return sorted(sections, key=lambda x: x["importance_rank"])

def is_heading(span, prev_size, prev_flags):
    size, flags = span["size"], span["flags"]
    text = span["text"].strip()
    if len(text) > 100 or not text:
        return None
    if size > 10 and (flags & 16):  
        if size >= prev_size * 1.2:
            return "H1" if size > 14 else "H2"
        elif size >= prev_size * 0.8:
            return "H2" if size > 12 else "H3"
    return None

def calculate_relevance(text, persona, job):
    keywords = job.lower().split() + persona.lower().split()
    count = sum(1 for keyword in keywords if keyword in text.lower())
    return max(1, 6 - min(count, 5))  

def extract_subsections(doc, sections):
    sub_sections = []
    for section in sections:
        page = doc[section["page_number"] - 1]
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if "lines" in block:
                text = " ".join(line["spans"][0]["text"] for line in block["lines"] if line["spans"])
                if len(text.strip()) < 100:  
                    relevance = calculate_relevance(text, "", section["section_title"])
                    sub_sections.append({
                        "document": doc.name,
                        "page_number": section["page_number"],
                        "refined_text": text.strip()[:50] + "..." if len(text) > 50 else text,
                        "importance_rank": relevance
                    })
    return sorted(sub_sections, key=lambda x: x["importance_rank"])

def process_documents(input_dir, output_dir):
    persona, job, docs = load_input_files(input_dir)
    output = {
        "metadata": {
            "documents": [doc.name for doc in docs],
            "persona": persona,
            "job_to_be_done": job,
            "processing_timestamp": datetime.utcnow().isoformat() + "Z"
        },
        "extracted_sections": [],
        "sub_section_analysis": []
    }
    
    for doc_path in docs:
        with fitz.open(doc_path) as doc:
            sections = extract_sections(doc, persona, job)
            sub_sections = extract_subsections(doc, sections)
            output["extracted_sections"].extend(sections[:5]) 
            output["sub_section_analysis"].extend(sub_sections[:5])  
    
    output_path = Path(output_dir) / "result.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

def main():
    input_dir = Path("/app/input")
    output_dir = Path("/app/output")
    output_dir.mkdir(exist_ok=True)
    process_documents(input_dir, output_dir)

if __name__ == "__main__":
    main()
