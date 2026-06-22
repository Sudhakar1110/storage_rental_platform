import frappe
from frappe.model.document import Document


class StorageBooking(Document):
    def autoname(self):
        if not self.booking_id:
            self.booking_id = frappe.generate_hash(length=8).upper()

    def before_save(self):
        if self.rental_plan:
            rental_plan = frappe.get_doc("Rental Plan", self.rental_plan)
            self.monthly_rent = rental_plan.price
        
        if self.storage_unit:
            storage_unit = frappe.get_doc("Storage Unit", self.storage_unit)
            self.security_deposit = storage_unit.security_deposit
        
        if self.monthly_rent and self.security_deposit:
            self.total_amount = self.monthly_rent + self.security_deposit
        
        if self.total_amount and self.discount_amount:
            self.balance_amount = self.total_amount - self.discount_amount - (self.advance_amount or 0)
    
    def on_submit(self):
        if self.storage_unit:
            storage_unit = frappe.get_doc("Storage Unit", self.storage_unit)
            if storage_unit.status == "Available":
                storage_unit.status = "Reserved"
                storage_unit.save(ignore_permissions=True)
    
    def on_cancel(self):
        if self.storage_unit:
            storage_unit = frappe.get_doc("Storage Unit", self.storage_unit)
            if storage_unit.status == "Reserved":
                storage_unit.status = "Available"
                storage_unit.save(ignore_permissions=True)
