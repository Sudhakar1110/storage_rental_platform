# Storage Rental Platform

A comprehensive Storage Rental Management System built for Frappe Framework v15 and ERPNext v15+.

## Features

- **Masters Management**: Storage Facilities, Storage Units, Storage Categories, Customer Profiles, Rental Plans
- **Transactions**: Storage Bookings, Rental Agreements, Payment Collections, Unit Handovers
- **Reports**: Comprehensive reporting for bookings, rentals, customers, facility occupancy, payments, and agreements
- **Workflows**: Automated workflows for Storage Bookings and Rental Agreements
- **Role-based Access**: Storage Administrator, Facility Manager, Customer User roles

## Installation

### Prerequisites

- Frappe Framework v15 or higher
- ERPNext v15 or higher

### Steps

1. **Get the app**:
   ```bash
   bench get-app storage_rental_platform <repo_url>
   ```

2. **Install the app**:
   ```bash
   bench --site yoursite install-app storage_rental_platform
   ```

3. **Run migrations**:
   ```bash
   bench --site yoursite migrate
   ```

4. **Build assets**:
   ```bash
   bench build
   ```

5. **Clear cache** (optional):
   ```bash
   bench --site yoursite clear-cache
   bench --site yoursite clear-website-cache
   ```

## Demo Data

Demo data is automatically created during installation. It includes:
- Sample Storage Facilities
- Sample Storage Units and Categories
- Sample Customers
- Sample Rental Plans
- Sample Bookings and Agreements
- Sample Payments

## User Roles

- **Storage Administrator**: Full access to all features
- **Facility Manager**: Manage facilities and units
- **Customer User**: View and manage their own bookings

## License

MIT License