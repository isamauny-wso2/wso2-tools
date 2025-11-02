#!/bin/bash

# Certificate generation script for WSO2 deployments
# Usage: ./generate-certs.sh [keystore_path] [keystore_password]
# If keystore_path is provided, adds keypair to existing keystore
# Otherwise creates new wso2carbon.jks in ./certs directory

set -e

CERTS_DIR="./certs"
EXISTING_KEYSTORE="$1"
KEYSTORE_PASSWORD="${2:-wso2carbon}"

# Create certificates directory if it doesn't exist
mkdir -p "$CERTS_DIR"

# Determine keystore to use
if [ -n "$EXISTING_KEYSTORE" ]; then
    if [ ! -f "$EXISTING_KEYSTORE" ]; then
        echo "❌ Error: Specified keystore not found: $EXISTING_KEYSTORE"
        exit 1
    fi

    echo "🔍 Using existing keystore: $EXISTING_KEYSTORE"
    echo "🔄 Adding new server certificate to existing keystore..."

    # Check if 'server' alias already exists
    if keytool -list -keystore "$EXISTING_KEYSTORE" -storepass "$KEYSTORE_PASSWORD" -alias server >/dev/null 2>&1; then
        echo "⚠️  Server alias already exists. Deleting existing entry..."
        keytool -delete -alias server -keystore "$EXISTING_KEYSTORE" -storepass "$KEYSTORE_PASSWORD"
    fi

    KEYSTORE_FILE="$EXISTING_KEYSTORE"
    KEYSTORE_PASS="$KEYSTORE_PASSWORD"
else
    # Create new keystore in certs directory
    KEYSTORE_FILE="$CERTS_DIR/wso2carbon.jks"
    KEYSTORE_PASS="wso2carbon"
    echo "📋 Creating new WSO2 keystore: $KEYSTORE_FILE"
fi

echo "📋 Generating RSA server certificate..."

# Generate RSA server certificate and add to keystore
keytool -genkeypair \
    -alias server \
    -keyalg RSA \
    -keysize 2048 \
    -sigalg SHA256withRSA \
    -validity 365 \
    -keystore "$KEYSTORE_FILE" \
    -storetype JKS \
    -storepass "$KEYSTORE_PASS" \
    -keypass "$KEYSTORE_PASS" \
    -dname "CN=server,OU=Engineering,O=acme,C=com" \
    -ext "SAN=DNS:localhost,IP:127.0.0.1,IP:0.0.0.0"

# Export server certificate
echo "📤 Exporting server certificate..."
keytool -exportcert \
    -alias server \
    -keystore "$KEYSTORE_FILE" \
    -storetype JKS \
    -storepass "$KEYSTORE_PASS" \
    -file "$CERTS_DIR/server-cert.crt"

# Create client truststore and import server certificate
echo "🛡️ Creating client truststore..."
keytool -importcert \
    -alias server \
    -file "$CERTS_DIR/server-cert.crt" \
    -keystore "$CERTS_DIR/client-truststore.jks" \
    -storetype JKS \
    -storepass wso2carbon \
    -noprompt

echo "✅ Certificate generation completed!"
echo ""
echo "🔧 Generated files:"
echo "   - $KEYSTORE_FILE (Keystore with server certificate)"
echo "   - $CERTS_DIR/server-cert.crt (Exported server certificate)"
echo "   - $CERTS_DIR/client-truststore.jks (Client truststore with server cert)"
echo ""
echo "🔑 Keystore details:"
echo "   - Keystore password: $KEYSTORE_PASS"
echo "   - Key password: $KEYSTORE_PASS"
echo "   - Server alias: server"
echo ""
echo "📋 Usage examples:"
echo "   # Create new keystore:"
echo "   ./generate-certs.sh"
echo ""
echo "   # Add to existing keystore:"
echo "   ./generate-certs.sh /path/to/existing.jks [password]"
echo ""
echo "   # List certificates:"
echo "   keytool -list -keystore $KEYSTORE_FILE -storepass $KEYSTORE_PASS"