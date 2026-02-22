#!/bin/bash

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}--- HSR Warp Tracker Installer ---${NC}"

OS_TYPE="Linux"
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" || "$OSTYPE" == "win32" ]]; then
    OS_TYPE="Windows"
    echo -e "${YELLOW}System erkannt: Windows (Git Bash/Cygwin)${NC}"
fi

echo "Get docker-compose from Github"
curl -sSL https://raw.githubusercontent.com/Haencky/HSR-Warps/refs/heads/main/docker-compose.yml -o docker-compose.yml

read -p "Path to Database [./db.sqlite3]: " DB_INPUT
read -p "Path to media folder [./media]: " MEDIA_INPUT

DB_PATH=$(echo $DB_INPUT | sed 's/\\/\//g')
MEDIA_PATH=$(echo $MEDIA_INPUT | sed 's/\\/\//g')

DB_PATH=${DB_PATH:-./db.sqlite3}
MEDIA_PATH=${MEDIA_PATH:-./media}
mkdir -p "$(dirname "$DB_PATH")"

if [ ! -f "$DB_PATH" ]; then
    echo "Create Database File in $DB_PATH..."
    touch "$DB_PATH"
fi

if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    LOCAL_IP=$(ipconfig.exe | grep -i "IPv4" | grep -v "127.0.0.1" | awk -F': ' '{print $2}' | head -n 1 | tr -d '\r')
else
    LOCAL_IP=$(hostname -I 2>/dev/null | awk '{print $1}')
    if [ -z "$LOCAL_IP" ]; then
        LOCAL_IP=$(ip route get 1 2>/dev/null | awk '{print $7}')
    fi
fi

echo -e "System-IP: \033[0;32m$LOCAL_IP\033[0m"
read -p "Under which IP/domain should the API be accessible? [$LOCAL_IP]: " USER_IP
API_URL_IP=${USER_IP:-$LOCAL_IP}

FINAL_API_URL="http://$API_URL_IP:8000"

echo -e "Die API wurde konfiguriert auf: \033[0;34m$FINAL_API_URL\033[0m"

read -p "Allowed Hosts [localhost,127.0.0.1,$FINAL_API_URL]: " ALLOWED_HOSTS
ALLOWED_HOSTS=${ALLOWED_HOSTS:-127.0.0.1,localhost,$FINAL_API_URL}

echo -e "${YELLOW}Create .env ...${NC}"
cat <<EOF > .env
DB_PATH=$DB_PATH
MEDIA_PATH=$MEDIA_PATH
ALLOWED_HOSTS=$ALLOWED_HOSTS
CORS_ALLOWED_ORIGINS=http://localhost:5173,$FINAL_API_URL
VITE_API_URL=$FINAL_API_URL
EOF

if ! command -v docker &> /dev/null; then
    echo -e "\033[0;31mError: Couldnt find docker, please install docker (desktop)!\033[0m"
    exit 1
fi

echo -e "${GREEN}Starting Container...${NC}"
docker compose pull
docker compose up -d

echo "Waiting for database..."
sleep 5

echo -e "${GREEN}Running migrations...${NC}"
docker compose exec backend python manage.py migrate

echo -e "${YELLOW}Prüfe vorhandene Admin-Accounts...${NC}"

EXISTING_ADMINS=$(docker compose exec -T backend python manage.py shell <<EOF
from django.contrib.auth import get_user_model
User = get_user_model()
admins = User.objects.filter(is_superuser=True).values_list('username', flat=True)
print(", ".join(admins))
EOF
)

if [ -n "$EXISTING_ADMINS" ]; then
    echo -e "${GREEN}Existing admins: $EXISTING_ADMINS${NC}"
    read -p "Do you want to create a new admin account (y/N)[n]: " CREATE_AGAIN
    CREATE_AGAIN=${CREATE_AGAIN:-n}

    if [[ "$CREATE_AGAIN" =~ ^[yY]$ ]]; then
        docker compose exec backend python manage.py createsuperuser
    else
        echo "Skip creating admin accounts"
    fi
else
    echo -e "${YELLOW}No admin accounts found. Begin creation...${NC}"
    docker compose exec backend python manage.py createsuperuser
fi

echo -e "${GREEN}Done! All is up and running!${NC}"