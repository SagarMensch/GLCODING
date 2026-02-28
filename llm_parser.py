import httpx
import json
import logging
import os
from dotenv import load_dotenv

# Load environment variables (Rule 5: Engineer for Reversibility)
load_dotenv()

MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY", "zuo8I57aSASX5O066kZbjMsCPHWzkb2u")
MISTRAL_URL = "https://api.mistral.ai/v1/chat/completions"


def _safe_float(val, default=None):
    """Safely convert a value to float, handling None, strings, and invalid types."""
    if val is None or val == "":
        return default
    try:
        if isinstance(val, str):
            val = val.replace(',', '')  # Strip commas before float conversion
        return float(val)
    except (ValueError, TypeError):
        return default


def _sanitize_line_items(items):
    """Ensure every line item has valid numeric fields."""
    if not isinstance(items, list):
        return []
    cleaned = []
    for item in items:
        if not isinstance(item, dict):
            continue
        cleaned.append({
            "description": str(item.get("description", "")),
            "quantity": _safe_float(item.get("quantity"), 0.0),
            "rate": _safe_float(item.get("rate"), 0.0),
        })
    return cleaned


def parse_invoice_text(raw_text: str) -> dict:
    """Uses Mistral JSON mode to extract highly structured data from messy invoice text in chunks.
    
    Breaks massive Markdown strings (e.g. 30,000+ chars from 15 pages) into 4,000 character chunks
    to avoid LLM API timeouts or context window overallocation.
    """
    
    CHUNK_SIZE = 4000
    chunks = [raw_text[i:i+CHUNK_SIZE] for i in range(0, len(raw_text), CHUNK_SIZE)]
    logging.info(f"Split {len(raw_text)} characters into {len(chunks)} chunks of {CHUNK_SIZE} chars to prevent LLM timeouts.")
    
    master_result = {
        "vendor_name": "Unknown",
        "amount": None,
        "po_number": None,
        "description": "",
        "line_items": []
    }
    
    headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Process chunks sequentially
    for idx, chunk in enumerate(chunks):
        logging.info(f"Processing LLM Chunk {idx+1}/{len(chunks)}...")
        
        prompt = f"""
        You are an elite Accounts Payable extraction AI. Your job is to extract highly accurate financial data from a specific chunk of OCR text.
        
        Always respond in valid JSON using EXACTLY this schema:
        {{
            "vendor_name": "string",
            "amount": "float or null",
            "po_number": "string or null",
            "description": "string",
            "line_items": [
                {{
                    "description": "string",
                    "quantity": 0.0,
                    "rate": 0.0
                }}
            ]
        }}
        
        IMPORTANT RULES:
        1. PO NUMBER: Look for "Purchase Order", "PO No.". If none, `null`.
        2. AMOUNT: Look for Total Amount, Grand Total. If no clear grand total is in this specific text chunk, output `null`. Do not guess.
        3. DATA TYPES: `amount`, `quantity`, and `rate` MUST be floats. Strip commas.
        4. VENDOR: Standardize primary billing entity to an uppercase string.
        5. If this chunk is just random terms and has no invoice data, output nulls and empty lists.
        
        --- RAW INVOICE TEXT CHUNK ({idx+1}/{len(chunks)}) ---
        {chunk}
        """

        payload = {
            "model": "mistral-large-latest",
            "messages": [{"role": "user", "content": prompt}],
            "response_format": {"type": "json_object"},
            "temperature": 0.0
        }

        try:
            with httpx.Client(timeout=45.0) as client:
                response = client.post(MISTRAL_URL, headers=headers, json=payload)
                response.raise_for_status()
            
            result_content = response.json()["choices"][0]["message"]["content"]
            extracted_data = json.loads(result_content)
            
            # Merge findings into master record
            if extracted_data.get("vendor_name") and extracted_data["vendor_name"].upper() not in ["", "UNKNOWN", "STRING"]:
                if master_result["vendor_name"] == "Unknown":
                     master_result["vendor_name"] = extracted_data["vendor_name"]
                     
            if extracted_data.get("po_number") and str(extracted_data["po_number"]).upper() not in ["NULL", "NONE", "STRING"]:
                if not master_result["po_number"]:
                     master_result["po_number"] = extracted_data["po_number"]
                     
            if extracted_data.get("description") and str(extracted_data["description"]).upper() not in ["", "STRING"]:
                if not master_result["description"]:
                     master_result["description"] = extracted_data["description"]
            
            # For amount, we only overwrite if we find a larger total (to avoid a subtotal overriding a grand total)
            chunk_amount = _safe_float(extracted_data.get("amount"))
            if chunk_amount and chunk_amount > 0:
                current_amount = _safe_float(master_result["amount"], 0.0)
                if chunk_amount > current_amount:
                    master_result["amount"] = chunk_amount
            
            # Append any line items found in this chunk
            chunk_items = _sanitize_line_items(extracted_data.get("line_items", []))
            if chunk_items:
                master_result["line_items"].extend(chunk_items)
                
            # Early exit heuristic: If we found Vendor, PO, Amount, and some line items, we might not need to read 10 more pages of terms & conditions.
            if (master_result["vendor_name"] != "Unknown" and 
                master_result["amount"] is not None and 
                master_result["amount"] > 0 and 
                len(master_result["line_items"]) > 0 and
                idx >= 1): # At least read 2 chunks to be safe
                logging.info(f"Early exit triggered at chunk {idx+1}. Sufficient data extracted.")
                break
                
        except Exception as e:
            logging.error(f"LLM Parsing failed on chunk {idx+1}: {str(e)}")
            continue # Try the next chunk even if this one failed
            
    # Final sanity check: If amount is still None but we have line items, calculate it
    final_amount = _safe_float(master_result["amount"])
    if (final_amount is None or final_amount == 0.0) and master_result["line_items"]:
        master_result["amount"] = sum(item.get("quantity", 0.0) * item.get("rate", 0.0) for item in master_result["line_items"])
        logging.info(f"Final Amount computed from line items: {master_result['amount']}")

    return master_result
