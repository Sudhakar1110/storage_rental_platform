import frappe


def execute(filters=None):
    columns = [
        {"label": "Customer ID", "fieldname": "name", "fieldtype": "Link", "options": "Customer Profile", "width": 150},
        {"label": "Customer Name", "fieldname": "customer_name", "fieldtype": "Data", "width": 150},
        {"label": "Customer Type", "fieldname": "customer_type", "fieldtype": "Data", "width": 100},
        {"label": "Email", "fieldname": "email", "fieldtype": "Data", "width": 180},
        {"label": "Mobile Number", "fieldname": "mobile_number", "fieldtype": "Data", "width": 120},
        {"label": "City", "fieldname": "city", "fieldtype": "Data", "width": 100},
        {"label": "Active Bookings", "fieldname": "active_bookings", "fieldtype": "Int", "width": 120},
        {"label": "Total Rentals", "fieldname": "total_rentals", "fieldtype": "Int", "width": 120},
        {"label": "Status", "fieldname": "status", "fieldtype": "Data", "width": 100}
    ]

    query = """
        SELECT
            cp.name,
            cp.customer_name,
            cp.customer_type,
            cp.email,
            cp.mobile_number,
            cp.city,
            (SELECT COUNT(*) FROM `tabStorage Booking` sb WHERE sb.customer = cp.name AND sb.status = 'Active') as active_bookings,
            (SELECT COUNT(*) FROM `tabStorage Booking` sb WHERE sb.customer = cp.name) as total_rentals,
            cp.status
        FROM `tabCustomer Profile` cp
        WHERE 1=1
    """

    if filters:
        if filters.get("status"):
            query += f" AND cp.status = '{filters.get('status')}'"
        if filters.get("customer_type"):
            query += f" AND cp.customer_type = '{filters.get('customer_type')}'"
        if filters.get("city"):
            query += f" AND cp.city = '{filters.get('city')}'"

    query += " ORDER BY cp.creation DESC"

    data = frappe.db.sql(query, as_dict=1)

    return columns, data
