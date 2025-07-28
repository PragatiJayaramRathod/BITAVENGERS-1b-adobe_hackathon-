# BITAVENGERS-1b-adobe_hackathon-

**Adobe India Hackathon 2025 - Round 1B Solution**

**Overview**

This repository contains the solution for Round 1B: Persona-Driven Document Intelligence of the Adobe India Hackathon 2025, themed "Connect What Matters — For the User Who Matters". The solution builds an intelligent document analyst that extracts and prioritizes relevant sections from a collection of 3-10 PDFs based on a specific persona and their job-to-be-done. It is designed to be generic, efficient, and accurate across diverse domains, personas, and tasks.


**Approach**


The solution leverages PyMuPDF (fitz) for PDF parsing and implements a rule-based, heuristic-driven system to analyze and rank document sections. The approach is modular and adaptable, avoiding machine learning models to meet the ≤ 1GB size constraint. Key components include:

**Input Processing:**

Accepts 3-10 PDFs, a persona (e.g., PhD Researcher, Investment Analyst), and a job-to-be-done (e.g., literature review, financial analysis).


Parses PDFs with PyMuPDF to extract text, metadata, and structure (headings, pages).


**Section Relevance Ranking:**

Identifies sections (H1, H2, H3) using heuristics (font size, boldness, text length, hierarchy).
Matches sections to the persona’s expertise and job-to-be-done using keyword matching and context analysis.
Assigns an importance_rank (1-5, 1 being most relevant) based on keyword frequency, section depth, and task alignment.
Example: For a PhD Researcher, sections with "methodologies" or "benchmarks" rank higher.


**Sub-section Analysis:**

Extracts granular sub-sections under relevant sections.
Refines text by summarizing or trimming irrelevant details, preserving key content.
Ranks sub-sections based on relevance to the job-to-be-done (e.g., focusing on "reaction kinetics" for a Chemistry Student).


**Multilingual Support:**

Handles Unicode text in any language using PyMuPDF’s text extraction and ensure_ascii=False in JSON encoding.


**Output Generation:**

Produces JSON in the required format, processing all documents in /app/input and saving output in /app/output.
Includes metadata (documents, persona, job, timestamp) and ranked sections/sub-sections.

**Performance Optimization:**

Optimized to process 3-5 documents in ≤ 60 seconds on an 8-CPU, 16GB RAM system.
Uses lightweight dependencies (~50MB for PyMuPDF, well within 1GB limit).


**Docker Compatibility:**

Runs in a python:3.9-slim container for AMD64 architecture.
Operates offline with --network none.
Mounts /app/input (PDFs, persona, job files) and /app/output for I/O.



**Dependencies**

PyMuPDF (1.23.6): A lightweight (~50MB) library for PDF parsing and text extraction.
No external models or API calls required, ensuring compliance with offline and ≤ 1GB constraints.


**Directory Structure**


BITAVENGERS-1b-adobe_hackathon-/


├── Dockerfile


├── README.md


├── approach_explanation.md


├── requirements.txt


├── process_pdfs_round1b.py


**Dockerfile:** Defines the AMD64 image, installs dependencies, and sets up execution.
**README.md:** This file, documenting the solution and instructions.
**approach_explanation.md:** Explains the methodology (300-500 words, included below).
**requirements.txt:** Lists PyMuPDF==1.23.6.
**process_pdfs_round1b.py:** Main script for Round 1B processing.

**Approach Explanation (approach_explanation.md)**

This solution implements a persona-driven document intelligence system using a rule-based approach with PyMuPDF for PDF parsing. The methodology prioritizes generality and efficiency to handle diverse document collections (e.g., research papers, financial reports), personas (e.g., Researcher, Analyst), and jobs (e.g., literature review, trend analysis).

The process begins with parsing PDFs to extract text blocks, headings, and page numbers using PyMuPDF’s "dict" output. Heuristics identify section hierarchies (H1, H2, H3) based on font size, boldness, and text length, ensuring robustness across layouts. A keyword-based relevance engine then matches sections to the persona’s expertise and job-to-be-done, defined in input files (e.g., JSON or text). Keywords are derived from the job description (e.g., "methodologies" for a PhD Researcher), with weights adjusted for frequency and section depth.

Sub-section analysis refines extracted text by summarizing content relevant to the task, using simple truncation or sentence filtering to meet size constraints. Rankings (1-5) are assigned based on keyword density and contextual alignment, validated against test cases (e.g., prioritizing "revenue trends" for an Investment Analyst).

Performance is optimized by caching parsed text and limiting processing to relevant sections, achieving ≤ 60 seconds for 3-5 documents on an 8-CPU, 16GB RAM system. The solution avoids ML models to stay within the ≤ 1GB limit, relying on lightweight PyMuPDF (~50MB). Multilingual support is enabled through Unicode handling, tested with Japanese PDFs. The modular design supports future integration with Adobe’s PDF Embed API in Round 2, with separate functions for parsing, ranking, and output generation


**How to Build and Run**


**Prerequisites**

Docker: Install Docker Desktop (or Docker CLI for Linux) from docker.com.
Input Files: Prepare a directory with 3-10 PDFs, a persona.txt (role description), and a job.txt (task) in input.

**Build the Docker Image**

Navigate to the project directory:cd path/to/adobe-hackathon-2025-round1b

Build the Docker image:docker build --platform linux/amd64 -t persona-doc-analyzer:v1 .


--platform linux/amd64: Ensures AMD64 compatibility.
-t persona-doc-analyzer:v1: Names the image persona-doc-analyzer with tag v1.
.: Specifies the current directory with the Dockerfile.



**Run the Docker Container**

Create input and output directories:

        mkdir input output


Place PDFs, persona.txt, and job.txt in input.

Run the container:
        
        docker run --rm -v $(pwd)/input:/app/input -v $(pwd)/output:/app/output --network none persona-doc-analyzer:v1


        --rm: Removes the container post-execution.
        
        -v $(pwd)/input:/app/input: Mounts local input to /app/input.
        
        -v $(pwd)/output:/app/output: Mounts local output to /app/output.
        
        --network none: Enforces offline execution.


**Check output for a result.json file.**

**Expected Output**

A single result.json in /app/output:

{
  
  
  "metadata": {
    
    
    "documents": ["doc1.pdf", "doc2.pdf", "doc3.pdf"],
    
    
    "persona": "PhD Researcher in Computational Biology",
    
    
    "job_to_be_done": "Prepare a comprehensive literature review focusing on methodologies, datasets, and performance benchmarks",
    
    
    "processing_timestamp": "2025-07-28T09:33:00Z"
  
  
  },
  
  
  "extracted_sections": 
  
  [
    
    
    {
      
      
      "document": "doc1.pdf",
      
      
      "page_number": 1,
      
      
      "section_title": "Methodologies",
      
      
      "importance_rank": 1
    
    
    }
  
  
  ],
  
  
  "sub_section_analysis": [
    
    
    {
      
      
      "document": "doc1.pdf",
      
      
      "page_number": 2,
      
      
      "refined_text": "Summary of methodology X...",
      
      
      "importance_rank": 1
    
    
    }
  
  
  ]


}

**Testing**

**Local Testing:**

Install dependencies:
      
        
        pip install -r requirements.txt


Run:
        
        python process_pdfs_round1b.py


**Multilingual Issues:**


Ensure json.dump uses ensure_ascii=False for Unicode support.
