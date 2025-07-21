from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type
class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            text_type(user.email) + text_type(timestamp) +
            text_type(user.is_active)
            # six.text_type(user.email) + six.text_type(timestamp)
        )
account_activation_token = TokenGenerator() 