from django.contrib.auth.tokens import PasswordResetTokenGenerator


class EmailTokenGenerator(PasswordResetTokenGenerator):
    """
    Generates single-use, time-limited tokens for email verification links.

    Reuses Django's PasswordResetTokenGenerator machinery but mixes in
    `is_active` and `email` into the hash so that:
      - a token becomes invalid if the user's email changes after it was sent
      - a token can't be reused once the account has already been verified
    """

    def _make_hash_value(self, user, timestamp):
        return str(user.pk) + str(timestamp) + str(user.email) + str(user.is_active)


# Singleton instance imported wherever we need to create/check a
# verification token (see accounts/views.py).
email_token = EmailTokenGenerator()
