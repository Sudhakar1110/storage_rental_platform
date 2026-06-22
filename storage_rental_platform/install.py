import frappe
from frappe.utils import today, add_days


WORKSPACE_NAMES_TO_KEEP = ["Storage Rental Platform"]


def after_install():
    create_custom_roles()
    create_demo_data()


def after_migrate():
    """Cleanup orphaned workspace records that no longer exist as fixture files."""
    cleanup_orphaned_workspaces()


def cleanup_orphaned_workspaces():
    """Delete workspace records that are not in the allowed keep list.
    These are orphaned records from old fixtures that were removed."""
    all_workspaces = frappe.get_all(
        "Workspace",
        fields=["name", "module"],
        filters=[
            ["module", "in", ["storage_rental_platform", "Storage Rental Platform"]]
        ]
    )
    for ws in all_workspaces:
        if ws.name not in WORKSPACE_NAMES_TO_KEEP:
            try:
                frappe.delete_doc("Workspace", ws.name, force=1, ignore_permissions=True)
                print(f"Cleaned up orphaned workspace: {ws.name}")
            except Exception as e:
                print(f"Could not delete workspace {ws.name}: {e}")
    frappe.db.commit()


def create_custom_roles():
    roles_data = [
        {
            "role_name": "Storage Administrator",
            "description": "Full access to all Storage Rental Platform features",
            "is_custom": 1,
            "desk_access": 1
        },
        {
            "role_name": "Facility Manager",
            "description": "Manage facilities and storage units",
            "is_custom": 1,
            "desk_access": 1
        },
        {
            "role_name": "Customer User",
            "description": "View and manage own bookings as a customer",
            "is_custom": 1,
            "desk_access": 1
        }
    ]

    for role_data in roles_data:
        if not frappe.db.exists("Role", role_data["role_name"]):
            role = frappe.new_doc("Role")
            role.update(role_data)
            role.insert(ignore_permissions=True)


def create_demo_data():
    if frappe.db.exists("Storage Facility", "Central Storage - Delhi"):
        return

    # Create Storage Facilities
    facilities = [
        {
            "doctype": "Storage Facility",
            "facility_name": "Central Storage - Delhi",
            "location": "Delhi",
            "address": "123 Main Market, Connaught Place, New Delhi - 110001",
            "contact_number": "+91 11 2345 6789",
            "email": "delhi@storagerental.com",
            "facility_manager": "Administrator",
            "status": "Active",
            "description": "Premium storage facility in the heart of Delhi"
        },
        {
            "doctype": "Storage Facility",
            "facility_name": "Mumbai Storage Hub",
            "location": "Mumbai",
            "address": "456 Andheri East, Mumbai - 400069",
            "contact_number": "+91 22 2345 6789",
            "email": "mumbai@storagerental.com",
            "facility_manager": "Administrator",
            "status": "Active",
            "description": "State-of-the-art storage facility in Mumbai"
        },
        {
            "doctype": "Storage Facility",
            "facility_name": "Bangalore Storage Center",
            "location": "Bangalore",
            "address": "789 Whitefield, Bangalore - 560066",
            "contact_number": "+91 80 2345 6789",
            "email": "bangalore@storagerental.com",
            "facility_manager": "Administrator",
            "status": "Active",
            "description": "Modern storage solutions in Bangalore"
        }
    ]

    created_facilities = {}
    for facility_data in facilities:
        if not frappe.db.exists("Storage Facility", facility_data["facility_name"]):
            facility = frappe.get_doc(facility_data)
            facility.insert(ignore_permissions=True)
            created_facilities[facility_data["facility_name"]] = facility.name
        else:
            created_facilities[facility_data["facility_name"]] = frappe.db.get_value(
                "Storage Facility", {"facility_name": facility_data["facility_name"]}, "name"
            )

    # Create Storage Categories
    categories = [
        {
            "doctype": "Storage Category",
            "category_name": "Small",
            "storage_type": "Small",
            "description": "Small storage units for personal items",
            "min_height": 5,
            "max_height": 7,
            "is_active": 1
        },
        {
            "doctype": "Storage Category",
            "category_name": "Medium",
            "storage_type": "Medium",
            "description": "Medium storage units for household items",
            "min_height": 7,
            "max_height": 10,
            "is_active": 1
        },
        {
            "doctype": "Storage Category",
            "category_name": "Large",
            "storage_type": "Large",
            "description": "Large storage units for business inventory",
            "min_height": 10,
            "max_height": 15,
            "is_active": 1
        },
        {
            "doctype": "Storage Category",
            "category_name": "Extra Large",
            "storage_type": "Extra Large",
            "description": "Extra large units for commercial storage",
            "min_height": 15,
            "max_height": 20,
            "is_active": 1
        }
    ]

    created_categories = {}
    for category_data in categories:
        if not frappe.db.exists("Storage Category", category_data["category_name"]):
            category = frappe.get_doc(category_data)
            category.insert(ignore_permissions=True)
            created_categories[category_data["category_name"]] = category.name
        else:
            created_categories[category_data["category_name"]] = frappe.db.get_value(
                "Storage Category", {"category_name": category_data["category_name"]}, "name"
            )

    # Create Storage Units for Delhi Facility
    delhi_facility = created_facilities.get("Central Storage - Delhi")
    if delhi_facility:
        units_data = [
            {"unit_number": "U-101", "storage_category": created_categories.get("Small"), "unit_size": "5x5", "dimensions": "5ft x 5ft x 8ft", "floor": 1, "monthly_rent": 2000, "security_deposit": 4000, "status": "Available"},
            {"unit_number": "U-102", "storage_category": created_categories.get("Small"), "unit_size": "5x5", "dimensions": "5ft x 5ft x 8ft", "floor": 1, "monthly_rent": 2000, "security_deposit": 4000, "status": "Available"},
            {"unit_number": "U-201", "storage_category": created_categories.get("Medium"), "unit_size": "10x10", "dimensions": "10ft x 10ft x 10ft", "floor": 2, "monthly_rent": 4000, "security_deposit": 8000, "status": "Occupied"},
            {"unit_number": "U-202", "storage_category": created_categories.get("Medium"), "unit_size": "10x10", "dimensions": "10ft x 10ft x 10ft", "floor": 2, "monthly_rent": 4000, "security_deposit": 8000, "status": "Available"},
            {"unit_number": "U-301", "storage_category": created_categories.get("Large"), "unit_size": "15x15", "dimensions": "15ft x 15ft x 12ft", "floor": 3, "monthly_rent": 7000, "security_deposit": 14000, "status": "Available"},
            {"unit_number": "U-401", "storage_category": created_categories.get("Extra Large"), "unit_size": "20x20", "dimensions": "20ft x 20ft x 15ft", "floor": 4, "monthly_rent": 12000, "security_deposit": 24000, "status": "Available"},
        ]

        for unit_data in units_data:
            unit_data["doctype"] = "Storage Unit"
            unit_data["facility"] = delhi_facility
            if not frappe.db.exists("Storage Unit", unit_data["unit_number"]):
                unit = frappe.get_doc(unit_data)
                unit.insert(ignore_permissions=True)

    # Create Customer Profiles
    customers_data = [
        {
            "doctype": "Customer Profile",
            "customer_name": "Rahul Sharma",
            "customer_type": "Individual",
            "email": "rahul.sharma@email.com",
            "mobile_number": "9876543210",
            "phone": "+91 11 2345 6789",
            "address": "456 Green Park, South Delhi",
            "city": "Delhi",
            "state": "Delhi",
            "pincode": "110016",
            "country": "India",
            "date_of_birth": "1985-06-15",
            "id_proof": "Aadhar Card",
            "id_number": "1234-5678-9012",
            "status": "Active"
        },
        {
            "doctype": "Customer Profile",
            "customer_name": "Priya Patel",
            "customer_type": "Individual",
            "email": "priya.patel@email.com",
            "mobile_number": "9876543211",
            "phone": "+91 22 2345 6789",
            "address": "789 Andheri West, Mumbai",
            "city": "Mumbai",
            "state": "Maharashtra",
            "pincode": "400058",
            "country": "India",
            "id_proof": "PAN Card",
            "id_number": "ABCDE1234F",
            "status": "Active"
        },
        {
            "doctype": "Customer Profile",
            "customer_name": "Tech Solutions Pvt Ltd",
            "customer_type": "Company",
            "email": "admin@techsolutions.com",
            "mobile_number": "9876543212",
            "phone": "+91 80 2345 6789",
            "address": "100 Electronic City, Phase 1",
            "city": "Bangalore",
            "state": "Karnataka",
            "pincode": "560100",
            "country": "India",
            "id_proof": "PAN Card",
            "id_number": "AABCT1234E",
            "status": "Active"
        },
        {
            "doctype": "Customer Profile",
            "customer_name": "Anita Verma",
            "customer_type": "Individual",
            "email": "anita.verma@email.com",
            "mobile_number": "9876543213",
            "address": "321 MG Road, Pune",
            "city": "Pune",
            "state": "Maharashtra",
            "pincode": "411001",
            "country": "India",
            "id_proof": "Passport",
            "id_number": "J1234567",
            "status": "Active"
        },
        {
            "doctype": "Customer Profile",
            "customer_name": "Global Traders Inc",
            "customer_type": "Company",
            "email": "info@globaltraders.com",
            "mobile_number": "9876543214",
            "phone": "+91 11 2345 6790",
            "address": "555 Nehru Place, New Delhi",
            "city": "Delhi",
            "state": "Delhi",
            "pincode": "110019",
            "country": "India",
            "id_proof": "PAN Card",
            "id_number": "AABCG5678H",
            "status": "Active"
        }
    ]

    created_customers = {}
    for customer_data in customers_data:
        if not frappe.db.exists("Customer Profile", {"customer_name": customer_data["customer_name"]}):
            customer = frappe.get_doc(customer_data)
            customer.insert(ignore_permissions=True)
            created_customers[customer_data["customer_name"]] = customer.name
        else:
            created_customers[customer_data["customer_name"]] = frappe.db.get_value(
                "Customer Profile", {"customer_name": customer_data["customer_name"]}, "name"
            )

    # Create Rental Plans
    plans_data = [
        {
            "doctype": "Rental Plan",
            "plan_name": "Monthly Basic",
            "duration": 30,
            "duration_type": "Monthly",
            "price": 2000,
            "discount_percentage": 0,
            "description": "Basic monthly rental plan",
            "is_active": 1
        },
        {
            "doctype": "Rental Plan",
            "plan_name": "Monthly Standard",
            "duration": 30,
            "duration_type": "Monthly",
            "price": 4000,
            "discount_percentage": 5,
            "description": "Standard monthly rental plan with 5% discount",
            "is_active": 1
        },
        {
            "doctype": "Rental Plan",
            "plan_name": "Quarterly Premium",
            "duration": 90,
            "duration_type": "Quarterly",
            "price": 10800,
            "discount_percentage": 10,
            "description": "Quarterly premium plan with 10% discount",
            "is_active": 1
        },
        {
            "doctype": "Rental Plan",
            "plan_name": "Yearly Enterprise",
            "duration": 365,
            "duration_type": "Yearly",
            "price": 36000,
            "discount_percentage": 20,
            "description": "Annual enterprise plan with 20% discount",
            "is_active": 1
        }
    ]

    created_plans = {}
    for plan_data in plans_data:
        if not frappe.db.exists("Rental Plan", plan_data["plan_name"]):
            plan = frappe.get_doc(plan_data)
            plan.insert(ignore_permissions=True)
            created_plans[plan_data["plan_name"]] = plan.name
        else:
            created_plans[plan_data["plan_name"]] = frappe.db.get_value(
                "Rental Plan", {"plan_name": plan_data["plan_name"]}, "name"
            )

    # Create a Storage Booking
    rahul_customer = created_customers.get("Rahul Sharma")
    unit_u102 = frappe.db.get_value("Storage Unit", {"unit_number": "U-102"}, "name")
    plan_basic = created_plans.get("Monthly Basic")

    if rahul_customer and unit_u102 and plan_basic:
        if not frappe.db.exists("Storage Booking", {"customer": rahul_customer, "storage_unit": unit_u102}):
            booking = frappe.get_doc({
                "doctype": "Storage Booking",
                "customer": rahul_customer,
                "storage_unit": unit_u102,
                "rental_plan": plan_basic,
                "booking_date": today(),
                "start_date": today(),
                "end_date": add_days(today(), 30),
                "status": "Draft",
                "monthly_rent": 2000,
                "security_deposit": 4000,
                "total_amount": 6000,
                "notes": "First booking for Rahul Sharma"
            })
            booking.insert(ignore_permissions=True)

    # Create a Rental Agreement
    priya_customer = created_customers.get("Priya Patel")
    unit_u201 = frappe.db.get_value("Storage Unit", {"unit_number": "U-201"}, "name")
    plan_standard = created_plans.get("Monthly Standard")

    if priya_customer and unit_u201 and plan_standard:
        if not frappe.db.exists("Rental Agreement", {"customer": priya_customer}):
            agreement = frappe.get_doc({
                "doctype": "Rental Agreement",
                "customer": priya_customer,
                "storage_unit": unit_u201,
                "agreement_date": today(),
                "start_date": today(),
                "end_date": add_days(today(), 365),
                "status": "Draft",
                "monthly_rent": 4000,
                "security_deposit": 8000,
                "total_rent": 48000,
                "payment_due_day": 5,
                "notice_period": 30,
                "terms_and_conditions": "Standard rental terms and conditions apply."
            })
            agreement.insert(ignore_permissions=True)

    # Create a Payment Collection
    if priya_customer:
        if not frappe.db.exists("Payment Collection", {"customer": priya_customer, "payment_type": "Security Deposit"}):
            payment = frappe.get_doc({
                "doctype": "Payment Collection",
                "customer": priya_customer,
                "payment_date": today(),
                "payment_type": "Security Deposit",
                "payment_mode": "Bank Transfer",
                "amount": 8000,
                "total_amount": 8000,
                "payment_status": "Completed",
                "reference_number": "TXN" + frappe.generate_hash(length=8).upper()
            })
            payment.insert(ignore_permissions=True)

    # Create a Unit Handover
    tech_solutions = created_customers.get("Tech Solutions Pvt Ltd")
    if tech_solutions:
        unit_u301 = frappe.db.get_value("Storage Unit", {"unit_number": "U-301"}, "name")
        if unit_u301:
            handover = frappe.get_doc({
                "doctype": "Unit Handover",
                "customer": tech_solutions,
                "storage_unit": unit_u301,
                "handover_type": "Move In",
                "handover_date": today(),
                "status": "Scheduled",
                "keys_received": 1,
                "remote_received": 1,
                "access_card_received": 1,
                "unit_condition": "Excellent",
                "cleaning_status": "Clean"
            })
            handover.insert(ignore_permissions=True)
