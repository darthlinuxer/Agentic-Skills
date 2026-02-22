# Ralph Configuration
# Copy this file to config.sh and customize for your environment

# OpenClaw Configuration
# ---------------------
# OpenClaw can run locally or remotely. Configure below:

# Mode: "local" runs openclaw agent --local, "remote" runs via gateway HTTP API
OPENCLAW_MODE="local"

# For remote mode: Gateway HTTP URL (use http://, not ws://)
# Example: OPENCLAW_GATEWAY_URL="http://127.0.0.1:18789"
OPENCLAW_GATEWAY_URL="http://127.0.0.1:18789"

# For remote mode: Authentication token (if required)
OPENCLAW_TOKEN="xMgRW1QXlLlOG2fP8I1DivnoFaznWl2Y"

# Agent ID to use (default: main)
OPENCLAW_AGENT="main"

# Session mode: "new" creates new session each time, "same" reuses session
# For Telegram integration, use "same" to keep conversation in one thread
OPENCLAW_SESSION_MODE="new"

# Channel to deliver Ralph updates (telegram, whatsapp, discord, etc.)
# When set, Ralph will send progress updates to this channel
OPENCLAW_DELIVER_CHANNEL="telegram"

# Target for delivery (Telegram user ID, WhatsApp number, Discord channel, etc.)
# For Telegram direct messages, use your numeric user ID
OPENCLAW_DELIVER_TO="1605712073"

# Additional openclaw agent flags
# Examples: --thinking medium, --verbose on
# OPENCLAW_EXTRA_FLAGS="--thinking medium"
