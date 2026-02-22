"""
生成自签名SSL证书
"""
import os
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import datetime

cert_dir = os.path.join(os.path.dirname(__file__), 'ssl')
os.makedirs(cert_dir, exist_ok=True)

key_path = os.path.join(cert_dir, 'key.pem')
cert_path = os.path.join(cert_dir, 'cert.pem')

key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
)

subject = issuer = x509.Name([
    x509.NameAttribute(NameOID.COUNTRY_NAME, "CN"),
    x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "Beijing"),
    x509.NameAttribute(NameOID.LOCALITY_NAME, "Beijing"),
    x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Fund Valuation System"),
    x509.NameAttribute(NameOID.COMMON_NAME, "localhost"),
])

cert = x509.CertificateBuilder().subject_name(
    subject
).issuer_name(
    issuer
).public_key(
    key.public_key()
).serial_number(
    x509.random_serial_number()
).not_valid_before(
    datetime.datetime.utcnow()
).not_valid_after(
    datetime.datetime.utcnow() + datetime.timedelta(days=365)
).add_extension(
    x509.SubjectAlternativeName([
        x509.DNSName("localhost"),
        x509.DNSName("127.0.0.1"),
    ]),
    critical=False,
).sign(key, hashes.SHA256())

with open(key_path, "wb") as f:
    f.write(key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption(),
    ))

with open(cert_path, "wb") as f:
    f.write(cert.public_bytes(serialization.Encoding.PEM))

print("SSL证书生成成功!")
print(f"证书文件: {cert_path}")
print(f"私钥文件: {key_path}")
