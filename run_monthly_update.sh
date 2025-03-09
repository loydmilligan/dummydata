#!/bin/bash

# Log file path (configurable)
LOG_DIR="${LOG_DIR:-/home/mmariani/Projects/dummydata/logs}"
LOG_FILE="$LOG_DIR/scheduled_run_$(date +%Y%m%d_%H%M%S).log"

# Ensure log directory exists
mkdir -p "$LOG_DIR"

# Record start time
echo "Starting monthly data generation at $(date)" | tee -a "$LOG_FILE"

# Change to script directory
cd "$(dirname "$0")" || {
  echo "Error: Failed to change to script directory" | tee -a "$LOG_FILE"
  exit 1
}

# Run the data generation with proper Python path
# Generate just the current month
python3 generate_monthly.py 2>&1 | tee -a "$LOG_FILE"

# Record completion
echo "Completed monthly data generation at $(date)" | tee -a "$LOG_FILE"

# Print status
if [ ${PIPESTATUS[0]} -eq 0 ]; then
  echo "Success: Monthly data generation completed successfully" | tee -a "$LOG_FILE"
  exit 0
else
  echo "Error: Monthly data generation failed" | tee -a "$LOG_FILE"
  exit 1
fi