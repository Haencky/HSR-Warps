# HSR-Warps
This [file](https://haencky.github.io/HSR-Warps/itemIDs.json) contains IDs to each item in Honkai Star Rail

> [!TIP]
> You can pull it as an docker image:
> ``` bash
> docker pull haenck/hsr-warptracker
> ```

# FAQ
## Banner not showing
Banner only show up if they are connected to an item
It will be created an connected when the limited 5 star item is obtained an added to the Database
You can add an item manually and link the banner to it:

> [!TIP]
> A banner without an item is only represented as `number:` withhout any name after it
> `2XXX` banner are (currently) limited characters and `3XXX` are limited LC

1. Add your item like [here](#add-new-item)
2. Go to the admin page and click on `"Banners" -> "[banner without item]"`
3. Click on `item_id` and select the item you want

# How to use
## Symbols:
- `🎫`: Add new pulls
- `➕`: Manually add new item
- `🚩`: List all banners (newest first)
- `⚙️`: Admin Page

## Add new pulls
1. Click on `🎫`
2. Click on `Paste me to Powershell 📄`
3. Copy your Clipboard to Powershell and hit enter
4. Paste your Clipboard to URL inbox
5. Click on `Add`

> [!WARNING]
> HSR must have created the link. Therefore, open the recordings of the warps ingame before pasting the command to powershell
> When opened HSR will create this URL to connect to the API

## Add new item
> [!NOTE]
> You can always add or edit entries of the DB on the admin page.
> But here the image is downloaded and the ID is set

> [!IMPORTANT]
> The search is **case sensetive**, therefore `Kafka != kafka`
> I would recommend to copy the name directly from the [Wiki](https://honkai-star-rail.fandom.com/wiki/Honkai:_Star_Rail_Wiki)
 
1. Click on `➕`
2. Enter the (english) Name of the item
3. If the Item cant be found some suggestions are provided
4. You will be redirected to the admin page were you should edit the new created item


## List Banners
> [!TIP]
> You can hover over the image to see how much pulls you used and if you won or lost 50/50
> The exterior border is green if you obtained a limited 5 star item
> The inner border is green if you dont obtained a non limited 5 star item

| exterior (left) / inner (right) Border   | Green             | Red                                              |
|--------------------------|-----------------------------------|---------------------------------------------------|
| Green                    | Item obtained; Only limited items | Item obtained; More than 0 non limited 5 Star     |
| Red                      | Item not obtained; No 5 Star      | Item not obtained; More than 0 non limited 5 Star |

