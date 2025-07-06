import React, { useEffect, useState } from "react";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell, LineChart, Line } from 'recharts';

const API_URL = process.env.REACT_APP_API_URL;

const AdminDashboard = () => {
  const [feedback, setFeedback] = useState([]);
  const [grouped, setGrouped] = useState({});
  const [blockedAds, setBlockedAds] = useState([]);
  const [userAnalytics, setUserAnalytics] = useState([]);
  const [systemStats, setSystemStats] = useState({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        // Fetch feedback
        const feedbackRes = await fetch(`${API_URL}/feedback`);
        const feedbackData = await feedbackRes.json();
        console.log("Raw feedback response:", feedbackData);
        
        // Check if feedbackData is an array (which it should be from your backend)
        if (Array.isArray(feedbackData)) {
          setFeedback(feedbackData);
          
          // Group feedback by user_id
          const groupedByUser = feedbackData.reduce((acc, entry) => {
            const userId = entry.user_id;
            if (!acc[userId]) {
              acc[userId] = [];
            }
            acc[userId].push(entry);
            return acc;
          }, {});
          
          setGrouped(groupedByUser);
          
          // Get unique users from feedback data
          const users = [...new Set(feedbackData.map(entry => entry.user_id))];
          
          // Fetch user analytics for all users with feedback
          const analyticsPromises = users.map(async (userId) => {
            try {
              const res = await fetch(`${API_URL}/analytics/user/${userId}`);
              const data = await res.json();
              return { userId, ...data };
            } catch (err) {
              console.error(`Failed to fetch analytics for user ${userId}:`, err);
              return null;
            }
          });
          const analyticsResults = await Promise.all(analyticsPromises);
          const analyticsData = analyticsResults.filter(result => result !== null);
          setUserAnalytics(analyticsData);

          // Calculate system statistics
          calculateSystemStats(feedbackData, analyticsData);
        } else {
          console.error("Feedback data is not an array:", feedbackData);
          setFeedback([]);
          setGrouped({});
        }

        // Fetch blocked ads
        const blockedRes = await fetch(`${API_URL}/blocked_ads`);
        const blockedData = await blockedRes.json();
        setBlockedAds(Array.isArray(blockedData) ? blockedData : []);
        
      } catch (err) {
        console.error("Failed to fetch data:", err);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const calculateSystemStats = (feedbackData, analyticsData) => {
    const totalInteractions = feedbackData.length;
    const totalUsers = analyticsData.length;
    const emotionDistribution = {};
    const vulnerabilityStats = { high: 0, medium: 0, low: 0 };

    feedbackData.forEach(entry => {
      const emotion = entry.emotion || 'neutral';
      emotionDistribution[emotion] = (emotionDistribution[emotion] || 0) + 1;
      
      // Simulate vulnerability levels based on emotions
      if (['stressed', 'anxious', 'depressed'].includes(emotion)) {
        vulnerabilityStats.high++;
      } else if (['neutral'].includes(emotion)) {
        vulnerabilityStats.medium++;
      } else {
        vulnerabilityStats.low++;
      }
    });

    const avgEngagement = totalUsers > 0 ? 
      analyticsData.reduce((sum, user) => sum + user.engagement_rate, 0) / totalUsers : 0;

    setSystemStats({
      totalInteractions,
      totalUsers,
      avgEngagement: avgEngagement.toFixed(1),
      emotionDistribution,
      vulnerabilityStats
    });
  };

  const countVotes = (data) => {
    const adStats = {};
    data.forEach(({ ad_title, feedback }) => {
      if (!adStats[ad_title]) adStats[ad_title] = { up: 0, down: 0, block: 0 };
      adStats[ad_title][feedback]++;
    });
    return adStats;
  };

  console.log("feedback data", feedback);

  const adStats = countVotes(feedback);
  const mostLikedAd = Object.entries(adStats).sort((a, b) => b[1].up - a[1].up)[0];
  const mostDislikedAd = Object.entries(adStats).sort((a, b) => b[1].down - a[1].down)[0];
  const mostFlaggedAd = Object.entries(adStats).sort((a, b) => b[1].block - a[1].block)[0];

  const handleBlockAd = async (adTitle) => {
    if (blockedAds.includes(adTitle)) return;

    try {
      const res = await fetch(`${API_URL}/block_ad`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ ad_title: adTitle }),
      });

      const result = await res.json();
      if (result.status === "success") {
        alert(`✅ Blocked "${result.blocked}" globally.`);
        setBlockedAds((prev) => [...prev, adTitle]);
      } else {
        alert("❌ Failed to block the ad.");
      }
    } catch (err) {
      alert("⚠️ Error while blocking ad.");
      console.error(err);
    }
  };

  // Prepare chart data
  const emotionChartData = Object.entries(systemStats.emotionDistribution || {}).map(([emotion, count]) => ({
    emotion: emotion.charAt(0).toUpperCase() + emotion.slice(1),
    count,
    color: emotion === 'stressed' ? '#ff6b6b' : emotion === 'anxious' ? '#ffa726' : 
           emotion === 'depressed' ? '#ef5350' : emotion === 'happy' ? '#66bb6a' : '#78909c'
  }));

  const vulnerabilityChartData = Object.entries(systemStats.vulnerabilityStats || {}).map(([level, count]) => ({
    level: level.charAt(0).toUpperCase() + level.slice(1),
    count,
    color: level === 'high' ? '#f44336' : level === 'medium' ? '#ff9800' : '#4caf50'
  }));

  const engagementChartData = userAnalytics.map(user => ({
    userId: user.userId,
    engagement: user.engagement_rate,
    interactions: user.total_interactions
  }));

  if (loading) {
    return (
      <div className="p-6 max-w-7xl mx-auto">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading TrustGuardAI Analytics...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="p-6 max-w-7xl mx-auto bg-gray-50 min-h-screen">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-800 mb-2">🛡️ TrustGuardAI Admin Dashboard</h1>
        <p className="text-gray-600">AI-Powered Ad Ethics & Emotional Safety Analytics</p>
      </div>

      {/* System Overview Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div className="bg-white p-6 rounded-lg shadow-md">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">Total Interactions</p>
              <p className="text-2xl font-bold text-blue-600">{systemStats.totalInteractions}</p>
            </div>
            <div className="bg-blue-100 p-3 rounded-full">
              <span className="text-blue-600 text-xl">📊</span>
            </div>
          </div>
        </div>
        
        <div className="bg-white p-6 rounded-lg shadow-md">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">Active Users</p>
              <p className="text-2xl font-bold text-green-600">{systemStats.totalUsers}</p>
            </div>
            <div className="bg-green-100 p-3 rounded-full">
              <span className="text-green-600 text-xl">👥</span>
            </div>
          </div>
        </div>
        
        <div className="bg-white p-6 rounded-lg shadow-md">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">Avg Engagement</p>
              <p className="text-2xl font-bold text-purple-600">{systemStats.avgEngagement}%</p>
            </div>
            <div className="bg-purple-100 p-3 rounded-full">
              <span className="text-purple-600 text-xl">💡</span>
            </div>
          </div>
        </div>
        
        <div className="bg-white p-6 rounded-lg shadow-md">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">Blocked Ads</p>
              <p className="text-2xl font-bold text-red-600">{blockedAds.length}</p>
            </div>
            <div className="bg-red-100 p-3 rounded-full">
              <span className="text-red-600 text-xl">🚫</span>
            </div>
          </div>
        </div>
      </div>

      {/* Charts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
        {/* EmpathyEngine Analytics */}
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h3 className="text-lg font-semibold mb-4">🧠 EmpathyEngine - Emotional States</h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={emotionChartData}
                cx="50%"
                cy="50%"
                outerRadius={80}
                dataKey="count"
                label={({ emotion, count }) => `${emotion}: ${count}`}
              >
                {emotionChartData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>

        {/* Vulnerability Distribution */}
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h3 className="text-lg font-semibold mb-4">🛡️ Vulnerability Protection Stats</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={vulnerabilityChartData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="level" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="count" fill="#8884d8">
                {vulnerabilityChartData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* TrustFlow+ Insights */}
      <div className="bg-white p-6 rounded-lg shadow-md mb-8">
        <h3 className="text-lg font-semibold mb-4">🔍 TrustFlow+ User Engagement Analytics</h3>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={engagementChartData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="userId" />
            <YAxis />
            <Tooltip />
            <Line type="monotone" dataKey="engagement" stroke="#2196f3" strokeWidth={2} />
          </LineChart>
        </ResponsiveContainer>
      </div>

      {/* Ad Performance Section */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
        {/* Most Liked */}
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h3 className="text-lg font-semibold mb-4 text-green-600">🔥 Most Liked Ad</h3>
          {mostLikedAd ? (
            <div className="bg-green-50 p-4 rounded-lg">
              <p className="font-medium text-gray-800">{mostLikedAd[0]}</p>
              <div className="mt-2 text-sm text-gray-600">
                <span className="text-green-600 font-medium">👍 {mostLikedAd[1].up}</span> | 
                <span className="text-red-500 ml-2">👎 {mostLikedAd[1].down}</span> | 
                <span className="text-gray-500 ml-2">🚫 {mostLikedAd[1].block}</span>
              </div>
            </div>
          ) : (
            <p className="text-gray-500">No data available</p>
          )}
        </div>

        {/* Most Disliked */}
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h3 className="text-lg font-semibold mb-4 text-red-600">💔 Most Disliked Ad</h3>
          {mostDislikedAd ? (
            <div className="bg-red-50 p-4 rounded-lg">
              <p className="font-medium text-gray-800">{mostDislikedAd[0]}</p>
              <div className="mt-2 text-sm text-gray-600">
                <span className="text-green-600">👍 {mostDislikedAd[1].up}</span> | 
                <span className="text-red-500 font-medium ml-2">👎 {mostDislikedAd[1].down}</span> | 
                <span className="text-gray-500 ml-2">🚫 {mostDislikedAd[1].block}</span>
              </div>
            </div>
          ) : (
            <p className="text-gray-500">No data available</p>
          )}
        </div>

        {/* Most Flagged */}
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h3 className="text-lg font-semibold mb-4 text-yellow-600">🚫 Most Flagged Ad</h3>
          {mostFlaggedAd ? (
            <div className="bg-yellow-50 p-4 rounded-lg">
              <p className="font-medium text-gray-800 mb-2">{mostFlaggedAd[0]}</p>
              <div className="text-sm text-gray-600 mb-3">
                <span className="text-yellow-600 font-medium">🚫 {mostFlaggedAd[1].block}</span> | 
                <span className="text-green-600 ml-2">👍 {mostFlaggedAd[1].up}</span> | 
                <span className="text-red-500 ml-2">👎 {mostFlaggedAd[1].down}</span>
              </div>
              <button
                onClick={() => handleBlockAd(mostFlaggedAd[0])}
                disabled={blockedAds.includes(mostFlaggedAd[0])}
                className={`px-4 py-2 rounded text-white text-sm font-medium ${
                  blockedAds.includes(mostFlaggedAd[0])
                    ? "bg-gray-400 cursor-not-allowed"
                    : "bg-red-600 hover:bg-red-700"
                }`}
              >
                {blockedAds.includes(mostFlaggedAd[0]) ? "Blocked" : "Block Globally"}
              </button>
            </div>
          ) : (
            <p className="text-gray-500">No data available</p>
          )}
        </div>
      </div>

      {/* All Ads Management */}
      <div className="bg-white p-6 rounded-lg shadow-md mb-8">
        <h3 className="text-xl font-semibold mb-4">📋 Ad Performance & Management</h3>
        <div className="space-y-3">
          {Object.entries(adStats).map(([title, stats]) => (
            <div key={title} className="p-4 border border-gray-200 rounded-lg flex justify-between items-center">
              <div>
                <p className="font-medium text-gray-800">{title}</p>
                <div className="text-sm text-gray-600 mt-1">
                  <span className="text-green-600">👍 {stats.up}</span> | 
                  <span className="text-red-500 ml-2">👎 {stats.down}</span> | 
                  <span className="text-gray-500 ml-2">🚫 {stats.block}</span>
                  <span className="ml-4 text-blue-600">
                    Engagement: {stats.up + stats.down + stats.block > 0 ? 
                      Math.round((stats.up / (stats.up + stats.down + stats.block)) * 100) : 0}%
                  </span>
                </div>
              </div>
              <button
                onClick={() => handleBlockAd(title)}
                disabled={blockedAds.includes(title)}
                className={`px-3 py-1 rounded text-white text-sm ${
                  blockedAds.includes(title)
                    ? "bg-gray-400 cursor-not-allowed"
                    : "bg-red-600 hover:bg-red-700"
                }`}
              >
                {blockedAds.includes(title) ? "Blocked" : "Block"}
              </button>
            </div>
          ))}
        </div>
      </div>

      {/* User Feedback Details */}
      <div className="bg-white p-6 rounded-lg shadow-md">
        <h3 className="text-xl font-semibold mb-4">👤 User Feedback Analysis</h3>
        <div className="space-y-4">
          {Object.entries(grouped).map(([user, items]) => (
            <div key={user} className="border border-gray-200 p-4 rounded-lg">
              <h4 className="font-bold mb-3 text-gray-800">
                User: {user}
                <span className="ml-2 text-sm text-gray-500">
                  ({Array.isArray(items) ? items.length : 0} interactions)
                </span>
              </h4>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
                {Array.isArray(items) ? items.map((entry, idx) => (
                  <div key={idx} className="flex justify-between items-center bg-gray-50 p-2 rounded text-sm">
                    <span className="text-gray-700">📝 {entry.ad_title}</span>
                    <div className="flex items-center">
                      <span className="mr-2 text-gray-500">
                        {entry.emotion && `😊 ${entry.emotion}`}
                      </span>
                      <span>
                        {entry.feedback === "up" && "👍"}
                        {entry.feedback === "down" && "👎"}
                        {entry.feedback === "block" && "🚫"}
                      </span>
                    </div>
                  </div>
                )) : (
                  <p className="text-gray-500">No feedback data available</p>
                )}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default AdminDashboard;