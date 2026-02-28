"""
Extensive Seed Script for ML Training
=====================================
Seeds 10 vendors, 15 POs, 50 invoices, operational proofs.
This gives enough data for:
- RandomForest GL Auto-Coder (Feature 5)
- KDE Duplicate Detection (Feature 6) 
- Bayesian ITC Trust Scoring (Feature 7)
- Bayesian Variance Thresholds (Feature 4)
"""

from database import engine, SessionLocal, Base
import models
import datetime
import random

# Create all tables
Base.metadata.create_all(bind=engine)

db = SessionLocal()

# Clear old data
db.query(models.AuditLog).delete()
db.query(models.InvoiceLineItem).delete()
db.query(models.Invoice).delete()
db.query(models.OperationalProof).delete()
db.query(models.PurchaseOrderItem).delete()
db.query(models.PurchaseOrder).delete()
db.query(models.Vendor).delete()
db.commit()

# ============================================================
# 1. VENDORS (10 vendors with payment history)
# ============================================================
vendors = [
    {"id": "V-001", "name": "Honda Components Ltd",     "trust": 0.92, "total": 48, "success": 45},
    {"id": "V-002", "name": "Syrma SGS Technology",     "trust": 0.88, "total": 35, "success": 31},
    {"id": "V-003", "name": "Tata Steel Limited",       "trust": 0.95, "total": 60, "success": 58},
    {"id": "V-004", "name": "Reliance Jio Infocomm",    "trust": 0.78, "total": 25, "success": 20},
    {"id": "V-005", "name": "Mahindra Logistics",       "trust": 0.85, "total": 40, "success": 35},
    {"id": "V-006", "name": "Infosys BPM Services",     "trust": 0.90, "total": 30, "success": 28},
    {"id": "V-007", "name": "Larsen & Toubro Ltd",      "trust": 0.93, "total": 55, "success": 52},
    {"id": "V-008", "name": "Wipro IT Services",        "trust": 0.82, "total": 20, "success": 17},
    {"id": "V-009", "name": "Godrej Properties",        "trust": 0.70, "total": 15, "success": 11},
    {"id": "V-010", "name": "DHL Express India",        "trust": 0.87, "total": 42, "success": 37},
]

for v in vendors:
    db.add(models.Vendor(
        id=v["id"], name=v["name"], trust_score=v["trust"],
        historical_payments=v["total"], successful_payments=v["success"]
    ))

print(f"Seeded {len(vendors)} vendors.")
db.commit()

# ============================================================
# 2. PURCHASE ORDERS (15 POs with line items)
# ============================================================
pos = [
    {"id": "PO-2024-001", "vendor": "V-001", "amount": 150000, "status": "open", "items": [
        {"desc": "Steel Fasteners M8 50-pack", "qty": 100, "rate": 500, "uom": "pack"},
        {"desc": "Hex Bolts Grade 8.8",        "qty": 200, "rate": 500, "uom": "piece"},
    ]},
    {"id": "PO-2024-002", "vendor": "V-002", "amount": 75000, "status": "open", "items": [
        {"desc": "PCB Assembly Module Type-A", "qty": 50, "rate": 1000, "uom": "unit"},
        {"desc": "SMD Resistor 10K Ohm",       "qty": 5000, "rate": 5,  "uom": "piece"},
    ]},
    {"id": "PO-2024-003", "vendor": "V-003", "amount": 500000, "status": "open", "items": [
        {"desc": "Hot Rolled Steel Coil 3mm",   "qty": 10, "rate": 45000, "uom": "ton"},
        {"desc": "Cold Rolled Sheet 1.2mm",     "qty": 5,  "rate": 10000, "uom": "ton"},
    ]},
    {"id": "PO-2024-004", "vendor": "V-004", "amount": 120000, "status": "open", "items": [
        {"desc": "Enterprise Internet 1Gbps",  "qty": 12, "rate": 10000, "uom": "month"},
    ]},
    {"id": "PO-2024-005", "vendor": "V-005", "amount": 200000, "status": "open", "items": [
        {"desc": "Warehouse Logistics Service", "qty": 4,  "rate": 50000, "uom": "month"},
    ]},
    {"id": "PO-2024-006", "vendor": "V-006", "amount": 300000, "status": "open", "items": [
        {"desc": "IT Helpdesk Support L1",     "qty": 6, "rate": 30000, "uom": "month"},
        {"desc": "Application Support L2",     "qty": 6, "rate": 20000, "uom": "month"},
    ]},
    {"id": "PO-2024-007", "vendor": "V-007", "amount": 1500000, "status": "open", "items": [
        {"desc": "Civil Construction Phase-1", "qty": 1,  "rate": 1000000, "uom": "lot"},
        {"desc": "Electrical Wiring Works",    "qty": 1,  "rate": 500000,  "uom": "lot"},
    ]},
    {"id": "PO-2024-008", "vendor": "V-008", "amount": 180000, "status": "open", "items": [
        {"desc": "Cloud Migration Services",   "qty": 3, "rate": 60000, "uom": "phase"},
    ]},
    {"id": "PO-2024-009", "vendor": "V-009", "amount": 2400000, "status": "open", "items": [
        {"desc": "Office Lease Monthly Rent",  "qty": 12, "rate": 200000, "uom": "month"},
    ]},
    {"id": "PO-2024-010", "vendor": "V-010", "amount": 90000, "status": "open", "items": [
        {"desc": "Express Courier Domestic",   "qty": 300, "rate": 200, "uom": "shipment"},
        {"desc": "International Freight Air",  "qty": 30,  "rate": 1000, "uom": "kg"},
    ]},
    {"id": "PO-2024-011", "vendor": "V-001", "amount": 85000, "status": "open", "items": [
        {"desc": "Brake Disc Assembly Kit",    "qty": 50, "rate": 1700, "uom": "kit"},
    ]},
    {"id": "PO-2024-012", "vendor": "V-003", "amount": 320000, "status": "closed", "items": [
        {"desc": "Structural Steel H-Beam",    "qty": 8, "rate": 40000, "uom": "ton"},
    ]},
    {"id": "PO-2024-013", "vendor": "V-005", "amount": 95000, "status": "open", "items": [
        {"desc": "Last Mile Delivery Service", "qty": 500, "rate": 190, "uom": "delivery"},
    ]},
    {"id": "PO-2024-014", "vendor": "V-006", "amount": 450000, "status": "open", "items": [
        {"desc": "SAP FICO Implementation",    "qty": 1, "rate": 450000, "uom": "project"},
    ]},
    {"id": "PO-2024-015", "vendor": "V-007", "amount": 750000, "status": "open", "items": [
        {"desc": "HVAC Installation Plant-B",  "qty": 1, "rate": 750000, "uom": "lot"},
    ]},
]

for po in pos:
    db.add(models.PurchaseOrder(
        id=po["id"], vendor_id=po["vendor"],
        total_amount=po["amount"], status=po["status"]
    ))
    for item in po["items"]:
        db.add(models.PurchaseOrderItem(
            po_id=po["id"], description=item["desc"],
            quantity=item["qty"], rate=item["rate"], uom=item["uom"]
        ))

print(f"Seeded {len(pos)} purchase orders with line items.")
db.commit()

# ============================================================
# 3. HISTORICAL INVOICES (Supervised Learning Labels & Anomalies)
# ============================================================
# Seed 150+ highly varied invoices to train the Random Forest & KDE algorithms
gl_codes = {
    "hardware":    "GL5100300",
    "software":    "GL5100500",
    "telecom":     "GL5300200",
    "logistics":   "GL5100800",
    "consulting":  "GL5200300",
    "maintenance": "GL5300400",
    "construction":"GL5400100",
    "rent":        "GL5300100",
    "utilities":   "GL5300200",
    "travel":      "GL5200100",
}

invoices = []
invoice_line_items = []
audit_logs = []

# Base standard behavior
for i in range(1, 151):
    # Pick a random PO
    po = random.choice(pos)
    vendor_id = po["vendor"]
    is_anomaly = random.random() < 0.15 # 15% chance of anomaly
    has_po = random.random() > 0.10     # 10% chance it arrives without PO
    
    inv_id = f"INV-2024-{1000+i}"
    
    # Variance Logic
    amount_variance = 1.0
    if is_anomaly:
        amount_variance = random.choice([1.10, 0.90, 1.25, 0.50]) # 10% or 25% price variances
        desc_add = random.choice([" + dynamic freight surcharge", " + expedite fee", " (partial delivery)", " - weather delay discount"])
    else:
        # Micro penny variances (common in real world)
        amount_variance = random.uniform(0.995, 1.005)
        desc_add = " monthly billing"
        
    inv_amount = round(po["amount"] * amount_variance, 2)
    
    # Determine GL code based on Vendor pseudo-domain
    base_gl = "GL5100300" # Default hardware
    if vendor_id in ["V-004", "V-008"]: base_gl = "GL5100500" # Software/Telecom
    if vendor_id in ["V-005", "V-010"]: base_gl = "GL5100800" # Logistics
    if vendor_id in ["V-006", "V-009"]: base_gl = "GL5200300" # Consulting/Rent
    if vendor_id in ["V-007"]: base_gl = "GL5400100"          # Construction
    
    invoices.append({
        "id": inv_id,
        "vendor": vendor_id,
        "po": po["id"] if has_po else None,
        "amount": inv_amount,
        "desc": f"Invoice against {po['id']}{desc_add}",
        "gl": base_gl,
        "status": "approved" if not is_anomaly else random.choice(["pending", "rejected"])
    })
    
    # Seed Invoice Line Items with UOM Mismatches
    for item in po["items"]:
        qty_variance = 1.0 if not is_anomaly else random.choice([0.5, 0.8, 1.0])
        inv_uom = item["uom"]
        # Inject UOM mismatches (e.g. PO says 'pack', Invoice says 'pieces')
        if random.random() < 0.2:
            if inv_uom == "pack": inv_uom = "piece"
            elif inv_uom == "ton": inv_uom = "kg"
            elif inv_uom == "month": inv_uom = "days"
            
        invoice_line_items.append({
            "inv_id": inv_id,
            "desc": item["desc"],
            "qty": item["qty"] * qty_variance,
            "rate": item["rate"] * amount_variance,
            "uom": inv_uom
        })
        
    # Build Episodic Memory (Audit Logs) for HUMAN decisions on past variances
    days_ago = random.randint(1, 180)
    decision_date = datetime.datetime.now(datetime.UTC) - datetime.timedelta(days=days_ago)
    
    if is_anomaly and has_po:
        action = "approved_variance" if inv_amount < po["amount"] * 1.15 else "rejected_variance"
        log = f"Agent flagged {amount_variance*100-100:.1f}% variance. Human reviewer: {action} due to market conditions."
        audit_logs.append({"inv_id": inv_id, "action": action, "agent": "human_reviewer", "details": log, "date": decision_date})
    elif not has_po:
        audit_logs.append({"inv_id": inv_id, "action": "po_requested", "agent": "intake_agent", "details": "PO missing, emailed vendor.", "date": decision_date})
    else:
        audit_logs.append({"inv_id": inv_id, "action": "auto_approved", "agent": "root_orchestrator", "details": "Matched entirely within tolerance.", "date": decision_date})


for inv in invoices:
    days_ago = random.randint(1, 180)
    db.add(models.Invoice(
        id=inv["id"], vendor_id=inv["vendor"], po_number=inv["po"],
        amount=inv["amount"], description=inv["desc"],
        gl_code=inv["gl"], status=inv["status"],
        date_received=datetime.datetime.now(datetime.UTC) - datetime.timedelta(days=days_ago)
    ))

for item in invoice_line_items:
    db.add(models.InvoiceLineItem(
        invoice_id=item["inv_id"], description=item["desc"],
        quantity=item["qty"], rate=item["rate"], uom=item["uom"]
    ))

print(f"Seeded {len(invoices)} historical invoices with variance/UOM complexities.")
db.commit()


# Configure Audit Logs
for log in audit_logs:
    db.add(models.AuditLog(
        invoice_id=log["inv_id"], action=log["action"],
        agent=log["agent"], details=log["details"]
    ))
print(f"Seeded {len(audit_logs)} Episodic Memory Audit Logs.")
db.commit()


# ============================================================
# 4. OPERATIONAL PROOFS (Unstructured RAG Context for SES Deadlocks)
# ============================================================
# Simulated emails, gate logs, and GRNs for the Agent to semantic-search against
proofs = [
    {"source": "email_plant_manager", "content": "Confirming HVAC installation Plant-B completed by L&T on Jan 15. Pending SES creation.", "days": 30},
    {"source": "gate_digital_log", "content": "GRN-2024-8812: 10 Tons Hot Rolled Steel Coil received from Tata Steel. Plate #MH12-8812.", "days": 25},
    {"source": "teams_chat_it", "content": "Wipro cloud migration Phase 1 is done. We can approve invoice INV-2024-1035.", "days": 20},
    {"source": "email_warehouse", "content": "Alert: We only received 5000 units of SMD Resistors from Syrma (PO-2024-002), short by 500.", "days": 15},
    {"source": "gate_digital_log", "content": "DHL Express picked up 50 packages. Tracking series #99812-99862.", "days": 10},
    {"source": "email_facilities", "content": "Godrej rent for March paid. Includes ad-hoc $500 maintenance fee for lobby repair.", "days": 8},
    {"source": "jira_ticketing", "content": "Infosys SLA met for current month: 99.8% uptime L2 support.", "days": 5},
    {"source": "gate_digital_log", "content": "Honda parts delivery. Note: Arrived in 20 'boxes', not 'packs' as per PO.", "days": 3},
    {"source": "email_network", "content": "Jio bandwidth upgraded to 1Gbps active as of 12:00 AM.", "days": 2},
]

for p in proofs:
    db.add(models.OperationalProof(
        source=p["source"], content=p["content"],
        date=datetime.datetime.now(datetime.UTC) - datetime.timedelta(days=p["days"])
    ))

print(f"Seeded {len(proofs)} unstructured Operational Proofs for RAG.")

db.commit()
db.close()

print("\n" + "="*50)
print("COMPLEX SEED COMPLETE!")
print("="*50)
print(f"  Vendors:           {len(vendors)}")
print(f"  Purchase Orders:   {len(pos)}")
print(f"  Invoices (Train):  {len(invoices)}")
print(f"  Line Item Complex: {len(invoice_line_items)}")
print(f"  Episodic Logs:     {len(audit_logs)}")
print(f"  Operational Proofs:{len(proofs)}")
print("="*50)
print("ML models will now train on highly adversarial data at server startup.")
