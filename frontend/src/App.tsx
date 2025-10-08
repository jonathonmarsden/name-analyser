import { useState } from 'react'
import NameInput from './components/NameInput'
import ResultsDisplay from './components/ResultsDisplay'

export interface AnalysisResult {
  name: string
  language: string
  ipa: string
  macquarie: string
  pronunciation_guidance: string
  confidence: number
  language_info: {
    family_name_first: boolean
    note: string
  }
}

function App() {
  const [result, setResult] = useState<AnalysisResult | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleAnalyse = async (name: string) => {
    setLoading(true)
    setError(null)

    try {
      // Use environment variable for API URL, fallback to relative path
      const apiUrl = import.meta.env.VITE_API_URL || '/api'
      const response = await fetch(`${apiUrl}/analyse`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ name }),
      })

      if (!response.ok) {
        throw new Error('Failed to analyse name')
      }

      const data = await response.json()
      setResult(data)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-vercel-gray-50 to-vercel-gray-100">
      <div className="container mx-auto px-4 py-12">
        <header className="text-center mb-12">
          <h1 className="text-4xl font-bold text-vercel-black mb-2">
            Name Pronunciation Analyser
          </h1>
        </header>

        <div className="max-w-4xl mx-auto">
          <NameInput onAnalyse={handleAnalyse} loading={loading} />

          {error && (
            <div className="mt-6 p-4 bg-red-50 border border-red-200 rounded-lg">
              <p className="text-red-800">{error}</p>
            </div>
          )}

          {result && <ResultsDisplay result={result} />}
        </div>
      </div>
    </div>
  )
}

export default App
