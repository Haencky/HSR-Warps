import { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import './details.css'

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
    const VITE_API_URL = import.meta.env.VITE_API_URL

    const c = {
        3: 'lightblue',
        4: 'darkviolet',
        5: 'goldenrod'
    }

    useEffect(() =>  {
        fetch(`${VITE_API_URL}/api/details/${id}`)
            .then(res => res.json())
            .then(data => setItem(data))
            .catch(err => console.error(err))
    }, [id])
    
    return (
        <div className="item-content-details">
            <h1 className={`hr${item?.rarity}`}>{item?.name}</h1>
            {item?.name !== item?.eng_name
                ? <h2 className={`hr${item?.rarity}`}>{item?.eng_name}</h2>
                : ``
            }
            {item?.image && (
                <div className="detail-content" style={{backgroundImage: `url(${VITE_API_URL}${item.image})`}}>
                    <div className="info-overlay">
                        <div
                            className={`count-detail`}
                            style={{filter: 
                                `drop-shadow(0 0 5px ${c[item?.rarity as keyof typeof c] || 'white'})
                                drop-shadow(0 0 15px ${c[item?.rarity as keyof typeof c] || 'white'})`
                            }}
                        > 
                        {item.obtained}
                        </div>
                        <div className="path">
                            <img 
                                src={`${VITE_API_URL}${item.path_icon}`}
                                alt={item.path_name}
                            />
                        </div>
                    </div>
                </div>
            )}
        </div>
    )
}

export default Details