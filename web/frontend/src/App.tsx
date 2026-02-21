import { BrowserRouter, Routes, Route } from 'react-router-dom'


import Navbar from './components/Navbar'
import Banner from './pages/Banner'
import Home from  './pages/Home'
import Add from './pages/Add'
import AddItems from './pages/AddItems'
import Items from './pages/Items'
import Footer from './components/Footer'
import Details from './pages/Details'

import './App.css'

function App() {
  return (
    <BrowserRouter>
      <div className='app-container'>
        <Navbar />
          <main className='main-content'>
            <Routes>
              <Route path='/' element={<Home />} />
              <Route path='/banners' element={<Banner />} />
              <Route path='/add' element={<Add />} />
              <Route path='/add/item' element={<AddItems />} />
              <Route path='/items' element={<Items />} />
              <Route path='/details/:id' element={< Details />} />
            </Routes>
          </main>
          <Footer />
        </div>
      </BrowserRouter>
  )
}

export default App