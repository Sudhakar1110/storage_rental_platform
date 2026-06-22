# Storage Rental Platform — Standard Operating Procedure (SOP)

**Version:** 1.0  
**Platform:** Frappe Framework v15 / ERPNext v15  
**App Name:** `storage_rental_platform`  
**Last Updated:** June 2026

---

## Table of Contents

1. [System Overview](#1-system-overview)
2. [Architecture & Directory Structure](#2-architecture--directory-structure)
3. [Installation & Setup](#3-installation--setup)
4. [User Roles & Permissions](#4-user-roles--permissions)
5. [Master Data Management](#5-master-data-management)
6. [Transaction Processing](#6-transaction-processing)
7. [Workflows](#7-workflows)
8. [Reports & Analytics](#8-reports--analytics)
9. [Demo Data](#9-demo-data)
10. [Maintenance & Troubleshooting](#10-maintenance--troubleshooting)
11. [Frequently Asked Questions](#11-frequently-asked-questions)

---

## 1. System Overview

### 1.1 Purpose

The **Storage Rental Platform** is a Frappe/ERPNext app that provides a complete digital solution for managing storage facility rentals. It handles the full lifecycle from facility management through customer booking, rental agreements, payment collection, and unit handovers.

### 1.2 Business Processes Covered

```
Facility Setup → Unit Categorization → Customer Onboarding
         ↓
    Booking Creation → Confirmation → Active Rental
         ↓
    Rental Agreement → Payments → Handover → Completion
```

### 1.3 Core Modules

| Module | Description |
|--------|-------------|
| **Masters** | Facilities, Units, Categories, Customers, Plans, Pricing |
| **Transactions** | Bookings, Agreements, Payments, Handovers |
| **Reports** | 7 Script Reports for operational analytics |
| **Workflows** | 2 automated workflows for Bookings & Agreements |

---

## 2. Architecture & Directory Structure

### 2.1 File Layout

```
storage_rental_platform/
├── config/
│   └── desktop.py              # Desk configuration
├── fixtures/
│   ├── roles.json               # Custom roles (fixture)
│   ├── workflow_states.json     # Workflow states (fixture)
│   └── workflows.json           # Workflow definitions (fixture)
├── storage_rental_platform/     # Main module directory
│   ├── doctype/                 # DocType definitions (auto-detected by sync)
│   │   ├── customer_profile/
│   │   ├── handover_checklist/
│   │   ├── payment_collection/
│   │   ├── pricing/
│   │   ├── rental_agreement/
│   │   ├── rental_plan/
│   │   ├── storage_booking/
│   │   ├── storage_category/
│   │   ├── storage_facility/
│   │   ├── storage_unit/
│   │   ├── unit_amenity/
│   │   └── unit_handover/
│   ├── report/                  # Report definitions (auto-detected by sync)
│   │   ├── active_rental_report/
│   │   ├── customer_report/
│   │   ├── facility_occupancy_report/
│   │   ├── payment_collection_report/
│   │   ├── rental_agreement_report/
│   │   ├── storage_booking_report/
│   │   └── unit_availability_report/
│   └── workspace/               # Workspace definitions
│       └── Storage Rental Platform/
│           └── Storage Rental Platform.json
├── demo_data.py                 # Demo data generator
├── hooks.py                     # App hooks (fixtures, after_install, after_migrate)
├── install.py                   # Install/migrate scripts
├── modules.txt                  # Module list
├── patches.txt                  # Patch history
├── SOP.md                       # THIS DOCUMENT
└── README.md                    # Quick start guide
```

### 2.2 Key Frappe v15 Design Principles Used

| Principle | Implementation |
|-----------|---------------|
| **Standard directory layout** | DocTypes in `doctype/{name}/`, Reports in `report/{name}/`, Workspaces in `workspace/{name}/` |
| **Fixture-based import** | Roles, Workflows, Workflow States, Workspace imported via `hooks.py` `fixtures` list |
| **Script Reports** | All 7 reports are Script Reports with raw SQL for flexible querying |
| **Workflow-driven status** | `override_status: 0` keeps `status` field independent from `workflow_state` |
| **Module-based scoping** | Single module `storage_rental_platform` namespaces all records |

---

## 3. Installation & Setup

### 3.1 Prerequisites

| Requirement | Version |
|-------------|---------|
| Frappe Framework | v15.x or higher |
| ERPNext | v15.x or higher |
| Python | 3.10+ |
| Node.js | 18.x+ |
| MariaDB | 10.6+ |

### 3.2 Installation Steps

```bash
# 1. Get the app
bench get-app storage_rental_platform https://github.com/Sudhakar1110/storage_rental_platform.git

# 2. Install on your site
bench --site yoursite install-app storage_rental_platform

# 3. Run migration (creates tables, imports fixtures, runs hooks)
bench --site yoursite migrate

# 4. Build frontend assets
bench build

# 5. Clear cache
bench --site yoursite clear-cache
bench --site yoursite clear-website-cache

# 6. Restart bench
bench restart
```

### 3.3 Post-Installation Checklist

- [ ] Workspace "Storage Rental Platform" visible in sidebar
- [ ] All 12 DocTypes created in module `storage_rental_platform`
- [ ] All 7 Reports created and linked to their Reference DocTypes
- [ ] 3 Custom Roles created (Storage Administrator, Facility Manager, Customer User)
- [ ] 2 Workflows active (Storage Booking Workflow, Rental Agreement Workflow)
- [ ] Demo data populated with 5 facilities, 22 units, 8 customers, 6 bookings, etc.

### 3.4 Verifying Installation via Console

```bash
bench --site yoursite console
```

```python
# Check workspace
frappe.get_all("Workspace", filters={"module": "storage_rental_platform"})

# Check DocTypes
frappe.get_all("DocType", filters={"module": "storage_rental_platform"})

# Check Reports
frappe.get_all("Report", filters={"ref_doctype": ["in", ["Storage Booking", "Rental Agreement"]]})

# Check roles
frappe.get_all("Role", filters={"name": ["in", ["Storage Administrator", "Facility Manager", "Customer User"]]})

# Verify demo data
frappe.db.count("Storage Facility")
frappe.db.count("Storage Unit")
frappe.db.count("Customer Profile")
frappe.db.count("Storage Booking")
```

---

## 4. User Roles & Permissions

### 4.1 Role Definitions

| Role | Description | Desk Access |
|------|-------------|-------------|
| **Storage Administrator** | Full access — create, read, update, delete, submit all DocTypes | Yes |
| **Facility Manager** | Can manage facilities, units, view customers, create bookings, manage handovers | Yes |
| **Customer User** | Can view own bookings, update own profile, create new bookings | Yes |

### 4.2 DocType-Level Permissions

| DocType | Storage Administrator | Facility Manager | Customer User |
|---------|-----------------------|------------------|---------------|
| **Storage Facility** | CRUD | Read, Write | Read |
| **Storage Unit** | CRUD | Read, Write | — |
| **Storage Category** | CRUD | Read, Write | — |
| **Customer Profile** | CRUD | Read, Write | Read, Write |
| **Rental Plan** | CRUD | Read | — |
| **Pricing** | CRUD | Read | — |
| **Storage Booking** | CRUD + Submit | Read, Write, Create | Read, Write, Create |
| **Rental Agreement** | CRUD + Submit | Read, Write, Create | — |
| **Payment Collection** | CRUD + Submit | Read, Write, Create, Submit | — |
| **Unit Handover** | CRUD + Submit | Read, Write, Create, Submit | — |

### 4.3 Assigning Roles to Users

In the Frappe Desk:
1. Go to **Setup > User**
2. Open the target user
3. In the **Roles** section, add one or more of:
   - `Storage Administrator`
   - `Facility Manager`
   - `Customer User`
4. Save

---

## 5. Master Data Management

### 5.1 Storage Facility

**Purpose:** Defines a physical storage location.

**Key Fields:**

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| Facility Name | Data | Yes | Auto-named from this field |
| Location | Data | Yes | City/area |
| Address | Small Text | No | Full address |
| Contact Number | Data | No | Phone |
| Email | Data | No | Email address |
| Facility Manager | Link (User) | No | Assigned manager |
| Status | Select | No | Active / Inactive |
| Description | Text Editor | No | Rich description |

**Procedure:**
1. Navigate to **Storage Rental Platform > Masters > Storage Facility**
2. Click **+ Add Storage Facility**
3. Fill in facility details (Name, Location, Address, etc.)
4. Set Status to **Active**
5. Save

### 5.2 Storage Category

**Purpose:** Classifies units by size tier (Small, Medium, Large, Extra Large).

**Key Fields:**

| Field | Type | Required |
|-------|------|----------|
| Category Name | Data | Yes |
| Description | Text Editor | No |
| Storage Type | Select | No (Small/Medium/Large/Extra Large) |
| Min Height (ft) | Float | No |
| Max Height (ft) | Float | No |
| Is Active | Check | No |

**Procedure:**
1. Navigate to **Storage Rental Platform > Masters > Storage Category**
2. Click **+ Add Storage Category**
3. Enter category name and description
4. Set height range
5. Ensure **Is Active** is checked
6. Save

### 5.3 Storage Unit

**Purpose:** An individual rentable storage space within a facility.

**Key Fields:**

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| Unit Number | Data | Yes | Auto-named from this field |
| Storage Category | Link (Storage Category) | Yes | Size tier |
| Storage Facility | Link (Storage Facility) | Yes | Parent facility |
| Unit Size | Data | No | e.g., "10x10" |
| Dimensions | Data | No | e.g., "10ft x 10ft x 10ft" |
| Floor | Int | No | Floor number |
| Monthly Rent | Currency | Yes | Current rent |
| Security Deposit | Currency | No | Required deposit |
| Status | Select | No | Available / Occupied / Maintenance / Reserved |
| Amenities | Table (Unit Amenity) | No | Child table of amenity items |

**Procedure:**
1. Navigate to **Storage Rental Platform > Masters > Storage Unit**
2. Click **+ Add Storage Unit**
3. Select the **Storage Facility** and **Storage Category**
4. Enter unit dimensions, floor, rent, and deposit
5. Set initial **Status** (typically Available)
6. Optionally add amenities via the child table
7. Save

### 5.4 Unit Amenity (Child Table)

**Purpose:** Lists amenities associated with a storage unit.

| Field | Type | Required |
|-------|------|----------|
| Amenity | Data | Yes |
| Description | Data | No |

**Common Amenities:** 24/7 CCTV Surveillance, Climate Control, Fire Safety System, Individual Lock, Drive-Up Access, Elevator Access, Shelving Included, Power Backup

### 5.5 Customer Profile

**Purpose:** Stores customer information for individuals and companies.

**Key Fields:**

| Field | Type | Required |
|-------|------|----------|
| Customer Name | Data | Yes |
| Customer Type | Select | Yes (Individual / Company) |
| Email | Data | Yes |
| Mobile Number | Data | No |
| Phone | Data | No |
| Address | Small Text | No |
| City / State / Pincode | Data | No |
| Country | Link (Country) | No |
| Date of Birth | Date | No |
| ID Proof Type | Select | No |
| ID Number | Data | No |
| Status | Select | No (Active / Inactive / Blocked) |
| Notes | Text Editor | No |

**Procedure:**
1. Navigate to **Storage Rental Platform > Masters > Customer Profile**
2. Click **+ Add Customer Profile**
3. Enter customer details
4. Collect and enter KYC documents (ID Proof, ID Number)
5. Set Status to **Active**
6. Save

### 5.6 Rental Plan

**Purpose:** Defines pricing plans with various durations and discounts.

**Key Fields:**

| Field | Type | Required |
|-------|------|----------|
| Plan Name | Data | Yes |
| Duration (Days) | Int | Yes |
| Duration Type | Select | Yes (Daily / Weekly / Monthly / Quarterly / Yearly) |
| Price | Currency | Yes |
| Discount Percentage | Float | No |
| Final Price | Currency | Read-only (auto-calculated) |
| Description | Text Editor | No |
| Is Active | Check | No |
| Features | Text Editor | No |

**Available Plans (Demo):**

| Plan | Duration | Price | Discount |
|------|----------|-------|----------|
| Daily Flex | 1 day | ₹100 | 0% |
| Monthly Basic | 30 days | ₹2,000 | 0% |
| Monthly Standard | 30 days | ₹4,000 | 5% |
| Quarterly Saver | 90 days | ₹10,800 | 10% |
| Half-Yearly Advantage | 180 days | ₹20,400 | 15% |
| Yearly Enterprise | 365 days | ₹36,000 | 20% |

### 5.7 Pricing

**Purpose:** Defines per-category and per-facility pricing rates.

**Key Fields:**

| Field | Type | Required |
|-------|------|----------|
| Pricing Name | Data | Yes |
| Storage Category | Link | Yes |
| Storage Facility | Link | Yes |
| Base Price | Currency | Yes |
| Price Per Day/Week/Month/Quarter/Year | Currency | No |
| Security Deposit | Currency | No |
| Is Active | Check | No |
| Effective From | Date | Yes |
| Effective To | Date | No |

---

## 6. Transaction Processing

### 6.1 Storage Booking

**Purpose:** Records a customer's intent to rent a storage unit.

**Workflow States:** Draft → Confirmed → Active → Completed / Cancelled

**Key Fields:**

| Field | Type | Required |
|-------|------|----------|
| Customer | Link (Customer Profile) | Yes |
| Storage Unit | Link (Storage Unit) | Yes |
| Rental Plan | Link (Rental Plan) | Yes |
| Booking Date | Date | Yes |
| Start Date | Date | Yes |
| End Date | Date | Yes |
| Status | Select | Yes |
| Monthly Rent | Currency | No |
| Security Deposit | Currency | No |
| Total Amount | Currency | No |
| Discount Amount | Currency | No |
| Advance Amount | Currency | No |
| Balance Amount | Currency | No |
| Special Requirements | Text Editor | No |

**Step-by-Step Procedure:**

1. Navigate to **Storage Rental Platform > Transactions > Storage Booking**
2. Click **+ Add Storage Booking**
3. Select the **Customer** (from Customer Profile)
4. Select the **Storage Unit** (must be Available or Reserved)
5. Select the **Rental Plan**
6. Set **Start Date** and **End Date**
7. Pricing fields auto-populate from the unit and plan
8. Save → Status is **Draft**
9. **Transition to Confirmed:** Click **Actions > Confirm** (requires Storage Administrator role)
10. **Transition to Active:** Click **Actions > Activate**
11. **Complete:** Click **Actions > Complete** when the rental period ends
12. **Cancel:** Click **Actions > Cancel** at any stage

### 6.2 Rental Agreement

**Purpose:** A legally binding document formalizing the rental arrangement.

**Workflow States:** Draft → Active → Expired / Terminated

**Key Fields:**

| Field | Type | Required |
|-------|------|----------|
| Storage Booking | Link (Storage Booking) | Yes |
| Customer | Link (Customer Profile) | Yes |
| Storage Unit | Link (Storage Unit) | Yes |
| Agreement Date | Date | Yes |
| Start Date / End Date | Date | Yes |
| Status | Select | Yes |
| Monthly Rent | Currency | Yes |
| Security Deposit | Currency | Yes |
| Total Rent | Currency | No |
| Payment Due Day | Int | No (default: 5) |
| Late Fee | Currency | No (default: ₹500) |
| Notice Period (Days) | Int | No (default: 30) |
| Terms and Conditions | Text Editor | No |

**Step-by-Step Procedure:**

1. Navigate to **Storage Rental Platform > Transactions > Rental Agreement**
2. Click **+ Add Rental Agreement**
3. Link to an existing **Storage Booking**
4. Customer and Storage Unit auto-populate from the booking
5. Set **Start Date**, **End Date**, **Monthly Rent**, **Security Deposit**
6. Configure **Payment Due Day** (e.g., 5th of each month)
7. Set **Late Fee** and **Notice Period**
8. Add **Terms and Conditions** (use template from demo data as reference)
9. Save → Status is **Draft**
10. **Activate:** Click **Actions > Activate**
11. **Terminate:** Click **Actions > Terminate** if needed
12. **Mark Expired:** Click **Actions > Mark Expired** when the agreement ends

### 6.3 Payment Collection

**Purpose:** Records payments received from customers.

**Key Fields:**

| Field | Type | Required |
|-------|------|----------|
| Customer | Link (Customer Profile) | Yes |
| Rental Agreement | Link (Rental Agreement) | No |
| Storage Booking | Link (Storage Booking) | No |
| Payment Date | Date | Yes |
| Payment Type | Select | Yes (Rent / Security Deposit / Late Fee / Other) |
| Payment Mode | Select | Yes (Cash / Bank Transfer / UPI / Credit Card / Debit Card / Cheque / Demand Draft) |
| Amount | Currency | Yes |
| GST Amount | Currency | No |
| Total Amount | Currency | No |
| Payment Status | Select | No (Pending / Completed / Failed / Refunded) |
| Reference Number | Data | No |
| Payment For Month | Date | No |

**Step-by-Step Procedure:**

1. Navigate to **Storage Rental Platform > Transactions > Payment Collection**
2. Click **+ Add Payment Collection**
3. Select the **Customer**
4. Optionally link to a **Rental Agreement** or **Storage Booking**
5. Set **Payment Date**
6. Select **Payment Type** (Rent, Security Deposit, etc.)
7. Select **Payment Mode** (Cash, UPI, Bank Transfer, etc.)
8. Enter **Amount** (and optional GST)
9. Enter **Reference Number** (transaction ID/cheque number)
10. Set **Payment Status** to Completed
11. If Rent, set **Payment For Month** to the billing month
12. Save and Submit

### 6.4 Unit Handover

**Purpose:** Manages physical move-in, move-out, and inspection of storage units.

**Key Fields:**

| Field | Type | Required |
|-------|------|----------|
| Rental Agreement | Link (Rental Agreement) | Yes |
| Customer | Link (Customer Profile) | Yes |
| Storage Unit | Link (Storage Unit) | Yes |
| Handover Type | Select | Yes (Move In / Move Out / Inspection) |
| Handover Date | Datetime | Yes |
| Status | Select | No (Scheduled / In Progress / Completed / Cancelled) |
| Keys Received | Check | No |
| Remote Received | Check | No |
| Access Card Received | Check | No |
| Unit Condition | Select | No (Excellent / Good / Fair / Poor) |
| Cleaning Status | Select | No (Clean / Needs Cleaning / Dirty) |
| Damage Notes | Text Editor | No |
| Checklist Items | Table (Handover Checklist) | No |

**Handover Checklist Items (Child Table):**

| Field | Type | Required |
|-------|------|----------|
| Checklist Item | Data | Yes |
| Checked | Check | No |
| Remarks | Small Text | No |

**Step-by-Step Procedure:**

1. Navigate to **Storage Rental Platform > Transactions > Unit Handover**
2. Click **+ Add Unit Handover**
3. Select the **Rental Agreement** (customer and unit auto-populate)
4. Select **Handover Type** (Move In for new rentals, Move Out for vacating)
5. Set **Handover Date** and time
6. Record which items were received (Keys, Remote, Access Card)
7. Assess **Unit Condition** and **Cleaning Status**
8. Add checklist items via the child table
9. Add any **Damage Notes** with photos if needed
10. Set Status to **Completed** once the handover is done
11. Save

---

## 7. Workflows

### 7.1 Storage Booking Workflow

**States & Transitions:**

```
                    ┌─────────────┐
                    │   DRAFT     │ (Initial - DocStatus 0)
                    └──────┬──────┘
                           │
              ┌────────────┼────────────┐
              │ Confirm    │            │ Cancel
              ▼            │            ▼
        ┌───────────┐      │      ┌────────────┐
        │ CONFIRMED │      │      │ CANCELLED  │ (DocStatus 2 - final)
        └─────┬─────┘      │      └────────────┘
              │            │
       ┌──────┼──────┐     │
       │ Activate   │ Cancel│
       ▼            │      │
 ┌──────────┐      │      │
 │  ACTIVE  │      │      │
 └─────┬────┘      │      │
       │           │      │
  ┌────┼────┐      │      │
  │    │    │      │      │
  │Compl│   │Term. │      │
  ▼    │    ▼      │      │
┌─────┐│ ┌──────┐ │      │
│COMP.││ │CANCEL│◄┘      │
└─────┘│ └──────┘◄───────┘
       │
       └──► CANCELLED (already handled above)
```

**Allowed Transitions:**

| From | To | Action | Allowed Role |
|------|----|--------|-------------|
| Draft | Confirmed | Confirm | Storage Administrator |
| Draft | Cancelled | Cancel | Storage Administrator |
| Confirmed | Active | Activate | Storage Administrator |
| Confirmed | Cancelled | Cancel | Storage Administrator |
| Active | Completed | Complete | Storage Administrator |
| Active | Cancelled | Terminate | Storage Administrator |

### 7.2 Rental Agreement Workflow

**States & Transitions:**

```
                    ┌─────────────┐
                    │   DRAFT     │ (Initial - DocStatus 0)
                    └──────┬──────┘
                           │
              ┌────────────┼────────────┐
              │ Activate   │            │ Terminate
              ▼            │            ▼
        ┌───────────┐      │      ┌──────────────┐
        │  ACTIVE   │      │      │ TERMINATED   │ (DocStatus 2 - final)
        └─────┬─────┘      │      └──────────────┘
              │            │
       ┌──────┼──────┐     │
       │ Expire     │ Term.│
       ▼            │      │
 ┌──────────┐      │      │
 │ EXPIRED  │      │      │
 │(DocStatus│      │      │
 │ 2-final) │      │      │
 └──────────┘      │      │
                   │      │
                   └──────┘
```

**Allowed Transitions:**

| From | To | Action | Allowed Role |
|------|----|--------|-------------|
| Draft | Active | Activate | Storage Administrator |
| Draft | Terminated | Terminate | Storage Administrator |
| Active | Expired | Mark Expired | Storage Administrator |
| Active | Terminated | Terminate | Storage Administrator |

### 7.3 Workflow States Reference

| State | Style | Doc Status | Editable By |
|-------|-------|------------|-------------|
| Draft | Warning (Orange) | 0 (Draft) | All |
| Confirmed | Info (Blue) | 0 (Draft) | All |
| Active | Success (Green) | 1 (Submitted) | All |
| Completed | Secondary (Grey) | 2 (Cancelled) | None |
| Cancelled | Danger (Red) | 2 (Cancelled) | None |
| Expired | Danger (Red) | 2 (Cancelled) | None |
| Terminated | Danger (Red) | 2 (Cancelled) | None |

---

## 8. Reports & Analytics

### 8.1 Report Listing

| Report | Reference DocType | Purpose |
|--------|-------------------|---------|
| **Storage Booking Report** | Storage Booking | Complete list of all bookings with filters |
| **Active Rental Report** | Rental Agreement | Shows currently active agreements with days remaining |
| **Customer Report** | Customer Profile | Customer list with active booking counts |
| **Facility Occupancy Report** | Storage Facility | Occupancy % per facility with unit breakdown |
| **Payment Collection Report** | Payment Collection | All payments with type, mode, and status |
| **Unit Availability Report** | Storage Unit | Available & occupied units with size and rent |
| **Rental Agreement Report** | Rental Agreement | All agreements with customer and unit details |

### 8.2 Using Reports

**Standard Usage:**
1. Navigate to **Storage Rental Platform > Reports**
2. Click on any report
3. Apply filters as needed (e.g., status, customer, date range)
4. View results in the table

**Exporting:**
- Click the **Download** button in the report toolbar
- Choose format: Excel, CSV, or PDF

### 8.3 Report Details

#### Storage Booking Report
- Shows all bookings with customer, unit, plan, dates, and amounts
- Filters: Status, Customer, Date Range
- Sorted by creation date (newest first)

#### Active Rental Report
- Shows currently active rental agreements
- Calculates **Days Remaining** until agreement end
- Filters: Facility, Expiring Within Days
- Sorted by end date (nearest expiry first)
- **Note:** Searches by `status = 'Active'` not `docstatus` (demo agreements are unsubmitted)

#### Customer Report
- Lists all customers with their city and status
- Shows **Active Bookings** (count of bookings with status "Active")
- Shows **Total Rentals** (count of all bookings)
- Filters: Status, Customer Type, City

#### Facility Occupancy Report
- Per-facility occupancy analysis
- Columns: Total Units, Available, Occupied, Reserved, Maintenance, Occupancy %
- Occupancy % = (Occupied / Total) × 100
- Filters: Status (facility), Location
- Sorted by occupancy % (highest first)

#### Payment Collection Report
- All payments with customer, type, mode, and amounts
- Shows GST amount and total separately
- Filters: Payment Status, Payment Type, Customer, Date Range
- Sorted by payment date (newest first)

#### Unit Availability Report
- All storage units with their current status
- Includes category, facility, dimensions, floor, rent, and deposit
- Filters: Status, Facility, Category, Min/Max Rent

#### Rental Agreement Report
- All agreements with customer, unit, dates, and financials
- Filters: Status, Customer, Date Range
- Sorted by agreement date (newest first)

---

## 9. Demo Data

### 9.1 Overview

Demo data is automatically created during:
- **New site installation** (via `after_install` hook)
- **Migration** (via `after_migrate` hook — runs only once, tracked by a flag)

### 9.2 Demo Data Summary

| DocType | Records Created | Details |
|---------|----------------|---------|
| **Storage Facility** | 5 | Delhi, Mumbai, Bangalore, Chennai, Hyderabad |
| **Storage Category** | 4 | Small, Medium, Large, Extra Large |
| **Storage Unit** | 22 | Across all facilities with amenities & varied statuses |
| **Customer Profile** | 8 | 5 individuals + 3 companies with full KYC |
| **Rental Plan** | 6 | Daily Flex through Yearly Enterprise |
| **Pricing** | 20 | All facility × category combinations |
| **Storage Booking** | 6 | 3 Active, 1 Confirmed, 1 Draft, 1 Active |
| **Rental Agreement** | 5 | 4 Active, 1 Draft |
| **Payment Collection** | 13 | Security deposits + monthly rent payments |
| **Unit Handover** | 4 | Move In handovers with checklist items |

### 9.3 Manually Triggering Demo Data

If you need to regenerate demo data on an existing site:

```bash
bench --site yoursite console
```

```python
# Reset the flag so it runs again on next migrate
frappe.db.set_value("System Settings", "System Settings", "demo_data_created_v2", None)
frappe.db.commit()
exit()
```

Then run:
```bash
bench --site yoursite migrate
```

### 9.4 Demo Data Architecture

The demo data generator is in `demo_data.py` with these design principles:
- **Idempotent:** All functions check `frappe.db.exists()` before creating records
- **Ordered:** Proper dependency chaining (facilities → units → customers → bookings → agreements → payments → handovers)
- **Flag-protected:** Runs only once per site via `System Settings` flag
- **Workflow-aware:** Inserts as "Draft", then sets `status` field directly to bypass workflow validation

---

## 10. Maintenance & Troubleshooting

### 10.1 Common Issues & Fixes

| Symptom | Root Cause | Resolution |
|---------|------------|------------|
| **Workspace shows blank page** | `get_desktop_page()` API fails due to resolution issues | Check DNS resolution (`ping storage.local`), add to `/etc/hosts`, restart bench |
| **Report error: `getdoctype() missing argument`** | Report record has no `ref_doctype` | Run `bench --site site migrate` — `fix_reports_ref_doctype()` in `after_migrate` auto-fixes this |
| **Workflow error on booking/agreement creation** | Trying to insert document with non-initial workflow state | Insert as "Draft", then use workflow Actions to transition |
| **Fixture not importing** | `modified` timestamp in fixture file is older than DB | Remove `modified` field from fixture JSON (handled in latest version) |
| **Socket.io connection errors** | DNS/hostname resolution failure | Add `127.0.0.1 site.local` to `/etc/hosts`, check nginx/supervisor |

### 10.2 Routine Maintenance

**Weekly:**
```bash
bench --site yoursite clear-cache
```

**After code updates:**
```bash
cd ~/frappe-bench/apps/storage_rental_platform
git pull
bench --site yoursite migrate
bench --site yoursite clear-cache
bench build
bench restart
```

**Database health check:**
```bash
bench --site yoursite console
```

```python
# Check for records with missing references
frappe.db.sql("""
    SELECT name FROM `tabStorage Booking` 
    WHERE customer NOT IN (SELECT name FROM `tabCustomer Profile`)
""")
```

### 10.3 Backup & Restore

```bash
# Backup
bench --site yoursite backup --with-files

# Restore
bench --site yoursite restore /path/to/backup/file.sql.gz
```

### 10.4 Debugging Reports

If a Script Report shows no data:
1. Open the report in the desk
2. Open **Browser DevTools > Network tab**
3. Find the `frappe.desk.query_report.run` request
4. Check the **Response** tab for the SQL query result
5. Verify the SQL query manually:

```bash
bench --site yoursite console
```

```python
# Test the report query directly
query = """
    SELECT COUNT(*) as count 
    FROM `tabRental Agreement` 
    WHERE status = 'Active'
"""
frappe.db.sql(query, as_dict=1)
```

---

## 11. Frequently Asked Questions

**Q: How do I add a new storage facility?**
A: Navigate to **Storage Rental Platform > Masters > Storage Facility** and click **+ Add Storage Facility**.

**Q: How do I mark a unit as occupied?**
A: When a booking transitions to **Active**, the unit's status changes. You can also manually update the Storage Unit's Status field.

**Q: Which reports can I export?**
A: All 7 reports support export to CSV, Excel, and PDF via the Download button.

**Q: How do I create a new user with Storage Administrator access?**
A: Go to **Setup > User**, create the user, and assign the **Storage Administrator** role.

**Q: Why is my report showing no data?**
A: Check that:
1. The Reference DocType has records with matching status
2. The Active Rental Report filters on `status = 'Active'` — ensure agreements have status set
3. Run `bench --site yoursite migrate` to fix any missing `ref_doctype`

**Q: How do I reset all demo data?**
A: Clear the `demo_data_created_v2` flag in System Settings and re-run migrate:
```bash
bench --site yoursite console
```
```python
frappe.db.set_value("System Settings", "System Settings", "demo_data_created_v2", None)
frappe.db.commit()
```
```bash
bench --site yoursite migrate
```

**Q: Can I run this app without ERPNext?**
A: Yes, the app only depends on Frappe Framework v15+. ERPNext is optional.

**Q: How are GST calculations handled?**
A: GST is tracked as a separate field (`gst_amount`) on Payment Collection. Tax rates are manually entered during payment recording — the app does not auto-calculate GST.

**Q: What does `override_status: 0` mean in the workflow?**
A: It means the workflow's `workflow_state` is tracked separately from the document's `status` field. The `status` field can be set independently, while the workflow controls the `workflow_state` for transition validation.

---

## Appendix A: DB Schema Overview

```
tabStorage Facility
├── facility_name (Data, Unique)
├── location (Data)
├── address (Small Text)
├── contact_number (Data)
├── email (Data)
├── facility_manager (Link → User)
└── status (Select)

tabStorage Category
├── category_name (Data, Unique)
├── storage_type (Select)
├── min_height (Float)
├── max_height (Float)
└── is_active (Check)

tabStorage Unit
├── unit_number (Data, Unique)
├── storage_category (Link → Storage Category)
├── facility (Link → Storage Facility)
├── unit_size (Data)
├── dimensions (Data)
├── floor (Int)
├── monthly_rent (Currency)
├── security_deposit (Currency)
├── status (Select)
└── amenities (Table → Unit Amenity)

tabCustomer Profile
├── customer_name (Data, Unique)
├── customer_type (Select)
├── email (Data)
├── mobile_number (Data)
├── phone (Data)
├── address (Small Text)
├── city / state / pincode / country
├── date_of_birth (Date)
├── id_proof / id_number
├── status (Select)
└── notes (Text Editor)

tabRental Plan
├── plan_name (Data, Unique)
├── duration (Int)
├── duration_type (Select)
├── price (Currency)
├── discount_percentage (Float)
├── final_price (Currency, Read Only)
├── is_active (Check)
└── features (Text Editor)

tabPricing
├── pricing_name (Data, Unique)
├── storage_category (Link → Storage Category)
├── storage_facility (Link → Storage Facility)
├── base_price (Currency)
├── price_per_day/week/month/quarter/year (Currency)
├── security_deposit (Currency)
├── is_active (Check)
├── effective_from / effective_to (Date)
└── description (Text Editor)

tabStorage Booking (Submittable, Workflow)
├── customer (Link → Customer Profile)
├── storage_unit (Link → Storage Unit)
├── rental_plan (Link → Rental Plan)
├── booking_date / start_date / end_date (Date)
├── status (Select)
├── monthly_rent / security_deposit / total_amount (Currency)
├── discount_amount / advance_amount / balance_amount (Currency)
├── special_requirements (Text Editor)
└── notes (Text Editor)

tabRental Agreement (Submittable, Workflow)
├── storage_booking (Link → Storage Booking)
├── customer (Link → Customer Profile)
├── storage_unit (Link → Storage Unit)
├── agreement_date / start_date / end_date (Date)
├── status (Select)
├── monthly_rent / security_deposit / total_rent (Currency)
├── payment_due_day (Int)
├── late_fee (Currency)
├── notice_period (Int)
├── terms_and_conditions (Text Editor)
├── agreement_document / id_proof / address_proof (Attach)
└── notes (Text Editor)

tabPayment Collection (Submittable)
├── customer (Link → Customer Profile)
├── rental_agreement (Link → Rental Agreement)
├── storage_booking (Link → Storage Booking)
├── payment_date (Date)
├── payment_type / payment_mode (Select)
├── amount / gst_amount / total_amount (Currency)
├── payment_status (Select)
├── reference_number (Data)
├── payment_for_month (Date)
└── notes (Text Editor)

tabUnit Handover (Submittable)
├── rental_agreement (Link → Rental Agreement)
├── customer (Link → Customer Profile)
├── storage_unit (Link → Storage Unit)
├── handover_type (Select)
├── handover_date (Datetime)
├── status (Select)
├── keys_received / remote_received / access_card_received (Check)
├── unit_condition / cleaning_status (Select)
├── meter_reading (Data)
├── damage_notes (Text Editor)
├── checklist_items (Table → Handover Checklist)
└── notes (Text Editor)
```

---

*End of SOP Document — Storage Rental Platform v1.0*
