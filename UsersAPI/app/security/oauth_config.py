from authlib.integrations.starlette_client import OAuth
from ..config import conf

oauth = OAuth()

oauth.register(
    name='google',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_id=conf.GOOGLE_CLIENT_ID,
    client_secret=conf.GOOGLE_CLIENT_SECRET,
    client_kwargs={'scope': 'openid email profile'}
)