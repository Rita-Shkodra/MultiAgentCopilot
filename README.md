# Multi-Agent Supply Chain Copilot  

An evidence-grounded, multi-agent enterprise assistant that analyzes supply chain and transportation risks using retrieved corporate documents only.

The system performs structured planning, document retrieval, executive synthesis, and compliance verification — with full observability and prompt-injection defense.

---
## Live Demo

A working demo of the **Supply Chain Copilot** is available at:
https://supply-chain-copilot.streamlit.app/

# Architecture Overview

The system uses a 4-agent workflow built with **LangGraph**:

## Planner
- Breaks the business task into structured steps  
- Generates optimized research queries  
- Returns structured JSON plan  

##  Researcher
- Retrieves relevant evidence from vector database  
- Filters weak matches  
- Deduplicates chunks  

## Writer
- Produces board-ready executive deliverable  
- Strictly grounded in retrieved evidence  
- Enforces required output structure  

## Verifier
- Verifies every claim against retrieved evidence  
- Blocks unsupported statements  
- Returns PASS / FAIL  

---
### Data Sources
- All knowledge is taken from publicly available reports:
- UPS 10-K
- FedEx Annual Report
- DHL Report
- Amazon 10-K
- Target 10-K
- BCG Resilience Report
- McKinsey OTIF Analysis
- Deloitte Supply Chain Report
- CSCMP Glossary
- Inventory Turnover
- World Bank LPI Report

# Security & Guardrails

The system includes strong prompt-injection defense:

- Business task treated as untrusted input  
- Retrieved evidence treated as untrusted document text  
- Ignores instructions inside evidence  
- Never reveals system or developer messages  
- Never fabricates citations  
- Never uses external data  

The Verifier blocks:
- Invented numbers  
- Undocumented mitigation strategies  
- New entities or events  
- Direct contradictions  

If no relevant evidence exists → the system explicitly states so.

---

# Observability

Each agent logs:

- Status  
- Latency (ms)  
- Token usage  
- Errors  

Displayed in the Streamlit dashboard with:

- Total agent time  
- Total tokens used  
- Execution trace  

---

# Repository Structure
- /app → Streamlit UI app.py
- /agents → Planner, Researcher, Writer, Verifier, Guards
- /retrieval → Loaders, chunking, vectorstore
- /data → Documents + data README
- /eval → Evaluation set test_prompts.txt + test runner run_eval.py
- orchestrator.py → LangGraph workflow
- pipeline.py → Execution entry point
- README.md → Project documentation

# Evaluation set
- Located in : /eval/test_prompts.txt
Includes 10 structured tests covering:

- Risk analysis
- Mitigation identification
- Supplier concentration
- Fuel exposure
- Prompt injection attempts
- Unsupported topic detection
- Hidden document fabrication attempts 


### Installation
- Create virtual environment : python -m venv venv
- Activate environment : venv\Scripts\activate
- Install dependencies: pip install -r requirements.txt
- Add .env file: OPENAI_API_KEY=your_api_key_here
- Run the application: streamlit run app/app.py

### Run Evaluation

- bash:  python -m eval/run_eval.py

- Outputs:
- PASS / FAIL per test
- Token usage per test
- Summary statistics
### Acceptance Criteria 

- End-to-end multi-agent routing
- Output includes citations
- Verifier blocks unsupported claims
- Prompt injection defense implemented
- Trace log visible
- Observability table (latency + tokens)
- Evaluation set (10 tests)
- Runs locally within 5 minutes

### Nice to have features implemented
- Prompt Injection Defense
- Observability Table 
- Evaluation Set

 ### Example Output Structure
 - EXECUTIVE SUMMARY:
- CLIENT EMAIL:
- Subject:
- Greeting:
- Body:
- Closing:

- ACTION LIST:
- Action:
- Owner:
- Due date:
- Confidence:

- SOURCES:
- DocumentName#chunk-id