import six
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth.tokens import default_token_generator

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
                default_token_generator.make_token(user) + six.text_type(timestamp) +
                six.text_type(user.profile.signup_confirmation)
        )


account_activation_token = AccountActivationTokenGenerator()
