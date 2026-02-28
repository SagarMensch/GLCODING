<!-- image -->

<!-- image -->

## MASTER DATA MANAGEMENT

Comprehensive Approach Note

Vendor • Services • Materials • Governance

Prepared For:

Jubilant Foodworks Limited

Prepared By:

SequelString

January 2026

<!-- image -->

## Executive Summary

This document addresses the master data management challenges identified during our discovery session. MDM forms the foundation of every procurement and payment process - when master data is inconsistent, problems cascade through the entire P2R lifecycle.

<!-- image -->

6K+

Vendor Codes (Possible Duplicates)

## Key Assumptions

The  following  assumptions  are  based  on  our  discovery  discussions  and  should  be  validated  during assessment:

- Vendor Master: There may be significant duplication in vendor records (~6,000+ codes with estimated 500+ duplicates)
- Services Classification: Services may currently be purchased as materials with incorrect tax treatment (HSN instead of SAC codes)
- Material Descriptions: Same materials could have different descriptions across locations
- Governance: There may be limited approval workflows for master data creation/changes
- Cross-System Sync: Master data updates in SAP may not propagate to all 15+ connected systems

## Challenge 1: Vendor Duplicates

## Potential Issues Identified

The vendor master may contain approximately 6,000+ codes with significant duplication. Same vendors could exist under different names:

| Pattern                  | Example A         | Example B                 |
|--------------------------|-------------------|---------------------------|
| Legal suffix differences | ABC Foods Pvt Ltd | ABC Foods Private Limited |
| Spelling variations      | Amul Dairy        | Amual Dairy               |
| Abbreviations            | XYZ & Company     | XYZANDCO                  |
| Branch vsHQ              | Vendor (Mumbai)   | Vendor Corporate          |

## Business Impact (Potential)

- Cannot consolidate spend for volume negotiations
- Same vendor may receive payments through multiple codes
- Duplicate payment risk across vendor codes
- Inaccurate vendor performance analysis

<!-- image -->

Services Master (Gap Identified)

<!-- image -->

15+

Disconnected Systems

<!-- image -->

No

Formal Governance

<!-- image -->

## Proposed Solution: Intelligent Vendor Deduplication

## INTELLIGENTVENDORDEDUPLICATION

<!-- image -->

## The Deduplication Process

```
Step 1: Name Standardization - Convert to UPPERCASE - Remove: PVT, PRIVATE, LTD, LIMITED, INC, LLC - Expand: & → AND, CO → COMPANY - Remove: M/S, M/s, punctuation Example: "M/s. ABC Foods Pvt. Ltd." → "ABC FOODS" Step 2: Multi-Factor Comparison Name Similarity:     50% weight Tax ID (GSTIN):      25% weight City/Location:       15% weight Bank Account:        10% weight TOTAL SCORE = weighted sum of all factors Step 3: Decision Rules IF score >= 95% → AUTO-MERGE (clearly same vendor) IF score 85-94% → REVIEW QUEUE (needs confirmation) IF score < 85%  → NO ACTION (different vendors)
```

## Expected Outcomes

Metric

| Vendor codes        | 6,000+      | ~5,000 unique   |
|---------------------|-------------|-----------------|
| Duplicate detection | Manual/None | Automated       |
| Spend consolidation | Fragmented  | Unified view    |

## Alternative Approach: API-Based Golden Record

## If historical deduplication is too complex initially :

- Focus on preventing future duplicates using government APIs
- New vendor provides only GSTIN and PAN
- System calls GSTN/MCA APIs to auto-populate legal details
- Duplicate check before any new record creation
- Existing duplicates cleaned gradually

## Challenge 2: Missing Services Master

## Potential Issues Identified

This is a critical gap. Buying services as materials may cause:

- Wrong Tax Codes: HSN codes (for goods) used instead of SAC codes (for services)
- Incorrect GL Posting: COGS accounts instead of Operating Expenses
- GST Compliance Risk: Services incorrectly reported as goods in returns
- No Price Governance: Same service may cost different amounts across locations
- Zero Visibility: Cannot analyze service spend by category

## Proposed Solution: Autonomous Service Governance Layer

## AUTONOMOUSSERVICEGOVERNANCELAYER

IT Support: 998314 @ 18%

Security: 998211 @18%

Cleaning:998212@18%

Repair/Maint:998721@18%

Marketing:998361@18%

Legal: 998211 @ 18%

<!-- image -->

## SERVICE-MATERIALFIREWALL

Keywords detected:"Repair","Install","Visit"

GLCode=Material?→BLoCKED

Forcescorrectclassification

## DIGITAL SERVICE ENTRY(SES)

- 1.Vendor uploads completion photo
2. GPS confirms location at store
- 3.Auto-createsSESforpayment

100%SERVICECOMPLIANCE·CORRECTTAX·AUDITREADY

## Solution Component 1: Semantic Service Auto-Taxonomy

When a user types "fix fridge" or "AC repair", the system maps the intent to a Universal Service Master ID:

```
User Input: "Fix AC unit in kitchen" ↓ System Analysis: Detects "fix", "AC", "repair" keywords ↓ Maps to: SRV-AC-MAINT (AC Maintenance) ↓ Auto-assigns: SAC 998721 | GL 5200400 | GST 18%
```

## Solution Component 2: SAC-Locked Tax Compliance

Every Service Master ID is hard-linked to its government-mandated SAC Code:

| Service Category         |   SAC Code | GST Rate   | GL Account          |
|--------------------------|------------|------------|---------------------|
| IT Support & Maintenance |     998314 | 18%        | Technology Expenses |
| Security Services        |     998211 | 18%        | Security Expenses   |
| Facility Management      |     998212 | 18%        | Facilities Expenses |
| Cleaning & Housekeeping  |     998212 | 18%        | Cleaning Expenses   |

| Repair & Maintenance    |   998721 | 18%   | Maintenance Expenses   |
|-------------------------|----------|-------|------------------------|
| Marketing & Advertising |   998361 | 18%   | Marketing Expenses     |
| Legal & Professional    |   998211 | 18%   | Professional Fees      |
| Manpower/Staffing       |   998519 | 18%   | Contract Labor         |

## Solution Component 3: Regional Rate Card Vault

Price standardization across all locations:

```
Service: SRV-AC-MAINT (AC Maintenance) Regional Rate Card: Tier 1 Cities (Delhi, Mumbai, Bangalore): ₹2,500/visit Tier 2 Cities (Lucknow, Jaipur, Indore):  ₹1,800/visit Tier 3 Cities:                             ₹1,200/visit When PO created: System detects store location → Auto-populates correct rate No manual price entry → Price governance enforced
```

## Solution Component 4: Service-Material Firewall

Prevents misclassification by keyword detection:

```
Firewall Logic: Scan description for service keywords: "Repair", "Installation", "Visit", "Labor", "Maintenance", "Cleaning", "Service" IF keywords detected AND GL = Material Account: → BLOCK transaction → Force reclassification to Services Result: 100% of service spend correctly classified
```

## Solution Component 5: Digital Service Entry Sheet (SES)

Proof-of-service verification:

- . Vendor Completes Work: Uploads completion photo via mobile app

- . GPS Verification: System confirms vendor was at store location

- . Time Validation: Check-in/check-out tracked

- . Auto-SES Creation: Digital service entry generated

- . Payment Ready: Audit-ready documentation for processing

## Alternative Approach: Mandatory Classification

## If semantic classification is complex initially :

- Add mandatory "Is this a Service?" checkbox at PO creation
- If Service = Yes, show dropdown of service categories
- System auto-populates SAC code and GL based on selection
- Cannot save without proper classification

## Challenge 3: Material Description Inconsistency

## Potential Issues Identified

Same materials may have different descriptions across locations:

| Location 1   | Location 2             | Location 3           |
|--------------|------------------------|----------------------|
| MOZZ CHZ 1KG | Mozzarella Cheese 1Kg  | Mozerella Chz 1000GM |
| TOM KETCH 5L | Tomato Ketchup 5 Litre | Ketchup Tomato 5LTR  |

## Business Impact

- Cannot aggregate demand across stores
- Cannot negotiate volume discounts (no consolidated view)
- Inaccurate inventory reporting
- Forecasting models fail

## Proposed Solution: Semantic Material Normalization

```
Standardization Process: Found: "Dairy - Mozzarella Cheese 1 Kilogram Block" (92% match)
```

```
1. User enters: "Mozz Chz 1Kg pkt" 2. System analyzes: Product: Mozzarella Cheese (from "Mozz Chz") Size: 1 Kilogram (from "1Kg") Package: Packet (from "pkt") 3. System searches existing catalog: 4. System prompts: "Material already exists. Did you mean: ☑ Dairy - Mozzarella Cheese 1 Kilogram Block ☐ Create new (requires justification)"
```

## Standard Naming Format

Format: [Category] - [Product Name] [Size] [Unit] [Package]

## Examples

Dairy - Mozzarella Cheese 1 Kilogram Block

Condiments - Tomato Ketchup 5 Litre Bottle

Packaging - Pizza Box 12 Inch Pack of 50

## Alternative Approach: Picklist-Only Materials

## If semantic analysis is complex :

- Central team maintains approved material catalog
- Store managers can only select from picklist
- No free-form descriptions allowed
- New materials require formal request and approval

## Challenge 4: MDM Governance

## Potential Issues Identified

- Anyone may be able to create or modify master data
- No approval workflow for new vendors
- Bank detail changes made without verification
- No duplicate checking at point of entry
- Limited audit trail of changes

## Proposed Solution: Centralized MDM Governance

## MDMGOVERNANCEWORKFLOW

<!-- image -->

| Data Owner       | Overall accountability, sets policies, escalation point   | 3-5 people   |
|------------------|-----------------------------------------------------------|--------------|
| Data Steward     | Day-to-day management, reviews/approves records           | 5-10 people  |
| Data Entry Users | Submit requests with documentation                        | As needed    |

## Request-to-Activation Workflow

## New Vendor Request:

Step 1: SUBMIT

User provides: GSTIN, PAN, supporting documents

## Step 2: AUTOMATIC VALIDATION

- GSTIN format check

- GSTN API lookup for legal details

- PAN-GSTIN consistency check

- Duplicate check (same PAN/GSTIN exists?)

## Step 3: STEWARD REVIEW

- Verify supporting documents

- Confirm no duplicates

- Approve or return for corrections

## Step 4: ACTIVATE

- Create in SAP

- Sync to all 15 connected systems

## High-Risk Change Controls

Bank account changes require additional verification:

- . Documentation: New cancelled cheque, letterhead confirmation
- . Validation: Penny-drop test to verify account
- . Hold Period: 24-hour payment freeze
- . Notification: All stakeholders alerted

## Alternative Approach: Simple Approval Workflow

## If full governance is too complex initially :

- Implement basic approval workflow for all changes
- Manager approval required for new records
- Dual approval for bank detail changes
- Audit log for all modifications

## Implementation Approach

## Phased Roadmap

| Phase         | Duration   | Focus                         | Deliverables                       |
|---------------|------------|-------------------------------|------------------------------------|
| 1. Assessment | Weeks 1-3  | Extract data, profile quality | Quality report, duplicate analysis |

| 2. Vendor Cleanup   | Weeks 4-8   | Deduplication, merge execution   | Clean vendor master    |
|---------------------|-------------|----------------------------------|------------------------|
| 3. Services Master  | Weeks 9-12  | Build classification, rate cards | Service taxonomy live  |
| 4. Governance       | Weeks 13-16 | Workflows, controls              | Full governance active |

## Solution Selection Guide

| Challenge         | Recommended                 | Alternative If                             |
|-------------------|-----------------------------|--------------------------------------------|
| Vendor Duplicates | Multi-factor Dedup          | API prevention if cleanup too complex      |
| Services Master   | Autonomous Governance Layer | Mandatory dropdown if simpler start needed |
| Material Naming   | Semantic Normalization      | Picklist-only if strict control preferred  |
| Governance        | Full MDMGovernance          | Simple approval if quick start needed      |

## Next Steps

- . Validate assumptions during detailed assessment
- . Prioritize - Services Master may be highest impact
- . Extract samples from vendor and material masters
- . Define governance roles with stakeholders