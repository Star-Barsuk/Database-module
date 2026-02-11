#!/bin/sh
set -e

echo "🚀 Application entrypoint starting..."

PROJECT_ROOT="/app"
ENVS_DIR="$PROJECT_ROOT/envs"

mkdir -p "$ENVS_DIR"

if [ -f "$PROJECT_ROOT/.active-env" ]; then
    ACTIVE_ENV=$(cat "$PROJECT_ROOT/.active-env" | tr -d '[:space:]')
    echo "📁 Active environment from .active-env: $ACTIVE_ENV"
else
    echo "❌ ERROR: .active-env file not found in $PROJECT_ROOT/.active-env"
    echo "📋 Available files in /app:"
    ls -la /app/
    exit 1
fi

ENV_FILE_PATH="$ENVS_DIR/.env.$ACTIVE_ENV"
echo "🔍 Looking for environment file: $ENV_FILE_PATH"

if [ ! -f "$ENV_FILE_PATH" ]; then
    echo "❌ ERROR: Environment file not found: $ENV_FILE_PATH"
    echo "📋 Available env files in $ENVS_DIR:"
    ls -la "$ENVS_DIR/" 2>/dev/null || echo "   (directory empty)"
    exit 1
fi

DEST_ENV_FILE="$ENVS_DIR/.env"
cp "$ENV_FILE_PATH" "$DEST_ENV_FILE"
echo "✅ Copied: .env.$ACTIVE_ENV -> .env"

echo "🧹 Cleaning up other environment files..."
find "$ENVS_DIR" -name ".env.*" -type f ! -name ".env" -delete 2>/dev/null || true
echo "✅ Cleanup complete"

echo "🔄 Loading environment variables from .env..."
set -a
. "$DEST_ENV_FILE"
set +a


export APP_ENV="$ACTIVE_ENV"
export DOCKER_CONTAINER="true"

echo "✅ Environment '$ACTIVE_ENV' loaded successfully"

echo "📋 Environment summary:"
echo "   APP_ENV: $APP_ENV"
echo "   DOCKER_CONTAINER: $DOCKER_CONTAINER"
if [ -n "$DB_HOST" ]; then echo "   DB_HOST: ***"; fi
if [ -n "$DB_NAME" ]; then echo "   DB_NAME: ***"; fi
if [ -n "$DB_USER" ]; then echo "   DB_USER: ***"; fi

echo "🔧 Starting application..."
exec python -m src.main
