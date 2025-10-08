import { useState, FormEvent, useEffect } from 'react'

interface NameInputProps {
  onAnalyse: (name: string) => void
  loading: boolean
}

// Celebrated poets from diverse cultures - showcasing the app's capabilities
const EXAMPLE_NAMES = [
  '北岛', // Bei Dao - Chinese
  'Xuân Quỳnh', // Vietnamese with tones
  'محمود درويش', // Mahmoud Darwish - Arabic (Palestinian)
  'نازك الملائكة', // Nazik al-Malaika - Arabic (Iraqi)
  'אַבֿרהם סוצקעווער', // Abraham Sutzkever - Yiddish
  'রবীন্দ্রনাথ ঠাকুর', // Rabindranath Tagore - Bengali
  '与謝野晶子', // Yosano Akiko - Japanese
  'சுப்ரமணிய பாரதி', // Subramania Bharati - Tamil
  'Wole Soyinka', // Yoruba/English (Nigeria)
  'สุนทรภู่', // Sunthorn Phu - Thai
  'ጸጋዬ ገብረ መድኅን', // Tsegaye Gabre-Medhin - Amharic/Ge'ez
  'Анна Ахматова', // Anna Akhmatova - Russian
  '김소월', // Kim Sowol - Korean
  'Judith Wright', // English (Australia)
]

// Mobile-optimized subset (8 examples)
const MOBILE_EXAMPLES = [
  '北岛',
  'Xuân Quỳnh',
  'محمود درويش',
  'نازك الملائكة',
  'אַבֿרהם סוצקעווער',
  'রবীন্দ্রনাথ ঠাকুর',
  'Wole Soyinka',
  '与謝野晶子',
]

export default function NameInput({ onAnalyse, loading }: NameInputProps) {
  const [name, setName] = useState('')
  const [currentExample, setCurrentExample] = useState(0)
  const [isMobile, setIsMobile] = useState(false)

  // Detect mobile screen size
  useEffect(() => {
    const checkMobile = () => setIsMobile(window.innerWidth < 768)
    checkMobile()
    window.addEventListener('resize', checkMobile)
    return () => window.removeEventListener('resize', checkMobile)
  }, [])

  // Rotate examples
  useEffect(() => {
    const examples = isMobile ? MOBILE_EXAMPLES : EXAMPLE_NAMES
    const interval = setInterval(() => {
      setCurrentExample((prev) => (prev + 1) % examples.length)
    }, 4000) // Rotate every 4 seconds

    return () => clearInterval(interval)
  }, [isMobile])

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
            placeholder="for example: 张伟, Nguyễn Văn An, Marsden"
            className="w-full px-4 py-3 text-lg border border-vercel-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-vercel-black focus:border-transparent bg-white text-black"
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

      <div className="mt-6 text-sm">
        <p className="text-center text-vercel-gray-600">
          Try:{' '}
          <button
            type="button"
            onClick={() => {
              const examples = isMobile ? MOBILE_EXAMPLES : EXAMPLE_NAMES
              setName(examples[currentExample])
            }}
            disabled={loading}
            className="font-semibold text-vercel-gray-500 hover:text-blue-600 transition-colors disabled:opacity-50 disabled:cursor-not-allowed inline-flex items-center gap-1 px-2 py-1 rounded hover:bg-vercel-gray-100"
            title="Click to use this example"
          >
            <span className="transition-opacity duration-300 text-lg">
              {(isMobile ? MOBILE_EXAMPLES : EXAMPLE_NAMES)[currentExample]}
            </span>
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
            </svg>
          </button>
        </p>
      </div>
    </div>
  )
}
