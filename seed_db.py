import datetime
from database import engine, SessionLocal
import models

# Create all tables
models.Base.metadata.create_all(bind=engine)

def seed_database():
    db = SessionLocal()
    
    # Check if already seeded
    if db.query(models.Vendor).first():
        print("Database already seeded.")
        return

    # 1. Seed Vendors
    vendors = [
        models.Vendor(id="V-001", name="Honda Components Ltd", trust_score=0.9, historical_payments=50, successful_payments=50),
        models.Vendor(id="V-002", name="Syrma SGS Technology", trust_score=0.85, historical_payments=100, successful_payments=95),
        models.Vendor(id="V-003", name="Tata Steel", trust_score=0.99, historical_payments=500, successful_payments=500),
        models.Vendor(id="V-004", name="Reliance Logistics", trust_score=0.6, historical_payments=10, successful_payments=8),
        # A new vendor with no history
        models.Vendor(id="V-005", name="SteelCorp Suppliers", trust_score=0.5, historical_payments=0, successful_payments=0)
    ]
    db.add_all(vendors)
    db.commit()

    # 2. Seed POs
    pos = [
        models.PurchaseOrder(id="PO-2024-001", vendor_id="V-001", total_amount=150000, status="open"),
        models.PurchaseOrder(id="PO-2024-002", vendor_id="V-002", total_amount=75000, status="open"),
        models.PurchaseOrder(id="PO-2024-003", vendor_id="V-003", total_amount=200000, status="closed")
    ]
    db.add_all(pos)
    db.commit()

    # 3. Seed PO Line Items
    po_items = [
        models.PurchaseOrderItem(po_id="PO-2024-001", description="Fasteners 50-pack", quantity=100, rate=50.0, uom="pack"),
        models.PurchaseOrderItem(po_id="PO-2024-001", description="Steel brackets type A", quantity=50, rate=200.0, uom="piece"),
        models.PurchaseOrderItem(po_id="PO-2024-002", description="Microcontroller ATmega328", quantity=1000, rate=75.0, uom="unit"),
        models.PurchaseOrderItem(po_id="PO-2024-003", description="Cold rolled steel sheet 5mm", quantity=10, rate=20000.0, uom="ton"),
    ]
    db.add_all(po_items)
    db.commit()

    # 4. Seed Operational Proofs (for SES)
    proofs = [
        models.OperationalProof(source="email", content="AC repair completed at Plant A on Jan 15", date=datetime.datetime(2024, 1, 15)),
        models.OperationalProof(source="gate_log", content="Security guard delivery from ABC Services", date=datetime.datetime(2024, 1, 16)),
        models.OperationalProof(source="chat", content="Maintenance completed - elevator repair", date=datetime.datetime(2024, 1, 17)),
    ]
    db.add_all(proofs)
    db.commit()
    
    # 5. Seed Historical Invoices (to test KDE Duplicate Agent later)
    invoices = [
        models.Invoice(id="INV-HIST-001", vendor_id="V-001", po_number="PO-2024-001", amount=145000, description="Part delivery Jan", status="approved", gl_code="GL5100300"),
        models.Invoice(id="INV-HIST-002", vendor_id="V-002", amount=75000, description="PCB boards batch 1", status="approved", gl_code="GL5100300"),
    ]
    db.add_all(invoices)
    db.commit()

    print("Database seeded successfully with base records.")

if __name__ == "__main__":
    seed_database()
