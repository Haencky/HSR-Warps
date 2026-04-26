function Footer() {
    return (
       <footer className="w-full bg-[#1a1a1a] text-white py-6 mt-10 border-t border-white/5 shadow-[0_-4px_10px_rgba(0,0,0,0.3)]">
            <div className="container mx-auto px-4 flex flex-col items-center gap-3">
                <p className="text-sm text-gray-400">
                    &copy; 2026 <span className="text-white font-medium">Haencky</span> · 
                    Released under <a href="https://www.gnu.org/licenses/gpl-3.0.en.html" target="_blank" rel="noreferrer" className="text-amber-500 hover:underline ml-1">GPLv3</a>
                </p>
                
                <div className="flex flex-wrap justify-center gap-6 text-sm">
                    <a 
                        href='https://github.com/Haencky/HSR-Warps' 
                        target="_blank" 
                        rel="noopener noreferrer"
                        className="flex items-center gap-2 text-gray-400 hover:text-white transition-colors group"
                    >
                        <i className="fab fa-github group-hover:scale-110 transition-transform"></i>
                        Github
                    </a>
                    
                    <a 
                        href='https://hub.docker.com/repository/docker/haenck/hsr-warptracker-backend' 
                        target="_blank" 
                        rel='noopener noreferrer'
                        className="flex items-center gap-2 text-gray-400 hover:text-blue-500 transition-colors group"
                    >
                        <i className="fab fa-docker group-hover:scale-110 transition-transform"></i>
                        Docker Hub
                    </a>
                    
                    <a 
                        href='https://haencky.github.io/HSR-Warps/itemIDs.json' 
                        target='_blank' 
                        rel='noopener noreferrer'
                        className="text-gray-400 hover:text-amber-500 transition-colors"
                    >
                        Item IDs
                    </a>
                </div>
            </div>
       </footer>
    )
}

export default Footer