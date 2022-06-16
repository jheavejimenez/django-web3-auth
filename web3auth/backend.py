from django.contrib.auth import get_user_model, backends

from web3auth.settings import app_settings
from web3auth.utils import recover_to_addr


class Web3Backend(backends.ModelBackend):
    def authenticate(self, request, address=None, token=None, signature=None):
        # get user model
        User = get_user_model()
        if address != recover_to_addr(token, signature):
            return None
        # get address field for the user model
        address_field = app_settings.WEB3AUTH_USER_ADDRESS_FIELD
        kwargs = {
            f"{address_field}__iexact": address
        }
        return User.objects.filter(**kwargs).first()
