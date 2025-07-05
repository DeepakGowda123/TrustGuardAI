import React, { useEffect, useState } from "react";
import axios from "axios";
import {
  BarChart, Bar, XAxis, YAxis, Tooltip, Legend, ResponsiveContainer,
} from "recharts";

const FeedbackChart = ({ userId }) => {
  const [data, setData] = useState([]);

  useEffect(() => {
    axios.get(`http://localhost:8000/feedback/${userId}/summary`)
      .then(res => {
        const transformed = Object.entries(res.data).map(([title, counts]) => ({
          ad: title,
          up: counts.up,
          down: counts.down,
        }));
        setData(transformed);
      })
      .catch(err => console.error("Failed to fetch feedback summary", err));
  }, [userId]);

  return (
    <div className="bg-white rounded-lg shadow p-6 w-full max-w-3xl">
      <h2 className="text-xl font-semibold mb-4 text-gray-800">Your Feedback Summary</h2>
      {data.length > 0 ? (
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={data} layout="vertical" margin={{ left: 40 }}>
            <XAxis type="number" />
            <YAxis type="category" dataKey="ad" width={180} />
            <Tooltip />
            <Legend />
            <Bar dataKey="up" fill="#22c55e" name="👍 Relevant" />
            <Bar dataKey="down" fill="#ef4444" name="👎 Not Relevant" />
          </BarChart>
        </ResponsiveContainer>
      ) : (
        <p className="text-gray-500">No feedback data yet.</p>
      )}
    </div>
  );
};

export default FeedbackChart;
