"""
Qmoosa Bot - x402 Agentic Bazaar Marketplace
Decentralized service discovery and micro-service trading between autonomous agents.
"""

from typing import Dict, List, Any, Optional
import time
import uuid
import logging
from bazaar_x402.protocol import X402Protocol

logger = logging.getLogger("x402Marketplace")

class AgentServiceListing:
    def __init__(self, provider_id: str, service_name: str, cost_microunits: int, token: str = "QALGO", sla_seconds: int = 15):
        self.service_id = f"srv_{uuid.uuid4().hex[:8]}"
        self.provider_id = provider_id
        self.service_name = service_name
        self.cost_microunits = cost_microunits
        self.token = token
        self.sla_seconds = sla_seconds
        self.rating = 5.0
        self.total_completed = 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "service_id": self.service_id,
            "provider_id": self.provider_id,
            "service_name": self.service_name,
            "cost_microunits": self.cost_microunits,
            "token": self.token,
            "sla_seconds": self.sla_seconds,
            "rating": self.rating,
            "total_completed": self.total_completed,
        }


class X402BazaarMarketplace:
    """
    Peer-to-peer bazaar where specialized agents advertise and buy capabilities.
    """

    def __init__(self, protocol: Optional[X402Protocol] = None):
        self.protocol = protocol or X402Protocol()
        self.registry: Dict[str, AgentServiceListing] = {}
        self.order_history: List[Dict[str, Any]] = []
        self._seed_default_listings()

    def _seed_default_listings(self):
        defaults = [
            ("agent_solver_01", "CAPTCHA_BYPASS_AI", 2000, "QALGO", 5),
            ("agent_verifier_02", "EMAIL_AND_PHONE_VERIFIER", 5000, "QALGO", 10),
            ("agent_osint_03", "DEEP_INSTAGRAM_LEAD_EXTRACTOR", 15000, "QALGO", 30),
            ("agent_pqc_04", "QUANTUM_RESISTANT_NOTARIZATION", 8000, "QALGO", 3),
        ]
        for pid, name, cost, token, sla in defaults:
            listing = AgentServiceListing(pid, name, cost, token, sla)
            self.registry[listing.service_id] = listing

    def list_services(self) -> List[Dict[str, Any]]:
        return [listing.to_dict() for listing in self.registry.values()]

    def request_service_order(self, buyer_agent_id: str, service_id: str) -> Dict[str, Any]:
        """
        Buyer agent initiates procurement. Generates x402 payment challenge.
        """
        if service_id not in self.registry:
            return {"error": "Service not found in Bazaar registry"}

        srv = self.registry[service_id]
        receiver_wallet = f"WALLET_{srv.provider_id.upper()}_ALGO_MAINNET"
        challenge_headers = self.protocol.create_payment_challenge(
            service_name=srv.service_name,
            amount_microunits=srv.cost_microunits,
            receiver_address=receiver_wallet,
            token=srv.token
        )

        order_id = f"ord_{uuid.uuid4().hex[:8]}"
        order = {
            "order_id": order_id,
            "buyer_id": buyer_agent_id,
            "service_id": service_id,
            "service_name": srv.service_name,
            "cost_microunits": srv.cost_microunits,
            "status": "PAYMENT_REQUIRED",
            "x402_challenge": challenge_headers,
            "created_at": time.time(),
        }
        self.order_history.append(order)
        logger.info(f"[Bazaar] Order '{order_id}' created for buyer '{buyer_agent_id}'")
        return order

    def settle_order(self, order_id: str, payment_proof_txid: str) -> Dict[str, Any]:
        """
        Settles order upon valid payment proof, delivering output to buyer agent.
        """
        for ord_item in self.order_history:
            if ord_item["order_id"] == order_id:
                srv = self.registry[ord_item["service_id"]]
                v_res = self.protocol.verify_payment_proof(
                    payment_proof_txid=payment_proof_txid,
                    challenge_header=ord_item["x402_challenge"]["X-402-Challenge"],
                    expected_amount=ord_item["cost_microunits"],
                    expected_receiver=ord_item["x402_challenge"]["X-402-Receiver"]
                )

                if v_res.get("valid"):
                    ord_item["status"] = "SETTLED"
                    ord_item["settled_at"] = time.time()
                    srv.total_completed += 1
                    logger.info(f"[Bazaar] Order '{order_id}' SETTLED. Delivering service output.")
                    return {
                        "success": True,
                        "order_id": order_id,
                        "status": "DELIVERED",
                        "service_output": f"Executed capability '{ord_item['service_name']}' successfully for consumer.",
                        "payment_verification": v_res,
                    }
                else:
                    return {"success": False, "error": v_res.get("error")}

        return {"success": False, "error": "Order ID not found"}
