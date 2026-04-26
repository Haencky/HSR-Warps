import { Link } from "react-router-dom"
import { useEffect, useState, useRef } from "react"
import jade from '../assets/jade.png'

function Navbar() {
    interface ItemInterface {
        item_id: number;
        typ_name: string;
        path_name: string;
        path_icon: string;
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
    const [isUpdating, setIsUpdating] = useState(false)
    const dropdownRef = useRef<HTMLDivElement>(null)
    const VITE_API_URL = window._env_.BACKEND_URL

    useEffect(() => {
        fetch(`${VITE_API_URL}/api/items`)
            .then(res => res.json())
            .then(data => setItems(data))
            .catch(err => console.error(err))

        const handleClickOutside = (event: MouseEvent) => {
            if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
                setShowDropdown(false)
            }
        }
        document.addEventListener("mousedown", handleClickOutside)
        return () => document.removeEventListener("mousedown", handleClickOutside)
    }, [VITE_API_URL])

    const filteredItems = items.filter(item => 
        (item.name.toLowerCase().includes(query.toLowerCase()) || 
         item.eng_name.toLowerCase().includes(query.toLowerCase()))
    ).slice(0, 10)

    const triggerUpdate = async () => {
        setIsUpdating(true)
        try {
            await fetch(`${VITE_API_URL}/api/update`)
            window.location.reload()
        } catch (err) {
            console.error(err)
        } finally {
            setIsUpdating(false)
        }
    }

    return (
        <nav className="bg-[#1a1a1a] w-full fixed top-0 left-0 z-[9999] h-16 border-b border-white/5 flex items-center shadow-lg">
            <div className="container mx-auto px-4 flex items-center justify-between gap-4">
                
                <Link to='/' className="flex items-center gap-2 shrink-0 group">
                    <img 
                        src={jade} 
                        className={`w-8 h-8 transition-transform duration-500 ${isUpdating ? 'animate-spin' : 'group-hover:rotate-12'}`} 
                        alt="Logo" 
                        onClick={(e) => { e.preventDefault(); triggerUpdate(); }}
                    />
                    <span className="hidden sm:block text-xl font-black tracking-tighter text-white">
                        <span className="text-amber-500">WARPS</span>
                    </span>
                    <span className="absolute top-full mt-3 left-0 bg-neutral-800 text-white text-[10px] px-2 py-1 rounded opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none whitespace-nowrap z-50 border border-white/10 shadow-xl">
                        Click on jade to fetch missing images
                    </span>
                </Link>

                <div className="relative flex-grow max-w-md" ref={dropdownRef}>
                    <input
                        type="text"
                        placeholder="Search..."
                        className="w-full bg-black/40 border border-white/10 rounded-full py-2 px-5 text-sm text-white placeholder-gray-500 focus:outline-none focus:border-amber-500/50 transition-all"
                        value={query}
                        onChange={(e) => {
                            setQuery(e.target.value)
                            setShowDropdown(true)
                        }}
                        onFocus={() => setShowDropdown(true)}
                    />

                    {showDropdown && query.length > 0 && (
                        <div className="absolute top-full left-0 right-0 mt-2 bg-[#242424] border border-white/10 rounded-2xl shadow-2xl overflow-hidden max-h-[300px] overflow-y-auto custom-scrollbar">
                            {filteredItems.length > 0 ? (
                                filteredItems.map((item) => (
                                    <Link
                                        key={item.item_id}
                                        to={`/details/${item.item_id}`}
                                        className="block px-5 py-3 text-sm text-gray-200 hover:bg-white/5 border-b border-white/5 last:border-0 transition-colors"
                                        onClick={() => setShowDropdown(false)}
                                    >
                                        <div className="flex justify-between items-center">
                                            <span>{item.name}</span>
                                            <span className="text-[10px] uppercase text-gray-500">{item.typ_name}</span>
                                        </div>
                                    </Link>
                                ))
                            ) : (
                                <Link 
                                    to='/add/item' 
                                    className="block px-5 py-4 text-xs text-amber-500 hover:bg-white/5 transition-colors"
                                    onClick={() => setShowDropdown(false)}
                                >
                                    Item not found? Try reloading! <span className="underline">Or add manually</span>
                                </Link>
                            )}
                        </div>
                    )}
                </div>

                <div className="flex items-center gap-1 sm:gap-4">
                    {[
                        { to: '/add', icon: '🎫', label: 'Import Warps' },
                        { to: '/add/item', icon: '➕', label: 'Add items manually' },
                        { to: '/banners', icon: '🚩', label: 'Banners' },
                        { to: '/items', icon: '🎁', label: 'Items' },
                        { to: `${VITE_API_URL}/admin`, icon: '⚙️', label: 'Admin', external: true },
                    ].map((link) => (
                        link.external ? (
                            <a 
                                key={link.label}
                                href={link.to} 
                                className="w-10 h-10 flex items-center justify-center rounded-full"
                                title={link.label}
                            >
                                {link.icon}
                            </a>
                        ) : (
                            <Link 
                                key={link.label}
                                to={link.to} 
                                className="w-10 h-10 flex items-center justify-center rounded-full "
                                title={link.label}
                            >
                                {link.icon}
                            </Link>
                        )
                    ))}
                </div>
            </div>
        </nav>
    )
}

export default Navbar