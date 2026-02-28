import asyncio
import json
import io
import os
from server import ocr_engine, orchestrator

async def process_test_file():
    filepath = r"C:\Users\sagar\Downloads\23rd January1-26\LD-AA583721\Commercial Invoice.PDF"
    print("="*50)
    print(f"Testing File: {filepath}")
    print("="*50)
    
    if not os.path.exists(filepath):
        print(f"Error: File does not exist: {filepath}")
        return

    with open(filepath, "rb") as f:
        file_bytes = f.read()
        
    print("\n--- STAGE 1: DOCLING EXTRACTION ---")
    docling_result = ocr_engine.extract(file_bytes, "Commercial Invoice.PDF")
    
    print("\n[Docling Markdown (Truncated to 1000 chars)]:")
    print(docling_result.get("raw_text", "No text extracted")[:1000])
    
    print("\n--- STAGE 2: MISTRAL LLM PARSING ---")
    print(json.dumps({k: v for k, v in docling_result.items() if k != "raw_text"}, indent=2))
    
    print("\n--- STAGE 3: MULTI-AGENT ORCHESTRATION ---")
    invoice_data = {
        "id": "INV-TEST-001",
        "vendor_id": "V-001",
        "vendor_name": docling_result.get("vendor_name", "Unknown"),
        "amount": docling_result.get("amount", 0.0),
        "description": docling_result.get("description", ""),
        "po_number": docling_result.get("po_number"),
        "line_items": docling_result.get("line_items", [])
    }
    
    # Sanitize inputs exactly as in server.py
    po_val = str(invoice_data.get("po_number", "")).strip()
    if po_val.lower() in ["", "none", "null", "not found", "false", "undefined"]:
        invoice_data["po_number"] = None
    else:
        invoice_data["po_number"] = po_val
        
    try:
        invoice_data["amount"] = float(invoice_data.get("amount", 0))
    except (ValueError, TypeError):
        invoice_data["amount"] = 0.0
        
    print("\n[Input to Orchestrator]:")
    print(json.dumps(invoice_data, indent=2))
    
    orchestrator_result = await orchestrator.process_invoice(invoice_data)
    
    print("\n[Orchestrator Result]:")
    print(json.dumps(orchestrator_result, indent=2))

if __name__ == "__main__":
    asyncio.run(process_test_file())
