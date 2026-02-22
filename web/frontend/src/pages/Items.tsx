import { useState, useEffect } from "react"
import { Link } from "react-router-dom";
import './items.css'

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
        typ_name: string; // lc or character
        path_name: string;  // name of path
        path_icon: string;  // url to path icon
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
    const [types, setTypes] = useState<number[]>([]) // current item types
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
        setStars(prevS => {
            if(prevS.includes(star)) {
                return prevS.filter(item => item !== star)
            } else {
                return [...prevS, star]
            }
        })
    }

    const changeTypes = (t: number) => {
        setTypes(prevT => {
            if(prevT.includes(t)) {
                return prevT.filter(item => item !== t)
            } else {
                return [...prevT, t]
            }
        })

    }

    const changePaths = (p: number) => {
            setPaths(prevP => {
                if(prevP.includes(p)) {
                    return prevP.filter((item) => item !== p)
                } else {
                    return [...prevP, p]
                }
            })
        }

    return (
        <div className="item-content">
            <div className="filter">
                {[3,4,5].map((s) => (
                    <button key={s} className={`s${s} ${stars.includes(s) ? 'active' : 'inactive'} filter-chip`} onClick={() => changeStars(s)}> {s}⭐ </button>
                ))}
                {allTypes.map((t) =>
                    <button key={t.id} className={`${types.includes(t.id) ? 'active' : 'inactive'} filter-chip`} onClick={() => changeTypes(t.id)}> {t.name} </button>
                )}
                <select value={order} onChange={(e) => setOrder(e.target.value)} className="select-order">
                    <option value='count'>Count</option>
                    <option value='rarity'>Rarity</option>
                    <option value='name'>Name (A-Z)</option>
                </select>
                <div className="dropdown-container">
                    <button className="dropdown-btn" onClick={() => setShowPathDD(!showPathDD)}>Paths ▾</button>
                    {showPathDD && (
                        <div className="dropdown-menu">
                            <div className="dropdown-actions">
                                <span onClick={() => setPaths(allPaths.map(p => p.id))}>All</span>
                                <span onClick={() => setPaths([])}>None</span>
                            </div>
                            <hr />
                            {allPaths.map(p => (
                                <label key={p.id} className="dropdown-item">
                                    <input
                                        type="checkbox"
                                        checked={paths.includes(p.id)}
                                        onChange={() => changePaths(p.id)}
                                    />
                                    <img src={`${VITE_API_URL}${p.icon}`}/>
                                    {p.name}
                                </label>
                            ))}
                        </div>
                    )}
                </div>
            </div>
            <div className="items" onClick={() => setShowPathDD(false)}>
                {allPaths
                .filter(p => paths.includes(p.id))
                .map((p) => {
                    const pathItems = filteredItems.filter((x) => x.path === p.id)

                    if (!pathItems.length) return null
                    return (
                    
                        <div key={p.id} className="path-section">
                            <div className="path-header">
                                <img 
                                    src={`${VITE_API_URL}${p.icon}`}
                                    alt=""
                                />
                                <h2>{p.name}</h2>
                            </div>
                            <hr className="path-divider" />
                            <div className="path-items-grid">
                                {filteredItems.filter((x) => x.path === p.id).map((i) => 
                                <Link to={`/details/${i.item_id}`}>
                                    <div key={i.item_id} className={`item r${i.rarity}`}>
                                        <img 
                                            src={`${VITE_API_URL}${i.image}`}
                                            alt={i.name}
                                        />
                                        <div className={`count ${i.obtained ? 'obtained' : 'notobtained'}`}>
                                            {i.obtained}
                                        </div>
                                    </div>
                                </Link>
                                )}
                            </div>
                        </div>
                    )
                })}
            </div>
        </div>
    )
}

export default Items