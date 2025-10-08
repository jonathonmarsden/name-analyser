import { AnalysisResult } from '../App'

interface ResultsDisplayProps {
  result: AnalysisResult
}

export default function ResultsDisplay({ result }: ResultsDisplayProps) {
  return (
    <div className="mt-8 bg-white rounded-lg shadow-lg p-8">
      <h2 className="text-2xl font-bold text-vercel-black mb-6">
        Analysis Results
      </h2>

      <div className="space-y-6">
        {/* Original Name */}
        <div className="border-b border-vercel-gray-200 pb-4">
          <h3 className="text-sm font-medium text-vercel-gray-600 mb-2">
            Original Name
          </h3>
          <p className="text-3xl font-medium text-vercel-black">
            {result.name}
          </p>
        </div>

        {/* Language Detection */}
        <div className="border-b border-vercel-gray-200 pb-4">
          <h3 className="text-sm font-medium text-vercel-gray-600 mb-2">
            Detected Language
          </h3>
          <div className="flex items-center gap-3">
            <p className="text-xl font-medium text-vercel-black">
              {result.language}
            </p>
            <span className="px-3 py-1 bg-vercel-gray-100 text-vercel-gray-700 text-sm rounded-full">
              {Math.round(result.confidence * 100)}% confidence
            </span>
          </div>
        </div>

        {/* IPA Notation */}
        <div className="border-b border-vercel-gray-200 pb-4">
          <h3 className="text-sm font-medium text-vercel-gray-600 mb-2">
            IPA Pronunciation
          </h3>
          <div className="bg-vercel-gray-50 rounded-lg p-4">
            <p className="text-2xl font-mono text-vercel-black">
              {result.ipa}
            </p>
          </div>
          <p className="text-xs text-vercel-gray-500 mt-2">
            International Phonetic Alphabet notation
          </p>
        </div>

        {/* Macquarie Dictionary Notation */}
        {result.macquarie && (
          <div className="border-b border-vercel-gray-200 pb-4">
            <h3 className="text-sm font-medium text-vercel-gray-600 mb-2">
              Macquarie Dictionary Pronunciation
            </h3>
            <div className="bg-blue-50 rounded-lg p-4">
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
          <div className="border-b border-vercel-gray-200 pb-4">
            <h3 className="text-sm font-medium text-vercel-gray-600 mb-2">
              Pronunciation Guidance
            </h3>
            <div className="bg-green-50 rounded-lg p-4">
              <p className="text-base text-vercel-gray-800">
                {result.pronunciation_guidance}
              </p>
            </div>
          </div>
        )}

        {/* Cultural Context */}
        {result.language_info && result.language_info.note && (
          <div>
            <h3 className="text-sm font-medium text-vercel-gray-600 mb-2">
              Cultural Context
            </h3>
            <div className="bg-purple-50 rounded-lg p-4">
              <p className="text-base text-vercel-gray-800">
                {result.language_info.note}
              </p>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
