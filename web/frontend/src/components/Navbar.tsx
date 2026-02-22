import { Link } from "react-router-dom"
import { useEffect, useState } from "react"
import jade from '../assets/jade.png'
import './navbar.css'

function Navbar() {

    interface ItemInterface {
        item_id: number;
        typ_name: string; // lc or character
        path_name: string;  // name of path
        path_icon: string;  // url to path icon
        obtained: boolean;
        name: string;
        image: string;
        wiki: string;
        rarity: number;
        eng_name: string;
        typ: number;
        path: number;
    }

    const [query, setQuery] = useState('')
    const [items, setItems] = useState<ItemInterface[]>([])
    const [showDropdown, setShowDropdown] = useState(false)
    const VITE_API_URL = window._env_.BACKEND_URL

    useEffect(() => {
        fetch(`${VITE_API_URL}/api/items`)
            .then(res => res.json())
            .then(data => setItems(data))
            .catch(err => console.error(err))
    }, [])
    const filteredItems = items.filter(item => (item.name.toLowerCase().includes(query.toLowerCase()) || item.eng_name.toLowerCase().includes(query.toLowerCase()))).slice(0,10)

    return (
        <nav className='navbar'>
            <div className='nav-container'>
                <Link to='/'><img src={jade} className='image'/></Link>
                <div className="nav-search">
                    <input 
                        type="text"
                        placeholder="Search..."
                        className="search-input"
                        value={query}
                        onChange={(e) => {
                            setQuery(e.target.value)
                            setShowDropdown(true)
                        }}
                        onFocus={() => setShowDropdown(true)}
                        onBlur={() => setTimeout(() => setShowDropdown(false), 300)}
                    />
                    {showDropdown && query.length > 0 && filteredItems.length > 0 && (
                        <div className="autocomplete-dropdown">
                            {filteredItems.map(item => 
                                <div key={item.item_id}>
                                    <Link 
                                        key={item.item_id}
                                        to={`/details/${item.item_id}`}
                                        className="autocomplete-item"
                                        onClick={() => {
                                            setQuery("")
                                            setShowDropdown(false)
                                        }}
                                    >
                                        {item.name}
                                    </Link>
                                </div>
                            )}
                        </div>
                    )}
                    {showDropdown && query.length > 0 && filteredItems.length === 0 && (
                        <div className="autocomplete-dropdown">
                            <div key='missing' className="autocomplete-item">
                                <Link to={'/add/item'} style={{
                                    color: "inherit",
                                    textDecoration:"none"
                                }}>
                                    Item not showing? Try reloading! <br/>
                                    Or add an item by clicking!
                                </Link>
                            </div>
                        </div>
                    )}
                </div>
                <div className='nav-icons'>
                    <Link to='/add' className='icon-link'>🎫</Link>
                    <Link  to='/add/item' className='icon-link'>➕</Link>
                    <Link to='/banners' className='icon-link'>🚩</Link>
                    <Link to='/items' className='icon-link'>🎁</Link>
                    <Link to={`${VITE_API_URL}/admin`} className='icon-link'>⚙️</Link>
                </div>
            </div>
        </nav>
    )
}

export default Navbar