# HSR Warptracker
Django and React based Gacha-Tracker for Honkai Starrail

## Get your containers up and running!
```yaml
services:
  backend:
    image: haenck/hsr-warptracker-backend:latest # dont change
    volumes:
      - ./db.sqlite3:/app/db.sqlite3 # change the path to actual db
      - ./media:/app/media # change path to acutal media folder
    ports:
      - "8000:8000" # dont change
    environment:
      - ALLOWED_HOSTS=localhost,127.0.0.1 # * for allow all
      - CORS_ALLOWED_ORIGINS=http://localhost:5173 # url and port react is running
  
  frontend:
    image: haenck/hsr-warptracker-frontend:latest # dont change
    ports:
      - "5173:80" # dont change
```

> [!CAUTION]
> Items will be added after a delay of about 3-5 days after their release. <br>
> Adding items manually will fail unless the item is added in Item IDs.json in this repository

> [!CAUTION]
> This repository will get some fixes and upgrades in the future <br>
> Please note that the desktop app is currently not working to to chaanges on the backend

## Getting started
1. Create a media *folder* and a db.sqlite3 *file* where you want
2. Change the **values** (behind `=`) for your purposes (e.g. new path or url) in `docker-compose.yml`
3. Run `docker compose up -d`
4. Run `docker exec -it {backend-container} sh` to enter the container
  1. Run `python manage.py makemigrations`
  2. Run `python manage.py migrate` to migrate the db file
  3. Run `python manage.py createsuperuser` and follow instructions
  4. Hit `CTRL + d` to exit the container
5. Your containers should be running!

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
