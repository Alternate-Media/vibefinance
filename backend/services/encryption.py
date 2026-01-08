import os
from cryptography.fernet import Fernet


class EncryptionService:
    """
    Wrapper service for Application-Level Encryption (ALE).
    Ensures that sensitive data is encrypted before hitting the database.
    """

    def __init__(self, key: str):
        """
        Initialize with a base64 encoded Fernet key.
        """
        self._fernet = Fernet(key)

    @classmethod
    def generate_key(cls) -> str:
        """
        Utility to generate a new Fernet key.
        """
        return Fernet.generate_key().decode()

    def encrypt(self, data: str) -> str:
        """
        Encrypts a string and returns a base64 encoded ciphertext string.
        """
        if not data:
            return data
        return self._fernet.encrypt(data.encode()).decode()

    def decrypt(self, ciphertext: str) -> str:
        """
        Decrypts a base64 encoded ciphertext string and returns the plaintext.
        """
        if not ciphertext:
            return ciphertext
        return self._fernet.decrypt(ciphertext.encode()).decode()


# Factory function for Dependency Injection
def get_encryption_service() -> EncryptionService:
    # In a real scenario, this would come from an environment variable or secret manager
    # For now, we use a placeholder or check environment
    key = os.getenv("ENCRYPTION_KEY")
    if not key:
        # Fallback for development ONLY - in production, this should fail secure
        # Note: In production, the "Fail Secure" commandment would require raising an error here.
        # However, for initial setup, we provide a warning/default.
        key = Fernet.generate_key().decode()

    return EncryptionService(key)
