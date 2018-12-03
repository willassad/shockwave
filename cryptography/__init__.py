"""
Use encryption.py as a module.
__init__.py to set cryptography
as a package.
"""

"""
cryptography is a package that allows
for passwords to be saved securely
when executing the main script.
Encryption tools such as the sha256
hash function and others are managed 
by the cryptography package.
"""

__all__ = ['passwordtools',
           'assets',
           'wordEncrypt',
           'wordDecrypt',
           'sha256',
           'getFilePath'
           ]
