#!/bin/bash
# Ralph Wiggum - Long-running AI agent loop

# Default values
TOOL="amp"
MAX_ITERATIONS=10

# Help function
show_help() {
  cat << 'EOF'
Ralph - Autonomous AI Agent Loop

USAGE:
    ./ralph.sh [OPTIONS] [max_iterations]

OPTIONS:
    --tool TOOL       AI tool to use: amp or claude (default: amp)
    --tool=TOOL      Same as above but with = syntax
    --help, -h       Show this help message

ARGUMENTS:
    max_iterations   Number of iterations to run (default: 10)

EXAMPLES:
    # Run with default settings (amp, 10 iterations)
    ./ralph.sh

    # Run 5 iterations with Claude Code
    ./ralph.sh --tool claude 5

    # Run 3 iterations with Amp
    ./ralph.sh 3

    # Run with Claude using equals syntax
    ./ralph.sh --tool=claude 10

CONFIGURATION:
    Ralph reads config.sh for delivery settings:
    - OPENCLAW_DELIVER_CHANNEL: telegram, whatsapp, discord, etc.
    - OPENCLAW_DELIVER_TO: recipient ID (e.g., your Telegram user ID)
    - OPENCLAW_MODE: local or remote

    Copy config.sh.example to config.sh and customize.

TELEGRAM MESSAGES:
    When configured, Ralph sends:
    - Overview: Total/pending/completed stories before starting
    - Story Details: Title, description, acceptance criteria before each story
    - Progress: Iteration status after each completion
    - Completion: Final summary when done

FILES:
    prd.json         - Project requirements (user stories)
    progress.txt     - Progress log (appended each iteration)
    CLAUDE.md       - Agent instructions for Claude Code
    prompt.md       - Agent instructions for Amp
    config.sh       - Delivery configuration
    archive/        - Previous runs archived here

TROUBLESHOOTING:
    - If no progress: Check prd.json exists with valid userStories
    - If no delivery: Verify config.sh has OPENCLAW_DELIVER_CHANNEL set
    - If Claude fails: Ensure MiniMax API key configured in ~/.claude/settings.json

EOF
}

# Parse arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --help|-h)
      show_help
      exit 0
      ;;
    --tool)
      TOOL="$2"
      shift 2
      ;;
    --tool=*)
      TOOL="${1#*=}"
      shift
      ;;
    *)
      # Assume it's max_iterations if it's a number
      if [[ "$1" =~ ^[0-9]+$ ]]; then
        MAX_ITERATIONS="$1"
      fi
      shift
      ;;
  esac
done

# Validate tool choice
if [[ "$TOOL" != "amp" && "$TOOL" != "claude" ]]; then
  echo "Error: Invalid tool '$TOOL'. Must be 'amp' or 'claude'."
  echo "Run './ralph.sh --help' for usage information."
  exit 1
fi
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Load configuration
if [ -f "$SCRIPT_DIR/config.sh" ]; then
  source "$SCRIPT_DIR/config.sh"
fi

# Default values if not set in config
OPENCLAW_MODE="${OPENCLAW_MODE:-local}"
OPENCLAW_GATEWAY_URL="${OPENCLAW_GATEWAY_URL:-http://127.0.0.1:18789}"
OPENCLAW_TOKEN="${OPENCLAW_TOKEN:-}"
OPENCLAW_AGENT="${OPENCLAW_AGENT:-main}"
OPENCLAW_SESSION_MODE="${OPENCLAW_SESSION_MODE:-new}"
OPENCLAW_DELIVER_CHANNEL="${OPENCLAW_DELIVER_CHANNEL:-}"
OPENCLAW_DELIVER_TO="${OPENCLAW_DELIVER_TO:-}"

PRD_FILE="$SCRIPT_DIR/prd.json"
PROGRESS_FILE="$SCRIPT_DIR/progress.txt"
ARCHIVE_DIR="$SCRIPT_DIR/archive"
LAST_BRANCH_FILE="$SCRIPT_DIR/.last-branch"

# Archive previous run if branch changed
if [ -f "$PRD_FILE" ] && [ -f "$LAST_BRANCH_FILE" ]; then
  CURRENT_BRANCH=$(jq -r '.branchName // empty' "$PRD_FILE" 2>/dev/null || echo "")
  LAST_BRANCH=$(cat "$LAST_BRANCH_FILE" 2>/dev/null || echo "")
  
  if [ -n "$CURRENT_BRANCH" ] && [ -n "$LAST_BRANCH" ] && [ "$CURRENT_BRANCH" != "$LAST_BRANCH" ]; then
    # Archive the previous run
    DATE=$(date +%Y-%m-%d)
    # Strip "ralph/" prefix from branch name for folder
    FOLDER_NAME=$(echo "$LAST_BRANCH" | sed 's|^ralph/||')
    ARCHIVE_FOLDER="$ARCHIVE_DIR/$DATE-$FOLDER_NAME"
    
    echo "Archiving previous run: $LAST_BRANCH"
    mkdir -p "$ARCHIVE_FOLDER"
    [ -f "$PRD_FILE" ] && cp "$PRD_FILE" "$ARCHIVE_FOLDER/"
    [ -f "$PROGRESS_FILE" ] && cp "$PROGRESS_FILE" "$ARCHIVE_FOLDER/"
    echo "   Archived to: $ARCHIVE_FOLDER"
    
    # Reset progress file for new run
    echo "# Ralph Progress Log" > "$PROGRESS_FILE"
    echo "Started: $(date)" >> "$PROGRESS_FILE"
    echo "---" >> "$PROGRESS_FILE"
  fi
fi

# Track current branch
if [ -f "$PRD_FILE" ]; then
  CURRENT_BRANCH=$(jq -r '.branchName // empty' "$PRD_FILE" 2>/dev/null || echo "")
  if [ -n "$CURRENT_BRANCH" ]; then
    echo "$CURRENT_BRANCH" > "$LAST_BRANCH_FILE"
  fi
fi

# Initialize progress file if it doesn't exist
if [ ! -f "$PROGRESS_FILE" ]; then
  echo "# Ralph Progress Log" > "$PROGRESS_FILE"
  echo "Started: $(date)" >> "$PROGRESS_FILE"
  echo "---" >> "$PROGRESS_FILE"
fi

# Function to send update via OpenClaw
send_update() {
  local message="$1"
  
  if [ -z "$OPENCLAW_DELIVER_CHANNEL" ] || [ -z "$OPENCLAW_DELIVER_TO" ]; then
    echo "  [Delivery] No channel/to configured, skipping update"
    return
  fi
  
  echo "  [Delivery] Sending update via $OPENCLAW_DELIVER_CHANNEL to $OPENCLAW_DELIVER_TO"
  
  if [ "$OPENCLAW_MODE" = "remote" ]; then
    # Remote mode: use HTTP API
    local response
    response=$(curl -s -X POST "$OPENCLAW_GATEWAY_URL/api/messages/send" \
      -H "Content-Type: application/json" \
      ${OPENCLAW_TOKEN:+-H "Authorization: Bearer $OPENCLAW_TOKEN"} \
      -d "{
        \"channel\": \"$OPENCLAW_DELIVER_CHANNEL\",
        \"target\": \"$OPENCLAW_DELIVER_TO\",
        \"message\": \"$message\"
      }") || true
    
    if [ -n "$response" ]; then
      echo "  [Delivery] Response: $response"
    fi
  else
    # Local mode: use openclaw CLI
    openclaw message send \
      --channel "$OPENCLAW_DELIVER_CHANNEL" \
      --target "$OPENCLAW_DELIVER_TO" \
      --message "$message" || true
  fi
}

# Get PRD info for overview
TOTAL_STORIES=$(jq '.userStories | length' "$PRD_FILE" 2>/dev/null || echo "0")
PENDING_STORIES=$(jq '[.userStories[] | select(.passes == false)] | length' "$PRD_FILE" 2>/dev/null || echo "0")

# Build overview message
OVERVIEW_MSG="📋 **Ralph Overview**
━━━━━━━━━━━━━━━━━━
Total Stories: $TOTAL_STORIES
Pending: $PENDING_STORIES
Completed: $((TOTAL_STORIES - PENDING_STORIES))

**Pending Stories:**
$(jq -r '.userStories[] | select(.passes == false) | "• [\(.id)] \(.title) (Priority \(.priority))"' "$PRD_FILE" 2>/dev/null)

Tool: $TOOL | Max Iterations: $MAX_ITERATIONS"

echo "Starting Ralph - Tool: $TOOL - Max iterations: $MAX_ITERATIONS"
echo "Total user stories: $TOTAL_STORIES - Pending: $PENDING_STORIES"
send_update "$OVERVIEW_MSG"

for i in $(seq 1 $MAX_ITERATIONS); do
  # Get current story info
  CURRENT_STORY_ID=$(jq -r '.userStories[] | select(.passes == false) | .id' "$PRD_FILE" 2>/dev/null | head -1)
  
  if [ -n "$CURRENT_STORY_ID" ] && [ "$CURRENT_STORY_ID" != "null" ]; then
    # Get full story details
    STORY_TITLE=$(jq -r ".userStories[] | select(.id == \"$CURRENT_STORY_ID\") | .title" "$PRD_FILE" 2>/dev/null)
    STORY_DESC=$(jq -r ".userStories[] | select(.id == \"$CURRENT_STORY_ID\") | .description" "$PRD_FILE" 2>/dev/null)
    STORY_AC=$(jq -r ".userStories[] | select(.id == \"$CURRENT_STORY_ID\") | .acceptanceCriteria[]" "$PRD_FILE" 2>/dev/null)
    STORY_PRIORITY=$(jq -r ".userStories[] | select(.id == \"$CURRENT_STORY_ID\") | .priority" "$PRD_FILE" 2>/dev/null)
    
    STORY_MSG="📝 **Starting Story: $CURRENT_STORY_ID**
━━━━━━━━━━━━━━━━━━
**Title:** $STORY_TITLE

**Description:** $STORY_DESC

**Priority:** $STORY_PRIORITY

**Acceptance Criteria:**
$(echo "$STORY_AC" | sed 's/^/• /')

━━━━━━━━━━━━━━━━━━
Iteration: $i/$MAX_ITERATIONS"
    
    send_update "$STORY_MSG"
  fi
  echo ""
  echo "==============================================================="
  echo "  Ralph Iteration $i of $MAX_ITERATIONS ($TOOL)"
  echo "==============================================================="
  send_update "▶️ Ralph iteration $i/$MAX_ITERATIONS starting..."

  # Run the selected tool with the ralph prompt
  if [[ "$TOOL" == "amp" ]]; then
    OUTPUT=$(cat "$SCRIPT_DIR/prompt.md" | amp --dangerously-allow-all 2>&1 | tee /dev/stderr) || true
  else
    # Claude Code: use --dangerously-skip-permissions for autonomous operation, --print for output
    OUTPUT=$(node /skeleton/.npm-global/lib/node_modules/@anthropic-ai/claude-code/cli.js --dangerously-skip-permissions --print < "$SCRIPT_DIR/CLAUDE.md" 2>&1) || true
    echo "$OUTPUT"
  fi
  
  # Check for completion signal
  if echo "$OUTPUT" | grep -q "<promise>COMPLETE</promise>"; then
    echo ""
    echo "Ralph completed all tasks!"
    echo "Completed at iteration $i of $MAX_ITERATIONS"
    send_update "🎉 Ralph completed all tasks! (iteration $i/$MAX_ITERATIONS)"
    exit 0
  fi
  
  # Send iteration complete status
  TOTAL_PASSED=$(jq '[.userStories[] | select(.passes == true)] | length' "$PRD_FILE" 2>/dev/null || echo "0")
  TOTAL_STORIES=$(jq '.userStories | length' "$PRD_FILE" 2>/dev/null || echo "0")
  REMAINING=$((TOTAL_STORIES - TOTAL_PASSED))
  
  # Build status message
  STATUS_MSG="✅ **Iteration $i/$MAX_ITERATIONS Complete**
━━━━━━━━━━━━━━━━━━
Progress: $TOTAL_PASSED/$TOTAL_STORIES stories passed

**Passed:** $(jq -r '.userStories[] | select(.passes == true) | .id' "$PRD_FILE" 2>/dev/null | tr '\n' ' ')

**Remaining ($REMAINING):** $(jq -r '.userStories[] | select(.passes == false) | .id' "$PRD_FILE" 2>/dev/null | tr '\n' ' ')"
  
  send_update "$STATUS_MSG"
  
  echo "Iteration $i complete. Continuing..."
  sleep 2
done

echo ""
echo "Ralph reached max iterations ($MAX_ITERATIONS) without completing all tasks."
echo "Check $PROGRESS_FILE for status."
send_update "⏸️ Ralph reached max iterations ($MAX_ITERATIONS). Check progress.txt for status."
exit 1
