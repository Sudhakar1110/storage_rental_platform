import frappe


def execute(filters=None):
    columns = [
        {"label": "Facility", "fieldname": "facility_name", "fieldtype": "Link", "options": "Storage Facility", "width": 150},
        {"label": "Location", "fieldname": "location", "fieldtype": "Data", "width": 150},
        {"label": "Total Units", "fieldname": "total_units", "fieldtype": "Int", "width": 100},
        {"label": "Available Units", "fieldname": "available_units", "fieldtype": "Int", "width": 120},
        {"label": "Occupied Units", "fieldname": "occupied_units", "fieldtype": "Int", "width": 120},
        {"label": "Reserved Units", "fieldname": "reserved_units", "fieldtype": "Int", "width": 120},
        {"label": "Maintenance Units", "fieldname": "maintenance_units", "fieldtype": "Int", "width": 130},
        {"label": "Occupancy %", "fieldname": "occupancy_percentage", "fieldtype": "Float", "width": 100},
        {"label": "Status", "fieldname": "status", "fieldtype": "Data", "width": 100}
    ]

    query = """
        SELECT
            sf.name as facility_name,
            sf.location,
            sf.status,
            (SELECT COUNT(*) FROM `tabStorage Unit` su WHERE su.facility = sf.name) as total_units,
            (SELECT COUNT(*) FROM `tabStorage Unit` su WHERE su.facility = sf.name AND su.status = 'Available') as available_units,
            (SELECT COUNT(*) FROM `tabStorage Unit` su WHERE su.facility = sf.name AND su.status = 'Occupied') as occupied_units,
            (SELECT COUNT(*) FROM `tabStorage Unit` su WHERE su.facility = sf.name AND su.status = 'Reserved') as reserved_units,
            (SELECT COUNT(*) FROM `tabStorage Unit` su WHERE su.facility = sf.name AND su.status = 'Maintenance') as maintenance_units,
            ROUND(
                (SELECT COUNT(*) FROM `tabStorage Unit` su WHERE su.facility = sf.name AND su.status = 'Occupied') * 100.0 /
                NULLIF((SELECT COUNT(*) FROM `tabStorage Unit` su WHERE su.facility = sf.name), 0)
            , 2) as occupancy_percentage
        FROM `tabStorage Facility` sf
        WHERE 1=1
    """

    if filters:
        if filters.get("status"):
            query += f" AND sf.status = '{filters.get('status')}'"
        if filters.get("location"):
            query += f" AND sf.location = '{filters.get('location')}'"

    query += " ORDER BY occupancy_percentage DESC"

    data = frappe.db.sql(query, as_dict=1)

    return columns, data
