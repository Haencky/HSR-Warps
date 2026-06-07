import { useState, useEffect } from "react";

function AddItems() {
    interface Result {
        message: string;
    }

    interface Item {
        id:  string;
        name: string;
        rarity: number; 
    }

    const [itemId, setItemId] = useState('')
    const [items, setItems] = useState<Item[]>([])
    const [isLoading, setIsLoading] = useState(false)
    const [inputValue, setInputValue] = useState("");
    const [filteredItems, setFilteredItems] = useState<Item[]>([]);
    const [isOpen, setIsOpen] = useState(false); 
    const VITE_API_URL = window._env_.BACKEND_URL
    const fribbels_items = 'https://raw.githubusercontent.com/fribbels/hsr-optimizer/refs/heads/main/src/data/game_data.json'
    const image_url = 'https://raw.githubusercontent.com/Mar-7th/StarRailRes/master/'

   useEffect(() => {
        fetch(fribbels_items)
            .then(res => res.json())
            .then(data => {
                const itemList = Object.values(data).flatMap(obj => 
                    Object.entries(obj as Record<string, unknown>)
                        .filter(([key]) => /^\d+$/.test(key))
                        .map(([_, value]) => value)
                ) as Item[];
                
                setItems(itemList);
            })
            .catch(err => console.error("Error loading data:", err));
    }, []);

    const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const val = e.target.value;
        setInputValue(val);
        setIsOpen(true);

        if (val.trim() === "") {
            setFilteredItems([]);
            setItemId("");
            return;
        }
        const matches = items.filter(item => 
            item.name.toLowerCase().includes(val.toLowerCase())
        );
        matches.sort((a,b) => a.name.localeCompare(b.name))
        setFilteredItems(matches);
    };

    const handleSelectResult = (item: Item) => {
        setInputValue(item.name);
        setItemId(item.id);
        setIsOpen(false);
    };
    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault()
        if(!itemId) return
        setIsLoading(true)

        try {
            const r = await fetch(`${VITE_API_URL}/api/add_item`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({item_id: itemId})
            })
            const data: Result = await r.json()
            const msg = data['message']
            alert(msg)
            setIsLoading(false)
        } catch (err) {
            console.error(err)
        }
    } 

   return (
        <div className="bg-transparent p-10 rounded-xl max-w-[400px] w-full mx-auto my-[5vh] box-border">
            <form className="flex flex-col gap-4" onSubmit={handleSubmit}>
                <div className="relative w-full">
                    <input 
                        type="text"
                        className="w-full p-3 border border-gray-300 rounded-lg bg-white text-black shadow-sm focus:outline-none focus:ring-2 focus:ring-[#28a745] focus:border-transparent transition-all"
                        placeholder="Search for characters or lightcones"
                        value={inputValue}
                        onChange={handleInputChange}
                        onFocus={() => setIsOpen(true)}
                        onBlur={() => setTimeout(() => setIsOpen(false), 200)} 
                    />
                    
                    {isOpen && filteredItems.length > 0 && (
                        <div className="absolute top-full left-1/2 -translate-x-1/2 z-50 w-[200%] max-h-[450px] mt-2 overflow-y-auto bg-white border border-gray-100 rounded-2xl shadow-2xl p-4 text-black scrollbar-thin">
                            <div className="grid grid-cols-3 gap-4">
                                {filteredItems.filter(i => i.rarity === 5 && i.name != "Trailblazer" && Number(i.id) < 24000).map((item) => {
                                    const isLightcone = Number(item.id) >= 20000;
                                    return (
                                        <button
                                            key={item.id}
                                            type="button"
                                            onClick={() => handleSelectResult(item)}
                                            title={item.name}
                                            className="relative aspect-square overflow-hidden bg-gray-50 border border-gray-200 cursor-pointer rounded-xl p-0 focus:outline-none hover:border-gray-400 hover:shadow-xl transition-all duration-200 group"
                                        >
                                            <img 
                                                src={`${image_url}image/${
                                                    isLightcone ? "light_cone" : "character"
                                                }_portrait/${item.id}.png`}
                                                alt={item.name}
                                                className="w-full h-full object-cover transition-transform duration-300 group-hover:scale-105"
                                                loading="lazy"
                                            />
                                            <div className="absolute inset-0 bg-black/50 opacity-0 group-hover:opacity-100 transition-opacity duration-200 flex items-end p-3">
                                                <span className="text-white text-sm font-medium truncate w-full text-center">
                                                    {item.name}
                                                </span>
                                            </div>
                                        </button>
                                    );
                                })}
                            </div>
                        </div>
                    )}
                </div>
                
                <button 
                    className="w-full py-3 bg-[#28a745] hover:bg-[#218838] text-white rounded-lg font-bold shadow-md hover:shadow-lg disabled:bg-gray-400 disabled:shadow-none transition-all"
                    disabled={isLoading || !itemId} 
                    type="submit"
                >
                    {isLoading ? 'Adding...' : 'Add'}
                </button>
            </form>
        </div>
    )
}

export default AddItems