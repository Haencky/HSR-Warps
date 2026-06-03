# HSR Warptracker

A Django + React (Vite) based gacha tracker for **Honkai: Star Rail**.

Track your pulls, pity, banners, owned characters/light cones and more — all in a clean self-hosted web interface.

---

## Default Services

| Service | Port | URL |
|---|---|---|
| Frontend | `5173` | http://localhost:5173 |
| Backend API | `8000` | http://localhost:8000 |

---

# 🚀 Installation

> [!TIP]
> If you just want to run this locally and some technical terms confuse you:
>
> Just press `ENTER` to use the default values shown in `[]`.
>
> The defaults work perfectly fine for most users.
>
> Only make sure your paths for:
> - the database file
> - the media folder
>
> are set correctly.
>
> By default they will be created in your current directory.

## Quick Install

```bash
curl -sSL https://raw.githubusercontent.com/Haencky/HSR-Warps/refs/heads/main/install.sh -o install.sh && chmod +x install.sh && ./install.sh
```

---

# 🔄 Updating Docker Compose Containers

To update the application to the newest version:
## 1. Open your Terminal
```bash
cd /your/path/to/docker-compose.yml
```
or open your terminal from file explorer

## 2. Pull the newest images

```bash
docker compose pull
```

## 3. Recreate the containers

```bash
docker compose up -d
```

## 4. Migrate the database
```bash
docker exec -it hsr-backend python manage.py migrate
```

This will:
- download the newest frontend/backend images
- recreate the containers
- keep your mounted database/media files intact
- migrate the database if necessary

---

# ℹ️ Information

> [!TIP]
> Keep an eye on the announcements section:
>
> https://github.com/Haencky/HSR-Warps/discussions/categories/announcements
>
> New features, updates and bugfixes will be posted there.

---


# ⚖️ License & Disclaimer

This project is licensed under the **GNU General Public License v3.0**.

See the `LICENSE` file for details.

## Open Source

You are free to:
- use
- modify
- redistribute

this software under the same license.

## Disclaimer

This is a fan-made project and is **not affiliated with or endorsed by HoYoverse (miHoYo)**.

All game-related assets, characters and names belong to their respective owners.

## No Warranty

This software is provided **"as is"** without any guarantees.

Use it at your own risk.

---

# 📦 External Assets & Data

This application does not bundle game assets or third-party data in order to:
- reduce repository size
- reduce Docker image size
- respect copyright

Assets are downloaded dynamically on first use.

## Sources

### Images & Icons

Character and item assets are downloaded from:

https://github.com/Mar-7th/StarRailRes

Downloaded files are stored locally in the `/media` folder.

### Game Information

Character and Light Cone information is fetched dynamically from:

https://www.prydwen.gg/star-rail/

---

## Local Storage Notice

Once downloaded, assets remain stored locally to:
- reduce bandwidth usage
- improve loading times
- avoid repeated downloads

All assets remain the intellectual property of:
- HoYoverse
- or the respective contributors/owners

---

Copyright (c) 2026 Haencky
