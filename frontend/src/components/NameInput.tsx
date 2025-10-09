import { useState, FormEvent, useEffect } from 'react'
import { AnalysisResult } from '../App'

interface NameInputProps {
  onAnalyse: (name: string) => void
  loading: boolean
  result: AnalysisResult | null
}

interface PoetExample {
  name: string
  englishName?: string
  culture: string
  wikipedia: string
  note: string
}

// Celebrated poets from diverse cultures - showcasing the app's capabilities
const EXAMPLE_POETS: PoetExample[] = [
  {
    name: '北岛',
    englishName: 'Bei Dao',
    culture: 'Chinese',
    wikipedia: 'https://en.wikipedia.org/wiki/Bei_Dao',
    note: 'Influential Chinese poet and dissident, Nobel Prize nominee'
  },
  {
    name: 'Xuân Quỳnh',
    culture: 'Vietnamese',
    wikipedia: 'https://e.vnexpress.net/news/news/xuan-quynh-first-vietnamese-woman-on-google-doodle-3992620.html',
    note: 'Pioneering Vietnamese poet, first woman on Vietnam Google Doodle'
  },
  {
    name: 'محمود درويش',
    englishName: 'Mahmoud Darwish',
    culture: 'Palestinian',
    wikipedia: 'https://en.wikipedia.org/wiki/Mahmoud_Darwish',
    note: 'Palestine\'s national poet, master of Arabic verse'
  },
  {
    name: 'نازك الملائكة',
    englishName: 'Nazik Al-Malaika',
    culture: 'Iraqi',
    wikipedia: 'https://en.wikipedia.org/wiki/Nazik_Al-Malaika',
    note: 'Iraqi poet who pioneered free verse in Arabic poetry'
  },
  {
    name: 'אַבֿרהם סוצקעווער',
    englishName: 'Abraham Sutzkever',
    culture: 'Yiddish',
    wikipedia: 'https://en.wikipedia.org/wiki/Abraham_Sutzkever',
    note: 'Greatest Yiddish poet of the 20th century, Holocaust witness'
  },
  {
    name: 'রবীন্দ্রনাথ ঠাকুর',
    englishName: 'Rabindranath Tagore',
    culture: 'Bengali',
    wikipedia: 'https://en.wikipedia.org/wiki/Rabindranath_Tagore',
    note: 'Nobel laureate, composer of national anthems of India and Bangladesh'
  },
  {
    name: '与謝野晶子',
    englishName: 'Yosano Akiko',
    culture: 'Japanese',
    wikipedia: 'https://en.wikipedia.org/wiki/Yosano_Akiko',
    note: 'Modernist tanka poet, feminist icon of Meiji-era Japan'
  },
  {
    name: 'சுப்ரமணிய பாரதி',
    englishName: 'Subramania Bharati',
    culture: 'Tamil',
    wikipedia: 'https://en.wikipedia.org/wiki/Subramania_Bharati',
    note: 'Tamil poet and independence activist, transformed modern Tamil poetry'
  },
  {
    name: 'Wole Soyinka',
    culture: 'Nigerian (Yoruba)',
    wikipedia: 'https://en.wikipedia.org/wiki/Wole_Soyinka',
    note: 'First African Nobel laureate in Literature, playwright and poet'
  },
  {
    name: 'สุนทรภู่',
    englishName: 'Sunthorn Phu',
    culture: 'Thai',
    wikipedia: 'https://en.wikipedia.org/wiki/Sunthorn_Phu',
    note: 'Thailand\'s most celebrated poet, honored on UNESCO\'s Memory of the World'
  },
  {
    name: 'ጸጋዬ ገብረ መድኅን',
    englishName: 'Tsegaye Gabre-Medhin',
    culture: 'Ethiopian',
    wikipedia: 'https://en.wikipedia.org/wiki/Tsegaye_Gabre-Medhin',
    note: 'Ethiopia\'s Poet Laureate, wrote in Amharic and English'
  },
  {
    name: 'Анна Ахматова',
    englishName: 'Anna Akhmatova',
    culture: 'Russian',
    wikipedia: 'https://en.wikipedia.org/wiki/Anna_Akhmatova',
    note: 'Russian modernist poet, voice of Soviet-era suffering'
  },
  {
    name: '김소월',
    englishName: 'Kim Sowol',
    culture: 'Korean',
    wikipedia: 'https://en.wikipedia.org/wiki/Kim_Sowol',
    note: 'Korea\'s most beloved modern poet, master of han (longing)'
  },
  {
    name: 'Judith Wright',
    culture: 'Australian',
    wikipedia: 'https://en.wikipedia.org/wiki/Judith_Wright',
    note: 'Australia\'s foremost poet, environmentalist and Indigenous rights activist'
  },
]

// Mobile-optimized subset (8 examples)
const MOBILE_POET_INDICES = [0, 1, 2, 3, 4, 5, 8, 6]

export default function NameInput({ onAnalyse, loading, result }: NameInputProps) {
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

  // Rotate example after each analysis result
  useEffect(() => {
    if (result) {
      const maxExamples = isMobile ? MOBILE_POET_INDICES.length : EXAMPLE_POETS.length
      setCurrentExample((prev) => (prev + 1) % maxExamples)
    }
  }, [result, isMobile])

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault()
    if (name.trim()) {
      onAnalyse(name.trim())
    }
  }

  const currentPoet = isMobile
    ? EXAMPLE_POETS[MOBILE_POET_INDICES[currentExample]]
    : EXAMPLE_POETS[currentExample]

  return (
    <div className="bg-white/80 backdrop-blur-sm rounded-2xl shadow-sm border border-vercel-gray-200/60 p-8 transition-shadow hover:shadow-md">
      <form onSubmit={handleSubmit} className="space-y-5" role="search">
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
            className="w-full px-4 py-3 text-lg border border-vercel-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-brand-primary/50 focus:border-brand-primary bg-white text-vercel-black transition-all"
            disabled={loading}
            autoFocus
            aria-label="Name to analyze"
            aria-required="true"
            aria-busy={loading}
          />
        </div>

        <button
          type="submit"
          disabled={loading || !name.trim()}
          className="w-full bg-gradient-to-r from-brand-primary to-indigo-600 text-white py-3 px-6 rounded-xl font-medium hover:from-brand-primary/90 hover:to-indigo-600/90 disabled:from-vercel-gray-300 disabled:to-vercel-gray-300 disabled:cursor-not-allowed transition-all duration-200 shadow-sm hover:shadow"
          aria-label={loading ? 'Analyzing name' : 'Analyze name'}
        >
          {loading ? 'Analysing...' : 'Analyse Name'}
        </button>
      </form>

      <div className="mt-6 pt-5 border-t border-vercel-gray-200/60">
        <p className="text-center text-vercel-gray-600 text-sm mb-2">
          Try an example:
        </p>
        <div className="flex items-center justify-center gap-2">
          <button
            type="button"
            onClick={() => setName(currentPoet.name)}
            disabled={loading}
            className="group inline-flex items-center gap-2 px-3 py-2 rounded-lg hover:bg-vercel-gray-100 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            title={`${currentPoet.englishName || currentPoet.name} - ${currentPoet.note}`}
          >
            <span className="text-lg font-medium text-vercel-black">
              {currentPoet.name}
            </span>
            {currentPoet.englishName && (
              <span className="text-xs text-vercel-gray-500">
                ({currentPoet.englishName})
              </span>
            )}
            <svg className="w-4 h-4 text-vercel-gray-400 group-hover:text-brand-primary transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
            </svg>
          </button>
          <a
            href={currentPoet.wikipedia}
            target="_blank"
            rel="noopener noreferrer"
            className="p-2 text-vercel-gray-400 hover:text-brand-primary transition-colors rounded-lg hover:bg-vercel-gray-100"
            title={`Learn more about ${currentPoet.englishName || currentPoet.name}`}
            aria-label={`Wikipedia page for ${currentPoet.englishName || currentPoet.name}`}
          >
            <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
              <path d="M12 0C5.372 0 0 5.373 0 12s5.372 12 12 12 12-5.373 12-12S18.628 0 12 0zm5.562 11.048h-2.125l-1.825 5.064h-1.65l1.825-5.064H11.66l-1.825 5.064H8.188l1.825-5.064H7.888v-1.65h2.512l1.437-3.988h-2.45V3.76h2.837l1.825-5.063h1.65L13.875 3.76h2.125l1.825-5.063h1.65L17.65 3.76h2.125v1.65h-2.512L15.825 9.4h2.45v1.65h-2.837z"/>
            </svg>
          </a>
        </div>
        <p className="text-center text-xs text-vercel-gray-500 mt-2 max-w-md mx-auto">
          {currentPoet.note}
        </p>
      </div>
    </div>
  )
}
