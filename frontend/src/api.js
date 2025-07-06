// src/api.js
const API_URL = process.env.REACT_APP_API_URL;

export async function fetchData(endpoint, options = {}) {
  const res = await fetch(`${API_URL}${endpoint}`, options);
  if (!res.ok) {
    throw new Error(`API error: ${res.status}`);
  }
  return res.json();
}
