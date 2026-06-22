import frappe
from frappe.model.document import Document


class PaymentCollection(Document):
    def autoname(self):
        if not self.payment_id:
            self.payment_id = "PAY-" + frappe.generate_hash(length=8).upper()

    def before_save(self):
        if self.amount:
            self.total_amount = self.amount + (self.gst_amount or 0)

    def on_submit(self):
        if self.payment_status == "Completed":
            self.update_booking_status()

    def update_booking_status(self):
        if self.storage_booking:
            booking = frappe.get_doc("Storage Booking", self.storage_booking)
            if booking.status == "Confirmed":
                booking.status = "Active"
                booking.save(ignore_permissions=True)
