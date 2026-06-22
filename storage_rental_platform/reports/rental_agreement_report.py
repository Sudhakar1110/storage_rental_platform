import frappe


def execute(filters=None):
    columns = [
        {"label": "Agreement ID", "fieldname": "name", "fieldtype": "Link", "options": "Rental Agreement", "width": 150},
        {"label": "Storage Booking", "fieldname": "storage_booking", "fieldtype": "Link", "options": "Storage Booking", "width": 150},
        {"label": "Customer", "fieldname": "customer", "fieldtype": "Link", "options": "Customer Profile", "width": 150},
        {"label": "Storage Unit", "fieldname": "storage_unit", "fieldtype": "Link", "options": "Storage Unit", "width": 120},
        {"label": "Agreement Date", "fieldname": "agreement_date", "fieldtype": "Date", "width": 100},
        {"label": "Start Date", "fieldname": "start_date", "fieldtype": "Date", "width": 100},
        {"label": "End Date", "fieldname": "end_date", "fieldtype": "Date", "width": 100},
        {"label": "Monthly Rent", "fieldname": "monthly_rent", "fieldtype": "Currency", "width": 120},
        {"label": "Security Deposit", "fieldname": "security_deposit", "fieldtype": "Currency", "width": 130},
        {"label": "Status", "fieldname": "status", "fieldtype": "Data", "width": 100}
    ]

    query = """
        SELECT
            ra.name,
            ra.storage_booking,
            ra.customer,
            ra.storage_unit,
            ra.agreement_date,
            ra.start_date,
            ra.end_date,
            ra.monthly_rent,
            ra.security_deposit,
            ra.status
        FROM `tabRental Agreement` ra
        WHERE 1=1
    """

    if filters:
        if filters.get("status"):
            query += f" AND ra.status = '{filters.get('status')}'"
        if filters.get("customer"):
            query += f" AND ra.customer = '{filters.get('customer')}'"
        if filters.get("from_date"):
            query += f" AND ra.agreement_date >= '{filters.get('from_date')}'"
        if filters.get("to_date"):
            query += f" AND ra.agreement_date <= '{filters.get('to_date')}'"

    query += " ORDER BY ra.agreement_date DESC"

    data = frappe.db.sql(query, as_dict=1)

    return columns, data
