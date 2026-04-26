import { useState, useEffect } from "react";
import { useParams, Link } from "react-router-dom";
import { BarChart, Bar, YAxis, XAxis, Tooltip, ResponsiveContainer } from "recharts";
import specialpass from '../assets/specialpass.png'
import jade from '../assets/jade.png'

function DetailBanner () {
   // ... Interfaces bleiben identisch
   interface Warp { id: number; item_name: string; item_image: string; uid: number; time: string; item_id: number; item_rarity: number; }
   interface Item { item_id: number; count: number; name: string; image: string; rarity: number; }
   interface Type { name: string; item_id__typ: number; count: number; }
   interface Rarity { item_id__rarity: number; count: number; }
   interface Banner { id: number; gacha_id: number; gacha_type: number; item_id: number | null; item_image: string | null; item_name: string | null; }

   const [banner, setBanner] = useState<Banner>()
   const [warps, setWarps] = useState<Warp[]>([])
   const [items, setItems] = useState<Item[]>([])
   const [types, setTypes] = useState<Type[]>([])
   const [rarities, setRarities] = useState<Rarity[]>([])
   const [stars, setStars] = useState<number[]>([4,5])
   const { id } = useParams()
   const VITE_API_URL = window._env_.BACKEND_URL

   const changeStars = (star: number) => {
        setStars(prevS => prevS.includes(star) ? prevS.filter(item => item !== star) : [...prevS, star])
    }

    const c = { 3: '#7dd3fc', 4: '#a855f7', 5: '#eab308' }

    const barData = rarities.map((i) => ({
        name: `${i.item_id__rarity}⭐`,
        value: i.count,
        rarity: i.item_id__rarity,
        fill: c[i?.item_id__rarity as keyof typeof c]
    }))

   useEffect(() => {
    fetch(`${VITE_API_URL}/api/banner/${id}`)
        .then(res => res.json())
        .then(data => {
            setBanner(data['b'])
            setWarps(data['warps'])
            setItems(data['items'])
            setTypes(data['types'])
            setRarities(data['rarities'])
        })
        .catch(err => console.error(err))
   }, [id, VITE_API_URL])

   const getRarityBorder = (rarity: number) => {
    if (rarity === 3) return "border-sky-300";
    if (rarity === 4) return "border-purple-500";
    if (rarity === 5) return "border-amber-500";
    return "border-gray-400";
   }

   return (
    // h-screen und overflow-hidden verhindert das Scrollen der gesamten Seite
    <div className="mt-16 p-4 h-[calc(100vh-64px)] overflow-hidden grid grid-cols-1 md:grid-cols-2 gap-4 grid-rows-[auto_1fr]">
        
        {/* Header Sektion: Banner Bild & Stats */}
        <div className="md:col-span-2 flex flex-col md:flex-row gap-4 h-auto max-h-[40vh]">
            <img 
                src={`${VITE_API_URL}${banner?.item_image}`}
                alt="Banner"
                className="hidden md:block w-auto max-h-[30vh] object-contain rounded-lg cursor-pointer"
                onClick={() => banner?.item_id === null && window.open(`${VITE_API_URL}/admin/warptracker/banner/${banner?.id}/change`)}
            />
            <div className="flex-1 grid grid-cols-1 lg:grid-cols-[250px_1fr] gap-4 p-4 rounded-xl border border-white/5 backdrop-blur-md bg-white/5 overflow-hidden">
                <div className="flex flex-col justify-center">
                    <h1 className="text-xl font-bold mb-2 truncate">{banner?.item_name || banner?.gacha_id}</h1>
                    <table className="text-sm border-separate border-spacing-y-1">
                        <tbody>
                            <tr>
                                <td><img src={specialpass} alt="Pass" className="h-6 w-auto" /></td>
                                <td className="text-right font-mono">{warps.length}</td>
                            </tr>
                            <tr>
                                <td><img src={jade} alt="Jade" className="h-6 w-auto" /></td>
                                <td className="text-right font-mono">{(warps.length * 160).toLocaleString()}</td>
                            </tr>
                            {types.map((t) => (
                                <tr key={t.item_id__typ}>
                                    <td className="text-gray-400 text-xs uppercase">{t.name}</td>
                                    <td className="text-right font-mono text-xs">
                                        {t.count} <span className="text-gray-500">({((t.count / warps.length) * 100).toFixed(1)}%)</span>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
                <div className="h-full min-h-[150px]">
                    <ResponsiveContainer width="100%" height="100%">
                        <BarChart data={barData} baseValue={1}>
                            <YAxis scale="log" domain={[0.5, 'auto']} hide/>
                            <XAxis dataKey="name" stroke="#888" fontSize={12} />
                            <Tooltip contentStyle={{backgroundColor: '#1a1a1a', border: '1px solid #333'}} />
                            <Bar dataKey="value" />
                        </BarChart>
                    </ResponsiveContainer>
                </div>
            </div>
        </div>

        {/* Untere Sektion: Items (Links) & Warps (Rechts) */}
        <div className="flex flex-col overflow-hidden border border-white/5 bg-black/20 rounded-xl p-3">
            <h2 className="text-lg font-bold mb-2 border-b border-white/10 pb-1">Items</h2>
            <div className="overflow-y-auto pr-2 custom-scrollbar flex flex-wrap gap-3 content-start">
                {items.sort((a,b) => (a.item_id === banner?.item_id ? -1 : 1)).map((i) => 
                    <Link to={`/details/${i.item_id}`} key={i.item_id} className="group">
                        <div className={`relative border-2 rounded-lg transition-transform group-hover:scale-105 ${getRarityBorder(i.rarity)}`}
                             style={{ filter: i.item_id === banner?.item_id ? 'drop-shadow(0 0 4px #eab308)' : '' }}>
                            <img src={`${VITE_API_URL}/media/${i.image}`} alt="" className="w-16 h-20 rounded-md object-cover" />
                            <div className='absolute bottom-0 right-0 bg-black/60 px-1 rounded-tl-md text-[10px] font-bold text-white'>{i.count}</div>
                        </div>
                    </Link>
                )}
            </div>
        </div>

        <div className="flex flex-col overflow-hidden border border-white/5 bg-black/20 rounded-xl p-3">
            <div className="flex justify-between items-center mb-2 border-b border-white/10 pb-1">
                <h2 className="text-lg font-bold">Warps</h2>
                <div className="flex gap-1">
                    {[3,4,5].map((s) => (
                        <button key={s} 
                            className={`px-2 py-0.5 text-xs rounded-md border transition-colors ${stars.includes(s) ? 'bg-white/10 border-white/20' : 'opacity-30 border-transparent'}`}
                            onClick={() => changeStars(s)}> {s}⭐ </button>
                    ))}
                </div>
            </div>
            <div className="overflow-y-auto custom-scrollbar">
                <table className="w-full text-xs">
                    <thead className="sticky top-0 bg-neutral-900 shadow-sm">
                        <tr>
                            <th className="text-left p-2">Item</th>
                            <th className="text-right p-2">Time</th>
                        </tr>
                    </thead>
                    <tbody>
                        {[...warps].filter(w => stars.includes(w.item_rarity)).sort((a,b) => b.id - a.id).map((w) => (
                            <tr key={w.id} className={`hover:bg-white/5 border-b border-white/5 ${w.item_rarity === 5 ? 'text-amber-500 font-bold' : w.item_rarity === 4 ? 'text-purple-400' : 'text-gray-400'}`}>
                                <td className="p-2"><Link to={`/details/${w.item_id}`}>{w.item_name}</Link></td>
                                <td className="p-2 text-right opacity-60 font-mono">{w.time?.split('T')[0] || '-'}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    </div>
   )
}

export default DetailBanner;