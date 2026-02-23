# HSR Warptracker
Django and React (Vite) based Gacha-Tracker for Honkai Starrail

|**Service**|**Port**|**Most likely URL**|
|---|---|---|
|Frontend| 5173|http://localhost:5173|
|Backend (API)|8000|http://localhost:8000|

## Get your containers up and running!
> [!TIP]
> If you just want to run this on your PC and some technical terms confuse you just hit enter (default values in [] are set). This works just fine. <br>
> Only make sure to set your path to media and db file correct (per default the files will be created/selected in your current directory) <br>
> 

```bash
curl -sSL https://raw.githubusercontent.com/Haencky/HSR-Warps/refs/heads/main/install.sh -o install.sh && chmod +x install.sh && ./install.sh
```
## Info
> [!WARNING]
> Items will be added after a delay of about 3-5 days after their release. <br>
> Adding items manually will fail unless the item is added in Item IDs.json in this repository

> [!CAUTION]
> This repository will get some fixes and upgrades in the future <br>
> Please note that the desktop app is currently not working to to chaanges on the backend

## Migration
> [!CAUTION]
> **If you're new, it doesn't affect you! Only DB created before _2026-02-17_ are damaged.** <br>
> I kind of screwed up by renaming the django app from `warps` $\rightarrow$ `warptracker`, sorry!<br>
> Migrating your old database is possible by connecting to your database (e.g. via DB Browser for SQLite) and running the commands below to rename the old tables.<br>
> Make sure to wirte the changes to your database &  restart the container if running!!!

```sql
ALTER TABLE warps_banner RENAME TO warptracker_banner;
ALTER TABLE warps_gachatype RENAME TO warptracker_gachatype;
ALTER TABLE warps_itemtype RENAME TO warptracker_itemtype;
ALTER TABLE warps_item RENAME TO warptracker_item;
ALTER TABLE warps_path RENAME TO warptracker_path;
ALTER TABLE warps_warp RENAME TO warptracker_warp;

UPDATE django_content_type SET app_label = 'warptracker' WHERE app_label = 'warps';
UPDATE django_migrations SET app = 'warptracker' WHERE app = 'warps';
```

## Coordination
- `Jade-Image`: Home screen displaying current pity and more
- `Search-Bar`: Search for items in your language or english (**only items added in db will be displayed**)
- `🎫`: Paste your URL here (pasted to your clipboard after runnring the command in powershell
- `➕`: Enter the english name of an item you want to add manually
- `🚩`: Dislays your banners
  - By default only banner where you obtained an item will display an item
  - Borders: green (obtained) / red (not obtained)
  - On Hover: count of pulls (green: only limited 5 star item / red: at least one not limited item)
- `🎁`: Display items grouped by paths
- `⚙️`: Link to admin site
- Footer:
  - `Github`: Link to this repo
  - `Dockerhub`: Link to docker images (comming soon)
  - `Item IDs`: Link to a list of all items matching their id

 ---

## ⚖️ License & Disclaimer

This project is licensed under the **GNU General Public License v3.0**. See the `LICENSE` file for details.

- **Open Source**: You are free to use, modify, and redistribute this software under the same license.
- **Disclaimer**: This is a fan-made project and is **not** affiliated with or endorsed by HoYoverse (miHoYo). All game-related assets, characters, and names are the property of their respective owners.
- **No Warranty**: This software is provided "as is" without any guarantees. Use it at your own risk.

**Quick Links:**
- [GitHub Repository](https://github.com/Haencky/HSR-Warps)
- [Dockerhub-Frontend](https://hub.docker.com/repository/docker/haenck/hsr-warptracker-frontend), [Dockerhub-Backend](https://hub.docker.com/repository/docker/haenck/hsr-warptracker-backend)

---

## Credits
- **[prydwen.gg](https://www.prydwen.gg/star-rail/):** Item data
- **[Mar-7th/StarRailRes](https://github.com/Mar-7th/StarRailRes):** Icons and images

Copyright (c) 2026 Haencky
