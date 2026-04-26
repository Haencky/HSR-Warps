import { useState, useEffect } from "react"
import { Link } from "react-router-dom";

interface BannerInterface {
    gacha_id: number;
    item: string;
    item_image: string;
    item_type: string;
    hsr_gacha_id: number;
    count: number;
    obtained: number;
    ff: number;
    gacha_type: number;
}

interface Typ {
    gacha_type: number;
    name: string;
}

function Banner() {
    const [banner, setBanner] = useState<BannerInterface[]>([])
    const [allTypes, setAllTypes] = useState<Typ[]>([])
    const [types, setTypes] = useState<number[]>([])
    const [order, setOrder] = useState<string>('time-no')
    const VITE_API_URL = (window as any)._env_?.BACKEND_URL || ""

    useEffect(() => {
        fetch(`${VITE_API_URL}/api/gacha_types`)
            .then(res => res.json())
            .then(data => {
                setAllTypes(data)
                setTypes(() => data.map((i: Typ) => i.gacha_type))
            })
            .catch(err => console.error(err))
        fetch(`${VITE_API_URL}/api/banners`)
            .then(res => res.json())
            .then(data => setBanner(data))
            .catch(err => console.error(err))
    }, [VITE_API_URL])

    const changeTypes = (t: number) => {
        setTypes(prevT => 
            prevT.includes(t)
            ? prevT.filter(id => id !== t)
            : [...prevT, t]
        )
    }

    const filteredBanner = banner.filter(b => (types.includes(b.gacha_type))).sort((a, b) => {
        if(order === 'count-hl') return b.count - a.count
        if (order === 'count-lh') return a.count - b.count
        if (order === 'time-no') return b.hsr_gacha_id - a.hsr_gacha_id
        if (order === 'time-on') return a.hsr_gacha_id - b.hsr_gacha_id
        return 0
    })

    return (
        <div className="min-h-[calc(100vh-100px)] mt-[80px] p-5">
            <div className="flex gap-[10px] flex-row mb-5 justify-center">
                {allTypes.filter(i => i.gacha_type !== 1).map((t) => (
                    <button 
                        key={t.gacha_type} 
                        className={`px-4 py-2 rounded transition-colors ${
                            types.includes(t.gacha_type) 
                            ? 'bg-green-600 text-white' 
                            : 'bg-red-500 text-white'
                        }`} 
                        onClick={() => changeTypes(t.gacha_type)}
                    >
                        {t.name}
                    </button>
                ))}
                <select 
                    className="border rounded p-2 bg-white text-black" 
                    value={order} 
                    onChange={(e) => setOrder(e.target.value)}
                >
                    <option value='count-hl' className="text-black">Count ↓</option>
                    <option value='count-lh' className="text-black">Count ↑</option>
                    <option value='time-no' className="text-black">Time ↓</option>
                    <option value='time-on' className="text-black">Time ↑</option>
                </select>
            </div>

            <div className="flex flex-wrap gap-5 justify-center overflow-y-auto">
                {allTypes
                    .filter(t => types.includes(t.gacha_type) && t.gacha_type !== 1)
                    .map((t) => {
                        const typeBanner = filteredBanner.filter((x) => x.gacha_type === t.gacha_type)
                        if (!typeBanner.length) return null

                        return (
                            <div key={t.gacha_type} className="w-full">
                                <div className="mb-2">
                                    <h2 className="m-0 text-2xl font-bold">{t.name}</h2>
                                </div>
                                <hr className="border-0 h-[1px] bg-[#444] mb-5 w-full" />
                                
                                <div className="flex flex-wrap gap-5 justify-start">
                                    {typeBanner.map((b) => (
                                        <Link 
                                            key={b.gacha_id} 
                                            to={`/banner/${b.gacha_id}`} 
                                            className="no-underline text-inherit"
                                        >
                                            <div className="relative mb-5 ml-5 group">
                                                <img
                                                    src={`${VITE_API_URL}${b.item_image}`}
                                                    alt={b.hsr_gacha_id.toString()} 
                                                    className={`
                                                        w-[120px] h-[160px] rounded-[20px] object-cover block transition-transform duration-200 ease-in-out
                                                        group-hover:scale-105 group-hover:opacity-30
                                                        ${b.obtained > 4 ? 'border-[5px] border-green-600' : 'border-[5px] border-red-600'}
                                                    `}
                                                />
                                                <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 text-center opacity-0 group-hover:opacity-100 transition-opacity duration-500 ease-in-out pointer-events-none">
                                                    <span className={`
                                                        px-2 py-0.5 text-[15px] rounded-[10px] text-white font-bold
                                                        ${b.ff ? 'bg-red-600' : 'bg-green-600'}
                                                    `}>
                                                        {b.count}
                                                    </span>
                                                </div>
                                            </div>
                                        </Link>
                                    ))}
                                </div>
                            </div>
                        )
                    })
                } 
            </div>
        </div>
    )
}

export default Banner