#!/bin/bash
# Script de arranque para la instancia EC2 (Ubuntu): se pega en "User data"
# al crear la instancia. Instala Docker, clona el repo y levanta la app.
set -e
apt-get update -y
apt-get install -y docker.io docker-compose-v2 git
systemctl enable --now docker

cd /opt
git clone https://github.com/claudio4ndres/foodplease.git
cd foodplease
git checkout feature-cloud

TOKEN=$(curl -s -X PUT "http://169.254.169.254/latest/api/token" -H "X-aws-ec2-metadata-token-ttl-seconds: 300")
PUBLIC_IP=$(curl -s -H "X-aws-ec2-metadata-token: $TOKEN" http://169.254.169.254/latest/meta-data/public-ipv4)

cat > .env <<EOF
DJANGO_SECRET_KEY=$(head -c 32 /dev/urandom | base64)
DJANGO_ALLOWED_HOSTS=${PUBLIC_IP}
POSTGRES_PASSWORD=$(head -c 16 /dev/urandom | base64 | tr -d '=+/')
EOF

docker compose -f docker-compose.prod.yml up -d --build
