# script for genning SSLs, pub and priv keys along with handleing remote token authencation
import datetime

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes

import time


class TokenGen:
    def __init__(self, key, path):
        self.key = key
        self.path = path

    def genPriv(self):
        # Generate our key
        self.key = rsa.generate_private_key(

            public_exponent=65537,

            key_size=2048,
        )
        # Write our key to disk for safe keeping
        with open(self.path, "wb") as f:  # path = path/to/store/key.pem
            f.write(self.key.private_bytes(

                encoding=serialization.Encoding.PEM,

                format=serialization.PrivateFormat.TraditionalOpenSSL,

                encryption_algorithm=serialization.BestAvailableEncryption(b"passphrase"),
            ))

    def csRequest(self):
        # Generate a CSR
        csr = x509.CertificateSigningRequestBuilder().subject_name(x509.Name([
            # Provide various details about who we are.
            x509.NameAttribute(NameOID.COUNTRY_NAME, u"US"),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"California"),
            x509.NameAttribute(NameOID.LOCALITY_NAME, u"San Francisco"),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"My Company"),
            x509.NameAttribute(NameOID.COMMON_NAME, u"mysite.com"),
        ])).add_extension(

            x509.SubjectAlternativeName([
                # Describe what sites we want this certificate for.
                x509.DNSName(u"mysite.com"),
            ]),

            critical=False,
            # Sign the CSR with our private key.
        ).sign(self.key, hashes.SHA256())
        # Write our CSR out to disk.
        with open(self.path, "wb") as f:  # path = path/to/store/csr.pem
            f.write(csr.public_bytes(serialization.Encoding.PEM))

    def createSSL(self):
        # Various details about who we are. For a self-signed certificate the
        # subject and issuer are always the same.
        subject = issuer = x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, u"US"),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"California"),
            x509.NameAttribute(NameOID.LOCALITY_NAME, u"San Francisco"),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"My Company"),
            x509.NameAttribute(NameOID.COMMON_NAME, u"mysite.com"),
        ])
        cert = x509.CertificateBuilder().subject_name(

            subject
        ).issuer_name(

            issuer
        ).public_key(

            self.key.public_key()
        ).serial_number(

            x509.random_serial_number()
        ).not_valid_before(

            datetime.datetime.utcnow()
        ).not_valid_after(
            # Our certificate will be valid for 10 days
            datetime.datetime.utcnow() + datetime.timedelta(days=10)
        ).add_extension(

            x509.SubjectAlternativeName([x509.DNSName(u"localhost")]),

            critical=False,
            # Sign our certificate with our private key
        ).sign(self.key, hashes.SHA256())
        # Write our certificate out to disk.
        with open(self.path, "wb") as f:  # path = path/to/store/certificate.pem
            f.write(cert.public_bytes(serialization.Encoding.PEM))
