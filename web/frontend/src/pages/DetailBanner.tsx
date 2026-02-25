import { useState, useEffect } from "react";
import { useParams, Link } from "react-router-dom";
import { BarChart, Bar, YAxis, XAxis, Tooltip, ResponsiveContainer } from "recharts";
import './detailbanner.css'
import specialpass from '../assets/specialpass.png'
import jade from '../assets/jade.png'

function DetailBanner () {
   interface Warp {
    id: number;
    item_name: string;
    item_image: string;
    uid: number;
    time: string;
    item_id: number;
    item_rarity: number;
   }

   interface Item {
        item_id: number;
        count: number;
        name: string;
        image: string;
        rarity: number;
   }

   interface Type {
    name: string;
    item_id__typ: number;
    count: number;
   }

   interface Rarity {
    item_id__rarity: number;
    count: number;
   }

   interface Banner {
    id: number;
    gacha_id: number;
    gacha_type: number;
    item_id: number | null;
    item_image: string | null;
    item_name: string | null;
   }

   const [banner, setBanner] = useState<Banner>()
   const [warps, setWarps] = useState<Warp[]>([])
   const [items, setItems] = useState<Item[]>([])
   const [types, setTypes] = useState<Type[]>([])
   const [rarities, setRarities] = useState<Rarity[]>([])
   const [stars, setStars] = useState<number[]>([4,5])
   const { id } = useParams()
   const VITE_API_URL = window._env_.BACKEND_URL

   const changeStars = (star: number) => {
        setStars(prevS => {
            if(prevS.includes(star)) {
                return prevS.filter(item => item !== star)
            } else {
                return [...prevS, star]
            }
        })
    }

    const c = {
        3: 'lightblue',
        4: 'darkviolet',
        5: 'goldenrod'
    }

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
   }, [id])
   return (
    <div className="banner-content-details">
        <div className="overview">
            <img 
                src={`${VITE_API_URL}${banner?.item_image}`}
                alt="Edit"
                onClick={() => banner?.item_id !== null ? '' : window.open(`${VITE_API_URL}/admin/warptracker/banner/${banner?.id}/change`)}
            />
            <div className="dbanner-stats">
                <h1>{banner?.item_name || banner?.gacha_id}</h1>
                <table className="stat-table">
                    <tbody>
                        <tr>
                            <td><img src={specialpass} alt="Pass" /></td>
                            <td>{warps.length}</td>
                        </tr>
                        <tr>
                            <td><img src={jade} alt="Jade" /></td>
                            <td>{(warps.length * 160).toLocaleString()}</td>
                        </tr>
                        {types.map((t) => (
                            <tr key={t.item_id__typ}>
                                <td className="stat-item-label">{t.name}</td>
                                <td>
                                    {t.count} 
                                    <span className="stat-percentage">
                                        ({((t.count / warps.length) * 100).toFixed(2)}%)
                                    </span>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
                <div className="graph">
                    <ResponsiveContainer>
                        <BarChart responsive data={barData} baseValue={1}>
                            <YAxis scale="log" domain={[0.5, 'auto']} hide/>
                            <XAxis dataKey="name" />
                            <Tooltip />
                            <Bar dataKey="value" />
                        </BarChart>
                    </ResponsiveContainer>
                </div>
            </div>
        </div>
        <div className="dbanner-items">
            <h2 className="banner-sub-header">
                Items
            </h2>
            <div className="dbanner-items-grid">
                {items.sort((a,b) => {
                    if ((a.item_id === banner?.item_id) !== (b.item_id === banner?.item_id)) {
                        return (a.item_id === banner?.item_id) ? -1 : 1
                    }
                    return b.count - a.count
                }).map((i) => 
                    <div key={i.item_id} className={`item r${i.rarity}`} style={{
                            filter: 
                                `${i.item_id === banner?.item_id ? 'drop-shadow(0 0 1px goldenrod) drop-shadow(0 0 1px goldenrod)' : ''}`
                            }}
                        >
                        <Link to={`/details/${i.item_id}`}>
                            <img
                                src={`${VITE_API_URL}/media/${i.image}`}
                                alt={`${i.item_id}`}
                            />
                            <div className='count' style={{
                                color: "white"
                            }}>
                                {i.count}
                            </div>
                        </Link>
                    </div>
                )}
            </div>
        </div>
        <div className="dbanner-warps">
            <h2 className="banner-sub-header">Warps</h2>
            <div className="filter"> 
                {[3,4,5].map((s) => (
                    <button key={s} className={`s${s} ${stars.includes(s) ? 'active' : 'inactive'} filter-chip`} onClick={() => changeStars(s)}> {s}⭐ </button>
                ))}
            </div>
            <div className="dbanner-warps-content">
                {stars.length > 0 &&
                    <table className="warps-table">
                        <thead>
                            <tr>
                                <th>Item</th>
                                <th>Time</th>
                            </tr>
                        </thead>
                        <tbody>
                            {[...warps]
                            .filter((w) => stars.includes(w.item_rarity))
                            .sort((a,b) => a.id - b.id)
                            .map((w) => (
                                <tr key={w.id} className={`warp-row hr${w.item_rarity}`}>
                                    <td className="item-cell">
                                        <span className="rarity-indicator"></span>
                                        <Link key={w.item_id} to={`/details/${w.item_id}`} style={{
                                            textDecoration: "none",
                                            color: "inherit"
                                        }}>
                                            {w.item_name}                           
                                        </Link>
                                    </td>
                                    <td className="time">
                                        {w.time.replace('Z', '').replace('T', ' ')}
                                    </td>
                                </tr>
                            ))
                            }
                        </tbody>
                    </table>
                }
            </div>
        </div>
    </div>
   )
}

export default DetailBanner