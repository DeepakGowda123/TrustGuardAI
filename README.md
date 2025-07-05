# TrustGuardAI 🛡️

A privacy-first browser extension + backend system that empowers users to control the ads they see. Designed for transparency, user consent, and ethical ad personalization.

---

## 🚀 Problem Statement

Online users are increasingly concerned about **data privacy** and **unwanted ads**. Most existing ad systems lack transparency and do not offer granular user control.

---

## 💡 Our Solution

**TrustGuardAI** is a lightweight browser-integrated system that:
- Requests user consent before tracking.
- Allows users to set ad preferences.
- Automatically blocks irrelevant or unwanted ads.
- Includes an admin dashboard for feedback analysis and policy updates.

---

## 🔍 Key Features

- ✅ Consent-based tracking
- 🎯 Ad personalization based on user preferences
- 🚫 Ad blocking for undesired categories
- 📊 Feedback & analytics for admins
- 🧠 AI-ready modular design for future personalization

---

## 🛠️ Tech Stack

- **Frontend**: React.js, Tailwind CSS
- **Backend**: FastAPI (Python)
- **Data Storage**: JSON (for prototype), extendable to DB
- **Others**: Git, GitHub, localStorage (browser-side)

---

## 📸 Snapshots

> Include screenshots in your final push or link to them (optional)

---

## 🌐 Live MVP / Demo Link

👉 [Click here to try the prototype](#) *(replace with real link)*

---

## 📹 Demo Video

👉 [Watch demo video](#) *(replace with uploaded video link)*

---

## 📁 Directory Structure
TrustGuardAI/
├── backend/
│ ├── main.py
│ ├── ads.json
│ ├── blocked_ads.json
│ ├── feedback.json
│ ├── user_blocked_ads.json
│ ├── user_preferences.json
│ └── users.json
├── frontend/
│ ├── public/
│ │ ├── index.html
│ │ └── ...
│ ├── src/
│ │ ├── components/
│ │ │ ├── ConsentScreen.jsx
│ │ │ ├── AdCard.jsx
│ │ │ ├── AdminDashboard.jsx
│ │ │ ├── PreferencesPanel.jsx
│ │ ├── App.js
│ │ ├── index.js
│ │ └── index.css
└── README.md


## 🧭 Architecture Overview

- **Frontend** communicates via REST APIs with the **FastAPI backend**
- Data is stored in lightweight `.json` files (mock DB)
- Admin dashboard fetches real-time analytics
- Uses browser `localStorage` to preserve preferences


## 🚀 Future Enhancements

- Migrate JSON files to a database (e.g., MongoDB or PostgreSQL)
- Add AI personalization using NLP
- Create browser extension packaging
- Add OAuth login or SSO support

---

## 🏁 License

MIT License — free to use with attribution
