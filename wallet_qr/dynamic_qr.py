"""
Qmoosa Bot - Dynamic QR Code & Settlement Engine
Generates dynamic QR codes for instant Fiat (UPI, SEPA) and Crypto (Solana, Algorand, Lightning)
facilitating seamless human-to-agent and agent-to-agent payments.
"""

from typing import Dict, Any, Optional
import urllib.parse
import base64
import json
import logging

logger = logging.getLogger("DynamicQR")

class PaymentRail:
    UPI = "UPI"
    SOLANA_PAY = "SOLANA_PAY"
    ALGORAND = "ALGORAND"
    LIGHTNING = "LIGHTNING"
    STRIPE_FIAT = "STRIPE_FIAT"


class DynamicQREngine:
    """
    Renders standardized payment URIs and embedded QR representations
    for global multi-currency transactions.
    """

    def __init__(self, merchant_name: str = "Qmoosa Autonomous Bot"):
        self.merchant_name = merchant_name

    def generate_upi_qr(self, vpa: str, amount_inr: float, transaction_ref: str, note: str = "Agent Bounty") -> Dict[str, Any]:
        """
        Generates NPCI-compliant UPI Dynamic QR code URI.
        """
        params = {
            "pa": vpa,
            "pn": self.merchant_name,
            "mc": "8931",
            "tr": transaction_ref,
            "tn": note,
            "am": f"{amount_inr:.2f}",
            "cu": "INR",
        }
        uri = f"upi://pay?{urllib.parse.urlencode(params)}"
        return self._package_qr_response(PaymentRail.UPI, uri, amount_inr, "INR", transaction_ref)

    def generate_solana_pay_qr(self, recipient_pubkey: str, amount_sol: float, reference: str, memo: str = "Qmoosa B2B") -> Dict[str, Any]:
        """
        Generates Solana Pay specification URI.
        """
        params = {
            "amount": f"{amount_sol:.4f}",
            "label": self.merchant_name,
            "message": memo,
            "reference": reference,
        }
        uri = f"solana:{recipient_pubkey}?{urllib.parse.urlencode(params)}"
        return self._package_qr_response(PaymentRail.SOLANA_PAY, uri, amount_sol, "SOL", reference)

    def generate_algorand_qr(self, recipient_address: str, amount_microalgo: int, note: str = "x402_settlement") -> Dict[str, Any]:
        """
        Generates Algorand standard deep-link URI (Pera, Defly).
        """
        encoded_note = urllib.parse.quote(note)
        uri = f"algorand://{recipient_address}?amount={amount_microalgo}&note={encoded_note}"
        return self._package_qr_response(PaymentRail.ALGORAND, uri, amount_microalgo / 1e6, "ALGO", note)

    def generate_lightning_qr(self, bolt11_invoice: str) -> Dict[str, Any]:
        """
        Generates Bitcoin Lightning Network URI.
        """
        uri = f"lightning:{bolt11_invoice}"
        return self._package_qr_response(PaymentRail.LIGHTNING, uri, 0.0, "BTC_SATS", "ln_invoice")

    def _package_qr_response(self, rail: str, uri: str, amount: float, currency: str, ref: str) -> Dict[str, Any]:
        """
        Creates SVG matrix and Base64 representation suitable for Flutter/Web.
        """
        # Lightweight SVG QR placeholder matrix for zero-dependency portability
        svg_qr = f'<svg xmlns="http://www.w3.org/2000/svg" width="220" height="220" viewBox="0 0 220 220"><rect width="220" height="220" fill="#0b0f19"/><rect x="20" y="20" width="40" height="40" fill="#00ff88"/><rect x="160" y="20" width="40" height="40" fill="#00ff88"/><rect x="20" y="160" width="40" height="40" fill="#00ff88"/><text x="110" y="115" font-family="monospace" font-size="12" fill="#ffffff" text-anchor="middle">{rail}</text><text x="110" y="135" font-family="monospace" font-size="10" fill="#00f0ff" text-anchor="middle">{amount} {currency}</text></svg>'
        svg_b64 = base64.b64encode(svg_qr.encode()).decode()

        logger.info(f"[DynamicQR] Generated {rail} QR: {amount} {currency} [Ref: {ref}]")
        return {
            "rail": rail,
            "payment_uri": uri,
            "amount": amount,
            "currency": currency,
            "reference": ref,
            "svg_markup": svg_qr,
            "svg_base64": f"data:image/svg+xml;base64,{svg_b64}",
        }
