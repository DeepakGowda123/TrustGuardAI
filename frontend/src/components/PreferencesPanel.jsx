import React, { useState, useEffect } from "react";

const PreferencesPanel = ({ isOpen, onClose, userId, userPreferences, onPreferencesUpdate }) => {
  const [preferences, setPreferences] = useState({
    emotionFilter: true,
    dataCollection: true,
    personalizedAds: true,
    explanations: true,
    ...userPreferences
  });

  const [emotionalState, setEmotionalState] = useState("neutral");
  const [isSaving, setIsSaving] = useState(false);

  // Load user's current emotional state
  useEffect(() => {
    if (userId && isOpen) {
      // This would normally come from your users.json via an API call
      // For now, we'll use a placeholder
      setEmotionalState("neutral");
    }
  }, [userId, isOpen]);

  const handleSavePreferences = async () => {
    setIsSaving(true);
    try {
      // Prepare preferences with snake_case keys for backend
      const payload = {
        user_id: userId,
        preferences: {
          emotion_filter: preferences.emotionFilter,
          data_collection: preferences.dataCollection,
          personalization: preferences.personalizedAds,
          explanations: preferences.explanations,
        },
        emotional_state: emotionalState
      };
  
      // Send to backend
      const response = await fetch("http://localhost:8000/set_preferences", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });
  
      if (response.ok) {
        onPreferencesUpdate(preferences);
        console.log("Preferences saved successfully!");
        onClose();
      } else {
        throw new Error("Failed to save preferences");
      }
    } catch (error) {
      console.error("Failed to save preferences:", error);
    } finally {
      setIsSaving(false);
    }
  };
  
  const handleReset = () => {
    setPreferences({
      emotionFilter: true,
      dataCollection: true,
      personalizedAds: true,
      explanations: true
    });
    setEmotionalState("neutral");
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div className="bg-white rounded-2xl shadow-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="bg-gradient-to-r from-purple-600 to-blue-600 text-white p-6 rounded-t-2xl">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-white bg-opacity-20 rounded-full flex items-center justify-center">
                <span className="text-lg font-bold">⚙️</span>
              </div>
              <div>
                <h1 className="text-xl font-bold">Privacy & Ad Preferences</h1>
                <p className="text-purple-100 text-sm">Customize your TrustGuard AI experience</p>
              </div>
            </div>
            <button
              onClick={onClose}
              className="w-8 h-8 bg-white bg-opacity-20 rounded-full flex items-center justify-center hover:bg-opacity-30 transition-colors"
            >
              <span className="text-white">×</span>
            </button>
          </div>
        </div>

        {/* Content */}
        <div className="p-6">
          {/* Current Status */}
          <div className="mb-6 p-4 bg-gray-50 rounded-lg">
            <h3 className="font-semibold text-gray-800 mb-2">Current Status</h3>
            <div className="grid grid-cols-2 gap-4 text-sm">
              <div>
                <span className="text-gray-600">User ID:</span>
                <span className="ml-2 font-medium">{userId}</span>
              </div>
              <div>
                <span className="text-gray-600">Emotional State:</span>
                <span className="ml-2 font-medium capitalize">{emotionalState}</span>
              </div>
            </div>
          </div>

          {/* Emotional State Selector */}
          <div className="mb-6">
            <h3 className="font-semibold text-gray-800 mb-3">How are you feeling today?</h3>
            <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
              {[
                { value: "happy", label: "😊 Happy", color: "green" },
                { value: "neutral", label: "😐 Neutral", color: "gray" },
                { value: "stressed", label: "😰 Stressed", color: "red" },
                { value: "anxious", label: "😟 Anxious", color: "orange" },
                { value: "depressed", label: "😢 Sad", color: "blue" },
                { value: "relaxed", label: "😌 Relaxed", color: "teal" }
              ].map((state) => (
                <button
                  key={state.value}
                  onClick={() => setEmotionalState(state.value)}
                  className={`p-3 rounded-lg border-2 transition-all text-sm font-medium ${
                    emotionalState === state.value
                      ? `border-${state.color}-500 bg-${state.color}-50 text-${state.color}-700`
                      : "border-gray-200 hover:border-gray-300 text-gray-600"
                  }`}
                >
                  {state.label}
                </button>
              ))}
            </div>
          </div>

          {/* Preference Controls */}
          <div className="mb-6">
            <h3 className="font-semibold text-gray-800 mb-4">Ad Experience Preferences</h3>
            <div className="space-y-4">
              
              {/* Emotion-Based Filtering */}
              <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                <div className="flex-1">
                  <h4 className="font-medium text-gray-800">Emotion-Based Filtering</h4>
                  <p className="text-sm text-gray-600 mt-1">
                    Block inappropriate ads when you're vulnerable or stressed
                  </p>
                  <div className="mt-2 text-xs text-gray-500">
                    Status: {preferences.emotionFilter ? "✅ Active" : "❌ Disabled"}
                  </div>
                </div>
                <label className="flex items-center cursor-pointer ml-4">
                  <input
                    type="checkbox"
                    className="hidden"
                    checked={preferences.emotionFilter}
                    onChange={(e) => setPreferences(prev => ({
                      ...prev,
                      emotionFilter: e.target.checked
                    }))}
                  />
                  <div className={`w-12 h-6 rounded-full transition-colors ${
                    preferences.emotionFilter ? "bg-green-500" : "bg-gray-300"
                  }`}>
                    <div className={`w-6 h-6 rounded-full bg-white shadow transform transition-transform ${
                      preferences.emotionFilter ? "translate-x-6" : "translate-x-0"
                    }`}></div>
                  </div>
                </label>
              </div>

              {/* Data Collection */}
              <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                <div className="flex-1">
                  <h4 className="font-medium text-gray-800">Behavioral Analysis</h4>
                  <p className="text-sm text-gray-600 mt-1">
                    Allow analysis of interaction patterns for better ad matching
                  </p>
                  <div className="mt-2 text-xs text-gray-500">
                    Status: {preferences.dataCollection ? "✅ Enabled" : "❌ Disabled"}
                  </div>
                </div>
                <label className="flex items-center cursor-pointer ml-4">
                  <input
                    type="checkbox"
                    className="hidden"
                    checked={preferences.dataCollection}
                    onChange={(e) => setPreferences(prev => ({
                      ...prev,
                      dataCollection: e.target.checked
                    }))}
                  />
                  <div className={`w-12 h-6 rounded-full transition-colors ${
                    preferences.dataCollection ? "bg-green-500" : "bg-gray-300"
                  }`}>
                    <div className={`w-6 h-6 rounded-full bg-white shadow transform transition-transform ${
                      preferences.dataCollection ? "translate-x-6" : "translate-x-0"
                    }`}></div>
                  </div>
                </label>
              </div>

              {/* Personalized Ads */}
              <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                <div className="flex-1">
                  <h4 className="font-medium text-gray-800">Personalized Ads</h4>
                  <p className="text-sm text-gray-600 mt-1">
                    Receive ads tailored to your interests and current mood
                  </p>
                  <div className="mt-2 text-xs text-gray-500">
                    Status: {preferences.personalizedAds ? "✅ On" : "❌ Off"}
                  </div>
                </div>
                <label className="flex items-center cursor-pointer ml-4">
                  <input
                    type="checkbox"
                    className="hidden"
                    checked={preferences.personalizedAds}
                    onChange={(e) => setPreferences(prev => ({
                      ...prev,
                      personalizedAds: e.target.checked
                    }))}
                  />
                  <div className={`w-12 h-6 rounded-full transition-colors ${
                    preferences.personalizedAds ? "bg-green-500" : "bg-gray-300"
                  }`}>
                    <div className={`w-6 h-6 rounded-full bg-white shadow transform transition-transform ${
                      preferences.personalizedAds ? "translate-x-6" : "translate-x-0"
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
                  <div className="mt-2 text-xs text-gray-500">
                    Status: {preferences.explanations ? "✅ Shown" : "❌ Hidden"}
                  </div>
                </div>
                <label className="flex items-center cursor-pointer ml-4">
                  <input
                    type="checkbox"
                    className="hidden"
                    checked={preferences.explanations}
                    onChange={(e) => setPreferences(prev => ({
                      ...prev,
                      explanations: e.target.checked
                    }))}
                  />
                  <div className={`w-12 h-6 rounded-full transition-colors ${
                    preferences.explanations ? "bg-green-500" : "bg-gray-300"
                  }`}>
                    <div className={`w-6 h-6 rounded-full bg-white shadow transform transition-transform ${
                      preferences.explanations ? "translate-x-6" : "translate-x-0"
                    }`}></div>
                  </div>
                </label>
              </div>

            </div>
          </div>

          {/* Privacy Info */}
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6">
            <h4 className="font-medium text-blue-800 mb-2">🔒 Your Privacy Rights</h4>
            <ul className="text-sm text-blue-700 space-y-1">
              <li>• Your data never leaves your device unnecessarily</li>
              <li>• You can withdraw consent at any time</li>
              <li>• We never sell your personal information</li>
              <li>• Emotional analysis is done securely and privately</li>
            </ul>
          </div>

          {/* Action Buttons */}
          <div className="flex gap-4">
            <button
              onClick={handleReset}
              className="flex-1 bg-gray-100 text-gray-700 py-3 rounded-lg font-medium hover:bg-gray-200 transition-colors"
            >
              Reset to Defaults
            </button>
            <button
              onClick={handleSavePreferences}
              disabled={isSaving}
              className="flex-1 bg-gradient-to-r from-purple-600 to-blue-600 text-white py-3 rounded-lg font-medium hover:from-purple-700 hover:to-blue-700 transition-all duration-200 shadow-md hover:shadow-lg disabled:opacity-50"
            >
              {isSaving ? "Saving..." : "Save Preferences"}
            </button>
          </div>

          {/* Data Export */}
          <div className="mt-6 pt-4 border-t border-gray-200">
            <h4 className="font-medium text-gray-800 mb-2">Data Management</h4>
            <div className="flex gap-2 text-sm">
              <button className="text-purple-600 hover:text-purple-700">
                Export My Data
              </button>
              <span className="text-gray-300">|</span>
              <button className="text-red-600 hover:text-red-700">
                Delete All Data
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PreferencesPanel;