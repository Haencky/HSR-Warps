import { useState, useEffect } from "react";
import specialpass from "../assets/specialpass.png";
import starlight from "../assets/starlight.png";

function Calculator() {
  interface Calculator {
    percent: number;
    starlight: number;
    total_pulls: number;
  }

  interface GachaType {
    pity: number;
    warranted: boolean;
    gacha_type: number;
  }

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

  interface PassCalculation {
    days: number;
    cost: number;
  }

  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [gachaTypes, setGachaTypes] = useState<GachaType[]>([]);
  const [pulls, setPulls] = useState<number>();
  const [t_chars, setTChars] = useState<number>(1);
  const [t_lcs, setTLcs] = useState<number>(0);
  const [light_cone, setLightCone] = useState<number>(2);
  const [character, setCharacter] = useState<number>(1);
  const [items, setItems] = useState<Item[]>();
  const [calc, setCalc] = useState<Calculator>();
  const VITE_API_URL = window._env_.BACKEND_URL;

  const requestBody = {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      pulls: pulls,
      characters: t_chars,
      lightcones: t_lcs,
      character_id: character,
      lightcone_id: light_cone,
    }),
  };

  const calculateMaxPulls = (
    missing: number,
    isWarranted: boolean,
    pity: number,
    hardPity: number,
  ) => {
    if (missing <= 0) return 0;
    const firstCopyMax = (isWarranted ? 1 : 2) * hardPity;
    const remainingCopiesMax = (missing - 1) * (2 * hardPity);

    return firstCopyMax + remainingCopiesMax - pity;
  };

  const worst_case = () => {
    const charHardPity = 90;
    const lcHardPity = 80;

    const currentChar = items?.find((i) => i.item_id === character);
    const currentLc = items?.find((i) => i.item_id === light_cone);

    const missingChars = Math.max(0, t_chars - (currentChar?.obtained ?? 0));
    const missingLc = Math.max(0, t_lcs - (currentLc?.obtained ?? 0));

    const c_type = gachaTypes?.find((t) => t.gacha_type === 11);
    const l_type = gachaTypes?.find((t) => t.gacha_type === 12);

    const maxCharPulls = calculateMaxPulls(
      missingChars,
      c_type?.warranted ?? false,
      c_type?.pity ?? 0,
      charHardPity,
    );

    const maxLcPulls = calculateMaxPulls(
      missingLc,
      l_type?.warranted ?? false,
      l_type?.pity ?? 0,
      lcHardPity,
    );
    return maxCharPulls + maxLcPulls;
  };

  const jadeNeeded = Math.max(0, (worst_case() - (pulls || 0)) * 160);
  const dailyIncomeF2P = 225 / 7 + 60 + 800 / 14 + 800 / 30 + 600 / 42;

  const f2pDays = Math.ceil(jadeNeeded / dailyIncomeF2P);

  const calculatePassDays = (): PassCalculation => {
    if (jadeNeeded <= 0) return { days: 0, cost: 0 };

    let days = 0;
    let accumulatedJade = 0;
    let activePasses = 0;

    while (accumulatedJade < jadeNeeded) {
      if (days % 30 === 0) {
        activePasses++;
        accumulatedJade += 300;
      }

      if (accumulatedJade >= jadeNeeded) break;

      days++;
      accumulatedJade += dailyIncomeF2P + 90;
    }
    return { days: days, cost: activePasses * 5.99 };
  };

  const passResult = calculatePassDays();

  useEffect(() => {
    fetch(`${VITE_API_URL}/api/items`)
      .then((res) => res.json())
      .then((data) => setItems(data))
      .catch((err) => console.error(err));

    fetch(`${VITE_API_URL}/api/dashboard`)
      .then((res) => res.json())
      .then((data) => setGachaTypes(data))
      .catch((err) => console.error(err));
  }, []);

  const handleSimulate = async () => {
    setIsLoading(true);
    await fetch(`${VITE_API_URL}/api/calculator`, requestBody)
      .then((res) => res.json())
      .then((data) => {
        setCalc(data);
      });
    setIsLoading(false);
  };

  return (
    <div className="mt-20 p-6 w-full flex flex-col md:flex-row gap-8 justify-center items-start">
      <div className="w-full lg:w-[40%] p-6 rounded-2xl bg-neutral-900/50 border border-white/10 backdrop-blur-md shadow-2xl">
        <h3 className="text-xl font-bold text-white mb-6 flex items-center gap-2">
          <span className="text-amber-500">✦</span> Pull Calculator
        </h3>

        <div className="space-y-6">
          <div className="grid grid-cols-2 place-items-begin">
            <img src={specialpass} alt="Pulls" className="h-10 w-auto"></img>
            <input
              type="number"
              value={pulls}
              onChange={(e) =>
                setPulls(Math.max(0, parseInt(e.target.value) || 0))
              }
              className="w-full bg-neutral-800/50 border border-white/5 rounded-xl px-4 py-3 text-white outline-none focus:border-amber-500/50 focus:ring-1 focus:ring-amber-500/20 transition-all"
              placeholder="e.g. 180"
            />
          </div>

          <div className="grid grid-cols-2">
            <div className="flex flex-col gap-2">
              <select
                value={character}
                onChange={(e) => setCharacter(parseInt(e.target.value))}
                className="w-full bg-neutral-800/50 border border-white/5 rounded-xl px-4 py-3 text-white outline-none focus:border-amber-500/50 transition-all appearance-none cursor-pointer"
              >
                <option key={1} value={1}>
                  New Character
                </option>
                {items
                  ?.filter((i) => i.item_id < 20000 && i.rarity === 5)
                  .sort((a, b) => a.name.localeCompare(b.name))
                  .map((x) => (
                    <option key={x.item_id} value={x.item_id}>
                      {x.name}
                    </option>
                  ))}
              </select>
            </div>
            <div className="flex flex-col gap-2">
              <select
                value={light_cone}
                onChange={(e) => setLightCone(parseInt(e.target.value))}
                className="w-full bg-neutral-800/50 border border-white/5 rounded-xl px-4 py-3 text-white outline-none focus:border-amber-500/50 transition-all appearance-none cursor-pointer"
              >
                <option key={2} value={2}>
                  New Lightcone
                </option>
                {items
                  ?.filter((i) => i.item_id >= 20000 && i.rarity === 5)
                  .sort((a, b) => a.name.localeCompare(b.name))
                  .map((x) => (
                    <option key={x.item_id} value={x.item_id}>
                      {x.name}
                    </option>
                  ))}
              </select>
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="flex flex-col gap-2">
              <select
                value={t_chars}
                onChange={(e) => setTChars(parseInt(e.target.value))}
                className="w-full bg-neutral-800/50 border border-white/5 rounded-xl px-4 py-3 text-white outline-none focus:border-amber-500/50 transition-all appearance-none cursor-pointer"
              >
                <option key={0} value={0}>
                  0
                </option>
                {[...Array(7).keys()].map((n) => (
                  <option
                    key={n + 1}
                    value={n + 1}
                    disabled={
                      items?.find((i) => i.item_id === character)?.obtained! >=
                      n + 1
                    }
                  >
                    E{n}
                  </option>
                ))}
              </select>
            </div>

            <div className="flex flex-col gap-2">
              <select
                value={t_lcs}
                onChange={(e) => setTLcs(parseInt(e.target.value))}
                className="w-full bg-neutral-800/50 border border-white/5 rounded-xl px-4 py-3 text-white outline-none focus:border-amber-500/50 transition-all appearance-none cursor-pointer"
              >
                {[...Array(6).keys()].map((n) => (
                  <option
                    key={n}
                    value={n}
                    disabled={
                      items?.find((i) => i.item_id === light_cone)?.obtained! >=
                      n
                    }
                  >
                    S{n}
                  </option>
                ))}
              </select>
            </div>
          </div>
          <button
            onClick={handleSimulate}
            className={`w-full mt-4 text-white font-bold py-4 rounded-xl shadow-lg transition-all active:scale-[0.98]
                        ${isLoading ? "bg-white-600 hover: bg-white-500 shadow-white-900/20" : "bg-amber-600 hover:bg-amber-500 shadow-amber-900/20"}
                        `}
            disabled={isLoading || !pulls}
          >
            {isLoading ? "Calculating..." : "Calculate"}
          </button>
        </div>
      </div>
      {calc != null && (
        <div className="flex flex-col gap-8 w-full lg:w-[60%] animate-in fade-in slide-in-from-right-4 duration-500">
          {/* cards */}
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-6">
            <div className="bg-slate-800/50 p-6 rounded-2xl border border-amber-500/20 flex flex-col items-center justify-center shadow-xl">
              <span className="text-amber-400 text-xs font-bold uppercase tracking-widest mb-1">
                ~Success Rate
              </span>
              <div className="text-3xl font-black text-white">
                {(calc.percent * 100).toFixed(2)}
                <span className="text-amber-500 text-lg ml-0.5">%</span>
              </div>
            </div>

            <div className="bg-slate-800/50 p-6 rounded-2xl border border-slate-700 flex flex-col items-center justify-center shadow-xl">
              <img src={specialpass} alt="Pass"></img>
              <div className="text-3xl font-black text-white">
                ~{Math.round(calc.total_pulls)}
              </div>
            </div>

            <div className="bg-slate-800/50 p-6 rounded-2xl border border-slate-700 flex flex-col items-center justify-center shadow-xl">
              <img src={starlight} alt="Starlight" />
              <div className="text-3xl font-black text-white">
                ~{Math.round(calc.starlight)}
              </div>
            </div>
          </div>
          {calc.percent !== 1 && (
            <div className="flex flex-col gap-6 w-full max-w-[1400px] animate-in fade-in slide-in-from-bottom-4 duration-700">
              <div className="p-8 rounded-2xl bg-neutral-900/40 border border-white/5 text-slate-300 shadow-2xl">
                <h4 className="text-white text-lg font-bold mb-6 flex items-center gap-2">
                  <span className="text-amber-500">✦</span> Roadmap to Guarantee (Worst Case)
                </h4>

                <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                  <div className="space-y-6">
                    <p className="leading-relaxed">
                      Based on your current resources, your goal of{" "}
                      <span className="text-white font-semibold">
                        E{t_chars - 1} / S{t_lcs}
                      </span>{" "}
                      has a
                      <span
                        className={`ml-1 font-bold ${calc.percent > 0.7 ? "text-green-400" : "text-amber-400"}`}
                      >
                        {(calc.percent * 100).toFixed(2)}%
                      </span>{" "}
                      success rate.
                    </p>
                    <div className="h-px bg-gradient-to-r from-white/10 to-transparent" />
                    <div className="grid grid-cols-2 gap-4">
                      <div>
                        <span className="text-[10px] uppercase tracking-widest text-slate-500 font-bold block mb-1">
                          Worst Case Needs
                        </span>
                        <p className="text-white font-bold">
                          {worst_case()} Pulls
                        </p>
                      </div>
                      <div>
                        <span className="text-[10px] uppercase tracking-widest text-amber-500/70 font-bold block mb-1">
                          Missing Jades
                        </span>
                        <p className="text-amber-500 font-bold">
                          {(
                            Math.max(0, worst_case() - (pulls || 0)) * 160
                          ).toLocaleString()}
                        </p>
                      </div>
                    </div>
                  </div>

                  <div className="flex flex-col gap-4">
                    <span className="text-[10px] uppercase tracking-widest text-slate-400 font-bold">
                      Estimated Time to Goal
                    </span>

                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                      <div className="group relative bg-white/5 p-4 rounded-xl border border-white/5 transition-all hover:bg-white/10">
                        <p className="text-[10px] font-bold text-slate-500 uppercase mb-1 flex items-center justify-center gap-1">
                          Free to Play
                          <span className="text-slate-600 cursor-help">ⓘ</span>
                        </p>

                        <div className="absolute bottom-full mb-2 left-1/2 -translate-x-1/2 w-48 p-2 bg-neutral-950 border border-white/10 rounded-lg text-[10px] text-slate-400 leading-tight opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all z-50 shadow-2xl pointer-events-none">
                          <p className="font-bold text-white mb-1">Based on:</p>
                          <ul className="list-disc list-inside space-y-1">
                            <li>Dailies (60)</li>
                            <li>Sim. Universe (225/Week)</li>
                            <li>Endgame (800/2 Weeks)</li>
                            <li>Shop Reset (5 Pulls/Month)</li>
                            <li>Maintenance (600/Patch)</li>
                          </ul>
                          <div className="absolute top-full left-1/2 -translate-x-1/2 border-4 border-transparent border-t-neutral-950"></div>
                        </div>

                        <p className="text-xl font-bold text-white text-center">
                          {f2pDays}{" "}
                          <span className="text-sm font-normal text-slate-400">
                            Days
                          </span>
                        </p>
                      </div>

                      <div className="group relative bg-amber-500/10 p-4 rounded-xl border border-amber-500/20 transition-all hover:bg-amber-500/20">
                        <p className="text-[10px] font-bold text-amber-500 uppercase mb-1 flex items-center justify-center gap-1">
                          Express Pass
                          <span className="text-amber-600 cursor-help">ⓘ</span>
                        </p>

                        {/* TOOLTIP PASS */}
                        <div className="absolute bottom-full mb-2 left-1/2 -translate-x-1/2 w-48 p-2 bg-neutral-950 border border-amber-500/30 rounded-lg text-[10px] text-slate-400 leading-tight opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all z-50 shadow-2xl pointer-events-none">
                          <p className="font-bold text-amber-500 mb-1">
                            F2P + Express Pass:
                          </p>
                          <ul className="list-disc list-inside space-y-1">
                            <li>All F2P</li>
                            <li>
                              <span className="text-white">+90 daily jade</span>
                            </li>
                            <li>
                              <span className="text-white">
                                +300 jade for purchase
                              </span>{" "}
                              ({Math.round(passResult.days / 30)}x)
                            </li>
                          </ul>
                          <div className="absolute top-full left-1/2 -translate-x-1/2 border-4 border-transparent border-t-neutral-950"></div>
                        </div>

                        <p className="text-xl font-bold text-white text-center">
                          {passResult.days}{" "}
                          <span className="text-sm font-normal text-slate-400">
                            Days
                          </span>
                        </p>
                        <p className="text-[10px] text-amber-500/80 mt-1 font-semibold text-center border-t border-amber-500/10 pt-1">
                          Total Cost: {passResult.cost.toFixed(2)} €
                        </p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default Calculator;
