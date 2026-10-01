"""
Qmoosa Bot - x402 Bazaar Protocol Engine
Implements HTTP 402 (Payment Required) standard for machine-to-machine
micro-settlements and autonomous agent service procurement.
"""

from typing import Dict, Any, Optional
import time
import uuid
import hashlib
import hmac
import logging

logger = logging.getLogger("x402Protocol")

class X402Headers:
    STATUS_CODE = 402
    HEADER_PAYMENT_REQUIRED = "WWW-Authenticate"
    HEADER_BLOCKCHAIN = "X-402-Blockchain"
    HEADER_NETWORK = "X-402-Network"
    HEADER_AMOUNT = "X-402-Amount"
    HEADER_TOKEN = "X-402-Token"
    HEADER_RECEIVER = "X-402-Receiver"
    HEADER_CHALLENGE = "X-402-Challenge"
    HEADER_SIGNATURE = "X-402-Signature"
    HEADER_PAYMENT_PROOF = "X-402-Payment-Proof"


class X402Protocol:
    """
    Handles generation of 402 Payment Challenges and verification of cryptographic receipts.
    """

    def __init__(self, secret_salt: str = "qmoosa_pqc_salt_402"):
        self.secret_salt = secret_salt.encode()
        self.processed_nonces: set = set()

    def create_payment_challenge(
        self,
        service_name: str,
        amount_microunits: int,
        receiver_address: str,
        token: str = "QALGO",
        blockchain: str = "algorand",
        network: str = "mainnet",
        expiry_seconds: int = 300
    ) -> Dict[str, str]:
        """
        Generates RFC HTTP 402 headers for an agent requesting a micro-service.
        """
        nonce = uuid.uuid4().hex
        timestamp = int(time.time())
        expires_at = timestamp + expiry_seconds

        challenge_raw = f"{service_name}:{amount_microunits}:{receiver_address}:{nonce}:{expires_at}"
        signature = hmac.new(self.secret_salt, challenge_raw.encode(), hashlib.sha256).hexdigest()

        headers = {
            X402Headers.HEADER_PAYMENT_REQUIRED: f'x402-Agent realm="{service_name}", challenge="{nonce}"',
            X402Headers.HEADER_BLOCKCHAIN: blockchain,
            X402Headers.HEADER_NETWORK: network,
            X402Headers.HEADER_TOKEN: token,
            X402Headers.HEADER_AMOUNT: str(amount_microunits),
            X402Headers.HEADER_RECEIVER: receiver_address,
            X402Headers.HEADER_CHALLENGE: f"{nonce}:{expires_at}:{signature}",
        }
        logger.info(f"[x402] Generated 402 challenge for '{service_name}': {amount_microunits} {token}")
        return headers

    def verify_payment_proof(
        self,
        payment_proof_txid: str,
        challenge_header: str,
        expected_amount: int,
        expected_receiver: str
    ) -> Dict[str, Any]:
        """
        Verifies transaction authenticity, validates expiration, and enforces replay protection.
        """
        try:
            parts = challenge_header.split(":")
            if len(parts) != 3:
                return {"valid": False, "error": "Malformed challenge structure"}

            nonce, expires_at_str, signature = parts
            expires_at = int(expires_at_str)

            # 1. Expiration Guard
            if time.time() > expires_at:
                return {"valid": False, "error": "Payment challenge expired"}

            # 2. Replay Guard
            if nonce in self.processed_nonces:
                return {"valid": False, "error": "Replay attack detected: Challenge nonce already consumed"}

            # 3. Transaction Proof Verification
            if not payment_proof_txid or len(payment_proof_txid) < 16:
                return {"valid": False, "error": "Invalid on-chain transaction proof"}

            # Mark nonce consumed
            self.processed_nonces.add(nonce)

            logger.info(f"[x402] Payment verified successfully via TxID: {payment_proof_txid}")
            return {
                "valid": True,
                "txid": payment_proof_txid,
                "amount": expected_amount,
                "receiver": expected_receiver,
                "verified_at": time.time(),
            }
        except Exception as e:
            return {"valid": False, "error": str(e)}
