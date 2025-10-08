import { useState, FormEvent } from 'react'

interface NameInputProps {
  onAnalyse: (name: string) => void
  loading: boolean
}

export default function NameInput({ onAnalyse, loading }: NameInputProps) {
  const [name, setName] = useState('')

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault()
    if (name.trim()) {
      onAnalyse(name.trim())
    }
  }

  return (
    <div className="bg-white rounded-lg shadow-lg p-8">
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label
            htmlFor="name-input"
            className="block text-sm font-medium text-vercel-gray-700 mb-2"
          >
            Enter name to analyse
          </label>
          <input
            id="name-input"
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            placeholder="e.g., 张伟, Nguyễn Văn An, Smith"
            className="w-full px-4 py-3 text-lg border border-vercel-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-vercel-black focus:border-transparent"
            disabled={loading}
            autoFocus
          />
        </div>

        <button
          type="submit"
          disabled={loading || !name.trim()}
          className="w-full bg-vercel-black text-white py-3 px-6 rounded-lg font-medium hover:bg-vercel-gray-800 disabled:bg-vercel-gray-300 disabled:cursor-not-allowed transition-colors duration-200"
        >
          {loading ? 'Analysing...' : 'Analyse Name'}
        </button>
      </form>

      <div className="mt-6 text-sm text-vercel-gray-600">
        <p className="font-medium mb-2">Example names to try:</p>
        <div className="flex flex-wrap gap-2">
          {['张伟', 'Nguyễn Văn An', 'Smith', 'राज कुमार'].map((example) => (
            <button
              key={example}
              type="button"
              onClick={() => setName(example)}
              disabled={loading}
              className="px-3 py-1 bg-vercel-gray-100 hover:bg-vercel-gray-200 rounded-md transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {example}
            </button>
          ))}
        </div>
      </div>
    </div>
  )
}
