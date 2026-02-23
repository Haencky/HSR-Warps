# HSR Warptracker
Django and React based Gacha-Tracker for Honkai Starrail

## Get your containers up and running!
``` bash
curl -sSL https://raw.githubusercontent.com/Haencky/HSR-Warps/refs/heads/main/install.sh -o install.sh && chmod +x install.sh && ./install.sh
```

> [!CAUTION]
> Items will be added after a delay of about 3-5 days after their release. <br>
> Adding items manually will fail unless the item is added in Item IDs.json in this repository

> [!CAUTION]
> This repository will get some fixes and upgrades in the future <br>
> Please note that the desktop app is currently not working to to chaanges on the backend

## Migration
> [!CAUTION]
> I kind of screwed up by renaiming the django app from `warps` $\rightarrow$ `warptracker`, sorry!<br>
> if you are new it has no effect on you. <br>
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
