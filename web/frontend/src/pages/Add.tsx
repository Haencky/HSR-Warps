import { useState } from "react";
import './add.css'

function Add () {

    interface Result {
        name: string;
        count: number;
    }

    interface Import {
        message: string;
        details: Result[];
    }

    const [inputUrl, setInputUrl] = useState('')
    const [isLoading, setIsLoading] = useState(false)
    const VITE_API_URL = import.meta.env.VITE_API_URL


    const copyToClipboard = () => {
        navigator.clipboard.writeText('[Net.ServicePointManager]::SecurityProtocol = [Net.ServicePointManager]::SecurityProtocol -bor [Net.SecurityProtocolType]::Tls12; Invoke-Expression (New-Object Net.WebClient).DownloadString("https://gist.githubusercontent.com/Star-Rail-Station/2512df54c4f35d399cc9abbde665e8f0/raw/get_warp_link_os.ps1?cachebust=srs")')
    }

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault()
        if (!inputUrl) return
        setIsLoading(true)

        try {
            const r = await fetch(`${VITE_API_URL}/api/add`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({url: inputUrl})
            })
            if (r.ok) {
                const data : Import = await r.json()
                const ban = data.details.map(d => `- ${d.name}: ${d.count}`).join('\n')
                if (!data.details.length) {
                    window.alert('Nothing added')
                } else {
                    window.alert(`${data.message}\n\n${ban}`)
                }

                setInputUrl('')                
            } else {
                alert('Error importing data!')
            }
        } catch (err) {
            console.error('Network error', err)
        } finally {
            setIsLoading(false)
        }
    }

    return(
        <div className="page">
            <button className="url-btn" onClick={copyToClipboard}>
                Click me, then paste to Powershell
            </button>
            <form onSubmit={handleSubmit} className="form">
                <p>
                    <input
                        type="textarea"
                        value={inputUrl}
                        onChange={(e) => setInputUrl(e.target.value)}
                        placeholder="Enter URL"
                        disabled={isLoading}
                    />
                </p>
                <button type="submit" disabled={isLoading} className="add-btn">
                    {isLoading ? "Sending..." : "Add"}
                </button>
            </form>
        </div>
    )
}

export default Add