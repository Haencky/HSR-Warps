import { useState, useEffect } from "react"
import { Link } from "react-router";

function Home() {
  interface LastWin {
    item_id__image: string;
    item_id__name: string;
  }

  interface Warp { id: number; item_name: string; uid: number; time: string; item_id: number; item_rarity: number; item_eng_name: string; pity: number; warp_id: number}

  interface DashboardType {
    id: number;
    gacha_type: number;
    name: string;
    pity: number;
    warranted: boolean;
    wr: number;
    c: number;
    max_pity: number;
    last_win: LastWin | null;
    avg_pity: number;
  }

  const [types, setTypes] = useState<DashboardType[]>([])
  const [selectedId, setSelectedId] = useState<number | null>(null)
  const [stars, setStars] = useState<number[]>([4,5])
  const [searchTerm, setSearchTerm] = useState("")
  const [warps, setWarps] = useState<Warp[]>([])
  const [isLoading, setIsLoading] = useState<boolean>(false)
  const VITE_API_URL = window._env_.BACKEND_URL

  useEffect(() => {
    fetchTypes()
  }, [])

  const selectedType = types.find(t => t.id === selectedId);

  const fetchTypes = async () => {
    try {
      const r = await fetch(`${VITE_API_URL}/api/dashboard`)
      const data = await r.json()
      setTypes(data)
    } catch (err) {
      console.error(err)
    }
  }

  const fetchWarps = async (gachaID: number) => {
    setIsLoading(true)
    await fetch(`${VITE_API_URL}/api/detail-types/${gachaID}`)
      .then(res => res.json())
      .then(data => setWarps(data.warps))
      .catch(e => console.error(e)) 
    setIsLoading(false)
  }

  useEffect(() => {
    if (selectedId) {
      fetchWarps(selectedId)
    }
  }, [selectedId])

  return (
    <div className="mt-20 p-6 w-full min-h-[calc(100vh-80px)]">
      <div className={`transition-all duration-500 ${
        selectedId 
          ? "grid grid-cols-1 lg:grid-cols-[450px_1fr] gap-8 items-start" 
          : "flex flex-wrap gap-8 justify-center"
      }`}>
        

        <div className={`flex flex-wrap gap-8 ${selectedId ? "flex-col w-full" : "justify-center"}`}>
          {types.map((t) => (
            <div 
              key={t.id} 
              onClick={() => setSelectedId(t.id)}
              className={`cursor-pointer relative overflow-hidden rounded-2xl bg-neutral-900/50 border shadow-2xl backdrop-blur-sm transition-all duration-300 hover:scale-[1.02] w-full max-w-[450px] grid grid-cols-[120px_1fr] gap-4 p-4
                ${selectedId === t.id ? "border-amber-500/50 ring-1 ring-amber-500/20" : "border-white/10 hover:border-white/20"}
              `}
            >
          <div className="flex items-center justify-center bg-black/40 rounded-xl overflow-hidden h-[120px]">
            {t.last_win?.item_id__image ? (
              <img
                src={`${VITE_API_URL}${t.last_win.item_id__image}`}
                alt={t.last_win.item_id__name}
                className="w-full h-full object-cover"
              />
            ) : (
              <div className="text-gray-600 text-xs text-center p-2">{t.last_win?.item_id__name}</div>
            )}
          </div>

          <div className="flex flex-col justify-between py-1">
            <div className="flex justify-between items-start">
              <h3 className="text-lg font-bold text-white leading-tight">
                {t.name}
              </h3>
              <span className="text-xs bg-white/10 px-2 py-1 rounded text-gray-400">
                Total: {t.c}
              </span>
            </div>

            <div className="space-y-1 mt-2">
              <div className="text-sm">
                <span className="text-gray-400 uppercase text-[10px] tracking-wider block">Current Pity</span>
                <span className="text-amber-500 font-mono text-lg font-bold">
                  {t.pity} <span className="text-gray-500 font-normal">/</span> {t.max_pity}
                </span>
                {t.warranted && (t.gacha_type !== 1 && t.gacha_type !== 2) && (
                  <span className="ml-2 text-[10px] bg-amber-500/20 text-amber-500 px-1.5 py-0.5 rounded uppercase font-bold">
                    Guaranteed
                  </span>
                )}
              </div>

                <div className="text-sm">
                  <span className="text-gray-400 uppercase text-[10px] tracking-wider inline-block mr-2">Expected Pulls:</span>
                  <span className="text-white font-mono">{t.avg_pity}</span>
                  {t.wr !== null && (t.gacha_type !== 1 && t.gacha_type !== 2) && (
                    <div>
                      <span className="text-gray-400 uppercase text-[10px] tracking-wider inline-block mr-2">Winrate:</span>
                      <span className="text-white font-mono">{t.wr}%</span>
                    </div>
                  )}
                </div>
            </div>

            <div className="mt-3 pt-2 border-t border-white/5 flex justify-between items-baseline">
                <span className="text-green-400 font-mono text-sm">{t.c * 160} Jade</span>
                <span className="text-gray-500 text-xs">{(t.c * 2.64).toFixed(2)}€</span>
            </div>
          </div>
        </div>
        ))}
        </div>
        <div>
        {selectedId && (
        <div className="w-full bg-neutral-900/30 border border-white/5 rounded-2xl p-6 min-h-[600px] animate-in fade-in slide-in-from-right-4 duration-500 min-w-0">
          <div className="flex justify-between items-center mb-6">
             <h2 className="text-2xl font-bold text-white">{selectedType?.name}</h2>
             <button 
               onClick={() => setSelectedId(null)}
               className="text-gray-400 hover:text-white text-sm"
             >
              Close ✕
             </button>
          </div>
          <div className="text-gray-400">
            {selectedType && (
  <div className="w-full space-y-4 animate-in fade-in slide-in-from-right-4 duration-500">

  <div className="flex flex-col sm:flex-row justify-between items-center mb-4 gap-3 border-b border-white/10 pb-3">
    
    <div className="relative w-full max-w-md">
      <input
        type="text"
        placeholder={`Search in ${selectedType.name}...`}
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
        className="w-full bg-white/5 border border-white/10 rounded-lg py-1.5 pl-3 pr-10 text-sm text-white placeholder-gray-500 focus:outline-none focus:ring-1 focus:ring-amber-500/50 transition-all"
      />
      {searchTerm && (
        <button 
          onClick={() => setSearchTerm("")}
          className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-500 hover:text-white"
        >
          ✕
        </button>
      )}
    </div>
    <div className="flex gap-1">
      {[3, 4, 5].map((s) => (
        <button key={s} 
          className={`px-2 py-0.5 text-xs rounded-md border transition-colors ${
            stars.includes(s) ? 'bg-white/10 border-white/20 text-white' : 'opacity-30 border-transparent text-gray-400'
          }`}
          onClick={() => setStars(prev => prev.includes(s) ? prev.filter(x => x !== s) : [...prev, s])}
        > 
          {s}⭐ 
        </button>
      ))}
    </div>
  </div>

  <div className="overflow-y-auto custom-scrollbar max-h-[70vh]">
    {isLoading?
      <div role="status" className="flex justify-center items-center py-10 w-full">
          <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
      </div>
      :
      <table className="w-full text-xs border-separate border-spacing-0">
      <thead className="sticky top-0 bg-neutral-900 z-10">
        <tr>
          <th className="text-left p-2 font-semibold text-gray-400 border-b border-white/10">Pity</th>
          <th className="text-center p-2 font-semibold text-gray-400 border-b border-white/10">Item</th>
          <th className="text-right p-2 font-semibold text-gray-400 border-b border-white/10">Time</th>
        </tr>
      </thead>
      <tbody>
        {warps.filter(w => 
            stars.includes(w.item_rarity) && 
            (w.item_name.toLowerCase().includes(searchTerm.toLowerCase()) || w.item_eng_name.toLowerCase().includes(searchTerm.toLowerCase()))
          )
          .sort((a, b) => b.warp_id - a.warp_id) 
          .map((w) => (
            <tr key={w.id} className="hover:bg-white/5 transition-colors group">
              <td className="p-2 align-middle text-left border-b border-white/5">
                {w.pity}
              </td>
              <td className={`p-2 align-middle border-b border-white/5 ${
                w.item_rarity === 5 ? 'text-amber-500 font-bold' : 
                w.item_rarity === 4 ? 'text-purple-400' : 'text-sky-400'
              }`}>
                <Link to={`/details/${w.item_id}`}>
                  {w.item_name}
                </Link>
              </td>
              <td className="p-2 text-right align-middle border-b border-white/5 opacity-60 font-mono text-[10px] text-gray-400">
                {w.time? `${w.time.split('T')[0]} ${w.time.split('T')[1].slice(0,8)}` : '-'}
              </td>
            </tr>
          ))}
      </tbody>
    </table>
    }

    {warps.filter(w => 
      stars.includes(w.item_rarity) && 
      (w.item_name.toLowerCase().includes(searchTerm.toLowerCase()) || w.item_eng_name.toLowerCase().includes(searchTerm.toLowerCase()))
    ).length === 0 && (
      <div className="p-10 text-center text-gray-500 italic text-sm">
        {searchTerm ? `No results for "${searchTerm}"` : "No warps found."}
      </div>
    )}
  </div>
</div>
)}
          </div>
        </div>
      )}
        </div>
      </div>
    </div>
  )
}

export default Home