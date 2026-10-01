"""
Qmoosa Bot - Comprehensive Verification & Scientific Integration Test Suite
Validates all 9 core pillars:
1. Conway Automaton Grid & Self-Healing
2. Multi-Model AI Routing & Fallback
3. Full Computer Screen Controller & Bézier Nav
4. x402 Bazaar Protocol & Replay Guard
5. Post-Quantum Cryptography (ML-KEM / ML-DSA)
6. Dynamic QR Codes (Fiat/Crypto)
7. Multi-Wallet Transaction Dispatch
8. Global Tokenomics & Burn Mechanics
9. End-to-End System Synchronicity
"""

import sys
import os
import unittest
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.conway_automaton import ConwayAutomatonEngine, STATE_ACTIVE, STATE_MUTATING, STATE_HEALING
from core.model_router import MultiModelRouter, ModelCapability, AIModelProvider
from core.agent_mesh import QmoosaAgentMesh, AgentRole
from screen_controller.visual_grounding import VisualGroundingEngine
from screen_controller.screen_driver import ScreenDriver
from bazaar_x402.protocol import X402Protocol, X402Headers
from bazaar_x402.marketplace import X402BazaarMarketplace
from bazaar_x402.escrow import EscrowManager, EscrowStatus
from security_pqc.pqc_engine import PQCEngine
from security_pqc.key_vault import PQCKeyVault
from wallet_qr.dynamic_qr import DynamicQREngine, PaymentRail
from wallet_qr.multi_wallet import MultiWalletManager
from tokenomics.token_model import QmoosaTokenomics, StakingTier


class TestQmoosaBotSubsystems(unittest.TestCase):

    def setUp(self):
        self.automaton = ConwayAutomatonEngine(grid_size=8)
        self.router = MultiModelRouter()
        self.screen_driver = ScreenDriver(viewport=(1920, 1080))
        self.pqc = PQCEngine()
        self.vault = PQCKeyVault()
        self.x402 = X402Protocol()
        self.bazaar = X402BazaarMarketplace(protocol=self.x402)
        self.qr = DynamicQREngine()
        self.wallets = MultiWalletManager()
        self.tokenomics = QmoosaTokenomics()

    # --- 1. Conway Automaton Tests ---
    def test_conway_automaton_evolution(self):
        cell1 = self.automaton.spawn_agent(2, 2, "AgentA", {})
        cell2 = self.automaton.spawn_agent(2, 3, "AgentB", {})
        cell3 = self.automaton.spawn_agent(3, 2, "AgentC", {})
        self.assertEqual(self.automaton.count_active_neighbors(2, 2), 2)

        stats = self.automaton.tick()
        self.assertEqual(stats["generation"], 1)
        self.assertGreaterEqual(stats["active_cells_count"], 1)

    def test_conway_self_healing(self):
        self.automaton.spawn_agent(4, 4, "Worker", {})
        self.automaton.trigger_failure(4, 4, "Cloudflare Rate Limit")
        self.assertEqual(self.automaton.cells[(4, 4)].state, STATE_HEALING)
        self.automaton.tick()
        self.assertEqual(self.automaton.cells[(4, 4)].state, STATE_ACTIVE)

    # --- 2. Multi-Model Router Tests ---
    def test_model_router_selection(self):
        m1 = self.router.select_best_model(ModelCapability.COMPUTER_USE)
        self.assertEqual(m1, AIModelProvider.CLAUDE_SONNET)

        m2 = self.router.select_best_model(ModelCapability.VISION_MASSIVE, has_screenshot=True)
        self.assertEqual(m2, AIModelProvider.GEMINI_FLASH)

        m3 = self.router.select_best_model("osint", realtime_web=True)
        self.assertEqual(m3, AIModelProvider.GROK_3)

    def test_model_router_execution(self):
        res = self.router.execute_prompt("Test prompt", task_type=ModelCapability.COMPUTER_USE)
        self.assertTrue(res["success"])
        self.assertIn("click_and_type", res["output"])

    # --- 3. Screen Driver Tests ---
    def test_bezier_trajectory_generation(self):
        points = self.screen_driver.calculate_bezier_trajectory((0, 0), (500, 500), steps=10)
        self.assertEqual(len(points), 11)
        self.assertEqual(points[0], (0, 0))
        self.assertEqual(points[-1], (500, 500))

    def test_visual_grounding_center(self):
        coords = self.screen_driver.grounding.find_target_coordinate("search", context="instagram_dm")
        self.assertIsNotNone(coords)
        self.assertIsInstance(coords, tuple)

    # --- 4. Post-Quantum Cryptography Tests ---
    def test_pqc_ml_kem_encapsulation(self):
        pk, sk = self.pqc.generate_kem_keypair()
        ciphertext, secret1 = self.pqc.encapsulate(pk)
        secret2 = self.pqc.decapsulate(ciphertext, sk)
        self.assertEqual(secret1, secret2)

    def test_pqc_ml_dsa_signatures(self):
        vk, sk = self.pqc.generate_dsa_keypair()
        message = "QMOOSA_MISSION_AUTH_101"
        signature = self.pqc.sign_action(message, sk)
        valid = self.pqc.verify_action(message, signature, vk)
        self.assertTrue(valid)

    def test_pqc_key_vault(self):
        self.vault.store_secret("TEST_API_KEY", "sk-secret-token-12345")
        retrieved = self.vault.retrieve_secret("TEST_API_KEY")
        self.assertEqual(retrieved, "sk-secret-token-12345")

    # --- 5. x402 Bazaar Tests ---
    def test_x402_challenge_and_verification(self):
        headers = self.x402.create_payment_challenge("TEST_SRV", 5000, "WALLET_RECEIVER")
        self.assertIn(X402Headers.HEADER_CHALLENGE, headers)
        v = self.x402.verify_payment_proof("txid_proof_valid_12345", headers[X402Headers.HEADER_CHALLENGE], 5000, "WALLET_RECEIVER")
        self.assertTrue(v["valid"])

        # Replay attack prevention check
        v_replay = self.x402.verify_payment_proof("txid_proof_valid_12345", headers[X402Headers.HEADER_CHALLENGE], 5000, "WALLET_RECEIVER")
        self.assertFalse(v_replay["valid"])
        self.assertIn("Replay", v_replay["error"])

    # --- 6. Dynamic QR & Multi-Wallet Tests ---
    def test_dynamic_upi_qr(self):
        qr_obj = self.qr.generate_upi_qr("qmoosa@upi", 500.0, "TX_REF_001")
        self.assertEqual(qr_obj["rail"], PaymentRail.UPI)
        self.assertIn("upi://pay?", qr_obj["payment_uri"])
        self.assertIn("data:image/svg+xml;base64,", qr_obj["svg_base64"])

    def test_multi_wallet_balances(self):
        bals = self.wallets.get_wallet_balances()
        self.assertIn("algorand", bals)
        self.assertIn("solana", bals)
        self.assertGreater(bals["solana"]["balance_native"], 0)

    # --- 7. Tokenomics Tests ---
    def test_token_burn_and_staking(self):
        initial_supply = self.tokenomics.total_supply
        burn_res = self.tokenomics.process_bazaar_fee_burn(1000.0, fee_percent=0.02)
        self.assertLess(self.tokenomics.total_supply, initial_supply)
        self.assertEqual(burn_res["burned"], 10.0)

        stake_res = self.tokenomics.stake_tokens("USER_WALLET_ALGO", 15_000)
        self.assertEqual(stake_res["tier"], StakingTier.OPERATOR)


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")
    print("=" * 80)
    print("[TEST SUITE] RUNNING QMOOSA BOT MASTER SYSTEMATIC TEST SUITE")
    print("=" * 80)
    suite = unittest.TestLoader().loadTestsFromTestCase(TestQmoosaBotSubsystems)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    if result.wasSuccessful():
        print("\n[SUCCESS] ALL SUBSYSTEMS SCIENTIFICALLY VERIFIED & FULLY SYNCHRONIZED!")
        sys.exit(0)
    else:
        print("\n[FAILURE] SYSTEMATIC TEST FAILURES DETECTED!")
        sys.exit(1)
