import frappe
from frappe.model.document import Document


class UnitHandover(Document):
    def autoname(self):
        if not self.handover_id:
            self.handover_id = "HO-" + frappe.generate_hash(length=8).upper()

    def before_save(self):
        if self.rental_agreement:
            agreement = frappe.get_doc("Rental Agreement", self.rental_agreement)
            if not self.customer:
                self.customer = agreement.customer
            if not self.storage_unit:
                self.storage_unit = agreement.storage_unit

    def on_submit(self):
        if self.handover_type == "Move In":
            self.update_unit_for_move_in()
        elif self.handover_type == "Move Out":
            self.update_unit_for_move_out()

    def update_unit_for_move_in(self):
        if self.storage_unit:
            storage_unit = frappe.get_doc("Storage Unit", self.storage_unit)
            storage_unit.status = "Occupied"
            storage_unit.save(ignore_permissions=True)

    def update_unit_for_move_out(self):
        if self.storage_unit:
            storage_unit = frappe.get_doc("Storage Unit", self.storage_unit)
            storage_unit.status = "Available"
            storage_unit.save(ignore_permissions=True)
