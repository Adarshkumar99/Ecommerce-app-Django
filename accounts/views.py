from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.utils.http import url_has_allowed_host_and_scheme
from .forms import UserRegistrationForm, UserLoginForm
from django.contrib import messages
from cart.helper.cart_util import merge_cart


def UserRegister(request):
  if request.method == 'POST':
    form = UserRegistrationForm(request.POST)
    if form.is_valid():
      form.save()
      username = form.cleaned_data.get('username')
      password = form.cleaned_data.get('password1')
      user = authenticate(username=username, password=password)
      if user is not None:
        login(request, user)
        merge_cart(request)
        messages.success(request, f'Account Created Successfully!', extra_tags='success')
        next_url = request.POST.get('next') or request.GET.get('next')

        if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
          return redirect(next_url)
        
        return redirect('home')
    else:
      error_list = []
      for field, errors in form.errors.items():
        for error in errors:
          error_list.append(f'• {field}: {error}')
    
      messages.error(request, '\n'.join(error_list), extra_tags='danger')
      return redirect('register')
  else:
    form = UserRegistrationForm()
  return render(request, 'register.html', {'form': form})



def UserLogin(request):
  if request.method == 'POST':
    form = UserLoginForm(request.POST)
    if form.is_valid():
      username = form.cleaned_data.get('username')
      password = form.cleaned_data.get('password')
      user = authenticate(username=username, password=password)
      if user is not None:
        login(request, user)
        # here we merge the cart after login to ensure that any items added to the cart while the user was not logged in are preserved and associated with their account.
        # Using session to merge the cart to db after user login
        merge_cart(request)
        messages.success(request, f'Logged in successfully!', extra_tags='success')
        next_url = request.POST.get('next') or request.GET.get('next')

        if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
          return redirect(next_url)
        
        return redirect('home')
      else:
        error_list = []
        for field, errors in form.errors.items():
          for error in errors:
            error_list.append(f'• {field}: {error}')
    
        messages.error(request, '\n'.join(error_list), extra_tags='danger')
  else:
    form = UserLoginForm()
  return render(request, 'login.html', {'form': form})


def UserLogout(request):
  logout(request)
  messages.info(request, 'you have been logged out')
  return redirect('home') 