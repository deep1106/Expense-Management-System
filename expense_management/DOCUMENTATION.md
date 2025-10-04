# Expense Management System Documentation

## Overview
This system allows company admins, managers, and employees to manage expenses efficiently. Key features include:

- Role-based dashboards for company admins, managers, and employees.
- Company admins can manage users, expense categories, and view all expenses.
- Managers can approve or reject pending expenses.
- Employees can submit expenses with category, amount, description, date, and optional receipt.
- AJAX-based interactions for smooth user experience without page reloads.
- Validation and error handling using Django forms.

## Key Components

### Models
- **ExpenseCategory**: Represents categories of expenses linked to a company.
- **Expense**: Represents an expense submitted by an employee, linked to a category and company.
- **CustomUser**: User model with roles (company_admin, manager, employee) and company association.

### Forms
- **ExpenseForm**: Used by employees to submit expenses. Filters categories by user's company.
- **ExpenseCategoryForm**: Used by company admins to add new expense categories. Requires company to be set.

### Views
- **index**: Main dashboard for company admins to manage users, categories, and view expenses.
- **manager_dashboard**: Managers view and approve/reject pending expenses.
- **employee_dashboard**: Employees submit expenses and view their own expense history.

### Templates
- Use Bootstrap 5 for responsive UI.
- AJAX used for approve/reject actions and expense submissions.
- Role-based UI rendering with navigation and access control.

## Known Issues and Fixes
- Fixed IntegrityError by ensuring company is set on ExpenseCategory before saving.
- Fixed category not saving in expenses by explicitly setting category from form.cleaned_data.
- Added company parameter to ExpenseCategoryForm to ensure company is assigned correctly.
- AJAX implemented for better UX in expense approval and submission.

## Testing
- Tested employee dashboard form rendering and category display.
- Tested AJAX form submission for adding expenses.
- Tested manager dashboard approve/reject functionality with AJAX.
- Further testing recommended for director signup, add user forms, and full application flow.

## Setup and Running
- Run `python manage.py migrate` to apply migrations.
- Run `python manage.py runserver` to start the development server.
- Access the app via `http://localhost:8000/`.

## Future Improvements
- Add edit functionality for expense categories.
- Enhance error handling and user feedback.
- Add reporting and analytics features.

---

For any questions or support, please contact the development team.
