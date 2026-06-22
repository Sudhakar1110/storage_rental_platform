import frappe
from frappe.utils import today, add_days, now_datetime


def create_extended_demo_data():
    """Create additional demo data for testing purposes."""
    
    # Create more Storage Facilities
    additional_facilities = [
        {
            "doctype": "Storage Facility",
            "facility_name": "Chennai Storage Warehouse",
            "location": "Chennai",
            "address": "200 T Nagar, Chennai - 600017",
            "contact_number": "+91 44 2345 6789",
            "email": "chennai@storagerental.com",
            "facility_manager": "Administrator",
            "status": "Active"
        },
        {
            "doctype": "Storage Facility",
            "facility_name": "Hyderabad Storage Hub",
            "location": "Hyderabad",
            "address": "300 Banjara Hills, Hyderabad - 500034",
            "contact_number": "+91 40 2345 6789",
            "email": "hyderabad@storagerental.com",
            "facility_manager": "Administrator",
            "status": "Active"
        }
    ]

    for facility_data in additional_facilities:
        if not frappe.db.exists("Storage Facility", facility_data["facility_name"]):
            facility = frappe.get_doc(facility_data)
            facility.insert(ignore_permissions=True)

    # Create more Storage Units
    chennai_facility = frappe.db.get_value("Storage Facility", {"facility_name": "Chennai Storage Warehouse"}, "name")
    hyderabad_facility = frappe.db.get_value("Storage Facility", {"facility_name": "Hyderabad Storage Hub"}, "name")
    medium_category = frappe.db.get_value("Storage Category", {"category_name": "Medium"}, "name")
    large_category = frappe.db.get_value("Storage Category", {"category_name": "Large"}, "name")

    if chennai_facility and medium_category:
        units = [
            {"unit_number": "C-101", "storage_category": medium_category, "unit_size": "10x10", "monthly_rent": 3500, "security_deposit": 7000, "status": "Available"},
            {"unit_number": "C-102", "storage_category": medium_category, "unit_size": "10x10", "monthly_rent": 3500, "security_deposit": 7000, "status": "Occupied"},
        ]
        for unit_data in units:
            if not frappe.db.exists("Storage Unit", unit_data["unit_number"]):
                unit_data["doctype"] = "Storage Unit"
                unit_data["facility"] = chennai_facility
                unit = frappe.get_doc(unit_data)
                unit.insert(ignore_permissions=True)

    if hyderabad_facility and large_category:
        units = [
            {"unit_number": "H-101", "storage_category": large_category, "unit_size": "15x15", "monthly_rent": 6000, "security_deposit": 12000, "status": "Available"},
            {"unit_number": "H-102", "storage_category": large_category, "unit_size": "15x15", "monthly_rent": 6000, "security_deposit": 12000, "status": "Available"},
        ]
        for unit_data in units:
            if not frappe.db.exists("Storage Unit", unit_data["unit_number"]):
                unit_data["doctype"] = "Storage Unit"
                unit_data["facility"] = hyderabad_facility
                unit = frappe.get_doc(unit_data)
                unit.insert(ignore_permissions=True)

    # Create more Customers
    additional_customers = [
        {
            "doctype": "Customer Profile",
            "customer_name": "Vikram Singh",
            "customer_type": "Individual",
            "email": "vikram.singh@email.com",
            "mobile_number": "9876543215",
            "city": "Delhi",
            "status": "Active"
        },
        {
            "doctype": "Customer Profile",
            "customer_name": "Neha Kapoor",
            "customer_type": "Individual",
            "email": "neha.kapoor@email.com",
            "mobile_number": "9876543216",
            "city": "Mumbai",
            "status": "Active"
        },
        {
            "doctype": "Customer Profile",
            "customer_name": "StartUp Innovations",
            "customer_type": "Company",
            "email": "hello@startupinnovations.com",
            "mobile_number": "9876543217",
            "city": "Bangalore",
            "status": "Active"
        }
    ]

    for customer_data in additional_customers:
        if not frappe.db.exists("Customer Profile", {"customer_name": customer_data["customer_name"]}):
            customer = frappe.get_doc(customer_data)
            customer.insert(ignore_permissions=True)

    # Create Pricing entries
    facilities_list = frappe.get_all("Storage Facility", pluck="name")
    categories_list = frappe.get_all("Storage Category", pluck="name")

    for facility in facilities_list:
        for category in categories_list:
            pricing_name = f"{facility}-{category}-Pricing"
            if not frappe.db.exists("Pricing", pricing_name):
                pricing = frappe.get_doc({
                    "doctype": "Pricing",
                    "pricing_name": pricing_name,
                    "storage_category": category,
                    "storage_facility": facility,
                    "base_price": 2000,
                    "price_per_day": 100,
                    "price_per_week": 500,
                    "price_per_month": 2000,
                    "price_per_quarter": 5500,
                    "price_per_year": 20000,
                    "security_deposit": 4000,
                    "is_active": 1,
                    "effective_from": today()
                })
                pricing.insert(ignore_permissions=True)

    # Create additional Bookings with various statuses
    customers = frappe.get_all("Customer Profile", pluck="name")
    units = frappe.get_all("Storage Unit", {"status": "Available"}, pluck="name")
    plans = frappe.get_all("Rental Plan", pluck="name")

    if customers and units and plans:
        # Booking 1
        booking1 = frappe.get_doc({
            "doctype": "Storage Booking",
            "customer": customers[0],
            "storage_unit": units[0] if len(units) > 0 else None,
            "rental_plan": plans[0] if len(plans) > 0 else None,
            "booking_date": today(),
            "start_date": add_days(today(), 7),
            "end_date": add_days(today(), 37),
            "status": "Confirmed",
            "monthly_rent": 2000,
            "security_deposit": 4000,
            "total_amount": 6000
        })
        if not frappe.db.exists("Storage Booking", {"customer": customers[0]}):
            booking1.insert(ignore_permissions=True)

    # Create additional Payments
    if customers:
        for i, customer in enumerate(customers[:3]):
            payment_data = {
                "doctype": "Payment Collection",
                "customer": customer,
                "payment_date": today(),
                "payment_type": "Rent",
                "payment_mode": "UPI" if i % 2 == 0 else "Bank Transfer",
                "amount": 2000 + (i * 500),
                "total_amount": 2000 + (i * 500),
                "payment_status": "Completed",
                "reference_number": "TXN" + frappe.generate_hash(length=8).upper(),
                "payment_for_month": add_days(today(), -30)
            }
            if not frappe.db.exists("Payment Collection", {"customer": customer, "payment_type": "Rent"}):
                payment = frappe.get_doc(payment_data)
                payment.insert(ignore_permissions=True)

    # Create additional Unit Handovers
    if customers and units and len(units) > 1:
        handover_data = {
            "doctype": "Unit Handover",
            "customer": customers[1] if len(customers) > 1 else customers[0],
            "storage_unit": units[1] if len(units) > 1 else units[0],
            "handover_type": "Inspection",
            "handover_date": now_datetime(),
            "status": "Scheduled",
            "keys_received": 1,
            "unit_condition": "Good",
            "cleaning_status": "Clean"
        }
        if not frappe.db.exists("Unit Handover", {"storage_unit": handover_data["storage_unit"], "handover_type": "Inspection"}):
            handover = frappe.get_doc(handover_data)
            handover.insert(ignore_permissions=True)


def delete_demo_data():
    """Delete all demo data (useful for testing)."""
    demo_records = [
        ("Unit Handover", {"customer_name": ["in", ["Rahul Sharma", "Priya Patel", "Tech Solutions Pvt Ltd", "Anita Verma", "Global Traders Inc"]]}),
        ("Payment Collection", {"customer_name": ["in", ["Rahul Sharma", "Priya Patel", "Tech Solutions Pvt Ltd"]]}),
        ("Rental Agreement", {"customer_name": ["in", ["Rahul Sharma", "Priya Patel", "Tech Solutions Pvt Ltd"]]}),
        ("Storage Booking", {"customer_name": ["in", ["Rahul Sharma", "Priya Patel", "Tech Solutions Pvt Ltd"]]}),
        ("Customer Profile", {"customer_name": ["in", ["Rahul Sharma", "Priya Patel", "Tech Solutions Pvt Ltd", "Anita Verma", "Global Traders Inc"]]}),
        ("Storage Unit", {"unit_number": ["like", "%U-%"]}),
        ("Storage Facility", {"facility_name": ["like", "%Storage%"]}),
        ("Rental Plan", {"plan_name": ["like", "%Plan%"]}),
    ]

    for doctype, filters in demo_records:
        try:
            frappe.db.delete(doctype, filters)
        except Exception:
            pass

    frappe.db.commit()
