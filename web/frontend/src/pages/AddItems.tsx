import { useState } from "react";
import './add.css'


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
    const VITE_API_URL = import.meta.env.VITE_API_URL

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault()
        if(!itemName) return
        setIsLoading(true)

        try {
            const r = await fetch(`${VITE_API_URL}api/add_item`, {
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
        <div className="page">
            <form className="form" method="post" onSubmit={handleSubmit}>
                <p>
                    <input
                        type="textarea"
                        placeholder="Name (eng.)"
                        value={itemName}
                        onChange={(e) => setItemName(e.target.value)}
                        disabled={isLoading}
                    />
                </p>
                <button className="add-btn" disabled={isLoading} type="submit">
                    {isLoading ? 'Adding' : 'Add'}
                </button>
            </form>
        </div>
    )
}

export default AddItems