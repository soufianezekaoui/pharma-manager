import React from 'react'
import ReactDOM from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import { Toaster } from 'react-hot-toast'
import App from './App'
import './styles/globals.css'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <BrowserRouter>
      <App />
      <Toaster
        position="top-right"
        toastOptions={{
          duration: 3500,
          style: {
            fontFamily: 'DM Sans, sans-serif',
            fontSize: '14px',
            borderRadius: '12px',
            boxShadow: '0 4px 20px rgba(0,0,0,0.12)',
          },
          success: { style: { background: '#effcfa', color: '#0a817b', border: '1px solid #c7f5ef' } },
          error: { style: { background: '#fff5f5', color: '#c53030', border: '1px solid #fed7d7' } },
        }}
      />
    </BrowserRouter>
  </React.StrictMode>
)
