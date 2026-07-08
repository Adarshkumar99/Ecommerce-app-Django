from django.conf import settings
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
  """
  Handles new user sign-up.

  On a valid POST:
    1. Creates the User via UserRegistrationForm.
    2. Generates a signed, time-limited email verification link and
       emails it to the user (failure to send email does not block
       registration, it just shows a warning message).
    3. Logs the user in immediately (so they don't have to log in twice)
       and merges any items they added to their guest/session cart.
    4. Redirects to `next` if present and safe, otherwise to `home`.
  """
  if request.method == 'POST':
    form = UserRegistrationForm(request.POST)
    if form.is_valid():

      # Persist the new user record.
      user = form.save()

      # Build a signed uid + token pair that uniquely (and securely)
      # identifies this user for the verification link. The token
      # expires and can't be reused once the account is verified.
      uid = urlsafe_base64_encode(force_bytes(user.pk))
      token = email_token.make_token(user)

      path = reverse('verify_email', kwargs={'uidb64': uid, 'token': token})
      verification_link = request.build_absolute_uri(path)

      html_message = render_to_string('verification_email.html', {
        'verification_link': verification_link,
      })

      # Send the verification email. Registration should still succeed
      # even if the email provider is down, so we swallow the error and
      # just warn the user instead of raising a 500.
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

      # Auto-login right after registration (same credentials just submitted).
      username = form.cleaned_data.get('username')
      password = form.cleaned_data.get('password1')
      user = authenticate(username=username, password=password)

      if user is not None:
        login(request, user)
        # Move any items added to the cart before the user had an
        # account (stored in the session) onto their new user cart.
        merge_cart(request)

        messages.success(request, 'Account created! Please verify your email.', extra_tags='success')

        # Respect a `next` redirect param (e.g. "continue to checkout"),
        # but only if it points to a safe, same-host URL to avoid
        # open-redirect vulnerabilities.
        next_url = request.POST.get('next') or request.GET.get('next')
        if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
          return redirect(next_url)

        return redirect('home')

    else:
      # Flatten form errors into a single readable message list.
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
  """
  Confirms a user's email address from the link sent in UserRegister().

  Decodes the uid, looks up the matching user, and checks the token is
  valid (not expired / not tampered with) before flipping
  `profile.is_verified` to True.
  """
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
  """
  Handles user login. On success, merges any guest/session cart items
  into the user's persistent cart and honours a safe `next` redirect,
  same as UserRegister().
  """
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
  """Logs the current user out and redirects to the home page."""
  logout(request)
  messages.info(request, 'You have been logged out', extra_tags="success")
  return redirect('home')
