import frappe


def execute(filters=None):
    columns = [
        {"label": "Payment ID", "fieldname": "name", "fieldtype": "Link", "options": "Payment Collection", "width": 150},
        {"label": "Customer", "fieldname": "customer", "fieldtype": "Link", "options": "Customer Profile", "width": 150},
        {"label": "Rental Agreement", "fieldname": "rental_agreement", "fieldtype": "Link", "options": "Rental Agreement", "width": 150},
        {"label": "Payment Date", "fieldname": "payment_date", "fieldtype": "Date", "width": 100},
        {"label": "Payment Type", "fieldname": "payment_type", "fieldtype": "Data", "width": 100},
        {"label": "Payment Mode", "fieldname": "payment_mode", "fieldtype": "Data", "width": 120},
        {"label": "Amount", "fieldname": "amount", "fieldtype": "Currency", "width": 120},
        {"label": "GST Amount", "fieldname": "gst_amount", "fieldtype": "Currency", "width": 100},
        {"label": "Total Amount", "fieldname": "total_amount", "fieldtype": "Currency", "width": 120},
        {"label": "Payment Status", "fieldname": "payment_status", "fieldtype": "Data", "width": 100}
    ]

    query = """
        SELECT
            pc.name,
            pc.customer,
            pc.rental_agreement,
            pc.payment_date,
            pc.payment_type,
            pc.payment_mode,
            pc.amount,
            pc.gst_amount,
            pc.total_amount,
            pc.payment_status
        FROM `tabPayment Collection` pc
        WHERE 1=1
    """

    if filters:
        if filters.get("payment_status"):
            query += f" AND pc.payment_status = '{filters.get('payment_status')}'"
        if filters.get("payment_type"):
            query += f" AND pc.payment_type = '{filters.get('payment_type')}'"
        if filters.get("customer"):
            query += f" AND pc.customer = '{filters.get('customer')}'"
        if filters.get("from_date"):
            query += f" AND pc.payment_date >= '{filters.get('from_date')}'"
        if filters.get("to_date"):
            query += f" AND pc.payment_date <= '{filters.get('to_date')}'"

    query += " ORDER BY pc.payment_date DESC"

    data = frappe.db.sql(query, as_dict=1)

    return columns, data
