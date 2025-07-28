

This solution implements a **persona-driven document intelligence system** using a rule-based approach with **PyMuPDF** for PDF parsing. The methodology prioritizes **generality** and **efficiency** to handle diverse document collections (e.g., research papers, financial reports), personas (e.g., Researcher, Analyst), and jobs (e.g., literature review, trend analysis).

The process begins with parsing PDFs to extract text blocks, headings, and page numbers using **PyMuPDF**’s `"dict"` output. Heuristics identify section hierarchies (H1, H2, H3) based on font size, boldness, and text length, ensuring robustness across layouts. A keyword-based relevance engine then matches sections to the **persona**’s expertise and **job-to-be-done**, defined in input files (e.g., JSON or text). Keywords are derived from the job description (e.g., "methodologies" for a PhD Researcher), with weights adjusted for frequency and section depth.

Sub-section analysis refines extracted text by summarizing content relevant to the task, using simple truncation or sentence filtering to meet size constraints. Rankings (1-5) are assigned based on keyword density and contextual alignment, validated against test cases (e.g., prioritizing "revenue trends" for an Investment Analyst).

Performance is optimized by caching parsed text and limiting processing to relevant sections, achieving ≤ 60 seconds for 3-5 documents on an 8-CPU, 16GB RAM system. The solution avoids ML models to stay within the ≤ 1GB limit, relying on lightweight **PyMuPDF** (~50MB). Multilingual support leverages Unicode handling, tested with Japanese PDFs. The modular design supports future integration with Adobe’s PDF Embed API in Round 2, with separate functions for parsing, ranking, and output generation.
