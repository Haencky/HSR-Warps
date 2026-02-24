import './footer.css'

function Footer() {
    return (
       <footer className="footer">
            <div className="footer-content">
                <p>&copy; 2026 Haencky · Released under <a href="https://www.gnu.org/licenses/gpl-3.0.en.html" target="_blank" rel="noreferrer">GPLv3</a></p>
                <div className="footer-links">
                    <a href='https://github.com/Haencky/HSR-Warps' target="_blank" rel="noopener norefferer">
                        <i className="fab fa-github">Github</i>
                    </a>
                    <a href='https://hub.docker.com/repository/docker/haenck/hsr-warptracker-backend' target="_blank" rel='noopener norefferer'>
                        <i className="fab fa-docker">Docker Hub</i>
                    </a>
                    <a href='https://haencky.github.io/HSR-Warps/itemIDs.json' target='_blank' rel='noopener norefferer'>
                        Item IDs
                    </a>
                </div>
            </div>
       </footer>
    )
}

export default Footer