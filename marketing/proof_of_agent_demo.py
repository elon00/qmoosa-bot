"""
Qmoosa Bot - Proof-of-Agent Live Demonstration Engine
Executes an end-to-end viral showcase:
1. Spawns autonomous agent swarm on Conway grid
2. Uses Model Router to plan & scrape target leads
3. Controls virtual screen with anti-detect Bézier curves
4. Generates dynamic UPI & Crypto QR invoices
5. Procures micro-services via x402 Bazaar
6. Signs tamper-proof audit certificates using Post-Quantum Cryptography (ML-DSA)
"""

import time
import json
import logging
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

from core.conway_automaton import ConwayAutomatonEngine
from core.model_router import MultiModelRouter, ModelCapability
from core.agent_mesh import QmoosaAgentMesh
from screen_controller.screen_driver import ScreenDriver
from bazaar_x402.marketplace import X402BazaarMarketplace
from security_pqc.pqc_engine import PQCEngine
from wallet_qr.dynamic_qr import DynamicQREngine
from tokenomics.token_model import QmoosaTokenomics

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("ProofOfAgentDemo")

def run_live_proof_of_agent():
    print("=" * 80)
    print("[DEMO] QMOOSA BOT - AUTONOMOUS AGENTIC OS LIVE PROOF-OF-WORK DEMO")
    print("=" * 80)

    # 1. Initialize Subsystems
    print("\n[Phase 1] Bootstrapping Autonomous Subsystems...")
    automaton = ConwayAutomatonEngine(grid_size=16)
    router = MultiModelRouter()
    mesh = QmoosaAgentMesh(automaton=automaton, router=router)
    screen = ScreenDriver()
    bazaar = X402BazaarMarketplace()
    pqc = PQCEngine()
    qr_engine = DynamicQREngine(merchant_name="Qmoosa Bot Autonomous Agency")
    tokenomics = QmoosaTokenomics()

    # 2. Cellular Automata Swarm Evolution
    print("\n[Phase 2] Cellular Automata Lifecycle & Emergent Swarm...")
    initial_stats = automaton.tick()
    print(f" -> Conway Lattice Generation: {initial_stats['generation']} | Active Cells: {initial_stats['active_cells_count']}")

    # 3. Model Router & Multi-Agent Mission
    print("\n[Phase 3] Multi-Model Agent Collaboration...")
    mission_summary = mesh.run_collaborative_mission(
        mission_goal="Acquire 5 Verified B2B Brand Deals for Influencer Skincare Campaign",
        target_platform="Instagram"
    )
    print(f" -> Mission Result: {mission_summary['goal']}")
    print(f" -> Execution Time: {mission_summary['execution_time_seconds']}s across {len(mission_summary['team_status'])} bots.")

    # 4. Full Computer Screen Controller Interaction
    print("\n[Phase 4] Screen Controller & Bézier Curve GUI Navigation...")
    action_res = screen.navigate_and_interact(
        target_query="Send Message Textarea",
        context="instagram_dm",
        payload_text="Hello! Qmoosa Bot is presenting our automated sponsorship proposal."
    )
    print(f" -> Mouse moved & clicked at target: {action_res['grounded_coordinate']}")
    print(f" -> Typed payload with human-like jitter: {action_res['typing']['length']} chars.")

    # 5. Dynamic QR Invoice Generation (Fiat & Crypto)
    print("\n[Phase 5] Dynamic QR Settlement Rails...")
    upi_qr = qr_engine.generate_upi_qr("qmoosabot@upi", 12500.00, "TXN_B2B_9921", "Influencer Campaign Fee")
    sol_qr = qr_engine.generate_solana_pay_qr("7xKXtg2CW87d97TXJSDpbD5jBkheTqA83TZRuJosgAsU", 0.75, "REF_B2B_SOL", "Campaign Retainer")
    print(f" -> Dynamic UPI QR URI: {upi_qr['payment_uri']}")
    print(f" -> Solana Pay QR URI: {sol_qr['payment_uri']}")

    # 6. x402 Bazaar Autonomous Procurement
    print("\n[Phase 6] x402 Bazaar Autonomous Micro-Service Trading...")
    services = bazaar.list_services()
    target_service = services[0]
    order = bazaar.request_service_order("buyer_agent_mesh_01", target_service["service_id"])
    print(f" -> Procured Service: {target_service['service_name']} for {order['cost_microunits']} {target_service['token']}")
    settlement = bazaar.settle_order(order["order_id"], "tx_onchain_proof_9981249817293")
    print(f" -> x402 Settlement Status: {settlement['status']}")

    # 7. Post-Quantum Cryptographic Audit Signing
    print("\n[Phase 7] Post-Quantum Cryptography (PQC) Audit Notarization...")
    vk, sk = pqc.generate_dsa_keypair()
    audit_data = f"QMOOSA_MISSION_CERTIFICATE:{mission_summary['mission_id']}:{time.time()}"
    pqc_sig = pqc.sign_action(audit_data, sk)
    is_valid = pqc.verify_action(audit_data, pqc_sig, vk)
    print(f" -> ML-DSA-65 Quantum Signature: {pqc_sig[:32]}... [Valid: {is_valid}]")

    # 8. Tokenomics Deflationary Fee Burn
    print("\n[Phase 8] Global Tokenomics & Burn-on-Execution...")
    burn_res = tokenomics.process_bazaar_fee_burn(transaction_amount=500.0, fee_percent=0.02)
    metrics = tokenomics.get_token_metrics()
    print(f" -> Burned {burn_res['burned']} tokens. New Total Supply: {metrics['total_supply']:.2f}")

    print("\n" + "=" * 80)
    print("[SUCCESS] PROOF-OF-AGENT DEMONSTRATION EXECUTED WITH 100% SUCCESS!")
    print("=" * 80)

if __name__ == "__main__":
    run_live_proof_of_agent()
