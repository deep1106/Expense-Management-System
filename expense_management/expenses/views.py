from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import JsonResponse
from accounts.models import CustomUser
from .models import Expense, ExpenseCategory
from .forms import ExpenseForm, ExpenseCategoryForm

@login_required
def index(request):
    if request.method == 'POST':
        if request.user.role == 'company_admin':
            if 'name' in request.POST:
                if not request.user.company:
                    # Handle case where company is None to avoid ValueError
                    return redirect('/')
                category_form = ExpenseCategoryForm(request.POST, company=request.user.company)
                if category_form.is_valid():
                    category = category_form.save()
                    return redirect('/')
            elif 'expense_id' in request.POST:
                expense_id = request.POST.get('expense_id')
                action = request.POST.get('action')
                try:
                    expense = Expense.objects.get(id=expense_id, company=request.user.company, status='pending')
                    if action == 'approve':
                        expense.status = 'approved'
                        expense.approved_by = request.user
                        expense.approved_at = timezone.now()
                    elif action == 'reject':
                        expense.status = 'rejected'
                        expense.approved_by = request.user
                    expense.save()
                    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                        return JsonResponse({'status': 'success'})
                except Expense.DoesNotExist:
                    pass  # ignore invalid requests
                if not request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return redirect('/')
        elif request.user.role == 'manager':
            expense_id = request.POST.get('expense_id')
            action = request.POST.get('action')
            try:
                expense = Expense.objects.get(id=expense_id, company=request.user.company, status='pending')
                if action == 'approve':
                    expense.status = 'approved'
                    expense.approved_by = request.user
                    expense.approved_at = timezone.now()
                elif action == 'reject':
                    expense.status = 'rejected'
                    expense.approved_by = request.user
                expense.save()
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({'status': 'success'})
            except Expense.DoesNotExist:
                pass  # ignore invalid requests
            if not request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return redirect('/')

    context = {}
    if request.user.role == 'company_admin':
        managers = CustomUser.objects.filter(company=request.user.company, role='manager')
        employees = CustomUser.objects.filter(company=request.user.company, role='employee')
        all_expenses = Expense.objects.filter(company=request.user.company).select_related('user', 'category', 'approved_by').order_by('-submitted_at')
        categories = ExpenseCategory.objects.filter(company=request.user.company)
        category_form = ExpenseCategoryForm()
        context = {
            'managers': managers,
            'employees': employees,
            'all_expenses': all_expenses,
            'categories': categories,
            'category_form': category_form,
        }
    elif request.user.role == 'manager':
        employees = CustomUser.objects.filter(company=request.user.company, role='employee')
        pending_expenses = Expense.objects.filter(company=request.user.company, status='pending').select_related('user', 'category').order_by('date')
        context = {
            'employees': employees,
            'pending_expenses': pending_expenses,
        }
    elif request.user.role == 'employee':
        expenses = Expense.objects.filter(user=request.user).select_related('category', 'approved_by').order_by('-date')
        context = {
            'expenses': expenses,
        }
    return render(request,'index.html', context)

@login_required
def manager_dashboard(request):
    if request.user.role != 'manager':
        return redirect('/')

    if request.method == 'POST':
        expense_id = request.POST.get('expense_id')
        action = request.POST.get('action')
        try:
            expense = Expense.objects.get(id=expense_id, company=request.user.company, status='pending')
            if action == 'approve':
                expense.status = 'approved'
                expense.approved_by = request.user
                expense.approved_at = timezone.now()
            elif action == 'reject':
                expense.status = 'rejected'
                expense.approved_by = request.user
            expense.save()
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'status': 'success'})
        except Expense.DoesNotExist:
            pass  # ignore invalid requests
        if not request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return redirect('/manager-dashboard')

    pending_expenses = Expense.objects.filter(company=request.user.company, status='pending').select_related('user', 'category').order_by('date')
    context = {'pending_expenses': pending_expenses}
    return render(request, 'manager_dashboard.html', context)

@login_required
def employee_dashboard(request):
    if request.user.role != 'employee':
        return redirect('/')

    if request.method == 'POST':
        form = ExpenseForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.company = request.user.company
            expense.category = form.cleaned_data['category']  # Ensure category is set from cleaned data
            expense.save()
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'id': expense.id,
                    'category': expense.category.name,
                    'amount': str(expense.amount),
                    'description': expense.description,
                    'date': expense.date.strftime('%Y-%m-%d'),
                    'status': expense.get_status_display(),
                })
            return redirect('/employee-dashboard')
    else:
        form = ExpenseForm(user=request.user)

    expenses = Expense.objects.filter(user=request.user).select_related('category', 'approved_by').order_by('-date')
    categories = ExpenseCategory.objects.filter(company=request.user.company)
    context = {'form': form, 'expenses': expenses, 'categories': categories}
    return render(request, 'employee_dashboard.html', context)
