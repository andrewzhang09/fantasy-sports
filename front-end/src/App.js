import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import AllProjections from './pages/AllProjections';

import './App.css';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/all-projections" element={<AllProjections />} />
        <Route path="/" element={<Home />} />
        {/* Other routes can go here */}
      </Routes>
    </BrowserRouter>
  )
}

export default App;
