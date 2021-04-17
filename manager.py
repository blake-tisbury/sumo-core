# fuck you - to blake at 8 am
import cryptography
import cryptUI
import sumoGame
from cryptography.fernet import Fernet, InvalidToken

cryptUI.main()


def genInitKey(self):  # Makes the encryption key and writes it to a file
    self.key_make = Fernet.generate_key()
    key_file = open('key.key', 'wb')
    key_file.write(self.key_make)
    key_file.close()
    key_file = open('key.key', 'rb')
    self.key = key_file.read()
    key_file.close()

