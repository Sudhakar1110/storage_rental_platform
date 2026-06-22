import frappe


def execute(filters=None):
    columns = [
        {"label": "Agreement ID", "fieldname": "name", "fieldtype": "Link", "options": "Rental Agreement", "width": 150},
        {"label": "Customer", "fieldname": "customer", "fieldtype": "Link", "options": "Customer Profile", "width": 150},
        {"label": "Storage Unit", "fieldname": "storage_unit", "fieldtype": "Link", "options": "Storage Unit", "width": 120},
        {"label": "Storage Facility", "fieldname": "facility", "fieldtype": "Link", "options": "Storage Facility", "width": 150},
        {"label": "Start Date", "fieldname": "start_date", "fieldtype": "Date", "width": 100},
        {"label": "End Date", "fieldname": "end_date", "fieldtype": "Date", "width": 100},
        {"label": "Days Remaining", "fieldname": "days_remaining", "fieldtype": "Int", "width": 100},
        {"label": "Monthly Rent", "fieldname": "monthly_rent", "fieldtype": "Currency", "width": 120},
        {"label": "Status", "fieldname": "status", "fieldtype": "Data", "width": 100}
    ]

    query = """
        SELECT
            ra.name,
            ra.customer,
            ra.storage_unit,
            su.facility,
            ra.start_date,
            ra.end_date,
            DATEDIFF(ra.end_date, CURDATE()) as days_remaining,
            ra.monthly_rent,
            ra.status
        FROM `tabRental Agreement` ra
        LEFT JOIN `tabStorage Unit` su ON ra.storage_unit = su.name
        WHERE ra.status = 'Active'
    """

    if filters:
        if filters.get("facility"):
            query += f" AND su.facility = '{filters.get('facility')}'"
        if filters.get("expiring_within_days"):
            query += f" AND DATEDIFF(ra.end_date, CURDATE()) <= {filters.get('expiring_within_days')}"

    query += " ORDER BY ra.end_date ASC"

    data = frappe.db.sql(query, as_dict=1)

    return columns, data
