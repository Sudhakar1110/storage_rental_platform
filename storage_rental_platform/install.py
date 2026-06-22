import frappe
from frappe.utils import today, add_days


WORKSPACE_NAMES_TO_KEEP = ["Storage Rental Platform"]


def after_install():
    create_custom_roles()
    _create_initial_demo_data()


# Flag file used to prevent re-running demo data on every migrate
_DEMO_FLAG = "demo_data_created_v2"


def after_migrate():
    """Run post-migration tasks."""
    cleanup_orphaned_workspaces()
    fix_reports_ref_doctype()
    _create_comprehensive_demo_data()


REPORT_REF_DOCTYPES = {
    "Storage Booking Report": "Storage Booking",
    "Active Rental Report": "Rental Agreement",
    "Customer Report": "Customer Profile",
    "Facility Occupancy Report": "Storage Facility",
    "Payment Collection Report": "Payment Collection",
    "Unit Availability Report": "Storage Unit",
    "Rental Agreement Report": "Rental Agreement",
}


def fix_reports_ref_doctype():
    """Fix Report records that are missing ref_doctype.
    
    This ensures existing Report records have their ref_doctype set correctly
    even if sync_for() skipped them due to timestamp comparison.
    """
    for report_name, ref_doctype in REPORT_REF_DOCTYPES.items():
        if not frappe.db.exists("Report", report_name):
            continue
        current = frappe.db.get_value("Report", report_name, "ref_doctype")
        if not current:
            try:
                frappe.db.set_value("Report", report_name, "ref_doctype", ref_doctype)
                print(f"Fixed ref_doctype for Report: {report_name} -> {ref_doctype}")
            except Exception as e:
                print(f"Could not fix Report {report_name}: {e}")
    frappe.db.commit()


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




def _create_comprehensive_demo_data():
    """Create comprehensive demo data on migrate if not already done.
    Uses a flag to ensure it only runs once.
    """
    if frappe.db.get_single_value("System Settings", _DEMO_FLAG):
        return

    from storage_rental_platform.demo_data import create_demo_data
    create_demo_data()

    # Set flag so this only runs once
    try:
        frappe.db.set_single_value("System Settings", _DEMO_FLAG, 1)
        frappe.db.commit()
    except Exception:
        pass
