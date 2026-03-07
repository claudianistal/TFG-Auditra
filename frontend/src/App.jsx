import React, { useState } from 'react'
import axios from 'axios'

function App() {
  const [datos, setDatos] = useState(null)

  const llamarPython = async () => {
    try {
      const res = await axios.get('http://127.0.0.1:8000/api/analizar')
      setDatos(res.data)
    } catch (error) {
      console.error("Error conectando con Python", error)
    }
  }

  return (
    <div style={{ padding: '50px', fontFamily: 'sans-serif' }}>
      <h1>🔬 Forense Audio IA</h1>
      <button onClick={llamarPython} style={{ padding: '10px 20px', cursor: 'pointer' }}>
        Simular Análisis Forense
      </button>

      {datos && (
        <div style={{ marginTop: '20px', border: '1px solid #ccc', padding: '20px' }}>
          <p><strong>Archivo:</strong> {datos.archivo}</p>
          <p><strong>Resultado:</strong> {datos.resultado}</p>
          <p><strong>Confianza:</strong> {datos.probabilidad * 100}%</p>
        </div>
      )}
    </div>
  )
}

export default App