import { useState, useEffect } from "react"
import './home.css'

function Home() {
    interface LastWin {
    item_image: string;
    item_name: string;
  }

  interface DashboardType {
    id: number;
    name: string;
    pity: number;
    warranted: boolean;
    wr: number;
    c: number;
    max_pity: number;
    last_win: LastWin | null;
  }

  const [types, setTypes] = useState<DashboardType[]>([])
  const VITE_API_URL = import.meta.env.VITE_API_URL

  useEffect(() => {
    fetchTypes()
  }, [])

  const fetchTypes = async () => {
    try {
      const r = await fetch(`${VITE_API_URL}/api/dashboard`)
      const data = await r.json()
      setTypes(data)
    } catch (err) {
      console.error(err)
    }
  }
  return (
      <div className='types-container'>
        {types.map((t) => (
          <div key={t.id} className='type-container'>
            <div className='type-image'> {t.last_win?.item_image && (
              <img
                src={`${VITE_API_URL}${t.last_win.item_image}`}
                alt={t.last_win.item_name}
              />
            )} 
            </div>
            <div className='type-header'><strong>{t.name}</strong> ({t.c}) </div>
            <div>
              <span className='type-pity'>5⭐ Pity: {t.pity} / </span>
              <span className={t.warranted? 'highlight-yes': 'highlight-no'}>{t.max_pity}</span>
            </div>
            {t.wr !== null && (
              <div className='type-wr'>
                Winrate: {t.wr}%
            </div>
            )}
            <div className='type-money'>
              {t.c * 160} Jade ({(t.c * 2.64).toFixed(2)}€)
            </div>
          </div>
        ))}
      </div>
  )
}

export default Home