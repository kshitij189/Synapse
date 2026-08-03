#!/usr/bin/env bash
# ==============================================================================
# Synapse Platform — Docker Compose Verification Script
# ==============================================================================
# Verifies that docker compose up starts all services and they become healthy.
#
# Usage:
#   bash backend/scripts/verify_compose.sh
#
# Requirements:
#   - Docker daemon running
#   - Docker Compose v2 available
#   - curl available
#   - Port 8000, 5432, 6379 available
# ==============================================================================

set -euo pipefail

# ── Configuration ────────────────────────────────────────────────────────
COMPOSE_FILE="docker-compose.yml"
HEALTH_URL="http://localhost:8000/health"
ROOT_URL="http://localhost:8000/"
VERSION_URL="http://localhost:8000/version"
MAX_WAIT=120
PASSED=0
FAILED=0

# ── Helpers ──────────────────────────────────────────────────────────────

log_info()  { echo -e "\033[0;34m[INFO]\033[0m  $*"; }
log_pass()  { echo -e "\033[0;32m[PASS]\033[0m  $*"; PASSED=$((PASSED + 1)); }
log_fail()  { echo -e "\033[0;31m[FAIL]\033[0m  $*"; FAILED=$((FAILED + 1)); }
log_title() { echo -e "\n\033[1;36m── $* ──\033[0m"; }

cleanup() {
    log_info "Stopping Docker Compose stack..."
    docker compose -f "${COMPOSE_FILE}" down --timeout 10 >/dev/null 2>&1 || true
}
trap cleanup EXIT

# ── Ensure .env exists ───────────────────────────────────────────────────
if [ ! -f "backend/.env" ]; then
    log_info "Creating backend/.env from .env.example..."
    cp backend/.env.example backend/.env
fi

# ── Test 1: Docker Compose Up ────────────────────────────────────────────
log_title "Test 1: Docker Compose Up"

if docker compose -f "${COMPOSE_FILE}" up -d --build; then
    log_pass "Docker Compose started successfully."
else
    log_fail "Docker Compose failed to start."
    exit 1
fi

# ── Test 2: Wait for All Services Healthy ────────────────────────────────
log_title "Test 2: Wait for Services to Become Healthy"

log_info "Waiting for all services to become healthy (max ${MAX_WAIT}s)..."

BACKEND_HEALTHY=false
POSTGRES_HEALTHY=false
REDIS_HEALTHY=false

for i in $(seq 1 "${MAX_WAIT}"); do
    # Check postgres
    if [ "${POSTGRES_HEALTHY}" = false ]; then
        PG_STATUS=$(docker inspect --format='{{.State.Health.Status}}' synapse-postgres 2>/dev/null || echo "missing")
        if [ "${PG_STATUS}" = "healthy" ]; then
            POSTGRES_HEALTHY=true
            log_pass "PostgreSQL is healthy (${i}s)."
        fi
    fi

    # Check redis
    if [ "${REDIS_HEALTHY}" = false ]; then
        REDIS_STATUS=$(docker inspect --format='{{.State.Health.Status}}' synapse-redis 2>/dev/null || echo "missing")
        if [ "${REDIS_STATUS}" = "healthy" ]; then
            REDIS_HEALTHY=true
            log_pass "Redis is healthy (${i}s)."
        fi
    fi

    # Check backend
    if [ "${BACKEND_HEALTHY}" = false ]; then
        BACKEND_STATUS=$(docker inspect --format='{{.State.Health.Status}}' synapse-backend 2>/dev/null || echo "missing")
        if [ "${BACKEND_STATUS}" = "healthy" ]; then
            BACKEND_HEALTHY=true
            log_pass "Backend is healthy (${i}s)."
        fi
    fi

    # All healthy?
    if [ "${POSTGRES_HEALTHY}" = true ] && [ "${REDIS_HEALTHY}" = true ] && [ "${BACKEND_HEALTHY}" = true ]; then
        break
    fi

    sleep 1
done

if [ "${POSTGRES_HEALTHY}" = false ]; then
    log_fail "PostgreSQL did not become healthy within ${MAX_WAIT}s."
    docker compose -f "${COMPOSE_FILE}" logs postgres 2>&1 | tail -20
fi

if [ "${REDIS_HEALTHY}" = false ]; then
    log_fail "Redis did not become healthy within ${MAX_WAIT}s."
    docker compose -f "${COMPOSE_FILE}" logs redis 2>&1 | tail -20
fi

if [ "${BACKEND_HEALTHY}" = false ]; then
    log_fail "Backend did not become healthy within ${MAX_WAIT}s."
    docker compose -f "${COMPOSE_FILE}" logs backend 2>&1 | tail -30
    exit 1
fi

# ── Test 3: Root Endpoint ────────────────────────────────────────────────
log_title "Test 3: Root Endpoint (GET /)"

ROOT_RESPONSE=$(curl -sf "${ROOT_URL}" || echo "CURL_FAILED")
if echo "${ROOT_RESPONSE}" | grep -q '"status":"running"'; then
    log_pass "Root endpoint returns running status."
else
    log_fail "Root endpoint response unexpected: ${ROOT_RESPONSE}"
fi

# ── Test 4: Health Endpoint ──────────────────────────────────────────────
log_title "Test 4: Health Endpoint (GET /health)"

HEALTH_RESPONSE=$(curl -sf "${HEALTH_URL}" || echo "CURL_FAILED")
if echo "${HEALTH_RESPONSE}" | grep -q '"status":"healthy"'; then
    log_pass "Health endpoint returns healthy status."
else
    log_fail "Health endpoint response unexpected: ${HEALTH_RESPONSE}"
fi

# ── Test 5: Version Endpoint ────────────────────────────────────────────
log_title "Test 5: Version Endpoint (GET /version)"

VERSION_RESPONSE=$(curl -sf "${VERSION_URL}" || echo "CURL_FAILED")
if echo "${VERSION_RESPONSE}" | grep -q '"version"'; then
    log_pass "Version endpoint returns version info."
else
    log_fail "Version endpoint response unexpected: ${VERSION_RESPONSE}"
fi

# ── Test 6: X-Request-ID Header ─────────────────────────────────────────
log_title "Test 6: X-Request-ID Header"

REQUEST_HEADERS=$(curl -sf -I "${HEALTH_URL}" 2>&1 || echo "CURL_FAILED")
if echo "${REQUEST_HEADERS}" | grep -qi "x-request-id"; then
    log_pass "X-Request-ID header is present."
else
    log_fail "X-Request-ID header is missing."
fi

# ── Test 7: PostgreSQL Connectivity ──────────────────────────────────────
log_title "Test 7: PostgreSQL Connectivity"

PG_READY=$(docker compose -f "${COMPOSE_FILE}" exec -T postgres pg_isready -U synapse -d synapse 2>/dev/null || echo "FAILED")
if echo "${PG_READY}" | grep -q "accepting connections"; then
    log_pass "PostgreSQL is accepting connections."
else
    log_fail "PostgreSQL connectivity check failed: ${PG_READY}"
fi

# ── Test 8: Redis Connectivity ───────────────────────────────────────────
log_title "Test 8: Redis Connectivity"

REDIS_PONG=$(docker compose -f "${COMPOSE_FILE}" exec -T redis redis-cli ping 2>/dev/null || echo "FAILED")
if echo "${REDIS_PONG}" | grep -q "PONG"; then
    log_pass "Redis responds to PING."
else
    log_fail "Redis connectivity check failed: ${REDIS_PONG}"
fi

# ── Test 9: Docker Compose PS ───────────────────────────────────────────
log_title "Test 9: All Services Running"

RUNNING_COUNT=$(docker compose -f "${COMPOSE_FILE}" ps --status running -q 2>/dev/null | wc -l)
if [ "${RUNNING_COUNT}" -ge 3 ]; then
    log_pass "All 3 services are running."
else
    log_fail "Expected 3 running services, found ${RUNNING_COUNT}."
    docker compose -f "${COMPOSE_FILE}" ps
fi

# ── Test 10: Network Exists ─────────────────────────────────────────────
log_title "Test 10: Docker Network"

if docker network inspect aaop_synapse-network >/dev/null 2>&1; then
    log_pass "synapse-network bridge network exists."
else
    # Try alternate naming convention
    NETWORK_NAME=$(docker network ls --filter "name=synapse-network" --format '{{.Name}}' | head -1)
    if [ -n "${NETWORK_NAME}" ]; then
        log_pass "synapse-network bridge network exists (${NETWORK_NAME})."
    else
        log_fail "synapse-network not found."
    fi
fi

# ── Summary ──────────────────────────────────────────────────────────────
log_title "Summary"
echo ""
echo "  Passed: ${PASSED}"
echo "  Failed: ${FAILED}"
echo "  Total:  $((PASSED + FAILED))"
echo ""

if [ "${FAILED}" -gt 0 ]; then
    log_fail "Docker Compose verification completed with ${FAILED} failure(s)."
    exit 1
else
    log_pass "All Docker Compose verification checks passed!"
    exit 0
fi
