import frappe


def execute(filters=None):
    columns = [
        {"label": "Unit Number", "fieldname": "name", "fieldtype": "Link", "options": "Storage Unit", "width": 120},
        {"label": "Storage Category", "fieldname": "storage_category", "fieldtype": "Link", "options": "Storage Category", "width": 130},
        {"label": "Facility", "fieldname": "facility", "fieldtype": "Link", "options": "Storage Facility", "width": 150},
        {"label": "Unit Size", "fieldname": "unit_size", "fieldtype": "Data", "width": 100},
        {"label": "Dimensions", "fieldname": "dimensions", "fieldtype": "Data", "width": 120},
        {"label": "Floor", "fieldname": "floor", "fieldtype": "Int", "width": 60},
        {"label": "Monthly Rent", "fieldname": "monthly_rent", "fieldtype": "Currency", "width": 120},
        {"label": "Security Deposit", "fieldname": "security_deposit", "fieldtype": "Currency", "width": 130},
        {"label": "Status", "fieldname": "status", "fieldtype": "Data", "width": 100}
    ]

    query = """
        SELECT
            su.name,
            su.storage_category,
            su.facility,
            su.unit_size,
            su.dimensions,
            su.floor,
            su.monthly_rent,
            su.security_deposit,
            su.status
        FROM `tabStorage Unit` su
        WHERE 1=1
    """

    if filters:
        if filters.get("status"):
            query += f" AND su.status = '{filters.get('status')}'"
        if filters.get("facility"):
            query += f" AND su.facility = '{filters.get('facility')}'"
        if filters.get("storage_category"):
            query += f" AND su.storage_category = '{filters.get('storage_category')}'"
        if filters.get("min_rent"):
            query += f" AND su.monthly_rent >= {filters.get('min_rent')}"
        if filters.get("max_rent"):
            query += f" AND su.monthly_rent <= {filters.get('max_rent')}"

    query += " ORDER BY su.facility, su.name"

    data = frappe.db.sql(query, as_dict=1)

    return columns, data
