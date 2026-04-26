import { useState } from "react";

function AddItems() {
    interface Suggestion {
        item: string;
        distance: number;
    }

    interface Result {
        message: string;
        id: number;
        suggestions: Suggestion[]
    }

    const [itemName, setItemName] = useState('')
    const [isLoading, setIsLoading] = useState(false)
    const VITE_API_URL = window._env_.BACKEND_URL

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault()
        if(!itemName) return
        setIsLoading(true)

        try {
            const r = await fetch(`${VITE_API_URL}/api/add_item`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({eng_name: itemName})
            })
            const data: Result = await r.json()
            const suggs = data.suggestions.map(s => `- ${s.item} (${s.distance})`).join('\n')
            let alertMsg = `${data.message}\n\n`
            if (data.message.startsWith('Added item')) {
                alertMsg += `Confirming will let you edit this item`
                if(window.confirm(alertMsg)) window.open(`${VITE_API_URL}/admin/warptracker/item/${data.id}/change`, '_blank', 'noopener,norefferer')
            } else {
                alertMsg += `${suggs.length ? `Try:\n${suggs}` : 'Try again'}`
                window.alert(alertMsg)
            }
            setIsLoading(false)
        } catch (err) {
            console.error(err)
        }
    } 

    return (
        <div className="bg-transparent p-10 rounded-xl max-w-[400px] w-full mx-auto my-[5vh] box-border">
            <form className="flex flex-col gap-4" method="post" onSubmit={handleSubmit}>
                <div className="flex justify-center">
                    <input
                        type="text"
                        placeholder="Name (eng.)"
                        className="py-5 px-4 rounded-[20px] bg-white text-black w-[90%] text-center border border-transparent focus:border-blue-500 focus:outline-none transition-colors disabled:opacity-50"
                        value={itemName}
                        onChange={(e) => setItemName(e.target.value)}
                        disabled={isLoading}
                    />
                </div>
                <button 
                    className="w-full padding-3 py-3 bg-[#28a745] hover:bg-[#218838] active:translate-y-[1px] text-white border-none rounded-md cursor-pointer text-[1.1rem] font-bold transition-all disabled:bg-gray-500 disabled:cursor-not-allowed"
                    disabled={isLoading} 
                    type="submit"
                >
                    {isLoading ? 'Adding' : 'Add'}
                </button>
            </form>
        </div>
    )
}

export default AddItems