import React, {useEffect, useState} from 'react'

export default function Status(){
  const [status, setStatus] = useState('unknown')

  useEffect(()=>{
    const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
    fetch(`${apiUrl}/health`).then(r=>r.json()).then(j=>setStatus(j.status)).catch(()=>setStatus('unreachable'))
  },[])

  return (
    <div>
      <strong>Backend:</strong> {status}
    </div>
  )
}
