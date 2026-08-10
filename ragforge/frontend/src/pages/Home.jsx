import React from 'react'
import Status from '../components/Status'

export default function Home() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="p-6 bg-white rounded shadow">
        <h1 className="text-2xl font-bold mb-4">RAGForge</h1>
        <p className="mb-4">Frontend running.</p>
        <Status />
      </div>
    </div>
  )
}
