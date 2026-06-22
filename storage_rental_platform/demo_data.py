import itertools

import frappe
from frappe.utils import today, add_days, add_months, now_datetime, getdate


def create_demo_data():
    """Create comprehensive demo data for the Storage Rental Platform.
    This is idempotent - safe to run multiple times.
    """
    facilities = _create_facilities()
    categories = _create_categories()
    amenities_list = _create_amenities()
    units = _create_units(facilities, categories, amenities_list)
    customers = _create_customers()
    plans = _create_plans()
    _create_pricing(facilities, categories)
    bookings = _create_bookings(customers, units, plans)
    agreements = _create_agreements(bookings, customers, units)
    _create_payments(customers, agreements)
    _create_handovers(customers, units, agreements)

    frappe.db.commit()
    print("✅ Demo data created successfully!")


def _create_facilities():
    """Create 5 storage facilities across Indian cities."""
    facilities_data = [
        {
            "facility_name": "Central Storage - Delhi",
            "location": "Delhi",
            "address": "123 Main Market, Connaught Place, New Delhi - 110001",
            "contact_number": "+91 11 2345 6789",
            "email": "delhi@storagerental.com",
            "facility_manager": "Administrator",
            "status": "Active",
            "description": "<p>Premium storage facility in the heart of Delhi with 24x7 security and climate-controlled units.</p>"
        },
        {
            "facility_name": "Mumbai Storage Hub",
            "location": "Mumbai",
            "address": "456 Andheri East, Mumbai - 400069",
            "contact_number": "+91 22 2345 6789",
            "email": "mumbai@storagerental.com",
            "facility_manager": "Administrator",
            "status": "Active",
            "description": "<p>State-of-the-art storage facility in Mumbai with easy access from Western and Harbour lines.</p>"
        },
        {
            "facility_name": "Bangalore Tech Storage",
            "location": "Bangalore",
            "address": "789 Whitefield, Bangalore - 560066",
            "contact_number": "+91 80 2345 6789",
            "email": "bangalore@storagerental.com",
            "facility_manager": "Administrator",
            "status": "Active",
            "description": "<p>Modern storage solutions in Bangalore's tech hub with advanced security systems.</p>"
        },
        {
            "facility_name": "Chennai Port Storage",
            "location": "Chennai",
            "address": "42 GST Road, Guindy, Chennai - 600032",
            "contact_number": "+91 44 2345 6789",
            "email": "chennai@storagerental.com",
            "facility_manager": "Administrator",
            "status": "Active",
            "description": "<p>Warehouse storage facility near Chennai port, ideal for businesses needing logistics access.</p>"
        },
        {
            "facility_name": "Hyderabad Hi-Tech Storage",
            "location": "Hyderabad",
            "address": "88 HITEC City, Hyderabad - 500081",
            "contact_number": "+91 40 2345 6789",
            "email": "hyderabad@storagerental.com",
            "facility_manager": "Administrator",
            "status": "Active",
            "description": "<p>Premium storage facility in Hyderabad's IT corridor with 24x7 surveillance.</p>"
        }
    ]

    created = {}
    for data in facilities_data:
        name = data["facility_name"]
        if not frappe.db.exists("Storage Facility", name):
            doc = frappe.get_doc({"doctype": "Storage Facility", **data})
            doc.insert(ignore_permissions=True)
            created[name] = doc.name
        else:
            created[name] = name
        print(f"  ✓ Facility: {name}")

    return created


def _create_categories():
    """Create 4 storage categories."""
    categories_data = [
        {
            "category_name": "Small",
            "storage_type": "Small",
            "description": "<p>Small storage units (5x5) ideal for personal items, documents, and boxes.</p>",
            "min_height": 5, "max_height": 7, "is_active": 1
        },
        {
            "category_name": "Medium",
            "storage_type": "Medium",
            "description": "<p>Medium storage units (10x10) perfect for household items and furniture.</p>",
            "min_height": 7, "max_height": 10, "is_active": 1
        },
        {
            "category_name": "Large",
            "storage_type": "Large",
            "description": "<p>Large storage units (15x15) suitable for business inventory and vehicles.</p>",
            "min_height": 10, "max_height": 15, "is_active": 1
        },
        {
            "category_name": "Extra Large",
            "storage_type": "Extra Large",
            "description": "<p>Extra large units (20x20) for commercial storage and bulk inventory.</p>",
            "min_height": 15, "max_height": 20, "is_active": 1
        }
    ]

    created = {}
    for data in categories_data:
        name = data["category_name"]
        if not frappe.db.exists("Storage Category", name):
            doc = frappe.get_doc({"doctype": "Storage Category", **data})
            doc.insert(ignore_permissions=True)
            created[name] = doc.name
        else:
            created[name] = name
        print(f"  ✓ Category: {name}")

    return created


def _create_amenities():
    """Create a list of amenity names to use for storage units."""
    return [
        {"amenity": "24/7 CCTV Surveillance", "description": "Round-the-clock video monitoring"},
        {"amenity": "Climate Control", "description": "Temperature and humidity regulated"},
        {"amenity": "Fire Safety System", "description": "Advanced fire detection and sprinklers"},
        {"amenity": "Individual Lock", "description": "Customer-provided lock for security"},
        {"amenity": "Drive-Up Access", "description": "Easy vehicle access for loading/unloading"},
        {"amenity": "Elevator Access", "description": "Freight elevator for upper floor units"},
        {"amenity": "Shelving Included", "description": "Built-in shelving for organization"},
        {"amenity": "Power Backup", "description": "Generator backup for essential systems"},
    ]


def _amenities_for_unit(unit_index, amenities_list):
    """Pick a subset of amenities for a unit based on its index."""
    # Rotate through amenities so each unit gets different ones
    cycler = itertools.cycle(amenities_list)
    count = 2 + (unit_index % 4)  # 2 to 5 amenities per unit
    return [next(cycler) for _ in range(count)]


def _create_units(facilities, categories, amenities_list):
    """Create storage units across all facilities with amenities."""
    unit_configs = {
        "Central Storage - Delhi": [
            {"unit_number": "DL-S-01", "category": "Small", "size": "5x5", "dimensions": "5ft x 5ft x 8ft", "floor": 1, "rent": 2000, "deposit": 4000, "status": "Available"},
            {"unit_number": "DL-S-02", "category": "Small", "size": "5x5", "dimensions": "5ft x 5ft x 8ft", "floor": 1, "rent": 2000, "deposit": 4000, "status": "Occupied"},
            {"unit_number": "DL-M-01", "category": "Medium", "size": "10x10", "dimensions": "10ft x 10ft x 10ft", "floor": 2, "rent": 4000, "deposit": 8000, "status": "Occupied"},
            {"unit_number": "DL-M-02", "category": "Medium", "size": "10x10", "dimensions": "10ft x 10ft x 10ft", "floor": 2, "rent": 4000, "deposit": 8000, "status": "Reserved"},
            {"unit_number": "DL-L-01", "category": "Large", "size": "15x15", "dimensions": "15ft x 15ft x 12ft", "floor": 3, "rent": 7000, "deposit": 14000, "status": "Available"},
            {"unit_number": "DL-XL-01", "category": "Extra Large", "size": "20x20", "dimensions": "20ft x 20ft x 15ft", "floor": 3, "rent": 12000, "deposit": 24000, "status": "Available"},
        ],
        "Mumbai Storage Hub": [
            {"unit_number": "MU-S-01", "category": "Small", "size": "5x5", "dimensions": "5ft x 5ft x 8ft", "floor": 1, "rent": 2500, "deposit": 5000, "status": "Available"},
            {"unit_number": "MU-S-02", "category": "Small", "size": "5x5", "dimensions": "5ft x 5ft x 8ft", "floor": 1, "rent": 2500, "deposit": 5000, "status": "Occupied"},
            {"unit_number": "MU-M-01", "category": "Medium", "size": "10x10", "dimensions": "10ft x 10ft x 10ft", "floor": 2, "rent": 5000, "deposit": 10000, "status": "Maintenance"},
            {"unit_number": "MU-L-01", "category": "Large", "size": "15x15", "dimensions": "15ft x 15ft x 12ft", "floor": 2, "rent": 8500, "deposit": 17000, "status": "Available"},
        ],
        "Bangalore Tech Storage": [
            {"unit_number": "BL-S-01", "category": "Small", "size": "5x5", "dimensions": "5ft x 5ft x 8ft", "floor": 1, "rent": 2200, "deposit": 4400, "status": "Available"},
            {"unit_number": "BL-S-02", "category": "Small", "size": "5x5", "dimensions": "5ft x 5ft x 8ft", "floor": 1, "rent": 2200, "deposit": 4400, "status": "Occupied"},
            {"unit_number": "BL-M-01", "category": "Medium", "size": "10x10", "dimensions": "10ft x 10ft x 10ft", "floor": 2, "rent": 4500, "deposit": 9000, "status": "Occupied"},
            {"unit_number": "BL-M-02", "category": "Medium", "size": "10x10", "dimensions": "10ft x 10ft x 10ft", "floor": 2, "rent": 4500, "deposit": 9000, "status": "Available"},
            {"unit_number": "BL-L-01", "category": "Large", "size": "15x15", "dimensions": "15ft x 15ft x 12ft", "floor": 3, "rent": 7500, "deposit": 15000, "status": "Available"},
        ],
        "Chennai Port Storage": [
            {"unit_number": "CH-M-01", "category": "Medium", "size": "10x10", "dimensions": "10ft x 10ft x 10ft", "floor": 1, "rent": 3500, "deposit": 7000, "status": "Occupied"},
            {"unit_number": "CH-M-02", "category": "Medium", "size": "10x10", "dimensions": "10ft x 10ft x 10ft", "floor": 1, "rent": 3500, "deposit": 7000, "status": "Available"},
            {"unit_number": "CH-L-01", "category": "Large", "size": "15x15", "dimensions": "15ft x 15ft x 12ft", "floor": 2, "rent": 6000, "deposit": 12000, "status": "Available"},
        ],
        "Hyderabad Hi-Tech Storage": [
            {"unit_number": "HY-S-01", "category": "Small", "size": "5x5", "dimensions": "5ft x 5ft x 8ft", "floor": 1, "rent": 2000, "deposit": 4000, "status": "Available"},
            {"unit_number": "HY-M-01", "category": "Medium", "size": "10x10", "dimensions": "10ft x 10ft x 10ft", "floor": 2, "rent": 3800, "deposit": 7600, "status": "Occupied"},
            {"unit_number": "HY-M-02", "category": "Medium", "size": "10x10", "dimensions": "10ft x 10ft x 10ft", "floor": 2, "rent": 3800, "deposit": 7600, "status": "Available"},
            {"unit_number": "HY-L-01", "category": "Large", "size": "15x15", "dimensions": "15ft x 15ft x 12ft", "floor": 3, "rent": 6500, "deposit": 13000, "status": "Available"},
        ],
    }

    created = {}
    unit_index = 0
    for facility_name, units_list in unit_configs.items():
        fac_name = facilities.get(facility_name)
        if not fac_name:
            continue
        for cfg in units_list:
            unit_index += 1
            unit_number = cfg["unit_number"]
            if frappe.db.exists("Storage Unit", unit_number):
                created[unit_number] = unit_number
                continue

            cat_name = categories.get(cfg["category"])
            doc = frappe.get_doc({
                "doctype": "Storage Unit",
                "unit_number": unit_number,
                "storage_category": cat_name,
                "facility": fac_name,
                "unit_size": cfg["size"],
                "dimensions": cfg["dimensions"],
                "floor": cfg["floor"],
                "monthly_rent": cfg["rent"],
                "security_deposit": cfg["deposit"],
                "status": cfg["status"],
            })

            # Add amenities
            selected = _amenities_for_unit(unit_index, amenities_list)
            for amenity in selected:
                doc.append("amenities", amenity)

            doc.insert(ignore_permissions=True)
            created[unit_number] = doc.name
            print(f"  ✓ Unit: {unit_number} ({facility_name})")

    return created


def _create_customers():
    """Create 8 customer profiles - mix of individuals and companies."""
    customers_data = [
        {
            "customer_name": "Rahul Sharma",
            "customer_type": "Individual",
            "email": "rahul.sharma@email.com",
            "mobile_number": "9876543210",
            "phone": "+91 11 2345 6789",
            "address": "456 Green Park, South Delhi",
            "city": "Delhi", "state": "Delhi", "pincode": "110016", "country": "India",
            "date_of_birth": "1985-06-15",
            "id_proof": "Aadhar Card", "id_number": "1234-5678-9012",
            "status": "Active",
            "notes": "<p>Regular customer since 2024. Prefers ground floor units.</p>"
        },
        {
            "customer_name": "Priya Patel",
            "customer_type": "Individual",
            "email": "priya.patel@email.com",
            "mobile_number": "9876543211",
            "phone": "+91 22 2345 6789",
            "address": "789 Andheri West, Mumbai",
            "city": "Mumbai", "state": "Maharashtra", "pincode": "400058", "country": "India",
            "date_of_birth": "1990-03-22",
            "id_proof": "PAN Card", "id_number": "ABCDE1234F",
            "status": "Active",
            "notes": "<p>Stores seasonal clothing and household items during relocation.</p>"
        },
        {
            "customer_name": "Tech Solutions Pvt Ltd",
            "customer_type": "Company",
            "email": "admin@techsolutions.com",
            "mobile_number": "9876543212",
            "phone": "+91 80 2345 6789",
            "address": "100 Electronic City, Phase 1",
            "city": "Bangalore", "state": "Karnataka", "pincode": "560100", "country": "India",
            "id_proof": "PAN Card", "id_number": "AABCT1234E",
            "status": "Active",
            "notes": "<p>IT company storing server equipment and office furniture.</p>"
        },
        {
            "customer_name": "Anita Verma",
            "customer_type": "Individual",
            "email": "anita.verma@email.com",
            "mobile_number": "9876543213",
            "address": "321 MG Road, Pune",
            "city": "Pune", "state": "Maharashtra", "pincode": "411001", "country": "India",
            "date_of_birth": "1978-11-08",
            "id_proof": "Passport", "id_number": "J1234567",
            "status": "Active",
            "notes": "<p>Interior designer storing client furniture and decor items.</p>"
        },
        {
            "customer_name": "Global Traders Inc",
            "customer_type": "Company",
            "email": "info@globaltraders.com",
            "mobile_number": "9876543214",
            "phone": "+91 11 2345 6790",
            "address": "555 Nehru Place, New Delhi",
            "city": "Delhi", "state": "Delhi", "pincode": "110019", "country": "India",
            "id_proof": "PAN Card", "id_number": "AABCG5678H",
            "status": "Active",
            "notes": "<p>Import/export business storing inventory and samples.</p>"
        },
        {
            "customer_name": "Vikram Singhania",
            "customer_type": "Individual",
            "email": "vikram.singhania@email.com",
            "mobile_number": "9988776655",
            "address": "12 Juhu Tara Road, Mumbai",
            "city": "Mumbai", "state": "Maharashtra", "pincode": "400049", "country": "India",
            "date_of_birth": "1982-09-30",
            "id_proof": "Driving License", "id_number": "MH01-2021-12345",
            "status": "Active",
            "notes": "<p>Stores sports equipment and seasonal items.</p>"
        },
        {
            "customer_name": "Sara Constructions Ltd",
            "customer_type": "Company",
            "email": "projects@saraconstructions.com",
            "mobile_number": "9876543299",
            "phone": "+91 44 2345 6700",
            "address": "88 Anna Salai, Chennai",
            "city": "Chennai", "state": "Tamil Nadu", "pincode": "600002", "country": "India",
            "id_proof": "PAN Card", "id_number": "AABCS8901K",
            "status": "Active",
            "notes": "<p>Construction company storing equipment and building materials.</p>"
        },
        {
            "customer_name": "Neha Kapoor",
            "customer_type": "Individual",
            "email": "neha.kapoor@email.com",
            "mobile_number": "9876543216",
            "address": "45 Jubilee Hills, Hyderabad",
            "city": "Hyderabad", "state": "Telangana", "pincode": "500033", "country": "India",
            "date_of_birth": "1995-12-18",
            "id_proof": "Voter ID", "id_number": "TS/01/123/456789",
            "status": "Active",
            "notes": "<p>Freelance photographer storing camera equipment and props.</p>"
        },
    ]

    created = {}
    for data in customers_data:
        name = data["customer_name"]
        existing = frappe.db.get_value("Customer Profile", {"customer_name": name}, "name")
        if existing:
            created[name] = existing
        else:
            doc = frappe.get_doc({"doctype": "Customer Profile", **data})
            doc.insert(ignore_permissions=True)
            created[name] = doc.name
        print(f"  ✓ Customer: {name}")

    return created


def _create_plans():
    """Create 6 rental plans with various durations and discounts."""
    plans_data = [
        {
            "plan_name": "Daily Flex",
            "duration": 1, "duration_type": "Daily",
            "price": 100, "discount_percentage": 0,
            "description": "<p>Pay-as-you-go daily plan for short-term storage needs.</p>",
            "is_active": 1,
            "features": "<ul><li>24-hour access</li><li>No long-term commitment</li><li>Cancel anytime</li></ul>"
        },
        {
            "plan_name": "Monthly Basic",
            "duration": 30, "duration_type": "Monthly",
            "price": 2000, "discount_percentage": 0,
            "description": "<p>Basic monthly rental plan with essential storage features.</p>",
            "is_active": 1,
            "features": "<ul><li>Standard access hours</li><li>Basic security</li><li>Month-to-month billing</li></ul>"
        },
        {
            "plan_name": "Monthly Standard",
            "duration": 30, "duration_type": "Monthly",
            "price": 4000, "discount_percentage": 5,
            "description": "<p>Standard monthly plan with priority support and 5% discount.</p>",
            "is_active": 1,
            "features": "<ul><li>Extended access hours</li><li>Priority support</li><li>Free moving trolley</li><li>5% monthly discount</li></ul>"
        },
        {
            "plan_name": "Quarterly Saver",
            "duration": 90, "duration_type": "Quarterly",
            "price": 10800, "discount_percentage": 10,
            "description": "<p>Quarterly plan saving 10% compared to monthly billing.</p>",
            "is_active": 1,
            "features": "<ul><li>Best value for 3-month storage</li><li>10% discount</li><li>Free lock</li><li>Climate-controlled unit</li></ul>"
        },
        {
            "plan_name": "Half-Yearly Advantage",
            "duration": 180, "duration_type": "Yearly",
            "price": 20400, "discount_percentage": 15,
            "description": "<p>6-month plan with 15% discount plus added benefits.</p>",
            "is_active": 1,
            "features": "<ul><li>15% discount</li><li>Free insurance up to ₹50,000</li><li>Premium security</li><li>Dedicated account manager</li></ul>"
        },
        {
            "plan_name": "Yearly Enterprise",
            "duration": 365, "duration_type": "Yearly",
            "price": 36000, "discount_percentage": 20,
            "description": "<p>Annual enterprise plan with maximum savings and premium features.</p>",
            "is_active": 1,
            "features": "<ul><li>20% discount</li><li>Free insurance up to ₹2,00,000</li><li>24/7 concierge access</li><li>Free pickup & delivery</li><li>Business invoicing</li></ul>"
        },
    ]

    created = {}
    for data in plans_data:
        name = data["plan_name"]
        if not frappe.db.exists("Rental Plan", name):
            doc = frappe.get_doc({"doctype": "Rental Plan", **data})
            doc.insert(ignore_permissions=True)
            created[name] = doc.name
        else:
            created[name] = name
        print(f"  ✓ Plan: {name}")

    return created


def _create_pricing(facilities, categories):
    """Create pricing entries for all facility-category combinations."""
    # Tiered pricing by city
    city_multiplier = {
        "Central Storage - Delhi": 1.2,
        "Mumbai Storage Hub": 1.3,
        "Bangalore Tech Storage": 1.1,
        "Chennai Port Storage": 1.0,
        "Hyderabad Hi-Tech Storage": 0.9,
    }
    base_price_by_category = {
        "Small": 1500,
        "Medium": 3500,
        "Large": 6000,
        "Extra Large": 10000,
    }

    count = 0
    for fac_name, fac_doc in facilities.items():
        multiplier = city_multiplier.get(fac_name, 1.0)
        for cat_name, cat_doc in categories.items():
            base = base_price_by_category.get(cat_name, 2000)
            monthly = int(base * multiplier)
            pricing_name = f"{fac_name} - {cat_name}"
            if frappe.db.exists("Pricing", pricing_name):
                continue

            doc = frappe.get_doc({
                "doctype": "Pricing",
                "pricing_name": pricing_name,
                "storage_category": cat_doc,
                "storage_facility": fac_doc,
                "base_price": monthly,
                "price_per_day": int(monthly / 30),
                "price_per_week": int(monthly / 4),
                "price_per_month": monthly,
                "price_per_quarter": int(monthly * 2.7),
                "price_per_year": int(monthly * 10),
                "security_deposit": monthly * 2,
                "is_active": 1,
                "effective_from": today(),
                "description": f"<p>Pricing for {cat_name} units at {fac_name}. Monthly rate: ₹{monthly:,}</p>"
            })
            doc.insert(ignore_permissions=True)
            count += 1

    print(f"  ✓ Pricing entries: {count}")


def _create_bookings(customers, units, plans):
    """Create 6 storage bookings with various statuses."""
    scenarios = [
        # (customer, unit_key, plan, final_state, start_offset_days, end_offset_days, special_requirements)
        ("Rahul Sharma", "DL-M-01", "Monthly Standard", "Active", -45, 320,
         "<p>Need ground floor access for heavy boxes. Will bring own lock.</p>"),
        ("Priya Patel", "MU-S-02", "Monthly Basic", "Active", -30, 335,
         "<p>Storing household items during home renovation. Requires climate-controlled unit.</p>"),
        ("Tech Solutions Pvt Ltd", "BL-M-01", "Yearly Enterprise", "Active", -90, 275,
         "<p>Storing sensitive IT equipment. Require temperature monitoring reports monthly.</p>"),
        ("Anita Verma", "DL-S-02", "Quarterly Saver", "Confirmed", 7, 97,
         "<p>Storing client furniture pieces. Will need drive-up access for delivery van.</p>"),
        ("Neha Kapoor", "HY-M-01", "Monthly Standard", "Draft", 14, 44,
         "<p>New customer referred by existing customer. Offering 5% loyalty discount.</p>"),
        ("Global Traders Inc", "CH-M-01", "Half-Yearly Advantage", "Active", -60, 120,
         "<p>Business inventory storage. Requires weekly access on Saturdays.</p>"),
    ]

    created = {}
    for customer_name, unit_key, plan_name, final_state, start_days, end_days, special_req in scenarios:
        customer = customers.get(customer_name)
        unit = units.get(unit_key)
        plan = plans.get(plan_name)

        if not customer or not unit or not plan:
            print(f"  ⚠ Booking skipped: {customer_name} -> {unit_key} (missing ref)")
            continue

        # Deduplicate: check if a booking already exists for this customer+unit
        existing = frappe.db.get_value("Storage Booking",
            {"customer": customer, "storage_unit": unit}, "name")
        if existing:
            created[f"{customer_name}-{unit_key}"] = existing
            continue

        start_date = add_days(today(), start_days)
        end_date = add_days(today(), end_days)

        # Insert as Draft (valid initial workflow state).
        # Then use db.set_value to set the desired workflow_state directly,
        # bypassing workflow transition validation (safe for demo data).
        doc = frappe.get_doc({
            "doctype": "Storage Booking",
            "customer": customer,
            "storage_unit": unit,
            "rental_plan": plan,
            "booking_date": add_days(start_date, -7),
            "start_date": start_date,
            "end_date": end_date,
            "status": "Draft",
            "monthly_rent": frappe.db.get_value("Storage Unit", unit, "monthly_rent") or 2000,
            "security_deposit": frappe.db.get_value("Storage Unit", unit, "security_deposit") or 4000,
            "total_amount": 6000,
            "discount_amount": 0,
            "advance_amount": 0,
            "balance_amount": 0,
            "special_requirements": special_req,
        })
        doc.insert(ignore_permissions=True)

        # Transition to desired workflow state directly via DB
        if final_state != "Draft":
            state = final_state
            # Set both workflow_state and the status field
            frappe.db.set_value("Storage Booking", doc.name, {
                "workflow_state": state,
                "status": state,
            })

        created[f"{customer_name}-{unit_key}"] = doc.name
        print(f"  ✓ Booking: {customer_name} - {unit_key} ({final_state})")

    frappe.db.commit()
    return created


def _create_agreements(bookings, customers, units):
    """Create rental agreements linked to active/confirmed bookings."""
    # Map bookings to agreements
    agreement_map = [
        ("Rahul Sharma-DL-M-01", "Rahul Sharma", "DL-M-01", "Active", -45, 320, 4000, 8000, 48000, 5, 30),
        ("Priya Patel-MU-S-02", "Priya Patel", "MU-S-02", "Active", -30, 335, 2000, 4000, 24000, 5, 30),
        ("Tech Solutions Pvt Ltd-BL-M-01", "Tech Solutions Pvt Ltd", "BL-M-01", "Active", -90, 275, 4500, 9000, 54000, 10, 60),
        ("Global Traders Inc-CH-M-01", "Global Traders Inc", "CH-M-01", "Active", -60, 120, 3500, 7000, 21000, 5, 30),
        ("Anita Verma-DL-S-02", "Anita Verma", "DL-S-02", "Draft", 7, 97, 2000, 4000, 6000, 5, 15),
    ]

    created = {}
    for booking_key, customer_name, unit_key, final_state, start_days, end_days, monthly_rent, deposit, total_rent, due_day, notice in agreement_map:
        booking = bookings.get(booking_key)
        customer = customers.get(customer_name)
        unit = units.get(unit_key)

        if not booking or not customer or not unit:
            print(f"  ⚠ Agreement skipped: {customer_name} (missing ref)")
            continue

        existing = frappe.db.get_value("Rental Agreement",
            {"customer": customer, "storage_unit": unit}, "name")
        if existing:
            created[booking_key] = existing
            continue

        start_date = add_days(today(), start_days)
        end_date = add_days(today(), end_days)

        terms = (
            "<ol>"
            "<li>The Lessee agrees to pay the monthly rent as specified on or before the due date.</li>"
            "<li>A late fee of ₹500 will be charged for payments received after the due date.</li>"
            "<li>The Lessee shall use the unit only for lawful storage purposes.</li>"
            "<li>Hazardous materials are strictly prohibited within the storage unit.</li>"
            "<li>The Lessor reserves the right to inspect the unit with 24-hour notice.</li>"
            "<li>Notice period as mentioned must be given before vacating the unit.</li>"
            "<li>The security deposit will be refunded within 15 days of vacating, subject to deductions for damages.</li>"
            "<li>The Lessee shall maintain insurance for stored items valued over ₹50,000.</li>"
            "</ol>"
        )

        # Insert as Draft (valid initial workflow state).
        # Then use db.set_value to set the desired workflow_state directly.
        doc = frappe.get_doc({
            "doctype": "Rental Agreement",
            "storage_booking": booking,
            "customer": customer,
            "storage_unit": unit,
            "agreement_date": start_date,
            "start_date": start_date,
            "end_date": end_date,
            "status": "Draft",
            "monthly_rent": monthly_rent,
            "security_deposit": deposit,
            "total_rent": total_rent,
            "payment_due_day": due_day,
            "late_fee": 500,
            "notice_period": notice,
            "terms_and_conditions": terms,
            "notes": f"<p>Agreement for {customer_name} at unit {unit_key}.</p>"
        })
        doc.insert(ignore_permissions=True)

        # Transition to desired workflow state directly via DB
        if final_state != "Draft":
            frappe.db.set_value("Rental Agreement", doc.name, {
                "workflow_state": final_state,
                "status": final_state,
            })

        created[booking_key] = doc.name
        print(f"  ✓ Agreement: {customer_name} - {unit_key} ({final_state})")

    frappe.db.commit()
    return created


def _create_payments(customers, agreements):
    """Create payment collections across customers and agreements."""
    payment_scenarios = [
        # (customer_name, agreement_booking_key, payment_type, payment_mode, amount, gst, status, offset_days, ref_prefix)
        ("Priya Patel", "Priya Patel-MU-S-02", "Security Deposit", "UPI", 4000, 0, "Completed", -30, "UPI"),
        ("Priya Patel", "Priya Patel-MU-S-02", "Rent", "UPI", 2000, 360, "Completed", -30, "UPI"),
        ("Priya Patel", "Priya Patel-MU-S-02", "Rent", "UPI", 2000, 360, "Completed", 0, "UPI"),
        ("Rahul Sharma", "Rahul Sharma-DL-M-01", "Security Deposit", "Bank Transfer", 8000, 0, "Completed", -45, "NEFT"),
        ("Rahul Sharma", "Rahul Sharma-DL-M-01", "Rent", "Bank Transfer", 4000, 720, "Completed", -45, "NEFT"),
        ("Rahul Sharma", "Rahul Sharma-DL-M-01", "Rent", "Bank Transfer", 4000, 720, "Completed", -15, "NEFT"),
        ("Tech Solutions Pvt Ltd", "Tech Solutions Pvt Ltd-BL-M-01", "Security Deposit", "Bank Transfer", 9000, 0, "Completed", -90, "NEFT"),
        ("Tech Solutions Pvt Ltd", "Tech Solutions Pvt Ltd-BL-M-01", "Rent", "Bank Transfer", 4500, 810, "Completed", -90, "NEFT"),
        ("Tech Solutions Pvt Ltd", "Tech Solutions Pvt Ltd-BL-M-01", "Rent", "Bank Transfer", 4500, 810, "Completed", -60, "NEFT"),
        ("Tech Solutions Pvt Ltd", "Tech Solutions Pvt Ltd-BL-M-01", "Rent", "Bank Transfer", 4500, 810, "Completed", -30, "NEFT"),
        ("Global Traders Inc", "Global Traders Inc-CH-M-01", "Security Deposit", "Cheque", 7000, 0, "Completed", -60, "CHQ"),
        ("Global Traders Inc", "Global Traders Inc-CH-M-01", "Rent", "Cheque", 3500, 630, "Pending", -60, "CHQ"),
        ("Vikram Singhania", None, "Other", "Credit Card", 5000, 900, "Completed", -10, "CC"),
    ]

    count = 0
    for customer_name, agreement_key, ptype, mode, amount, gst, status, offset_days, ref_prefix in payment_scenarios:
        customer = customers.get(customer_name)
        if not customer:
            continue

        agreement = agreements.get(agreement_key) if agreement_key else None
        payment_date = add_days(today(), offset_days)

        existing = frappe.db.get_value("Payment Collection",
            {"customer": customer, "payment_type": ptype,
             "payment_date": payment_date, "amount": amount}, "name")
        if existing:
            continue

        doc = frappe.get_doc({
            "doctype": "Payment Collection",
            "customer": customer,
            "rental_agreement": agreement,
            "payment_date": payment_date,
            "payment_type": ptype,
            "payment_mode": mode,
            "amount": amount,
            "gst_amount": gst,
            "total_amount": amount + gst,
            "payment_status": status,
            "reference_number": f"{ref_prefix}-{frappe.generate_hash(length=6).upper()}",
            "payment_for_month": payment_date if ptype == "Rent" else None,
            "notes": f"<p>{ptype} payment from {customer_name}</p>" if ptype == "Other" else ""
        })
        doc.insert(ignore_permissions=True)
        count += 1

    print(f"  ✓ Payments created: {count}")


def _create_handovers(customers, units, agreements):
    """Create unit handover records with checklist items."""
    handover_scenarios = [
        # (customer_name, unit_key, agreement_booking_key, handover_type, status, offset_days)
        ("Rahul Sharma", "DL-M-01", "Rahul Sharma-DL-M-01", "Move In", "Completed", -45),
        ("Priya Patel", "MU-S-02", "Priya Patel-MU-S-02", "Move In", "Completed", -30),
        ("Tech Solutions Pvt Ltd", "BL-M-01", "Tech Solutions Pvt Ltd-BL-M-01", "Move In", "Completed", -90),
        ("Global Traders Inc", "CH-M-01", "Global Traders Inc-CH-M-01", "Move In", "Completed", -60),
    ]

    checklist_templates = {
        "Move In": [
            {"item": "Unit inspected and clean", "checked": 1, "remarks": "Unit was clean and ready"},
            {"item": "Keys handed over", "checked": 1, "remarks": "2 sets of keys provided"},
            {"item": "Remote/gate access programmed", "checked": 0, "remarks": "Pending activation"},
            {"item": "Terms explained to customer", "checked": 1, "remarks": "Customer acknowledged terms"},
            {"item": "Insurance proof collected", "checked": 1, "remarks": "Policy document uploaded"},
            {"item": "Photo evidence taken", "checked": 1, "remarks": "Before-move-in photos saved"},
        ],
        "Inspection": [
            {"item": "Unit condition checked", "checked": 1, "remarks": "No visible damage"},
            {"item": "Lock checked", "checked": 1, "remarks": "Customer lock intact"},
            {"item": "Temperature logged", "checked": 1, "remarks": "22°C within acceptable range"},
            {"item": "Pest control check", "checked": 0, "remarks": "Next inspection due"},
            {"item": "Fire extinguisher checked", "checked": 1, "remarks": "Pressure OK, expiry valid"},
        ],
    }

    count = 0
    states = {
        "Move In": {"keys": 1, "remote": 1, "access_card": 1, "condition": "Excellent", "cleaning": "Clean"},
    }

    for customer_name, unit_key, agreement_key, htype, status, offset_days in handover_scenarios:
        customer = customers.get(customer_name)
        unit = units.get(unit_key)
        agreement = agreements.get(agreement_key)

        if not customer or not unit or not agreement:
            print(f"  ⚠ Handover skipped: {customer_name} (missing ref)")
            continue

        existing = frappe.db.get_value("Unit Handover",
            {"customer": customer, "storage_unit": unit, "handover_type": htype}, "name")
        if existing:
            continue

        state = states.get(htype, {"keys": 1, "remote": 0, "access_card": 0, "condition": "Good", "cleaning": "Clean"})

        doc = frappe.get_doc({
            "doctype": "Unit Handover",
            "rental_agreement": agreement,
            "customer": customer,
            "storage_unit": unit,
            "handover_type": htype,
            "handover_date": add_days(now_datetime(), offset_days),
            "status": status,
            "keys_received": state["keys"],
            "remote_received": state["remote"],
            "access_card_received": state["access_card"],
            "unit_condition": state["condition"],
            "cleaning_status": state["cleaning"],
            "damage_notes": "",
            "notes": f"<p>{htype} handover completed for {customer_name} at {unit_key}.</p>" if status == "Completed" else ""
        })

        # Add checklist items
        checklist = checklist_templates.get(htype, [])
        for item in checklist:
            doc.append("checklist_items", item)

        doc.insert(ignore_permissions=True)
        count += 1
        print(f"  ✓ Handover: {customer_name} - {unit_key} ({htype})")

    print(f"  ✓ Handover records: {count}")
