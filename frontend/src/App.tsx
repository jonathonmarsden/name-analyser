import { useState } from 'react'
import NameInput from './components/NameInput'
import ResultsDisplay from './components/ResultsDisplay'

export interface AnalysisResult {
  name: string
  language: string
  ipa: string
  macquarie: string
  pronunciation_guidance: string
  confidence?: number  // Backend sends this but we don't display it
  language_info: {
    family_name_first?: boolean
    note?: string
  }
  romanization_system?: string
  tone_marks_added?: boolean
  ambiguity?: {
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

    // Create abort controller with 30 second timeout
    const controller = new AbortController()
    const timeoutId = setTimeout(() => controller.abort(), 30000)

    try {
      // Use environment variable for API URL, fallback to relative path
      const apiUrl = import.meta.env.VITE_API_URL || '/api'
      const response = await fetch(`${apiUrl}/analyse`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ name }),
        signal: controller.signal,
      })

      clearTimeout(timeoutId)

      if (!response.ok) {
        let errorMessage = 'Failed to analyse name'
        try {
          const errorData = await response.json()
          // FastAPI returns {detail: "error message"}
          errorMessage = errorData.detail || errorMessage
        } catch {
          // If JSON parsing fails, use default message
        }
        throw new Error(errorMessage)
      }

      const data = await response.json()
      setResult(data)
    } catch (err) {
      if (err instanceof Error && err.name === 'AbortError') {
        setError('Request timed out. Please try again.')
      } else {
        setError(err instanceof Error ? err.message : 'An error occurred')
      }
    } finally {
      clearTimeout(timeoutId)
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
            <div
              className="mt-6 p-4 bg-red-50 border border-red-200 rounded-lg"
              role="alert"
              aria-live="assertive"
            >
              <p className="text-red-800">{error}</p>
            </div>
          )}

          {result && (
            <div aria-live="polite" aria-atomic="true">
              <ResultsDisplay result={result} />
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default App
