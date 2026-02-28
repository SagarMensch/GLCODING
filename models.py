from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from database import Base
import datetime

class Vendor(Base):
    __tablename__ = "vendors"
    
    id = Column(String, primary_key=True, index=True)
    name = Column(String, index=True)
    trust_score = Column(Float, default=0.6)
    historical_payments = Column(Integer, default=0)
    successful_payments = Column(Integer, default=0)

class PurchaseOrder(Base):
    __tablename__ = "purchase_orders"
    
    id = Column(String, primary_key=True)
    vendor_id = Column(String, ForeignKey("vendors.id"))
    total_amount = Column(Float)
    status = Column(String)  # open, closed
    
    vendor = relationship("Vendor")
    items = relationship("PurchaseOrderItem", back_populates="po")

class PurchaseOrderItem(Base):
    __tablename__ = "po_items"
    
    id = Column(Integer, primary_key=True, index=True)
    po_id = Column(String, ForeignKey("purchase_orders.id"))
    description = Column(String)
    quantity = Column(Float)
    rate = Column(Float)
    uom = Column(String)
    
    po = relationship("PurchaseOrder", back_populates="items")

class Invoice(Base):
    __tablename__ = "invoices"
    
    id = Column(String, primary_key=True)
    vendor_id = Column(String, ForeignKey("vendors.id"))
    po_number = Column(String, ForeignKey("purchase_orders.id"), nullable=True)
    ses_number = Column(String, nullable=True)
    amount = Column(Float)
    description = Column(String)
    date_received = Column(DateTime, default=datetime.datetime.utcnow)
    status = Column(String, default="pending")  # pending, approved, rejected, blocked
    gl_code = Column(String, nullable=True)
    is_duplicate = Column(Boolean, default=False)
    
class InvoiceLineItem(Base):
    __tablename__ = "invoice_line_items"
    
    id = Column(Integer, primary_key=True, index=True)
    invoice_id = Column(String, ForeignKey("invoices.id"))
    description = Column(String)
    quantity = Column(Float)
    rate = Column(Float)
    uom = Column(String, nullable=True) # Added for advanced UOM variance training
    matched_po_item_id = Column(Integer, nullable=True)

class OperationalProof(Base):
    __tablename__ = "operational_proofs"
    # Replaces the hardcoded "unstructured operational data"
    id = Column(Integer, primary_key=True, index=True)
    source = Column(String) # email, gate_log, chat
    content = Column(String)
    date = Column(DateTime)
    
class AuditLog(Base):
    __tablename__ = "audit_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    invoice_id = Column(String, ForeignKey("invoices.id"))
    action = Column(String)
    agent = Column(String)
    details = Column(Text)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
