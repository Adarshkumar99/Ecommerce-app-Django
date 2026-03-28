from django.contrib.auth.tokens import PasswordResetTokenGenerator

class EmailTokenGenerator(PasswordResetTokenGenerator):
  def _make_hash_value(self, user, timestamp):
    return str(user.pk) + str(timestamp) + str(user.email) + str(user.is_active)

email_token = EmailTokenGenerator()