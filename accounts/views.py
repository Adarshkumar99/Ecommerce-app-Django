from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.utils.http import url_has_allowed_host_and_scheme
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse

from .forms import UserRegistrationForm, UserLoginForm
from .tokens import email_token
from cart.helper.cart_util import merge_cart


def UserRegister(request):
  if request.method == 'POST':
    form = UserRegistrationForm(request.POST)
    if form.is_valid():
            
      #save user
      user = form.save()

      # generate email verification token
      uid = urlsafe_base64_encode(force_bytes(user.pk))
      token = email_token.make_token(user)

      path = reverse('verify_email', kwargs={'uidb64': uid, 'token': token})
      verification_link = request.build_absolute_uri(path)

      html_message = render_to_string('verification_email.html', {
        'verification_link': verification_link,
      })

      # send email
      try:
        send_mail(
          subject="Verify your account",
          message=f"Click this link to verify your account: {verification_link}",
          from_email=settings.DEFAULT_FROM_EMAIL,
          recipient_list=[user.email],
          html_message=html_message,
          fail_silently=False,
        )
      except Exception as e:
        messages.warning(request, 'Account created but verification email not sent. Contact support.', extra_tags='warning')

      # login user (same flow)
      username = form.cleaned_data.get('username')
      password = form.cleaned_data.get('password1')
      user = authenticate(username=username, password=password)

      if user is not None:
        login(request, user)
        merge_cart(request)

        messages.success(request, 'Account created! Please verify your email.', extra_tags='success')

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


def verify_email(request, uidb64, token):
  try:
    uid = force_str(urlsafe_base64_decode(uidb64))
    user = User.objects.get(pk=uid)
  except:
    user = None

  if user and email_token.check_token(user, token):
    user.profile.is_verified = True
    user.profile.save()
    messages.success(request, 'Account verified successfully!', extra_tags='success')
    return redirect('home')

  return HttpResponse("Invalid or expired link")


def UserLogin(request):
  if request.method == 'POST':
    form = UserLoginForm(request.POST)
    if form.is_valid():
      username = form.cleaned_data.get('username')
      password = form.cleaned_data.get('password')
      user = authenticate(username=username, password=password)

      if user is not None:
        login(request, user)
        merge_cart(request)

        messages.success(request, 'Logged in successfully!', extra_tags='success')

        next_url = request.POST.get('next') or request.GET.get('next')
        if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
          return redirect(next_url)

        return redirect('home')

      else:
        messages.error(request, 'Invalid username or password', extra_tags='danger')

  else:
    form = UserLoginForm()

  return render(request, 'login.html', {'form': form})


def UserLogout(request):
  logout(request)
  messages.info(request, 'You have been logged out', extra_tags="success")
  return redirect('home')