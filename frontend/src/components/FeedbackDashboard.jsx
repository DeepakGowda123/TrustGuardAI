// FeedbackDashboard.jsx
import React from "react";

const FeedbackDashboard = ({ feedbackData }) => {
  return (
    <div className="bg-white rounded-xl shadow-lg p-6 w-full max-w-2xl mt-8">
      <h2 className="text-2xl font-bold mb-4">📊 User Feedback</h2>

      {Object.entries(feedbackData).map(([userId, entries]) => (
        <div key={userId} className="mb-6">
          <h3 className="text-lg font-semibold text-blue-600 mb-2">User: {userId}</h3>
          <ul className="space-y-2">
            {entries.map((entry, idx) => (
              <li key={idx} className="bg-gray-50 p-2 rounded flex justify-between items-center">
                <span className="text-gray-700">📝 {entry.ad_title}</span>
                <div className="flex gap-2 text-sm">
                  {entry.emotion && <span>😊 {entry.emotion}</span>}
                  <span>
                    {entry.feedback === "up" && "👍"}
                    {entry.feedback === "down" && "👎"}
                    {entry.feedback === "block" && "🚫"}
                  </span>
                </div>
              </li>
            ))}
          </ul>
        </div>
      ))}
    </div>
  );
};

export default FeedbackDashboard;
