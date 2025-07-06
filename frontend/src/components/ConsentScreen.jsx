import React, { useState } from "react";

const API_URL = process.env.REACT_APP_API_URL;


const ConsentScreen = ({ onConsent, userId }) => {
  const [selectedPreferences, setSelectedPreferences] = useState({
    emotionFilter: true,
    dataCollection: true,
    personalizedAds: true,
    explanations: true
  });

  const handleConsentSubmit = async () => {
    try {
      const response = await fetch(`${API_URL}/set_preferences`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          user_id: userId,
          preferences: {
            emotion_filter: selectedPreferences.emotionFilter,
            data_collection: selectedPreferences.dataCollection,
            personalization: selectedPreferences.personalizedAds,
            explanations: selectedPreferences.explanations,
          },
          emotional_state: null  // or pass some default state
        }),
      });
  
      if (response.ok) {
        console.log("Consent saved successfully!");
        onConsent(selectedPreferences); // Now proceed only after saving
      } else {
        console.error("Failed to save consent preferences.");
      }
    } catch (error) {
      console.error("Error submitting consent:", error);
    }
  };
  

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div className="bg-white rounded-2xl shadow-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="bg-gradient-to-r from-purple-600 to-blue-600 text-white p-6 rounded-t-2xl">
          <div className="flex items-center gap-3 mb-4">
            <div className="w-12 h-12 bg-white bg-opacity-20 rounded-full flex items-center justify-center">
              <span className="text-xl font-bold">TG</span>
            </div>
            <div>
              <h1 className="text-2xl font-bold">Welcome to TrustGuard AI</h1>
              <p className="text-purple-100">Your privacy-first ad experience</p>
            </div>
          </div>
        </div>

        {/* Content */}
        <div className="p-6">
          <div className="mb-6">
            <h2 className="text-xl font-semibold text-gray-800 mb-3">
              How TrustGuard AI Protects You
            </h2>
            <div className="space-y-3">
              <div className="flex items-start gap-3">
                <div className="w-6 h-6 bg-green-100 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
                  <span className="text-green-600 text-sm">🛡️</span>
                </div>
                <div>
                  <p className="text-gray-700 text-sm">
                    <strong>EmpathyEngine:</strong> Detects when you're stressed or vulnerable and filters inappropriate ads
                  </p>
                </div>
              </div>
              <div className="flex items-start gap-3">
                <div className="w-6 h-6 bg-blue-100 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
                  <span className="text-blue-600 text-sm">💡</span>
                </div>
                <div>
                  <p className="text-gray-700 text-sm">
                    <strong>TrustFlow+:</strong> Explains why you see certain ads, building transparency and trust
                  </p>
                </div>
              </div>
              <div className="flex items-start gap-3">
                <div className="w-6 h-6 bg-purple-100 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
                  <span className="text-purple-600 text-sm">🔒</span>
                </div>
                <div>
                  <p className="text-gray-700 text-sm">
                    <strong>Privacy First:</strong> Your data stays secure and you control what you share
                  </p>
                </div>
              </div>
            </div>
          </div>

          {/* Consent Options */}
          <div className="mb-6">
            <h3 className="text-lg font-semibold text-gray-800 mb-4">Your Preferences</h3>
            <div className="space-y-4">
              
              {/* Emotion-Based Filtering */}
              <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                <div className="flex-1">
                  <h4 className="font-medium text-gray-800">Emotion-Based Ad Filtering</h4>
                  <p className="text-sm text-gray-600 mt-1">
                    Filter ads that might be inappropriate when you're stressed or vulnerable
                  </p>
                </div>
                <label className="flex items-center cursor-pointer ml-4">
                  <input
                    type="checkbox"
                    className="hidden"
                    checked={selectedPreferences.emotionFilter}
                    onChange={(e) => setSelectedPreferences(prev => ({
                      ...prev,
                      emotionFilter: e.target.checked
                    }))}
                  />
                  <div className={`w-12 h-6 rounded-full transition-colors ${
                    selectedPreferences.emotionFilter ? "bg-green-500" : "bg-gray-300"
                  }`}>
                    <div className={`w-6 h-6 rounded-full bg-white shadow transform transition-transform ${
                      selectedPreferences.emotionFilter ? "translate-x-6" : "translate-x-0"
                    }`}></div>
                  </div>
                </label>
              </div>

              {/* Data Collection */}
              <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                <div className="flex-1">
                  <h4 className="font-medium text-gray-800">Behavioral Analysis</h4>
                  <p className="text-sm text-gray-600 mt-1">
                    Allow analysis of your interaction patterns to improve ad relevance
                  </p>
                </div>
                <label className="flex items-center cursor-pointer ml-4">
                  <input
                    type="checkbox"
                    className="hidden"
                    checked={selectedPreferences.dataCollection}
                    onChange={(e) => setSelectedPreferences(prev => ({
                      ...prev,
                      dataCollection: e.target.checked
                    }))}
                  />
                  <div className={`w-12 h-6 rounded-full transition-colors ${
                    selectedPreferences.dataCollection ? "bg-green-500" : "bg-gray-300"
                  }`}>
                    <div className={`w-6 h-6 rounded-full bg-white shadow transform transition-transform ${
                      selectedPreferences.dataCollection ? "translate-x-6" : "translate-x-0"
                    }`}></div>
                  </div>
                </label>
              </div>

              {/* Personalized Ads */}
              <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                <div className="flex-1">
                  <h4 className="font-medium text-gray-800">Personalized Ads</h4>
                  <p className="text-sm text-gray-600 mt-1">
                    Receive ads tailored to your interests and preferences
                  </p>
                </div>
                <label className="flex items-center cursor-pointer ml-4">
                  <input
                    type="checkbox"
                    className="hidden"
                    checked={selectedPreferences.personalizedAds}
                    onChange={(e) => setSelectedPreferences(prev => ({
                      ...prev,
                      personalizedAds: e.target.checked
                    }))}
                  />
                  <div className={`w-12 h-6 rounded-full transition-colors ${
                    selectedPreferences.personalizedAds ? "bg-green-500" : "bg-gray-300"
                  }`}>
                    <div className={`w-6 h-6 rounded-full bg-white shadow transform transition-transform ${
                      selectedPreferences.personalizedAds ? "translate-x-6" : "translate-x-0"
                    }`}></div>
                  </div>
                </label>
              </div>

              {/* Ad Explanations */}
              <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                <div className="flex-1">
                  <h4 className="font-medium text-gray-800">Ad Explanations</h4>
                  <p className="text-sm text-gray-600 mt-1">
                    Show explanations for why you're seeing specific ads
                  </p>
                </div>
                <label className="flex items-center cursor-pointer ml-4">
                  <input
                    type="checkbox"
                    className="hidden"
                    checked={selectedPreferences.explanations}
                    onChange={(e) => setSelectedPreferences(prev => ({
                      ...prev,
                      explanations: e.target.checked
                    }))}
                  />
                  <div className={`w-12 h-6 rounded-full transition-colors ${
                    selectedPreferences.explanations ? "bg-green-500" : "bg-gray-300"
                  }`}>
                    <div className={`w-6 h-6 rounded-full bg-white shadow transform transition-transform ${
                      selectedPreferences.explanations ? "translate-x-6" : "translate-x-0"
                    }`}></div>
                  </div>
                </label>
              </div>

            </div>
          </div>

          {/* Privacy Notice */}
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6">
            <h4 className="font-medium text-blue-800 mb-2">Privacy Commitment</h4>
            <p className="text-sm text-blue-700">
              We never sell your data. Your emotional state analysis happens locally and securely. 
              You can change these preferences anytime and withdraw consent at any time.
            </p>
          </div>

          {/* Action Buttons */}
          <div className="flex gap-4">
            <button
              onClick={handleConsentSubmit}
              className="flex-1 bg-gradient-to-r from-purple-600 to-blue-600 text-white py-3 rounded-lg font-medium hover:from-purple-700 hover:to-blue-700 transition-all duration-200 shadow-md hover:shadow-lg"
            >
              Continue with TrustGuard AI
            </button>
          </div>

          {/* Legal Text */}
          <p className="text-xs text-gray-500 mt-4 text-center">
            By continuing, you agree to our privacy-first approach. You can modify these settings anytime.
          </p>
        </div>
      </div>
    </div>
  );
};

export default ConsentScreen;