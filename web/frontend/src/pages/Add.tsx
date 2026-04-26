import { useState } from "react";

function Add() {
    interface Result {
        name: string;
        count: number;
    }

    interface Import {
        message: string;
        details: Result[];
    }

    const [inputUrl, setInputUrl] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const VITE_API_URL = window._env_.BACKEND_URL;

    // ... (copyToClipboard und fallbackCopy Funktionen bleiben identisch)
    const copyToClipboard = async () => {
        const psScript = `[Net.ServicePointManager]::SecurityProtocol = [Net.ServicePointManager]::SecurityProtocol -bor [Net.SecurityProtocolType]::Tls12; Invoke-Expression (New-Object Net.WebClient).DownloadString("https://gist.githubusercontent.com/Star-Rail-Station/2512df54c4f35d399cc9abbde665e8f0/raw/get_warp_link_os.ps1?cachebust=srs")`
        if(navigator.clipboard && window.isSecureContext) {
            try { await navigator.clipboard.writeText(psScript) } catch (err) { console.error('Error') }
        } else { fallbackCopy(psScript) }
    }

    const fallbackCopy = (text: string) => {
        try {
            const textArea = document.createElement("textarea");
            textArea.value = text;
            textArea.style.position = "fixed";
            textArea.style.left = "-9999px";
            document.body.appendChild(textArea);
            textArea.focus();
            textArea.select();
            document.execCommand('copy');
            document.body.removeChild(textArea);
        } catch (err) { console.error('Fallback Copy failed', err); }
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!inputUrl) return;
        setIsLoading(true);
        try {
            const r = await fetch(`${VITE_API_URL}/api/add`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ url: inputUrl })
            });
            if (r.ok) {
                const data: Import = await r.json();
                const ban = data.details.map(d => `- ${d.name}: ${d.count}`).join('\n');
                window.alert(!data.details.length ? 'Nothing added' : `${data.message}\n\n${ban}`);
                setInputUrl('');
            } else { alert('Error importing data!'); }
        } catch (err) { console.error('Network error', err); } finally { setIsLoading(false); }
    };

    return (
        /* .page -> max-w-[400px], margin, padding, etc. */
        <div className="max-w-[400px] w-full mx-auto my-[5vh] p-10 bg-transparent rounded-[12px] box-border">
            
            {/* .url-btn -> background #261cb9, transition, hover, active */}
            <button 
                className="w-full p-3 bg-[#261cb9] text-white rounded-md cursor-pointer text-[1.1rem] font-bold transition-all duration-300 active:translate-y-[1px]"
                onClick={copyToClipboard}
            >
                Click me, then paste to Powershell
            </button>

            <form onSubmit={handleSubmit} className="mt-4">
                <p className="mb-4">
                    {/* .form input -> w-90%, padding, rounded, focus */}
                    <input
                        type="text"
                        className="w-[90%] mx-auto block p-5 rounded-[20px] bg-white text-black text-center border border-transparent focus:border-[#007bff] focus:outline-none transition-colors"
                        value={inputUrl}
                        onChange={(e) => setInputUrl(e.target.value)}
                        placeholder="Enter URL"
                        disabled={isLoading}
                    />
                </p>

                {/* .add-btn -> background #28a745, hover:bg-[#218838] */}
                <button 
                    type="submit" 
                    disabled={isLoading} 
                    className="w-full p-3 bg-[#28a745] hover:bg-[#218838] text-white rounded-md cursor-pointer text-[1.1rem] font-bold transition-all duration-300 active:translate-y-[1px] disabled:bg-gray-400"
                >
                    {isLoading ? "Sending..." : "Add"}
                </button>
            </form>
        </div>
    );
}

export default Add;