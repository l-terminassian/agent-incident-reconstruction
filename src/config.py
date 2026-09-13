"""Paths, model identifiers, and credential loading."""
from __future__ import annotations

import os
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).resolve().parent.parent / ".env")
except ImportError:                                          # optional dependency
    pass

ROOT = Path(__file__).resolve().parent.parent
ARTIFACTS = ROOT / "artifacts"
TASKS = ROOT / "tasks"

# Name of the environment variable holding the investigator API key. It is
# deliberately NOT the SDK's default variable: the SDK silently falls back to
# that one when a client is constructed without an explicit key, so a distinct
# name turns a missing credential into a loud failure rather than a call billed
# somewhere unexpected.
KEY_ENV = os.environ.get("INVESTIGATOR_KEY_ENV", "INVESTIGATOR_API_KEY")


def anthropic_key() -> str:
    key = os.environ.get(KEY_ENV, "").strip()
    if not key:
        raise SystemExit(
            f"{KEY_ENV} is not set. Export it or put it in a .env file at the "
            f"repository root. The SDK's default variable is not used as a "
            f"fallback, by design."
        )
    return key


def anthropic_client():
    # Imported here, not at module scope, so that the offline reproduction can
    # import this module without the provider SDK installed.
    from anthropic import Anthropic

    return Anthropic(api_key=anthropic_key())     # explicit: never reads the environment


# Investigator models. The first is the primary arm; the others replicate the
# frozen V1-vs-V1A comparison across capability tiers.
INVESTIGATORS = {
    "primary": "claude-sonnet-5",
    "cheap": "claude-haiku-4-5",
    "strong": "claude-opus-5",
}


# The agent is served locally through an OpenAI-compatible endpoint (vLLM).
# AGENT_MODEL is the served model name, not a path.
AGENT_MODEL = os.environ.get("AGENT_MODEL", "qwen")
AGENT_DTYPE = "bfloat16"
AGENT_ENDPOINT = os.environ.get("AGENT_ENDPOINT", "http://localhost:8000/v1")

N_EPISODES = 120
CORRUPTION_RATE = 0.5      # share of disclosing accessors whose log is redacted
N_AGENTS = 2               # agents per episode, working separate tasks
MAX_STEPS = 12             # tool actions per agent
N_REPS = 3                 # repeats per package, issued consecutively for cache reuse
CALIBRATION_EPISODES = 20
PILOT_EPISODES = 6
