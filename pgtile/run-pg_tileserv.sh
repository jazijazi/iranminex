#!/bin/sh

# run-pg_tileserv.sh - Script to run pg_tileserv with config
# This replicates the Docker ENTRYPOINT command

set -e  # Exit on any error

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PG_TILESERV_BINARY="./pg_tileserv"
CONFIG_FILE="./pg_tileserv.toml"

echo -e "${BLUE}Starting pg_tileserv...${NC}"

# Check if binary exists
if [ ! -f "$PG_TILESERV_BINARY" ]; then
    echo -e "${RED}ERROR: pg_tileserv binary not found at $PG_TILESERV_BINARY${NC}"
    exit 1
fi

# Check if binary is executable
if [ ! -x "$PG_TILESERV_BINARY" ]; then
    echo -e "${RED}ERROR: pg_tileserv binary is not executable${NC}"
    echo "Run: chmod +x $PG_TILESERV_BINARY"
    exit 1
fi

# Check if config file exists
if [ ! -f "$CONFIG_FILE" ]; then
    echo -e "${RED}ERROR: Config file not found at $CONFIG_FILE${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Binary found: $PG_TILESERV_BINARY${NC}"
echo -e "${GREEN}✓ Config found: $CONFIG_FILE${NC}"
echo -e "${BLUE}Starting pg_tileserv ...${NC}"
echo

# Run pg_tileserv with config (same as Docker ENTRYPOINT)
exec ./pg_tileserv --config ./pg_tileserv.toml