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
> [!TIP]
> Keep an eye on the [announcements](https://github.com/Haencky/HSR-Warps/discussions/categories/announcements)! <br>
> New features, updates and bugfixes will be diplayed there.

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
  - `Dockerhub`: Link to backend docker image
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
## 📦 External Assets & Data

This application does not bundle game assets or third-party data to keep the footprint small and respect copyright. Instead, it downloads them upon first request:

- **Images & Icons**: Character and item graphics are downloaded from the **[Mar-7th/StarRailRes](https://github.com/Mar-7th/StarRailRes)** repository and stored locally in the `/media` folder.
-   **Game Information**: Character and light cone details are fetched dynamically from **[prydwen.gg](https://www.prydwen.gg/star-rail/)**.

**Note on Local Storage:** Once downloaded, assets are kept locally to reduce bandwidth for both the user and the host providers. These files remain the intellectual property of **HoYoverse** or the respective contributors.

Copyright (c) 2026 Haencky
