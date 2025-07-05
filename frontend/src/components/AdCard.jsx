import React, { useState } from "react";

const AdCard = ({ ad, explanationNeeded, explanation }) => {
  const [showExplanation, setShowExplanation] = useState(false);

  return (
    <div className="bg-white rounded-xl shadow-lg overflow-hidden w-full max-w-md">
      {/* Ad Content */}
      <div className="relative">
        <img 
          src={ad.image_url} 
          alt={ad.title} 
          className="w-full h-48 object-cover"
        />
        
        {/* Subtle Trust Badge */}
        <div className="absolute top-3 right-3 bg-white/90 backdrop-blur-sm text-gray-600 text-xs px-2 py-1 rounded-full">
          Verified
        </div>
      </div>

      <div className="p-6">
        {/* Ad Title & Category */}
        <h2 className="text-xl font-semibold text-gray-800 mb-2">{ad.title}</h2>
        <div className="flex items-center gap-2 mb-4">
          <span className="text-sm text-gray-500 bg-gray-100 px-2 py-1 rounded-full">
            {ad.category}
          </span>
          {ad.target_audience && (
            <span className="text-sm text-blue-600 bg-blue-50 px-2 py-1 rounded-full">
              {ad.target_audience}
            </span>
          )}
        </div>

        {/* Ad Description */}
        {ad.description && (
          <p className="text-gray-600 text-sm mb-4">{ad.description}</p>
        )}

        {/* Subtle TrustFlow+ Explanation Section */}
        <div className="border-t border-gray-100 pt-4">
          <button
            className="flex items-center gap-2 text-sm text-gray-500 hover:text-gray-700 transition-colors"
            onClick={() => setShowExplanation(!showExplanation)}
          >
            <span className="text-base">ℹ️</span>
            Why am I seeing this?
            {explanationNeeded && (
              <span className="w-2 h-2 bg-blue-500 rounded-full ml-1"></span>
            )}
          </button>

          {showExplanation && (
            <div className="mt-3 p-4 bg-gray-50 border border-gray-200 rounded-lg">
              <p className="text-sm text-gray-700">
                {explanation || ad.explanation || "This ad was selected based on your interests and browsing activity."}
              </p>
            </div>
          )}
        </div>

        {/* CTA Button */}
        {ad.cta && (
          <div className="mt-4 pt-4 border-t border-gray-100">
            <button className="w-full bg-gradient-to-r from-purple-600 to-blue-600 text-white py-3 rounded-lg font-medium hover:from-purple-700 hover:to-blue-700 transition-all duration-200 shadow-md hover:shadow-lg">
              {ad.cta}
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default AdCard;