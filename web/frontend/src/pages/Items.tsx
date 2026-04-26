import { useState, useEffect } from "react"
import { Link } from "react-router-dom";

function Items() {
    interface Path {
        id: number;
        name: string;
        icon: string;
    }

    interface ItemType {
        id: number;
        name: string
    }

     interface Item {
        item_id: number;
        typ_name: string;
        path_name: string;
        path_icon: string;
        obtained: number;
        name: string;
        image: string;
        wiki: string;
        rarity: number;
        eng_name: string;
        typ: number;
        path: number;
    }

    const [stars, setStars] = useState([3,4,5])
    const [types, setTypes] = useState<number[]>([])
    const [allTypes, setAllTypes] = useState<ItemType[]>([])
    const [items, setItems] = useState<Item[]>([])
    const [order, setOrder] = useState('count')
    const [allPaths, setAllPaths] = useState<Path[]>([])
    const [paths, setPaths] = useState<number[]>([])
    const [showPathDD, setShowPathDD] = useState(false)
    const VITE_API_URL = window._env_.BACKEND_URL

    useEffect(() => {
        fetch(`${VITE_API_URL}/api/items`)
            .then(res => res.json())
            .then(data => setItems(data))
            .catch(err => console.error(err))
        fetch(`${VITE_API_URL}/api/item_types`)
            .then(res => res.json())
            .then(data => {
                setTypes(() => data.map((i:ItemType) => i.id))
                setAllTypes(data)
            })
            .catch(err => console.error(err))
        fetch(`${VITE_API_URL}/api/paths`)
            .then(res => res.json())
            .then(data => {
                setPaths(() => data.map((p: Path) => p.id))
                setAllPaths(data)
            })
            .catch(err => console.error(err))
    }, [])

    const filteredItems = items.filter(item => (stars.includes(item.rarity) && types.includes(item.typ))).sort((a, b) => {
        if(order === 'count') {
            return b.obtained - a.obtained
        } else if (order === 'rarity') {
            return a.rarity - b.rarity
        } else if (order === 'name') {
            return a.name.localeCompare(b.name)
        } else if (order === 'path') {
            return a.path_name.localeCompare(b.path_name)
        }
        return 0
    })

    const changeStars = (star: number) => {
        setStars(prevS => prevS.includes(star) ? prevS.filter(item => item !== star) : [...prevS, star])
    }

    const changeTypes = (t: number) => {
        setTypes(prevT => prevT.includes(t) ? prevT.filter(item => item !== t) : [...prevT, t])
    }

    const changePaths = (p: number) => {
        setPaths(prevP => prevP.includes(p) ? prevP.filter((item) => item !== p) : [...prevP, p])
    }

    const getRarityClass = (rarity: number) => {
        if (rarity === 3) return "border-sky-300"
        if (rarity === 4) return "border-purple-500"
        if (rarity === 5) return "border-amber-500"
        return "border-gray-400"
    }

    return (
        <div className="min-h-screen mt-20 p-5">
            <div className="flex flex-row flex-wrap gap-[10px] m-5 justify-center">
                {[3, 4, 5].map((s) => (
                    <button 
                        key={s} 
                        className={`px-4 py-1 rounded-full border-2 transition-colors ${stars.includes(s) ? 'border-green-600 bg-green-600/10' : 'border-gray-500 text-gray-500'} ${getRarityClass(s)}`} 
                        onClick={() => changeStars(s)}
                    > 
                        {s}⭐ 
                    </button>
                ))}
                
                {allTypes.map((t) => (
                    <button 
                        key={t.id} 
                        className={`px-4 py-1 rounded-full border-2 transition-colors ${types.includes(t.id) ? 'border-green-600 bg-green-600/10' : 'border-gray-500 text-gray-500'}`} 
                        onClick={() => changeTypes(t.id)}
                    > 
                        {t.name} 
                    </button>
                ))}

                <select 
                    value={order} 
                    onChange={(e) => setOrder(e.target.value)} 
                    className="rounded-full border border-gray-300 px-3 py-1 bg-transparent"
                >
                    <option value='count' className="bg-neutral-800">Count</option>
                    <option value='rarity' className="bg-neutral-800">Rarity</option>
                    <option value='name' className="bg-neutral-800">Name (A-Z)</option>
                </select>

                <div className="relative inline-block">
                    <button 
                        className="px-[15px] py-2 rounded-full border border-gray-300 cursor-pointer" 
                        onClick={() => setShowPathDD(!showPathDD)}
                    >
                        Paths ▾
                    </button>
                    {showPathDD && (
                        <div className="absolute top-full left-0 mt-1 bg-[#242424] z-[100] border border-gray-400 rounded-lg shadow-xl p-[10px] min-w-[200px] max-h-[300px] overflow-y-auto">
                            <div className="flex justify-between text-xs text-whitesmoke cursor-pointer pb-1">
                                <span onClick={() => setPaths(allPaths.map(p => p.id))}>All</span>
                                <span onClick={() => setPaths([])}>None</span>
                            </div>
                            <hr className="border-gray-600 my-1" />
                            {allPaths.map(p => (
                                <label key={p.id} className="flex items-center p-1 cursor-pointer gap-[10px] text-sm hover:bg-black rounded">
                                    <input
                                        type="checkbox"
                                        checked={paths.includes(p.id)}
                                        onChange={() => changePaths(p.id)}
                                        className="cursor-pointer"
                                    />
                                    <img src={`${VITE_API_URL}${p.icon}`} className="w-5 h-5" alt="" />
                                    {p.name}
                                </label>
                            ))}
                        </div>
                    )}
                </div>
            </div>

            <div className="p-5" onClick={() => setShowPathDD(false)}>
                {allPaths
                .filter(p => paths.includes(p.id))
                .map((p) => {
                    const pathItems = filteredItems.filter((x) => x.path === p.id)
                    if (!pathItems.length) return null

                    return (
                        <div key={p.id} className="mb-10 flex flex-col">
                            <div className="flex items-center gap-[15px]">
                                <img 
                                    src={`${VITE_API_URL}${p.icon}`}
                                    alt=""
                                    className="w-10 h-10"
                                />
                                <h2 className="m-0 text-2xl font-bold">{p.name}</h2>
                            </div>
                            <hr className="border-0 h-px bg-[#444] mt-[10px] mb-5 w-full" />
                            <div className="flex flex-wrap gap-5 justify-start">
                                {pathItems.map((i) => (
                                    <Link to={`/details/${i.item_id}`} key={i.item_id} className="ml-5 mb-5 group">
                                        <div className={`relative border-[3px] rounded-[20px] transition-transform duration-200 ease-in-out group-hover:scale-105 ${getRarityClass(i.rarity)}`}>
                                            <img 
                                                src={`${VITE_API_URL}${i.image}`}
                                                alt={i.name}
                                                className="w-[120px] h-[160px] rounded-[17px] object-cover block"
                                            />
                                            <div className={`text-center font-bold mt-1 ${i.obtained ? 'text-green-600' : 'text-red-600'}`}>
                                                {i.obtained}
                                            </div>
                                        </div>
                                    </Link>
                                ))}
                            </div>
                        </div>
                    )
                })}
            </div>
        </div>
    )
}

export default Items