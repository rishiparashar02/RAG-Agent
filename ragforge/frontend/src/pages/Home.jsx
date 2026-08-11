import React from 'react'
import Header from '../components/Header'
import Sidebar from '../components/Sidebar'

export default function Home(){
  return (
    <div>
      <Header />
      <div className="app-layout">
        <Sidebar />
        <main className="main">
          <div className="card">
            <h2 className="welcome">Welcome to RAGForge</h2>
            <p className="muted">Local-first RAG platform. Backend status shown elsewhere.</p>
          </div>
        </main>
      </div>
    </div>
  )
}
