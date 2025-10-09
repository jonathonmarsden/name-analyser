import { AnalysisResult } from '../App'

interface ResultsDisplayProps {
  result: AnalysisResult
}

export default function ResultsDisplay({ result }: ResultsDisplayProps) {
  return (
    <div className="mt-8 bg-white/80 backdrop-blur-sm rounded-2xl shadow-sm border border-vercel-gray-200/60 p-8">
      <h2 className="text-2xl font-semibold text-vercel-black mb-6 tracking-tight">
        Analysis Results
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
              Macquarie Dictionary Pronunciation
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
          <div className="pb-2">
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

      </div>
    </div>
  )
}
