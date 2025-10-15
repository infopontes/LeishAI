from slowapi import Limiter
from slowapi.util import get_remote_address

# The limiter's creation now lives here, in a central and independent location.
limiter = Limiter(key_func=get_remote_address)
