import { useState, useEffect } from "react";

interface Item {
    id: number;
    name: string;
    rarity: number;
}

interface Banner {
    id: number;
    gacha_id: number;
    item_id: number | null;
    item_name: string | null;
}

interface ModalProps {
    isOpen: boolean;
    onClose: () => void;
    banner: Banner | undefined;
    availableItems: Item[];
    onSave: (selectedItemId: number | null) => void;
}

const BannerEditModal: React.FC<ModalProps> = ({ isOpen, onClose, banner, availableItems, onSave }) => {
    const [selectedItemId, setSelectedItemId] = useState<string>("")

    useEffect(() => {
        if(banner) {
            setSelectedItemId(banner.item_id ? banner.item_id.toString(): "")
        }
    }, [banner, isOpen])

    if(!isOpen || !banner) return null;

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault()
        const updatedId = selectedItemId === "" ? null : Number(selectedItemId)
        onSave(updatedId)
    }

    return (
        <div
            onClick={onClose}
            className="fixed inset-0 bg-black/75 flex items-center justify-center z-[1000] backdrop-blur-sm"
        >
            <div
                onClick={(e) => e.stopPropagation()}
                className="bg-[#1f1f1f] text-white w-[350px] padding p-6 rounded-xl border border-white/10 shadow-[0_10px_25px_rgba(0,0,0,0.5)]"
            >
                <h3 className="text-xl font-bold mb-4">
                    Edit Banner ({banner.gacha_id})
                </h3>
                
                <form onSubmit={handleSubmit}>
                    <div className="mb-5">
                        <label className="block text-sm text-[#aaa] mb-1.5">
                            Featured Item:
                        </label>
                        <select
                            value={selectedItemId}
                            onChange={(e) => setSelectedItemId(e.target.value)}
                            className="w-full p-2 rounded-md bg-[#333] text-white border border-[#444] focus:outline-none focus:border-[#eab308]"
                        >
                            <option value="">-- No Item selected --</option>
                            {availableItems.filter(i => banner.gacha_id < 3000 ? (i.id < 20000) : (i.id >= 20000)).map(item => (
                                <option key={item.id} value={item.id}>{item.name}</option>
                            ))}
                        </select>
                    </div>

                    <div className="flex justify-end gap-2.5">
                        <button
                            type="button"
                            onClick={onClose}
                            className="px-3 py-1.5 rounded-md bg-[#444] text-white cursor-pointer hover:bg-[#555] transition-colors"
                        >
                            Cancel
                        </button>
                        <button
                            type="submit"
                            className="px-3 py-1.5 rounded-md bg-[#eab308] text-black font-bold cursor-pointer hover:bg-[#facc15] transition-colors"
                        >
                            Save
                        </button>
                    </div>
                </form>
            </div>
        </div>
    )
}

export default BannerEditModal