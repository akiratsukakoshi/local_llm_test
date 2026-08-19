"""Outer orchestrator for controlled Aider and local-LLM experiments."""

from .contract import Contract, ContractError, HarnessConfig, load_contract, load_harness_config

__all__ = [
    "Contract",
    "ContractError",
    "HarnessConfig",
    "load_contract",
    "load_harness_config",
]
