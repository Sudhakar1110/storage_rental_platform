app_name = "storage_rental_platform"
app_title = "Storage Rental Platform"
app_publisher = "Your Company"
app_description = "Storage Rental Platform for ERPNext"
app_email = "info@example.com"
app_license = "MIT"
app_version = "1.0.0"

fixtures = [
    {
        "doctype": "Role",
        "filters": [
            [
                "name",
                "in",
                [
                    "Storage Administrator",
                    "Facility Manager",
                    "Customer User"
                ]
            ]
        ]
    },
    {
        "doctype": "Workflow State",
        "filters": [
            [
                "workflow_state_name",
                "in",
                [
                    "Draft",
                    "Confirmed",
                    "Active",
                    "Completed",
                    "Cancelled",
                    "Expired",
                    "Terminated",
                    "Pending Approval",
                    "Approved",
                    "Rejected"
                ]
            ]
        ]
    },
    {
        "doctype": "Workflow",
        "filters": [
            [
                "workflow_name",
                "in",
                [
                    "Storage Booking Workflow",
                    "Rental Agreement Workflow"
                ]
            ]
        ]
    }
]

after_install = "storage_rental_platform.install.after_install"
