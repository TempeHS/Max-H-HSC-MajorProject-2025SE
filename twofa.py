import pyotp
import base64
import qrcode
from io import BytesIO

def generate_totp_secret():
    return pyotp.random_base32()

def get_totp_uri(username, secret):
    return pyotp.totp.TOTP(secret).provisioning_uri(name=username, issuer_name="WeatherSpoon")

def generate_qr_code(uri):
    img = qrcode.make(uri)
    buf = BytesIO()
    img.save(buf, format='PNG')
    return base64.b64encode(buf.getvalue()).decode('utf-8')

def verify_totp(secret, token):
    totp = pyotp.TOTP(secret)
    return totp.verify(token)