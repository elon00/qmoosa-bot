"""
Qmoosa Bot - Global Tokenomics Engine
Implements Proof-of-Resolution (PoR) minting, 50% deflationary fee burning,
and multi-tiered staking for autonomous compute swarms.
"""

from typing import Dict, Any, List, Optional
import math
import time
import logging

logger = logging.getLogger("Tokenomics")

class StakingTier:
    SCOUT = "Scout (1,000 Tokens)"
    OPERATOR = "Operator (10,000 Tokens)"
    SWARM_MASTER = "Swarm Master (100,000 Tokens)"


class QmoosaTokenomics:
    """
    Manages token supply, burn mechanics, staking tiers, and DePIN node rewards.
    """

    def __init__(self, initial_supply: float = 10_000_000.0):
        self.total_supply = initial_supply
        self.circulating_supply = initial_supply * 0.4
        self.total_burned = 0.0
        self.staking_pool = 0.0
        self.user_stakes: Dict[str, float] = {}

    def get_tier(self, staked_amount: float) -> str:
        if staked_amount >= 100_000:
            return StakingTier.SWARM_MASTER
        elif staked_amount >= 10_000:
            return StakingTier.OPERATOR
        elif staked_amount >= 1_000:
            return StakingTier.SCOUT
        return "Unstaked (Basic Access)"

    def stake_tokens(self, user_address: str, amount: float) -> Dict[str, Any]:
        if amount <= 0:
            raise ValueError("Staking amount must be positive")
        self.user_stakes[user_address] = self.user_stakes.get(user_address, 0.0) + amount
        self.staking_pool += amount
        self.circulating_supply -= amount
        tier = self.get_tier(self.user_stakes[user_address])
        logger.info(f"[Tokenomics] {user_address} staked {amount} tokens. Tier: {tier}")
        return {
            "user": user_address,
            "staked_total": self.user_stakes[user_address],
            "tier": tier,
            "staking_pool_total": self.staking_pool,
        }

    def process_bazaar_fee_burn(self, transaction_amount: float, fee_percent: float = 0.02) -> Dict[str, Any]:
        """
        Deducts fee and burns 50% permanently (Deflationary mechanism).
        Remaining 50% allocated to DePIN compute node operators.
        """
        fee = transaction_amount * fee_percent
        burn_amount = fee * 0.50
        depin_reward = fee * 0.50

        self.total_supply -= burn_amount
        self.total_burned += burn_amount

        logger.info(f"[Tokenomics] Burned {burn_amount:.4f} tokens permanently. DePIN reward: {depin_reward:.4f}")
        return {
            "fee_total": fee,
            "burned": burn_amount,
            "depin_reward_pool": depin_reward,
            "new_total_supply": self.total_supply,
            "cumulative_burned": self.total_burned,
        }

    def reward_proof_of_resolution(self, agent_id: str, complexity_score: float) -> Dict[str, Any]:
        """
        Mints Proof-of-Resolution (PoR) reward to high-performing agent workers.
        Formula: Reward = Base * log(1 + Complexity)
        """
        base_reward = 15.0
        mint_amount = round(base_reward * math.log(1 + complexity_score), 4)
        self.total_supply += mint_amount
        self.circulating_supply += mint_amount

        logger.info(f"[Tokenomics] PoR Minted {mint_amount} tokens to Agent '{agent_id}'")
        return {
            "agent_id": agent_id,
            "minted_reward": mint_amount,
            "complexity_score": complexity_score,
            "circulating_supply": self.circulating_supply,
        }

    def get_token_metrics(self) -> Dict[str, Any]:
        return {
            "token_symbol": "QMOOSA / QALGO",
            "total_supply": self.total_supply,
            "circulating_supply": self.circulating_supply,
            "total_burned": self.total_burned,
            "staking_pool": self.staking_pool,
            "burn_rate_percentage": round((self.total_burned / (self.total_supply + self.total_burned)) * 100, 2),
        }
