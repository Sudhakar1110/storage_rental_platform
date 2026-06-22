import frappe


def execute(filters=None):
    columns = [
        {"label": "Booking ID", "fieldname": "name", "fieldtype": "Link", "options": "Storage Booking", "width": 150},
        {"label": "Customer", "fieldname": "customer", "fieldtype": "Link", "options": "Customer Profile", "width": 150},
        {"label": "Storage Unit", "fieldname": "storage_unit", "fieldtype": "Link", "options": "Storage Unit", "width": 120},
        {"label": "Rental Plan", "fieldname": "rental_plan", "fieldtype": "Link", "options": "Rental Plan", "width": 120},
        {"label": "Booking Date", "fieldname": "booking_date", "fieldtype": "Date", "width": 100},
        {"label": "Start Date", "fieldname": "start_date", "fieldtype": "Date", "width": 100},
        {"label": "End Date", "fieldname": "end_date", "fieldtype": "Date", "width": 100},
        {"label": "Status", "fieldname": "status", "fieldtype": "Data", "width": 100},
        {"label": "Monthly Rent", "fieldname": "monthly_rent", "fieldtype": "Currency", "width": 120},
        {"label": "Total Amount", "fieldname": "total_amount", "fieldtype": "Currency", "width": 120}
    ]

    query = """
        SELECT
            name,
            customer,
            storage_unit,
            rental_plan,
            booking_date,
            start_date,
            end_date,
            status,
            monthly_rent,
            total_amount
        FROM `tabStorage Booking`
        WHERE 1=1
    """

    if filters:
        if filters.get("status"):
            query += f" AND status = '{filters.get('status')}'"
        if filters.get("customer"):
            query += f" AND customer = '{filters.get('customer')}'"
        if filters.get("from_date"):
            query += f" AND booking_date >= '{filters.get('from_date')}'"
        if filters.get("to_date"):
            query += f" AND booking_date <= '{filters.get('to_date')}'"

    query += " ORDER BY creation DESC"

    data = frappe.db.sql(query, as_dict=1)

    return columns, data
