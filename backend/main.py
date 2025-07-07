# from fastapi import FastAPI, Query, Request
# from fastapi.middleware.cors import CORSMiddleware
# import json
# import random
# import os
# from datetime import datetime
# from typing import Dict, List

# app = FastAPI(title="TrustGuard AI Backend", version="1.1.0")

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # ================================
# # EMPATHY ENGINE IMPLEMENTATION
# # ================================
# class EmpathyEngine:
#     @staticmethod
#     def analyze_user_vulnerability(user_data: Dict) -> Dict:
#         status = user_data.get("status", "neutral")
#         vulnerability_map = {
#             "stressed": {"level": "high", "score": 0.8, "triggers": ["luxury", "pressure"]},
#             "anxious": {"level": "high", "score": 0.9, "triggers": ["luxury", "social"]},
#             "depressed": {"level": "high", "score": 0.85, "triggers": ["luxury", "social", "comparison"]},
#             "neutral": {"level": "low", "score": 0.2, "triggers": []},
#             "happy": {"level": "low", "score": 0.1, "triggers": []},
#             "relaxed": {"level": "low", "score": 0.1, "triggers": []}
#         }
#         return vulnerability_map.get(status, vulnerability_map["neutral"])

#     @staticmethod
#     def filter_ads_by_emotion(ads: List[Dict], user_vulnerability: Dict) -> List[Dict]:
#         if user_vulnerability["level"] == "low":
#             return ads
#         triggers = user_vulnerability["triggers"]
#         return [ad for ad in ads if ad.get("category", "") not in triggers]

# # ================================
# # TRUSTFLOW++ IMPLEMENTATION
# # ================================
# class TrustFlowPlus:
#     @staticmethod
#     def predict_ad_expectation(user_data: Dict, ad_data: Dict) -> Dict:
#         user_status = user_data.get("status", "neutral")
#         ad_target = ad_data.get("target_audience", "neutral")
#         mismatch = user_status != ad_target
#         expectation_score = 0.3 if mismatch else 0.8
#         return {
#             "explanation_needed": mismatch,
#             "expectation_score": expectation_score,
#             "reason": f"User is {user_status}, ad targets {ad_target}" if mismatch else "Good match"
#         }

#     @staticmethod
#     def generate_explanation(user_data: Dict, ad_data: Dict) -> str:
#         explanations = [
#             ad_data.get("explanation", ""),
#             f"This ad matches users with similar interests in your area.",
#             f"Based on your browsing pattern, this might interest you.",
#             f"Others like you found this helpful during similar times."
#         ]
#         return random.choice([e for e in explanations if e])

# empathy_engine = EmpathyEngine()
# trustflow_plus = TrustFlowPlus()

# # ================================
# # UTILITIES
# # ================================
# def load_json(file: str, default):
#     if os.path.exists(file):
#         with open(file) as f:
#             return json.load(f)
#     else:
#         # Auto-create missing file with default content
#         with open(file, "w") as f:
#             json.dump(default, f, indent=2)
#         return default


# def save_json(file: str, data):
#     with open(file, "w") as f:
#         json.dump(data, f, indent=2)

# # ================================
# # MAIN ENDPOINTS
# # ================================
# @app.get("/")
# def root():
#     return {"message": "TrustGuard AI Backend v1.1", "status": "running"}

# @app.get("/health")
# def health_check():
#     return {
#         "status": "healthy",
#         "timestamp": datetime.now().isoformat()
#     }

# @app.get("/ads/{user_id}")
# def get_ad_with_ai(user_id: str):
#     try:
#         users = load_json("users.json", {})
#         ads = load_json("ads.json", [])
#         blocked_ads = load_json("blocked_ads.json", [])
#         user_blocked_ads = load_json("user_blocked_ads.json", {})
#         user_preferences = load_json("user_preferences.json", {})

#         user = users.get(user_id)
#         if not user:
#             return {"error": "User not found"}

#         prefs = user_preferences.get(user_id, {
#             "emotion_filter": True,
#             "personalization": True,
#             "explanations": True
#         })

#         # Empathy Engine
#         vulnerability = empathy_engine.analyze_user_vulnerability(user)
#         emotionally_safe_ads = empathy_engine.filter_ads_by_emotion(ads, vulnerability) if prefs["emotion_filter"] else ads

#         # Apply blocklists
#         user_blocked = user_blocked_ads.get(user_id, [])
#         final_ads = [ad for ad in emotionally_safe_ads if ad["title"] not in blocked_ads and ad["title"] not in user_blocked]

#         if not final_ads:
#             return {"error": "No suitable ads available."}

#         selected_ad = random.choice(final_ads)

#         # Handle personalization logic
#         if prefs["personalization"]:
#             trust_analysis = trustflow_plus.predict_ad_expectation(user, selected_ad)
#             explanation = trustflow_plus.generate_explanation(user, selected_ad) if prefs["explanations"] and trust_analysis["explanation_needed"] else ""
#         else:
#             trust_analysis = {
#                 "expectation_score": "N/A",
#                 "reason": "Personalization disabled"
#             }
#             explanation = ""

#         return {
#             "ad": selected_ad,
#             "explanation_needed": prefs["explanations"] and trust_analysis.get("explanation_needed", False),
#             "explanation": explanation,
#             "empathy_analysis": {
#                 "vulnerability_level": vulnerability["level"],
#                 "vulnerability_score": vulnerability["score"],
#                 "filtered_by_emotion": prefs["emotion_filter"] and vulnerability["level"] == "high"
#             },
#             "trust_analysis": {
#                 "expectation_score": trust_analysis["expectation_score"],
#                 "reason": trust_analysis["reason"]
#             }
#         }

#     except Exception as e:
#         return {"error": str(e)}
# @app.post("/feedback")
# async def receive_feedback(request: Request):
#     try:
#         data = await request.json()
#         user_id, ad_title, feedback = data["user_id"], data["ad_title"], data["feedback"]
#         emotion = data.get("emotion", "neutral")

#         # ✅ Check if user opted out of data collection
#         user_preferences = load_json("user_preferences.json", {})
#         prefs = user_preferences.get(user_id, {
#             "data_collection": True
#         })

#         if not prefs.get("data_collection", True):
#             return {
#                 "status": "opted_out",
#                 "message": "User has opted out of data collection. Feedback not saved."
#             }

#         # ✅ Continue as usual
#         ads = load_json("ads.json", [])
#         ad = next((a for a in ads if a["title"] == ad_title), None)
#         if ad and not emotion:
#             emotion = ad.get("target_audience", "neutral")

#         feedback_data = load_json("feedback.json", {})
#         feedback_data.setdefault(user_id, [])

#         if any(entry["ad_title"] == ad_title for entry in feedback_data[user_id]):
#             up = down = block = 0
#             for entries in feedback_data.values():
#                 for entry in entries:
#                     if entry["ad_title"] == ad_title:
#                         if entry["feedback"] == "up": up += 1
#                         if entry["feedback"] == "down": down += 1
#                         if entry["feedback"] == "block": block += 1
#             return {
#                 "status": "duplicate",
#                 "message": "Feedback already submitted.",
#                 "stats": {"up": up, "down": down, "block": block}
#             }

#         feedback_data[user_id].append({
#             "ad_title": ad_title,
#             "feedback": feedback,
#             "timestamp": datetime.now().isoformat(),
#             "emotion": emotion
#         })
#         save_json("feedback.json", feedback_data)

#         if feedback == "block":
#             blocked = load_json("user_blocked_ads.json", {})
#             blocked.setdefault(user_id, [])
#             if ad_title not in blocked[user_id]:
#                 blocked[user_id].append(ad_title)
#             save_json("user_blocked_ads.json", blocked)

#         up = down = block = 0
#         for entries in feedback_data.values():
#             for entry in entries:
#                 if entry["ad_title"] == ad_title:
#                     if entry["feedback"] == "up": up += 1
#                     if entry["feedback"] == "down": down += 1
#                     if entry["feedback"] == "block": block += 1

#         return {
#             "status": "success",
#             "message": "Feedback recorded.",
#             "stats": {"up": up, "down": down, "block": block}
#         }

#     except Exception as e:
#         return {"error": str(e)}



# @app.post("/set_preferences")
# async def set_user_preferences(request: Request):
#     try:
#         data = await request.json()
#         user_id = data["user_id"]
#         preferences = data.get("preferences", {})

#         # Extract preferences from nested object
#         emotion_filter = preferences.get("emotion_filter", True)
#         personalization = preferences.get("personalization", True)
#         explanations = preferences.get("explanations", True)
#         data_collection = preferences.get("data_collection", True)

#         prefs = load_json("user_preferences.json", {})
#         prefs[user_id] = {
#             "emotion_filter": emotion_filter,
#             "personalization": personalization,
#             "explanations": explanations,
#             "data_collection": data_collection
#         }

#         save_json("user_preferences.json", prefs)
#         return {"status": "success", "preferences": prefs[user_id]}
#     except Exception as e:
#         return {"error": str(e)}



# @app.get("/get_preferences/{user_id}")
# def get_user_preferences(user_id: str):
#     prefs = load_json("user_preferences.json", {})
#     return prefs.get(user_id, {
#         "emotion_filter": True,
#         "personalization": True,
#         "explanations": True,
#         "data_collection": True  # ✅ Add this
#     })

# # ================================
# # ANALYTICS & ADMIN
# # ================================
# @app.get("/analytics/user/{user_id}")
# def get_user_analytics(user_id: str):
#     try:
#         feedback_data = load_json("feedback.json", {})
#         user_feedback = feedback_data.get(user_id, [])

#         stats = {
#             "total_interactions": len(user_feedback),
#             "positive_feedback": sum(1 for f in user_feedback if f["feedback"] == "up"),
#             "negative_feedback": sum(1 for f in user_feedback if f["feedback"] == "down"),
#             "blocked_ads": sum(1 for f in user_feedback if f["feedback"] == "block"),
#             "engagement_rate": 0
#         }
#         if stats["total_interactions"]:
#             stats["engagement_rate"] = round((stats["positive_feedback"] / stats["total_interactions"]) * 100, 2)
#         return stats
#     except Exception as e:
#         return {"error": str(e)}

# @app.get("/feedback")
# def get_all_feedback():
#     return load_json("feedback.json", {})

# @app.get("/blocked_ads")
# def get_blocked_ads():
#     return load_json("blocked_ads.json", [])

# @app.post("/block_ad")
# async def block_ad_globally(request: Request):
#     try:
#         data = await request.json()
#         ad_title = data["ad_title"]
#         blocked = load_json("blocked_ads.json", [])
#         if ad_title not in blocked:
#             blocked.append(ad_title)
#             save_json("blocked_ads.json", blocked)
#         return {"status": "success", "blocked": ad_title}
#     except Exception as e:
#         return {"error": str(e)}

# @app.post("/block_ad_user")
# async def block_ad_for_user(request: Request):
#     try:
#         data = await request.json()
#         user_id, ad_title = data["user_id"], data["ad_title"]
#         user_blocked = load_json("user_blocked_ads.json", {})
#         user_blocked.setdefault(user_id, [])
#         if ad_title not in user_blocked[user_id]:
#             user_blocked[user_id].append(ad_title)
#         save_json("user_blocked_ads.json", user_blocked)
#         return {"status": "success", "user_id": user_id, "blocked": ad_title}
#     except Exception as e:
#         return {"error": str(e)}

# if __name__ == "__main__":
#     import uvicorn
#     port = int(os.environ.get("PORT", 10000))  # Render provides PORT env variable
#     uvicorn.run(app, host="0.0.0.0", port=port)


























from fastapi import FastAPI, Query, Request
from fastapi.middleware.cors import CORSMiddleware
import json
import random
import os
from datetime import datetime
from typing import Dict, List
from pathlib import Path
import httpx
from dotenv import load_dotenv
import asyncio

# Load environment variables
load_dotenv()

# Supabase configuration
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_API_KEY = os.getenv("SUPABASE_API_KEY")

if not SUPABASE_URL or not SUPABASE_API_KEY:
    raise ValueError("SUPABASE_URL and SUPABASE_API_KEY must be set in environment variables")

HEADERS = {
    "apikey": SUPABASE_API_KEY,
    "Authorization": f"Bearer {SUPABASE_API_KEY}",
    "Content-Type": "application/json"
}

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).parent
print(f"Base directory: {BASE_DIR}")

app = FastAPI(title="TrustGuard AI Backend", version="1.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ================================
# SUPABASE HELPER FUNCTIONS
# ================================
async def supabase_request(method: str, table: str, data: dict = None, params: dict = None):
    """Generic function to make requests to Supabase"""
    url = f"{SUPABASE_URL}/rest/v1/{table}"
    
    if params:
        query_string = "&".join([f"{k}=eq.{v}" for k, v in params.items()])
        url += f"?{query_string}"
    
    try:
        async with httpx.AsyncClient() as client:
            if method == "GET":
                response = await client.get(url, headers=HEADERS)
            elif method == "POST":
                response = await client.post(url, headers=HEADERS, json=data)
            elif method == "PUT":
                response = await client.put(url, headers=HEADERS, json=data)
            elif method == "PATCH":
                response = await client.patch(url, headers=HEADERS, json=data)
            elif method == "DELETE":
                response = await client.delete(url, headers=HEADERS)
            
            response.raise_for_status()
            return response.json() if response.content else []
    except httpx.RequestError as e:
        logger.error(f"Request error: {e}")
        return []
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error: {e.response.status_code} - {e.response.text}")
        return []

async def get_user_by_id(user_id: str):
    """Get user data from Supabase"""
    result = await supabase_request("GET", "users", params={"id": user_id})
    return result[0] if result else None

async def get_all_ads():
    """Get all ads from Supabase"""
    return await supabase_request("GET", "ads")

async def get_blocked_ads():
    """Get globally blocked ads from Supabase"""
    result = await supabase_request("GET", "blocked_ads")
    return [item["ad_title"] for item in result]

async def get_user_blocked_ads(user_id: str):
    """Get user-specific blocked ads from Supabase"""
    result = await supabase_request("GET", "user_blocked_ads", params={"user_id": user_id})
    return [item["ad_title"] for item in result]

async def get_user_preferences(user_id: str):
    """Get user preferences from Supabase"""
    result = await supabase_request("GET", "user_preferences", params={"user_id": user_id})
    if result:
        return result[0]
    return {
        "emotion_filter": True,
        "personalization": True,
        "explanations": True,
        "data_collection": True
    }

async def save_user_preferences(user_id: str, preferences: dict):
    """Save user preferences to Supabase"""
    # Check if preferences exist
    existing = await supabase_request("GET", "user_preferences", params={"user_id": user_id})
    
    data = {
        "user_id": user_id,
        "emotion_filter": preferences.get("emotion_filter", True),
        "personalization": preferences.get("personalization", True),
        "explanations": preferences.get("explanations", True),
        "data_collection": preferences.get("data_collection", True),
        "updated_at": datetime.now().isoformat()
    }
    
    if existing:
        # Update existing record
        await supabase_request("PATCH", f"user_preferences?user_id=eq.{user_id}", data)
    else:
        # Insert new record
        await supabase_request("POST", "user_preferences", data)

async def save_feedback(user_id: str, ad_title: str, feedback: str, emotion: str):
    """Save feedback to Supabase"""
    data = {
        "user_id": user_id,
        "ad_title": ad_title,
        "feedback": feedback,
        "emotion": emotion,
        "timestamp": datetime.now().isoformat()
    }
    await supabase_request("POST", "feedback", data)

async def get_user_feedback(user_id: str):
    """Get user feedback from Supabase"""
    return await supabase_request("GET", "feedback", params={"user_id": user_id})

async def get_all_feedback():
    """Get all feedback from Supabase"""
    return await supabase_request("GET", "feedback")

async def block_ad_for_user(user_id: str, ad_title: str):
    """Block ad for specific user"""
    data = {
        "user_id": user_id,
        "ad_title": ad_title,
        "blocked_at": datetime.now().isoformat()
    }
    result = await supabase_request("POST", "user_blocked_ads", data)
    logger.info(f"Blocked ad '{ad_title}' for user '{user_id}': {result}")
    return result

async def block_ad_globally(ad_title: str):
    """Block ad globally"""
    data = {
        "ad_title": ad_title,
        "blocked_at": datetime.now().isoformat()
    }
    await supabase_request("POST", "blocked_ads", data)



async def check_feedback_exists(user_id: str, ad_title: str):
    """Check if feedback already exists for this user and ad"""
    # FIXED: Use proper Supabase query parameters to filter by both user_id and ad_title
    url = f"{SUPABASE_URL}/rest/v1/feedback?user_id=eq.{user_id}&ad_title=eq.{ad_title}"
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=HEADERS)
            response.raise_for_status()
            result = response.json()
            return len(result) > 0
    except Exception as e:
        logger.error(f"Error checking feedback exists: {e}")
        return False



async def get_ad_feedback_stats(ad_title: str):
    """Get feedback statistics for a specific ad"""
    all_feedback = await get_all_feedback()
    ad_feedback = [f for f in all_feedback if f["ad_title"] == ad_title]
    
    up = sum(1 for f in ad_feedback if f["feedback"] == "up")
    down = sum(1 for f in ad_feedback if f["feedback"] == "down")
    block = sum(1 for f in ad_feedback if f["feedback"] == "block")
    
    return {"up": up, "down": down, "block": block}

# ================================
# EMPATHY ENGINE IMPLEMENTATION
# ================================
class EmpathyEngine:
    @staticmethod
    def analyze_user_vulnerability(user_data: Dict) -> Dict:
        status = user_data.get("status", "neutral")
        vulnerability_map = {
            "stressed": {"level": "high", "score": 0.8, "triggers": ["luxury", "pressure"]},
            "anxious": {"level": "high", "score": 0.9, "triggers": ["luxury", "social"]},
            "depressed": {"level": "high", "score": 0.85, "triggers": ["luxury", "social", "comparison"]},
            "neutral": {"level": "low", "score": 0.2, "triggers": []},
            "happy": {"level": "low", "score": 0.1, "triggers": []},
            "relaxed": {"level": "low", "score": 0.1, "triggers": []}
        }
        return vulnerability_map.get(status, vulnerability_map["neutral"])

    @staticmethod
    def filter_ads_by_emotion(ads: List[Dict], user_vulnerability: Dict) -> List[Dict]:
        if user_vulnerability["level"] == "low":
            return ads
        triggers = user_vulnerability["triggers"]
        return [ad for ad in ads if ad.get("category", "") not in triggers]

# ================================
# TRUSTFLOW++ IMPLEMENTATION
# ================================
class TrustFlowPlus:
    @staticmethod
    def predict_ad_expectation(user_data: Dict, ad_data: Dict) -> Dict:
        user_status = user_data.get("status", "neutral")
        ad_target = ad_data.get("target_audience", "neutral")
        mismatch = user_status != ad_target
        expectation_score = 0.3 if mismatch else 0.8
        return {
            "explanation_needed": mismatch,
            "expectation_score": expectation_score,
            "reason": f"User is {user_status}, ad targets {ad_target}" if mismatch else "Good match"
        }

    @staticmethod
    def generate_explanation(user_data: Dict, ad_data: Dict) -> str:
        explanations = [
            ad_data.get("explanation", ""),
            f"This ad matches users with similar interests in your area.",
            f"Based on your browsing pattern, this might interest you.",
            f"Others like you found this helpful during similar times."
        ]
        return random.choice([e for e in explanations if e])

empathy_engine = EmpathyEngine()
trustflow_plus = TrustFlowPlus()

# ================================
# MAIN ENDPOINTS
# ================================
@app.get("/")
def root():
    return {"message": "TrustGuard AI Backend v1.1 (Supabase)", "status": "running"}

@app.get("/health")
async def health_check():
    """Health check endpoint that also tests Supabase connection"""
    try:
        # Test Supabase connection
        test_result = await supabase_request("GET", "users")
        supabase_status = "connected" if test_result is not None else "disconnected"
    except Exception as e:
        supabase_status = f"error: {str(e)}"
    
    return {
        "status": "healthy",
        "supabase_status": supabase_status,
        "timestamp": datetime.now().isoformat()
    }

@app.get("/ads/{user_id}")
async def get_ad_with_ai(user_id: str):
    try:
        # Get user data
        user = await get_user_by_id(user_id)
        if not user:
            return {"error": "User not found"}

        # Get all necessary data
        ads = await get_all_ads()
        blocked_ads = await get_blocked_ads()
        user_blocked_ads = await get_user_blocked_ads(user_id)
        user_preferences = await get_user_preferences(user_id)

        # Empathy Engine
        vulnerability = empathy_engine.analyze_user_vulnerability(user)
        emotionally_safe_ads = empathy_engine.filter_ads_by_emotion(ads, vulnerability) if user_preferences["emotion_filter"] else ads

        # Apply blocklists
        final_ads = [ad for ad in emotionally_safe_ads if ad["title"] not in blocked_ads and ad["title"] not in user_blocked_ads]

        if not final_ads:
            return {"error": "No suitable ads available."}

        selected_ad = random.choice(final_ads)

        # Handle personalization logic - TrustFlow+
        if user_preferences["personalization"]:
            trust_analysis = trustflow_plus.predict_ad_expectation(user, selected_ad)
            explanation = trustflow_plus.generate_explanation(user, selected_ad) if user_preferences["explanations"] and trust_analysis["explanation_needed"] else ""
        else:
            trust_analysis = {
                "expectation_score": "N/A",
                "reason": "Personalization disabled"
            }
            explanation = ""

        return {
            "ad": selected_ad,
            "explanation_needed": user_preferences["explanations"] and trust_analysis.get("explanation_needed", False),
            "explanation": explanation,
            "empathy_analysis": {
                "vulnerability_level": vulnerability["level"],
                "vulnerability_score": vulnerability["score"],
                "filtered_by_emotion": user_preferences["emotion_filter"] and vulnerability["level"] == "high"
            },
            "trust_analysis": {
                "expectation_score": trust_analysis["expectation_score"],
                "reason": trust_analysis["reason"]
            }
        }

    except Exception as e:
        logger.error(f"Error in get_ad_with_ai: {str(e)}")
        return {"error": str(e)}

@app.post("/feedback")
async def receive_feedback(request: Request):
    try:
        data = await request.json()
        user_id, ad_title, feedback = data["user_id"], data["ad_title"], data["feedback"]
        emotion = data.get("emotion", "neutral")

        # Check if user opted out of data collection
        user_preferences = await get_user_preferences(user_id)
        if not user_preferences.get("data_collection", True):
            return {
                "status": "opted_out",
                "message": "User has opted out of data collection. Feedback not saved."
            }

        # Get ad data for emotion if not provided
        if not emotion:
            ads = await get_all_ads()
            ad = next((a for a in ads if a["title"] == ad_title), None)
            if ad:
                emotion = ad.get("target_audience", "neutral")

        # Check for duplicate feedback
        feedback_exists = await check_feedback_exists(user_id, ad_title)
        if feedback_exists:
            stats = await get_ad_feedback_stats(ad_title)
            return {
                "status": "duplicate",
                "message": "Feedback already submitted.",
                "stats": stats
            }

        # Save feedback
        await save_feedback(user_id, ad_title, feedback, emotion)
        logger.info(f"Feedback saved: user={user_id}, ad={ad_title}, feedback={feedback}")

        # FIXED: Handle blocking - Now with proper error handling and logging
        if feedback == "block":
            try:
                block_result = await block_ad_for_user(user_id, ad_title)
                logger.info(f"Successfully blocked ad '{ad_title}' for user '{user_id}'")
            except Exception as block_error:
                logger.error(f"Error blocking ad for user: {block_error}")
                # Still continue with feedback response even if blocking fails


        # Get updated stats
        stats = await get_ad_feedback_stats(ad_title)

        return {
            "status": "success",
            "message": "Feedback recorded successfully." + (" Ad blocked for future." if feedback == "block" else ""),
            "stats": stats,
            "blocked": feedback == "block"
        }
    
    except Exception as e:
        logger.error(f"Error in receive_feedback: {str(e)}")
        return {"error": str(e)}

@app.post("/set_preferences")
async def set_user_preferences(request: Request):
    try:
        data = await request.json()
        user_id = data["user_id"]
        preferences = data.get("preferences", {})

        await save_user_preferences(user_id, preferences)
        saved_prefs = await get_user_preferences(user_id)
        
        return {"status": "success", "preferences": saved_prefs}
    except Exception as e:
        logger.error(f"Error in set_user_preferences: {str(e)}")
        return {"error": str(e)}

@app.get("/get_preferences/{user_id}")
async def get_user_preferences_endpoint(user_id: str):
    try:
        preferences = await get_user_preferences(user_id)
        return preferences
    except Exception as e:
        logger.error(f"Error in get_user_preferences: {str(e)}")
        return {"error": str(e)}

# ================================
# ANALYTICS & ADMIN
# ================================
@app.get("/analytics/user/{user_id}")
async def get_user_analytics(user_id: str):
    try:
        user_feedback = await get_user_feedback(user_id)

        stats = {
            "total_interactions": len(user_feedback),
            "positive_feedback": sum(1 for f in user_feedback if f["feedback"] == "up"),
            "negative_feedback": sum(1 for f in user_feedback if f["feedback"] == "down"),
            "blocked_ads": sum(1 for f in user_feedback if f["feedback"] == "block"),
            "engagement_rate": 0
        }
        if stats["total_interactions"]:
            stats["engagement_rate"] = round((stats["positive_feedback"] / stats["total_interactions"]) * 100, 2)
        return stats
    except Exception as e:
        logger.error(f"Error in get_user_analytics: {str(e)}")
        return {"error": str(e)}

@app.get("/feedback")
async def get_all_feedback_endpoint():
    try:
        return await get_all_feedback()
    except Exception as e:
        logger.error(f"Error in get_all_feedback: {str(e)}")
        return {"error": str(e)}

@app.get("/blocked_ads")
async def get_blocked_ads_endpoint():
    try:
        return await get_blocked_ads()
    except Exception as e:
        logger.error(f"Error in get_blocked_ads: {str(e)}")
        return {"error": str(e)}

@app.post("/block_ad")
async def block_ad_globally_endpoint(request: Request):
    try:
        data = await request.json()
        ad_title = data["ad_title"]
        await block_ad_globally(ad_title)
        return {"status": "success", "blocked": ad_title}
    except Exception as e:
        logger.error(f"Error in block_ad_globally: {str(e)}")
        return {"error": str(e)}

@app.post("/block_ad_user")
async def block_ad_for_user_endpoint(request: Request):
    try:
        data = await request.json()
        user_id, ad_title = data["user_id"], data["ad_title"]
        await block_ad_for_user(user_id, ad_title)
        return {"status": "success", "user_id": user_id, "blocked": ad_title}
    except Exception as e:
        logger.error(f"Error in block_ad_for_user: {str(e)}")
        return {"error": str(e)}

# ================================
# DEBUG ENDPOINTS (Optional - for testing)
# ================================
@app.get("/debug/supabase")
async def debug_supabase():
    """Debug endpoint to test Supabase connection and data"""
    try:
        tables_status = {}
        tables = ["users", "ads", "blocked_ads", "user_blocked_ads", "feedback", "user_preferences"]
        
        for table in tables:
            try:
                data = await supabase_request("GET", table)
                tables_status[table] = {
                    "status": "connected",
                    "record_count": len(data) if data else 0,
                    "sample_data": data[:2] if data else []
                }
            except Exception as e:
                tables_status[table] = {
                    "status": "error",
                    "error": str(e)
                }
        
        return {
            "supabase_url": SUPABASE_URL,
            "tables_status": tables_status,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {"error": str(e)}
    


# ================================
# NEW DEBUG ENDPOINT FOR TESTING BLOCK FUNCTIONALITY
# ================================
@app.get("/debug/user_blocked_ads/{user_id}")
async def debug_user_blocked_ads(user_id: str):
    """Debug endpoint to check user's blocked ads"""
    try:
        blocked_ads = await get_user_blocked_ads(user_id)
        
        # Also get raw data from the table
        raw_data = await supabase_request("GET", "user_blocked_ads", params={"user_id": user_id})
        
        return {
            "user_id": user_id,
            "blocked_ads_list": blocked_ads,
            "raw_blocked_data": raw_data,
            "total_blocked": len(blocked_ads)
        }
    except Exception as e:
        logger.error(f"Error in debug_user_blocked_ads: {str(e)}")
        return {"error": str(e)}



if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)