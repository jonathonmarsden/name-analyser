import { AnalysisResult } from '../App'
import { EXAMPLE_POETS } from './NameInput'

interface ResultsDisplayProps {
  result: AnalysisResult
}

export default function ResultsDisplay({ result }: ResultsDisplayProps) {
  // Check if this name matches one of our poet examples
  const matchedPoet = EXAMPLE_POETS.find(poet =>
    poet.name === result.name || poet.englishName === result.name
  )
  return (
    <div className="mt-8 bg-white/80 backdrop-blur-sm rounded-2xl shadow-sm border border-vercel-gray-200/60 p-8">
      <h2 className="text-2xl font-semibold text-vercel-black mb-6 tracking-tight">
        Analysis
      </h2>

      <div className="space-y-6">
        {/* Original Name */}
        <div className="border-b border-vercel-gray-200/60 pb-5">
          <h3 className="text-sm font-medium text-vercel-gray-600 mb-3">
            Original Name
          </h3>
          <p className="text-3xl font-medium text-vercel-black">
            {result.name}
          </p>
        </div>

        {/* Language Inference */}
        <div className="border-b border-vercel-gray-200/60 pb-5">
          <h3 className="text-sm font-medium text-vercel-gray-600 mb-3">
            Inferred Language
          </h3>
          <p className="text-xl font-medium text-vercel-black">
            {result.language}
          </p>
        </div>

        {/* IPA Notation */}
        <div className="border-b border-vercel-gray-200/60 pb-5">
          <h3 className="text-sm font-medium text-vercel-gray-600 mb-3">
            IPA Pronunciation
          </h3>
          <div className="bg-gradient-to-br from-indigo-50/50 to-purple-50/30 rounded-xl p-5 border border-indigo-100/60">
            <p className="text-2xl text-vercel-black" style={{ fontFamily: "'Noto Sans', sans-serif" }}>
              {result.ipa}
            </p>
          </div>
          <p className="text-xs text-vercel-gray-500 mt-2">
            International Phonetic Alphabet notation
          </p>
        </div>

        {/* Macquarie Dictionary Notation */}
        {result.macquarie && (
          <div className="border-b border-vercel-gray-200/60 pb-5">
            <h3 className="text-sm font-medium text-vercel-gray-600 mb-3">
              Pronunciation
            </h3>
            <div className="bg-gradient-to-br from-amber-50/50 to-orange-50/30 rounded-xl p-5 border border-amber-100/60">
              <p className="text-2xl font-medium text-vercel-black">
                {result.macquarie}
              </p>
            </div>
            <p className="text-xs text-vercel-gray-500 mt-2">
              Australian English phonetic respelling
            </p>
          </div>
        )}

        {/* Pronunciation Guidance */}
        {result.pronunciation_guidance && (
          <div className="border-b border-vercel-gray-200/60 pb-5">
            <h3 className="text-sm font-medium text-vercel-gray-600 mb-3">
              Pronunciation Guidance
            </h3>
            <div className="bg-gradient-to-br from-emerald-50/50 to-teal-50/30 rounded-xl p-5 border border-emerald-100/60">
              <p className="text-base text-vercel-gray-800 leading-relaxed">
                {result.pronunciation_guidance}
              </p>
            </div>
          </div>
        )}

        {/* Notes Section - Show for poets or if there are cultural notes */}
        {(matchedPoet || result.cultural_notes) && (
          <div className="pb-2">
            <h3 className="text-sm font-medium text-vercel-gray-600 mb-3">
              Notes
            </h3>
            <div className="bg-gradient-to-br from-blue-50/50 to-indigo-50/30 rounded-xl p-5 border border-blue-100/60 space-y-3">
              {matchedPoet ? (
                <>
                  <p className="text-sm text-vercel-gray-800 leading-relaxed">{matchedPoet.note}</p>
                  <div>
                    <a
                      href={matchedPoet.wikipedia}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="inline-flex items-center gap-2 text-sm text-brand-primary hover:text-indigo-700 transition-colors font-medium"
                    >
                      <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
                        <path d="M12 0C5.372 0 0 5.373 0 12s5.372 12 12 12 12-5.373 12-12S18.628 0 12 0zm5.562 11.048h-2.125l-1.825 5.064h-1.65l1.825-5.064H11.66l-1.825 5.064H8.188l1.825-5.064H7.888v-1.65h2.512l1.437-3.988h-2.45V3.76h2.837l1.825-5.063h1.65L13.875 3.76h2.125l1.825-5.063h1.65L17.65 3.76h2.125v1.65h-2.512L15.825 9.4h2.45v1.65h-2.837z"/>
                      </svg>
                      Learn more on Wikipedia
                    </a>
                  </div>
                </>
              ) : result.cultural_notes ? (
                <p className="text-sm text-vercel-gray-800 leading-relaxed">{result.cultural_notes}</p>
              ) : null}
            </div>
          </div>
        )}

      </div>
    </div>
  )
}
