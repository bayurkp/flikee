import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter, Routes } from 'react-router'
import './index.css'
import { Route } from 'react-router'
import GeneratePage from '@/pages/generate'
import EditPage from '@/pages/edit'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path='/generate' element={<GeneratePage />}></Route>
        <Route path='/edit' element={<EditPage />}></Route>
      </Routes>
    </BrowserRouter>
  </StrictMode>
)
