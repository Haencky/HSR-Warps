import { useState, useEffect } from "react"
import { Link } from "react-router-dom";

import './banner.css'
function Banner() {

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

    const [banner, setBanner] = useState<BannerInterface[]>([])
    const [allTypes, setAllTypes] = useState<Typ[]>([])
    const [types, setTypes] = useState<number[]>([])
    const [order, setOrder] = useState<string>('count-hl')
    const VITE_API_URL = import.meta.env.VITE_API_URL

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
    }, [])

    const changeTypes = (t: number) => {
        setTypes(prevT => 
            prevT.includes(t)
            ? prevT.filter(id => id !== t)
            : [...prevT, t]
        )
    }

    const filteredBanner = banner.filter(b => (types.includes(b.gacha_type))).sort((a, b) => {
        if(order === 'count-hl') {
            return b.count - a.count
        } else if (order === 'count-lh') {
            return a.count - b.count
        } else if (order === 'time-no') {
            return b.hsr_gacha_id - a.hsr_gacha_id
        } else if (order === 'time-on') {
            return a.hsr_gacha_id - b.hsr_gacha_id
        }
        return 0
    })

    return (
        <div className="all-content">
            <div className="filter">
                {allTypes.filter(i => i.gacha_type !== 1).map((t) => (
                    <button key={t.gacha_type} className={`t filter-chip ${types.includes(t.gacha_type) ? 'active': 'inactive'}`} onClick={() => changeTypes(t.gacha_type)}>
                        {t.name}
                    </button>
                ))}
                <select className="select-order" value={order} onChange={(e) => setOrder(e.target.value)}>
                    <option value='count-hl'>Count ↓</option>
                    <option value='count-lh'>Count ↑</option>
                    <option value='time-no'>Time ↓</option>
                    <option value='time-on'>Time ↑</option>
                </select>
            </div>
            <div className="content">
                {allTypes
                    .filter(t => types.includes(t.gacha_type) && t.gacha_type !== 1)
                    .map((t) => {
                        const typeBanner = filteredBanner.filter((x) => x.gacha_type === t.gacha_type)

                        if (!typeBanner.length) return null
                        return (
                            <div className="type-section">
                                <div className="type-header">
                                    <h2>{t.name}</h2>
                                </div>
                                <hr className="type-divider" />
                                <div className="type-banner-grid">
                                    {filteredBanner.filter((x) => x.gacha_type === t.gacha_type).map((b) => {
                                        const banner_content = (
                                            <div key={b.gacha_id} className="banner">
                                                <img
                                                    src={`${VITE_API_URL}${b.item_image}`}
                                                    alt={b.hsr_gacha_id.toString()} 
                                                    className={b.obtained > 4? 'obtained banner-image': 'failed banner-image'}
                                                />
                                                <div className="stats">
                                                    <span className={`${b.ff ? 'ff_lost': 'ff_win'} `}>{b.count}</span>
                                                </div>
                                            </div>
                                        )
                                        return b.obtained < 5 ? (
                                            <Link to={`${VITE_API_URL}/admin/warptracker/banner/${b.gacha_id}/change/`} style={{
                                                textDecoration: 'none', 
                                                color: "inherit",
                                                display: "contents"
                                            }}>
                                                {banner_content}
                                            </Link>
                                        ) : banner_content
                                    })}
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