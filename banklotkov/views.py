from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from .forms import SignUpForm, LoginForm, BalanceRequestForm, LoanForm, ProfileEditForm, ReviewForm, ProductForm
from .models import Profile, Product, Transaction, Loan, Review
from django.contrib import messages


class CustomLoginView(LoginView):
    authentication_form = LoginForm
    template_name = 'login.html'
    redirect_authenticated_user = True


def home_page(request):
    return render(request, 'home_page.html')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            Profile.objects.get_or_create(user=user)
            return redirect('lk')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def lk_view(request):
    profile = Profile.objects.get(user=request.user)
    active_loans = Loan.objects.filter(borrower=profile, is_active=True)
    recent_transactions = Transaction.objects.filter(sender=profile).order_by('-created_at')[:5]
    
    context = {
        'profile': profile,
        'active_loans': active_loans,
        'recent_transactions': recent_transactions,
    }
    return render(request, 'lk.html', context)

@login_required
def balance_request(request):
    if request.method == 'POST':
        form = BalanceRequestForm(request.POST)
        if form.is_valid():
            balance_request = form.save(commit=False)
            balance_request.user = request.user
            balance_request.save()
            messages.success(request, 'Заявка на пополнение баланса успешно отправлена.')
            return redirect('lk')
    else:
        form = BalanceRequestForm()
    return render(request, 'balance_request.html', {'form': form})

@login_required
def transaction_history(request):
    profile = Profile.objects.get(user=request.user)
    transactions = Transaction.objects.filter(sender=profile).order_by('-created_at')
    paginator = Paginator(transactions, 10)  # 10 транзакций на страницу
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'transaction_history.html', {'page_obj': page_obj})

@login_required
def new_loan(request):
    if request.method == 'POST':
        form = LoanForm(request.POST)
        if form.is_valid():
            loan = form.save(commit=False)
            loan.borrower = Profile.objects.get(user=request.user)
            loan.save()
            messages.success(request, 'Заявка на кредит успешно отправлена.')
            return redirect('lk')
    else:
        form = LoanForm()
    return render(request, 'new_loan.html', {'form': form})

@login_required
def edit_profile(request):
    profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=profile, user=request.user)
        if form.is_valid():
            form.save(commit=False)
            messages.success(request, 'Профиль успешно обновлен.')
            return redirect('lk')
    else:
        form = ProfileEditForm(instance=profile, user=request.user)
    return render(request, 'edit_profile.html', {'form': form, 'profile': profile})

def thanks_view(request):
    return render(request, 'thanks.html')


def product_list_view(request):
    products_list = Product.objects.filter(availible=True)
    paginator = Paginator(products_list, 6)

    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)
    
    return render(request, 'product_list.html', {'products': products})


@login_required
def add_review(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    profile = Profile.objects.get(user=request.user)

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.author = profile
            review.save()
            messages.success(request, 'Ваш отзыв успешно добавлен!')
            return redirect('product_detail', product_id=product.id)
    else:
        form = ReviewForm()
    return render(request, 'add_review.html', {'form': form, 'product': product})


def product_detail_view(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    reviews = Review.objects.filter(product=product)
    return render(request, 'product_detail.html', {
        'product': product, 
        'reviews': reviews
    })

@login_required(login_url='login')
def purchase_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    profile = Profile.objects.get(user=request.user)

    if profile.balance >= product.price:
        profile.balance -= product.price
        profile.save()
        Transaction.objects.create(sender=profile, recipient=None, amount=product.price, transaction_type='purchase')
        return redirect('product_list')
    else:
        return redirect('product_detail', product_id=product_id)
    
@login_required(login_url='login')
def add_product_view(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'add_product.html', {'form': form})