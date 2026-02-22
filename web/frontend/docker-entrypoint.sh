#!/bin/sh

cat <<EOF > /usr/share/nginx/html/config.js
window._env_ = {
  BACKEND_URL: "${VITE_API_URL}"
};
EOF

echo "Using BACKEND_URL=$VITE_API_URL"

nginx -g "daemon off;"