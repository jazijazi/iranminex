#!/bin/bash

# PostgreSQL Docker Backup Script
# This script creates a backup of PostgreSQL database from Docker container
# and stores it locally with timestamp

# Get the directory where the script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ENV_FILE="${SCRIPT_DIR}/.env"

# Change to script directory so relative paths work
cd "$SCRIPT_DIR"

# Load environment variables from .env file
if [ -f "$ENV_FILE" ]; then
    echo "Loading environment variables from ${ENV_FILE}"
    # Remove quotes and export variables (skip UID and other protected vars)
    export $(grep -v '^#' "$ENV_FILE" | grep -v '^UID=' | grep -v '^EUID=' | grep -v '^PPID=' | sed 's/"//g' | xargs)
else
    echo "Warning: .env file not found at ${ENV_FILE}"
    echo "Using default values or expecting environment variables to be set"
fi

# Configuration (will use .env values if available, otherwise defaults)
# DOCKER_COMPOSE_FILES should be comma-separated in .env: "file1.yml,file2.yml"
DOCKER_COMPOSE_FILES="${DOCKER_COMPOSE_FILES:-${SCRIPT_DIR}/docker-compose.prod.yml}"
CONTAINER_NAME="${CONTAINER_NAME:-db}"

DB_USER="${POSTGRES_USER:-iranminexdbuser}"
DB_NAME="${POSTGRES_DB:-iranminexdb}"
LOCAL_BACKUP_DIR="${LOCAL_BACKUP_DIR:-/var/dbbackup}"
CONTAINER_TEMP_DIR="/tmp"

# Convert comma-separated files to array and build docker compose command
IFS=',' read -ra COMPOSE_FILES <<< "$DOCKER_COMPOSE_FILES"
DOCKER_COMPOSE_CMD="docker compose"
for file in "${COMPOSE_FILES[@]}"; do
    DOCKER_COMPOSE_CMD="$DOCKER_COMPOSE_CMD -f $(echo $file | xargs)"
done

# Generate timestamp for backup file
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILENAME="backup_${DB_NAME}_${TIMESTAMP}.sql"
CONTAINER_BACKUP_PATH="${CONTAINER_TEMP_DIR}/${BACKUP_FILENAME}"
LOCAL_BACKUP_PATH="${LOCAL_BACKUP_DIR}/${BACKUP_FILENAME}"

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Starting PostgreSQL backup process...${NC}"

# Create local backup directory if it doesn't exist
if [ ! -d "$LOCAL_BACKUP_DIR" ]; then
    echo -e "${YELLOW}Creating backup directory: ${LOCAL_BACKUP_DIR}${NC}"
    mkdir -p "$LOCAL_BACKUP_DIR"
    if [ $? -ne 0 ]; then
        echo -e "${RED}Failed to create backup directory${NC}"
        exit 1
    fi
fi

# Step 1: Create backup inside container
echo -e "${YELLOW}Creating database backup in container...${NC}"
$DOCKER_COMPOSE_CMD exec -T "$CONTAINER_NAME" pg_dump -U "$DB_USER" -d "$DB_NAME" > "$LOCAL_BACKUP_PATH"

if [ $? -eq 0 ]; then
    echo -e "${GREEN}Backup created successfully: ${BACKUP_FILENAME}${NC}"
    
    # Get backup file size
    BACKUP_SIZE=$(du -h "$LOCAL_BACKUP_PATH" | cut -f1)
    echo -e "${GREEN}Backup size: ${BACKUP_SIZE}${NC}"
else
    echo -e "${RED}Failed to create backup${NC}"
    exit 1
fi

# Step 2: Clean up any backup files in container (safety check)
echo -e "${YELLOW}Cleaning up container temp files...${NC}"
$DOCKER_COMPOSE_CMD exec -T "$CONTAINER_NAME" /bin/sh -c "rm -f ${CONTAINER_TEMP_DIR}/*.sql ${CONTAINER_TEMP_DIR}/*.dump 2>/dev/null || true"

if [ $? -eq 0 ]; then
    echo -e "${GREEN}Container cleanup completed${NC}"
else
    echo -e "${YELLOW}Warning: Container cleanup had issues (may be normal if no files existed)${NC}"
fi

# Step 3: Compress backup (optional, saves space)
echo -e "${YELLOW}Compressing backup...${NC}"
gzip "$LOCAL_BACKUP_PATH"

if [ $? -eq 0 ]; then
    echo -e "${GREEN}Backup compressed: ${BACKUP_FILENAME}.gz${NC}"
    COMPRESSED_SIZE=$(du -h "${LOCAL_BACKUP_PATH}.gz" | cut -f1)
    echo -e "${GREEN}Compressed size: ${COMPRESSED_SIZE}${NC}"
else
    echo -e "${YELLOW}Warning: Compression failed, keeping uncompressed backup${NC}"
fi

# Step 4: Clean up old backups (older than 10 days)
echo -e "${YELLOW}Cleaning up backups older than 10 days...${NC}"
OLD_BACKUPS=$(find "$LOCAL_BACKUP_DIR" -name "backup_*.sql.gz" -mtime +10 2>/dev/null)

if [ -n "$OLD_BACKUPS" ]; then
    echo -e "${YELLOW}Found old backups to delete:${NC}"
    echo "$OLD_BACKUPS"
    find "$LOCAL_BACKUP_DIR" -name "backup_*.sql.gz" -mtime +10 -delete
    echo -e "${GREEN}Old backups cleaned up successfully${NC}"
else
    echo -e "${GREEN}No old backups to clean up${NC}"
fi

# Also clean up uncompressed .sql files older than 10 days (if any exist)
find "$LOCAL_BACKUP_DIR" -name "backup_*.sql" -mtime +10 -delete 2>/dev/null

# Step 5: Show summary
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Backup completed successfully!${NC}"
echo -e "${GREEN}Location: ${LOCAL_BACKUP_DIR}${NC}"
echo -e "${GREEN}File: ${BACKUP_FILENAME}.gz${NC}"
echo -e "${GREEN}========================================${NC}"

# Optional: List all backups
echo -e "${YELLOW}All backups in ${LOCAL_BACKUP_DIR}:${NC}"
ls -lh "$LOCAL_BACKUP_DIR"
BACKUP_COUNT=$(ls -1 "$LOCAL_BACKUP_DIR"/backup_*.sql.gz 2>/dev/null | wc -l)
echo -e "${GREEN}Total backups: ${BACKUP_COUNT}${NC}"

exit 0
