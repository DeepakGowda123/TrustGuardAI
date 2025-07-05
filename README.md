# TrustGuardAI 🛡️

A privacy-first browser extension + backend system that empowers users to control the ads they see. Designed for transparency, user consent, and ethical ad personalization.

## 🚀 Problem Statement

Online users are increasingly concerned about **data privacy** and **unwanted ads**. Most existing ad systems lack transparency and do not offer granular user control.

## 💡 Our Solution

**TrustGuardAI** is a lightweight browser-integrated system that:
- Requests user consent before tracking
- Allows users to set ad preferences
- Automatically blocks irrelevant or unwanted ads
- Includes an admin dashboard for feedback analysis and policy updates

## 🔍 Key Features

- ✅ Consent-based tracking
- 🎯 Ad personalization based on user preferences
- 🚫 Ad blocking for undesired categories
- 📊 Feedback & analytics for admins
- 🧠 AI-ready modular design for future personalization

## 🛠️ Tech Stack

- **Frontend**: React.js, Tailwind CSS
- **Backend**: FastAPI (Python)
- **Data Storage**: JSON (for prototype), extendable to DB
- **Others**: Git, GitHub, localStorage (browser-side)

## 📸 Snapshots

> Include screenshots in your final push or link to them (optional)

## 🌐 Live MVP / Demo Link

👉 [Click here to try the prototype](#) *(replace with real link)*

## 📹 Demo Video

👉 [Watch demo video](#) *(replace with uploaded video link)*

## 📁 Directory Structure

```
TrustGuardAI/
├── backend/
│   ├── main.py
│   ├── ads.json
│   ├── blocked_ads.json
│   ├── feedback.json
│   ├── user_blocked_ads.json
│   ├── user_preferences.json
│   └── users.json
├── frontend/
│   ├── public/
│   │   ├── index.html
│   │   └── ...
│   ├── src/
│   │   ├── components/
│   │   │   ├── ConsentScreen.jsx
│   │   │   ├── AdCard.jsx
│   │   │   ├── AdminDashboard.jsx
│   │   │   └── PreferencesPanel.jsx
│   │   ├── App.js
│   │   ├── index.js
│   │   └── index.css
│   └── package.json
└── README.md
```

## 🧭 Architecture Overview

- **Frontend** communicates via REST APIs with the **FastAPI backend**
- Data is stored in lightweight `.json` files (mock DB)
- Admin dashboard fetches real-time analytics
- Uses browser `localStorage` to preserve preferences

## 🚀 Getting Started

### Prerequisites

- Node.js (v14+)
- Python (v3.8+)
- npm or yarn

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/TrustGuardAI.git
   cd TrustGuardAI
   ```

2. **Set up the backend**
   ```bash
   cd backend
   pip install fastapi uvicorn
   uvicorn main:app --reload
   ```

3. **Set up the frontend**
   ```bash
   cd frontend
   npm install
   npm start
   ```

4. **Access the application**
   - Frontend: `http://localhost:3000`
   - Backend API: `http://localhost:8000`

## 🎯 Usage

1. **User Consent**: First-time users see a consent screen
2. **Set Preferences**: Users can customize ad categories they want to see
3. **Browse Safely**: Unwanted ads are automatically blocked
4. **Admin Dashboard**: View analytics and user feedback

## 🔮 Future Enhancements

- Migrate JSON files to a database (e.g., MongoDB or PostgreSQL)
- Add AI personalization using NLP
- Create browser extension packaging
- Add OAuth login or SSO support
- Implement machine learning for better ad targeting
- Add real-time notifications for policy updates

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Team

- **Your Name** - *Full Stack Developer* - [GitHub](https://github.com/yourusername)

## 📞 Contact

Project Link: [https://github.com/yourusername/TrustGuardAI](https://github.com/yourusername/TrustGuardAI)

## 🙏 Acknowledgments

- Thanks to all contributors
- Inspired by privacy-focused ad blocking solutions
- Built with modern web technologies