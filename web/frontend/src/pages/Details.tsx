import { useState, useEffect } from "react";
import { useParams } from "react-router-dom";

function Details () {
    interface Item {
        item_id: number;
        typ_name: string;
        path_icon: string;
        path_name: string;
        obtained: number;
        name: string;
        image: string;
        wiki: string;
        rarity: number;
        eng_name: string;
    }

    const [item, setItem] = useState<Item>()
    const { id } = useParams()
    const VITE_API_URL = window._env_.BACKEND_URL

    const colors = {
        3: 'text-[#add8e6]', 
        4: 'text-[#a855f7]', 
        5: 'text-[#eab308]'  
    }

    const glowColors = {
        3: '#add8e6',
        4: '#a855f7',
        5: '#eab308'
    }

    useEffect(() =>  {
        fetch(`${VITE_API_URL}/api/details/${id}`)
            .then(res => res.json())
            .then(data => setItem(data))
            .catch(err => console.error(err))
    }, [id, VITE_API_URL])
    
    return (
        <div className="h-[calc(100vh-80px)] mt-20 flex items-center justify-center p-5 overflow-hidden">
            <div className="max-w-6xl w-full h-full grid grid-cols-1 md:grid-cols-2 gap-8 items-center">
                
                {/* Linke Seite: Das Bild */}
                <div className="relative h-full max-h-[80vh] flex items-center justify-center">
                    {item?.image && (
                        <img 
                            src={`${VITE_API_URL}${item.image}`}
                            alt={item.name}
                            className="max-w-full max-h-full object-contain drop-shadow-2xl"
                        />
                    )}
                </div>

                {/* Rechte Seite: Die Infos */}
                <div className="flex flex-col items-center md:items-start text-center md:text-left space-y-6">
                    <div>
                        <h1 className={`text-5xl md:text-6xl font-black uppercase tracking-tighter ${colors[item?.rarity as keyof typeof colors] || 'text-white'}`}>
                            {item?.name}
                        </h1>
                        {item?.name !== item?.eng_name && (
                            <h2 className="text-2xl text-gray-400 font-medium mt-1">
                                {item?.eng_name}
                            </h2>
                        )}
                    </div>

                    <div className="flex items-center gap-8 bg-white/5 backdrop-blur-md p-6 rounded-3xl border border-white/10 shadow-2xl">
                        <div className="flex flex-col items-center">
                            <span className="text-gray-400 text-xs uppercase tracking-widest mb-1">Obtained</span>
                            <div
                                className="text-6xl font-bold text-white tabular-nums"
                                style={{
                                    filter: `drop-shadow(0 0 10px ${glowColors[item?.rarity as keyof typeof glowColors] || 'white'})`
                                }}
                            > 
                                {item?.obtained}
                            </div>
                        </div>

                        <div className="w-px h-16 bg-white/10"></div>

                        <div className="flex flex-col items-center">
                            <span className="text-gray-400 text-xs uppercase tracking-widest mb-2">Path</span>
                            <img 
                                src={`${VITE_API_URL}${item?.path_icon}`}
                                alt={item?.path_name}
                                className="w-12 h-12 object-contain"
                                title={item?.path_name}
                            />
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default Details