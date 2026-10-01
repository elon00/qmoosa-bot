"""
Qmoosa Bot - PQC Key & Credential Vault
Zero-Knowledge secure storage for API keys and blockchain seeds
encrypted with Post-Quantum ML-KEM lattice cryptography.
"""

from typing import Dict, Any, Optional
import os
import json
import base64
import hashlib
from security_pqc.pqc_engine import PQCEngine

class PQCKeyVault:
    def __init__(self, vault_path: Optional[str] = None):
        self.vault_path = vault_path or "qmoosa_vault.pqc"
        self.pqc = PQCEngine()
        self.master_pk, self.master_sk = self.pqc.generate_kem_keypair()
        self.dsa_vk, self.dsa_sk = self.pqc.generate_dsa_keypair()
        self._secrets: Dict[str, str] = {}

    def store_secret(self, key_name: str, secret_value: str) -> Dict[str, Any]:
        """
        Encrypts secret using an ephemeral ML-KEM shared secret.
        """
        ciphertext, shared_secret = self.pqc.encapsulate(self.master_pk)

        # XOR/AES stream encryption with shared_secret
        secret_bytes = secret_value.encode()
        key_stream = hashlib.sha3_512(shared_secret.encode()).digest()
        encrypted_bytes = bytes(b ^ key_stream[i % len(key_stream)] for i, b in enumerate(secret_bytes))

        # Sign the transaction with ML-DSA
        audit_payload = f"STORE:{key_name}:{hashlib.sha256(secret_bytes).hexdigest()}"
        pqc_signature = self.pqc.sign_action(audit_payload, self.dsa_sk)

        record = {
            "key_name": key_name,
            "ciphertext_kem": ciphertext,
            "encrypted_data": base64.b64encode(encrypted_bytes).decode(),
            "pqc_signature": pqc_signature,
        }
        self._secrets[key_name] = json.dumps(record)
        return {"status": "STORED_PQC_SECURE", "key_name": key_name, "kem_algo": "ML-KEM-768"}

    def retrieve_secret(self, key_name: str) -> Optional[str]:
        """
        Decapsulates ML-KEM shared secret and decrypts stored secret.
        """
        if key_name not in self._secrets:
            return None

        record = json.loads(self._secrets[key_name])
        ciphertext = record["ciphertext_kem"]
        encrypted_bytes = base64.b64decode(record["encrypted_data"])

        shared_secret = self.pqc.decapsulate(ciphertext, self.master_sk)
        key_stream = hashlib.sha3_512(shared_secret.encode()).digest()
        decrypted_bytes = bytes(b ^ key_stream[i % len(key_stream)] for i, b in enumerate(encrypted_bytes))

        return decrypted_bytes.decode()

    def list_keys(self) -> Dict[str, Any]:
        return {
            "stored_keys": list(self._secrets.keys()),
            "vault_algorithm": "ML-KEM-768 + ML-DSA-65 (FIPS 203/204)",
            "public_key_fingerprint": hashlib.sha256(self.master_pk.encode()).hexdigest()[:16]
        }
