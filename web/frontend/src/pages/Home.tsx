import { useState, useEffect } from "react"

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
  const VITE_API_URL = window._env_.BACKEND_URL

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
    <div className="mt-20 p-6 w-full min-h-[calc(100vh-80px)] flex flex-wrap gap-8 justify-center items-start">
      {types.map((t) => (
        <div 
          key={t.id} 
          className="relative overflow-hidden rounded-2xl bg-neutral-900/50 border border-white/10 shadow-2xl backdrop-blur-sm transition-all duration-300 hover:scale-[1.02] hover:border-white/20 w-full max-w-[450px] grid grid-cols-[120px_1fr] gap-4 p-4"
        >
          <div className="flex items-center justify-center bg-black/40 rounded-xl overflow-hidden h-[120px]">
            {t.last_win?.item_image ? (
              <img
                src={`${VITE_API_URL}${t.last_win.item_image}`}
                alt={t.last_win.item_name}
                className="w-full h-full object-cover"
              />
            ) : (
              <div className="text-gray-600 text-xs text-center p-2">{t.last_win?.item_name}</div>
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
                {t.warranted && t.id !== 1 && (
                  <span className="ml-2 text-[10px] bg-amber-500/20 text-amber-500 px-1.5 py-0.5 rounded uppercase font-bold">
                    Guaranteed
                  </span>
                )}
              </div>

              {t.wr !== null && (
                <div className="text-sm">
                  <span className="text-gray-400 uppercase text-[10px] tracking-wider inline-block mr-2">Winrate:</span>
                  <span className="text-white font-mono">{t.wr}%</span>
                </div>
              )}
            </div>

            <div className="mt-3 pt-2 border-t border-white/5 flex justify-between items-baseline">
                <span className="text-green-400 font-mono text-sm">{t.c * 160} Jade</span>
                <span className="text-gray-500 text-xs">{(t.c * 2.64).toFixed(2)}€</span>
            </div>
          </div>
        </div>
      ))}
    </div>
  )
}

export default Home