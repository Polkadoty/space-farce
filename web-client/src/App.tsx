import { useEffect, useState } from 'react'
import { GalaxyVisualizer } from './components/GalaxyVisualizer'
import { Galaxy } from './types/galaxy'
import './App.css'

function App() {
  const [galaxy, setGalaxy] = useState<Galaxy | null>(null)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchGalaxy = async () => {
      try {
        console.log('Fetching galaxy data...');
        const response = await fetch('http://localhost:8080/api/v1/galaxy');
        
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        console.log('Received galaxy data:', data);
        setGalaxy(data);
      } catch (error) {
        console.error('Error fetching galaxy:', error);
        setError('Failed to fetch galaxy data');
      }
    }

    fetchGalaxy()
  }, [])

  if (error) {
    return <div className="error">{error}</div>
  }

  if (!galaxy) {
    return <div className="loading">Loading galaxy...</div>
  }

  return (
    <div className="app">
      <GalaxyVisualizer 
        galaxy={galaxy}
        width={1280}
        height={800}
      />
    </div>
  )
}

export default App
