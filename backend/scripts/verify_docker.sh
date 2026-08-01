#!/usr/bin/env bash
# ==============================================================================
# Synapse Backend — Docker Verification Script
# ==============================================================================
# Verifies that the Docker image builds, starts, and responds correctly.
#
# Usage:
#   cd backend
#   bash scripts/verify_docker.sh
#
# Requirements:
#   - Docker daemon running
#   - curl available
#   - Port 8000 available
# ==============================================================================

set -euo pipefail

# ── Configuration ────────────────────────────────────────────────────────
IMAGE_NAME="synapse-backend"
IMAGE_TAG="verify-test"
CONTAINER_NAME="synapse-backend-verify"
PORT=8000
HEALTH_URL="http://localhost:${PORT}/health"
ROOT_URL="http://localhost:${PORT}/"
VERSION_URL="http://localhost:${PORT}/version"
MAX_WAIT=30
PASSED=0
FAILED=0

# ── Helpers ──────────────────────────────────────────────────────────────

log_info()  { echo -e "\033[0;34m[INFO]\033[0m  $*"; }
log_pass()  { echo -e "\033[0;32m[PASS]\033[0m  $*"; PASSED=$((PASSED + 1)); }
log_fail()  { echo -e "\033[0;31m[FAIL]\033[0m  $*"; FAILED=$((FAILED + 1)); }
log_title() { echo -e "\n\033[1;36m── $* ──\033[0m"; }

cleanup() {
    log_info "Cleaning up container..."
    docker rm -f "${CONTAINER_NAME}" >/dev/null 2>&1 || true
}
trap cleanup EXIT

# ── Test 1: Production Build ─────────────────────────────────────────────
log_title "Test 1: Production Docker Build"

if docker build -t "${IMAGE_NAME}:${IMAGE_TAG}" --target production . ; then
    log_pass "Production image built successfully."
else
    log_fail "Production image build failed."
    exit 1
fi

# ── Test 2: Development Build ────────────────────────────────────────────
log_title "Test 2: Development Docker Build"

if docker build -t "${IMAGE_NAME}:dev-${IMAGE_TAG}" --target development . ; then
    log_pass "Development image built successfully."
else
    log_fail "Development image build failed."
fi

# ── Test 3: Container Startup ────────────────────────────────────────────
log_title "Test 3: Container Startup"

docker run -d \
    --name "${CONTAINER_NAME}" \
    -p "${PORT}:8000" \
    -e ENVIRONMENT=testing \
    "${IMAGE_NAME}:${IMAGE_TAG}"

log_info "Waiting for container to start (max ${MAX_WAIT}s)..."

STARTED=false
for i in $(seq 1 "${MAX_WAIT}"); do
    if curl -sf "${HEALTH_URL}" >/dev/null 2>&1; then
        STARTED=true
        break
    fi
    sleep 1
done

if [ "${STARTED}" = true ]; then
    log_pass "Container started and is responding."
else
    log_fail "Container did not become healthy within ${MAX_WAIT}s."
    docker logs "${CONTAINER_NAME}" 2>&1 || true
    exit 1
fi

# ── Test 4: Root Endpoint ────────────────────────────────────────────────
log_title "Test 4: Root Endpoint (GET /)"

ROOT_RESPONSE=$(curl -sf "${ROOT_URL}")
if echo "${ROOT_RESPONSE}" | grep -q '"status":"running"'; then
    log_pass "Root endpoint returns running status."
else
    log_fail "Root endpoint response unexpected: ${ROOT_RESPONSE}"
fi

# ── Test 5: Health Endpoint ──────────────────────────────────────────────
log_title "Test 5: Health Endpoint (GET /health)"

HEALTH_RESPONSE=$(curl -sf "${HEALTH_URL}")
if echo "${HEALTH_RESPONSE}" | grep -q '"status":"healthy"'; then
    log_pass "Health endpoint returns healthy status."
else
    log_fail "Health endpoint response unexpected: ${HEALTH_RESPONSE}"
fi

# ── Test 6: Version Endpoint ────────────────────────────────────────────
log_title "Test 6: Version Endpoint (GET /version)"

VERSION_RESPONSE=$(curl -sf "${VERSION_URL}")
if echo "${VERSION_RESPONSE}" | grep -q '"version"'; then
    log_pass "Version endpoint returns version info."
else
    log_fail "Version endpoint response unexpected: ${VERSION_RESPONSE}"
fi

# ── Test 7: Request ID Header ───────────────────────────────────────────
log_title "Test 7: X-Request-ID Header"

REQUEST_HEADERS=$(curl -sf -I "${HEALTH_URL}" 2>&1)
if echo "${REQUEST_HEADERS}" | grep -qi "x-request-id"; then
    log_pass "X-Request-ID header is present in response."
else
    log_fail "X-Request-ID header is missing."
fi

# ── Test 8: Environment Variable Override ────────────────────────────────
log_title "Test 8: Environment Variable Override"

# The container was started with ENVIRONMENT=testing
if echo "${HEALTH_RESPONSE}" | grep -q '"environment":"testing"'; then
    log_pass "Environment variable override works (ENVIRONMENT=testing)."
else
    log_fail "Environment variable override not reflected: ${HEALTH_RESPONSE}"
fi

# ── Test 9: Non-Root User ───────────────────────────────────────────────
log_title "Test 9: Non-Root User"

CONTAINER_USER=$(docker exec "${CONTAINER_NAME}" whoami 2>/dev/null || echo "unknown")
if [ "${CONTAINER_USER}" = "synapse" ]; then
    log_pass "Container runs as non-root user 'synapse'."
else
    log_fail "Container runs as '${CONTAINER_USER}' instead of 'synapse'."
fi

# ── Test 10: Image Size ─────────────────────────────────────────────────
log_title "Test 10: Image Size"

IMAGE_SIZE=$(docker image inspect "${IMAGE_NAME}:${IMAGE_TAG}" --format='{{.Size}}' 2>/dev/null || echo "0")
IMAGE_SIZE_MB=$((IMAGE_SIZE / 1024 / 1024))
if [ "${IMAGE_SIZE_MB}" -lt 500 ]; then
    log_pass "Image size is ${IMAGE_SIZE_MB}MB (under 500MB limit)."
else
    log_fail "Image size is ${IMAGE_SIZE_MB}MB (exceeds 500MB limit)."
fi

# ── Summary ──────────────────────────────────────────────────────────────
log_title "Summary"
echo ""
echo "  Passed: ${PASSED}"
echo "  Failed: ${FAILED}"
echo "  Total:  $((PASSED + FAILED))"
echo ""

if [ "${FAILED}" -gt 0 ]; then
    log_fail "Docker verification completed with ${FAILED} failure(s)."
    exit 1
else
    log_pass "All Docker verification checks passed!"
    exit 0
fi
