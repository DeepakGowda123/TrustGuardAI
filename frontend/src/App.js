import { useState, useEffect } from "react";
import axios from "axios";
import AdCard from "./components/AdCard";
import toast, { Toaster } from "react-hot-toast";
import { BrowserRouter as Router, Route, Routes, Link } from "react-router-dom";
import AdminDashboard from "./components/AdminDashboard";
import ConsentScreen from "./components/ConsentScreen";
import PreferencesPanel from "./components/PreferencesPanel";

function App() {
  const [userId, setUserId] = useState("u1");

  // Preferences and consent
  const [hasConsented, setHasConsented] = useState(false);
  const [userPreferences, setUserPreferences] = useState({
    emotionFilter: true,
    dataCollection: true,
    personalizedAds: true,
    explanations: true,
  });

  const [showConsentScreen, setShowConsentScreen] = useState(false);
  const [showPreferencesPanel, setShowPreferencesPanel] = useState(false);

  // Ad state
  const [adData, setAdData] = useState(null);
  const [feedback, setFeedback] = useState(null);
  const [voteCounts, setVoteCounts] = useState(null);
  const [isLoadingNextAd, setIsLoadingNextAd] = useState(false);

  const ad = adData?.ad;

  // Load consent and preferences on mount or user switch
  useEffect(() => {
    const saved = localStorage.getItem(`consent_${userId}`);
    if (saved) {
      const prefs = JSON.parse(saved);
      setUserPreferences(prefs);
      setHasConsented(true);
    } else {
      setHasConsented(false);
      setShowConsentScreen(true);
    }
  }, [userId]);

  // Fetch ad with current preferences
  useEffect(() => {
    if (!hasConsented || !userId) return;

    const fetchAd = async () => {
      try {
        const res = await axios.get(`http://localhost:8000/ads/${userId}`, {
          params: {
            emotion_filter: userPreferences.emotionFilter,
            personalized: userPreferences.personalizedAds,
          },
        });
        setAdData(res.data);
      } catch (err) {
        console.error("Ad fetch failed:", err);
        toast.error("Failed to load ad.");
      }
    };

    fetchAd();
  }, [userId, hasConsented, userPreferences]);

  // Handle feedback submission
  useEffect(() => {
    if (!feedback || !ad?.title || !hasConsented) return;

    const sendFeedback = async () => {
      try {
        if (userPreferences.dataCollection) {
          const res = await axios.post("http://localhost:8000/feedback", {
            user_id: userId,
            ad_title: ad.title,
            feedback,
          });

          if (res.data.status === "duplicate") {
            toast.error("You've already voted on this ad.");
            return;
          }

          if (feedback !== "block") {
            setVoteCounts({ up: res.data.stats.up, down: res.data.stats.down });
          }

          toast.success("Thanks for your feedback!");
        }

        loadNextAd();
      } catch (err) {
        console.error("Feedback error:", err);
        toast.error("Failed to send feedback.");
      }
    };

    sendFeedback();
  }, [feedback]);

  const loadNextAd = async () => {
    setIsLoadingNextAd(true);
    setTimeout(async () => {
      try {
        const res = await axios.get(`http://localhost:8000/ads/${userId}`, {
          params: {
            emotion_filter: userPreferences.emotionFilter,
            personalized: userPreferences.personalizedAds,
          },
        });
        setAdData(res.data);
        setFeedback(null);
        setVoteCounts(null);
      } catch (err) {
        toast.error("Failed to load next ad.");
      } finally {
        setIsLoadingNextAd(false);
      }
    }, 2000);
  };

  const handleFeedback = (type) => {
    if (!feedback && ad) setFeedback(type);
  };

  const handleConsent = (preferences) => {
    setUserPreferences(preferences);
    setHasConsented(true);
    setShowConsentScreen(false);
    localStorage.setItem(`consent_${userId}`, JSON.stringify(preferences));
    toast.success("Preferences saved. Welcome!");
  };

  const handlePreferencesUpdate = (newPrefs) => {
    setUserPreferences(newPrefs);
    localStorage.setItem(`consent_${userId}`, JSON.stringify(newPrefs));
    toast.success("Preferences updated!");
  };

  const handleUserChange = (newUserId) => {
    setUserId(newUserId);
    setAdData(null);
    setFeedback(null);
    setVoteCounts(null);

    const consent = localStorage.getItem(`consent_${newUserId}`);
    if (consent) {
      setUserPreferences(JSON.parse(consent));
      setHasConsented(true);
    } else {
      setHasConsented(false);
      setShowConsentScreen(true);
    }
  };

  return (
    <Router>
      <div className="min-h-screen bg-gradient-to-br from-purple-50 to-blue-50">
        {/* Navbar */}
        <nav className="flex justify-between items-center bg-white px-6 py-4 shadow-lg border-b border-purple-100">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 bg-gradient-to-r from-purple-600 to-blue-600 rounded-full flex items-center justify-center">
              <span className="text-white text-sm font-bold">TG</span>
            </div>
            <h1 className="text-xl font-bold bg-gradient-to-r from-purple-600 to-blue-600 bg-clip-text text-transparent">
              TrustGuard AI
            </h1>
          </div>

          <div className="flex items-center gap-4">
            <select
              value={userId}
              onChange={(e) => handleUserChange(e.target.value)}
              className="text-sm px-3 py-2 border border-purple-200 rounded-lg"
            >
              <option value="u1">User u1</option>
              <option value="u2">User u2</option>
              <option value="u3">User u3</option>
              <option value="u4">User u4</option>
              <option value="u5">User u5</option>
            </select>

            {hasConsented && (
              <button
                onClick={() => setShowPreferencesPanel(true)}
                className="text-sm text-purple-600 border border-purple-600 px-4 py-2 rounded-lg hover:bg-purple-50"
              >
                Preferences
              </button>
            )}

            <Link
              to="/admin"
              className="text-sm text-purple-600 border border-purple-600 px-4 py-2 rounded-lg hover:bg-purple-50"
            >
              Admin Dashboard
            </Link>
          </div>
        </nav>

        <Routes>
          <Route
            path="/"
            element={
              <div className="p-8 flex flex-col items-center gap-6">
                <Toaster position="bottom-center" />

                {hasConsented ? (
                  <>
                    {adData?.empathy_analysis?.filtered_by_emotion && (
                      <div className="bg-green-50 border border-green-200 p-3 rounded-lg w-full max-w-2xl">
                        <div className="flex items-center gap-2">
                          <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                          <span className="text-sm text-green-700">
                            Ads were filtered for a better experience
                          </span>
                        </div>
                      </div>
                    )}

                    {/* Toggle filter */}
                    {/* <div className="bg-white p-4 rounded-xl shadow-lg w-full max-w-2xl flex justify-between items-center">
                      <div>
                        <span className="text-gray-700 font-medium">Ad Filtering</span>
                        <p className="text-sm text-gray-500">Filter emotionally inappropriate ads</p>
                      </div>
                      <label className="flex items-center cursor-pointer">
                        <input
                          type="checkbox"
                          className="hidden"
                          checked={userPreferences.emotionFilter}
                          onChange={() =>
                            handlePreferencesUpdate({
                              ...userPreferences,
                              emotionFilter: !userPreferences.emotionFilter,
                            })
                          }
                        />
                        <div
                          className={`w-12 h-6 rounded-full transition-colors ${
                            userPreferences.emotionFilter ? "bg-green-500" : "bg-gray-300"
                          }`}
                        >
                          <div
                            className={`w-6 h-6 bg-white rounded-full shadow transform transition-transform ${
                              userPreferences.emotionFilter ? "translate-x-6" : "translate-x-0"
                            }`}
                          ></div>
                        </div>
                      </label>
                    </div> */}

                    {ad ? (
                      <AdCard
                        ad={ad}
                        explanationNeeded={userPreferences.explanations && adData?.explanation_needed}
                        explanation={adData?.explanation || ""}
                      />
                    ) : (
                      <div className="bg-white rounded-xl shadow-lg p-8 w-full max-w-md text-center">
                        <div className="animate-pulse">
                          <div className="bg-gray-200 h-48 rounded-lg mb-4"></div>
                          <div className="bg-gray-200 h-4 rounded mb-2"></div>
                          <div className="bg-gray-200 h-3 rounded w-3/4 mx-auto"></div>
                        </div>
                        <p className="text-gray-500 mt-4">Loading personalized ad...</p>
                      </div>
                    )}

                    {isLoadingNextAd && (
                      <div className="flex items-center gap-2 text-purple-600">
                        <div className="w-4 h-4 border-2 border-purple-600 border-t-transparent rounded-full animate-spin"></div>
                        <p className="text-sm">Loading next ad...</p>
                      </div>
                    )}

                    <div className="flex gap-4 flex-wrap justify-center">
                      <button
                        onClick={() => handleFeedback("up")}
                        disabled={!!feedback || isLoadingNextAd}
                        className={`px-6 py-3 rounded-lg font-medium transition-all ${
                          feedback === "up"
                            ? "bg-green-600 text-white shadow-lg"
                            : "bg-white border-2 border-green-600 text-green-600 hover:bg-green-50"
                        } ${isLoadingNextAd ? "opacity-50 cursor-not-allowed" : "hover:shadow-md"}`}
                      >
                        {feedback === "up" && voteCounts
                          ? `👍 Relevant (${voteCounts.up})`
                          : "👍 Relevant"}
                      </button>

                      <button
                        onClick={() => handleFeedback("down")}
                        disabled={!!feedback || isLoadingNextAd}
                        className={`px-6 py-3 rounded-lg font-medium transition-all ${
                          feedback === "down"
                            ? "bg-red-600 text-white shadow-lg"
                            : "bg-white border-2 border-red-600 text-red-600 hover:bg-red-50"
                        } ${isLoadingNextAd ? "opacity-50 cursor-not-allowed" : "hover:shadow-md"}`}
                      >
                        {feedback === "down" && voteCounts
                          ? `👎 Not Relevant (${voteCounts.down})`
                          : "👎 Not Relevant"}
                      </button>

                      <button
                        onClick={() => handleFeedback("block")}
                        disabled={!!feedback || isLoadingNextAd}
                        className={`px-6 py-3 rounded-lg font-medium transition-all ${
                          feedback === "block"
                            ? "bg-yellow-600 text-white shadow-lg"
                            : "bg-white border-2 border-yellow-600 text-yellow-600 hover:bg-yellow-50"
                        } ${isLoadingNextAd ? "opacity-50 cursor-not-allowed" : "hover:shadow-md"}`}
                      >
                        🚫 Block Forever
                      </button>
                    </div>
                  </>
                ) : (
                  <div className="text-center text-gray-500">
                    <p>Please complete the consent process to continue.</p>
                  </div>
                )}
              </div>
            }
          />
          <Route path="/admin" element={<AdminDashboard />} />
        </Routes>

        {/* Modals */}
        {showConsentScreen && (
          <ConsentScreen
            onConsent={handleConsent}
            userId={userId}
          />
        )}
        {showPreferencesPanel && (
          <PreferencesPanel
            isOpen={showPreferencesPanel}
            onClose={() => setShowPreferencesPanel(false)}
            userId={userId}
            userPreferences={userPreferences}
            onPreferencesUpdate={handlePreferencesUpdate}
          />
        )}
      </div>
    </Router>
  );
}

export default App;
