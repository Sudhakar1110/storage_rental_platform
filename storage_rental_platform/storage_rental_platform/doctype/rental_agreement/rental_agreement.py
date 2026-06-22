import frappe
from frappe.model.document import Document


class RentalAgreement(Document):
    def autoname(self):
        if not self.agreement_id:
            self.agreement_id = "RA-" + frappe.generate_hash(length=8).upper()

    def before_save(self):
        if self.storage_booking:
            booking = frappe.get_doc("Storage Booking", self.storage_booking)
            if not self.customer:
                self.customer = booking.customer
            if not self.storage_unit:
                self.storage_unit = booking.storage_unit
            if not self.start_date:
                self.start_date = booking.start_date
            if not self.end_date:
                self.end_date = booking.end_date
            if not self.monthly_rent:
                self.monthly_rent = booking.monthly_rent
            if not self.security_deposit:
                self.security_deposit = booking.security_deposit

    def on_submit(self):
        if self.storage_unit:
            storage_unit = frappe.get_doc("Storage Unit", self.storage_unit)
            if storage_unit.status in ["Available", "Reserved"]:
                storage_unit.status = "Occupied"
                storage_unit.save(ignore_permissions=True)
        
        if self.storage_booking:
            booking = frappe.get_doc("Storage Booking", self.storage_booking)
            booking.status = "Active"
            booking.save(ignore_permissions=True)

    def on_cancel(self):
        if self.storage_unit:
            storage_unit = frappe.get_doc("Storage Unit", self.storage_unit)
            if storage_unit.status == "Occupied":
                storage_unit.status = "Available"
                storage_unit.save(ignore_permissions=True)
