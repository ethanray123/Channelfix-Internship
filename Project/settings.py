from .local_settings import *

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'

FIXTURE_DIRS = (
    '/fixtures/',
    '/stream/fixtures/',
)

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, "media")
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'
