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

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Check if we're on Render or local
IS_RENDER = os.environ.get('RENDER') is not None

if IS_RENDER:
    # On Render, try to use a writable directory
    BASE_DIR = Path('/tmp/trustguard_data')  # Use /tmp for temporary writable storage
    BASE_DIR.mkdir(parents=True, exist_ok=True)
    logger.info(f"Running on Render, using temporary directory: {BASE_DIR}")
else:
    # Local development
    BASE_DIR = Path(__file__).parent
    logger.info(f"Running locally, using: {BASE_DIR}")

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
# UTILITIES WITH BETTER ERROR HANDLING
# ================================
def get_default_data(filename: str):
    """Get default data for each JSON file"""
    defaults = {
        "users.json": {
            "u1": {"name": "Alice", "status": "neutral", "age": 25, "location": "Mumbai"},
            "u2": {"name": "Bob", "status": "stressed", "age": 30, "location": "Delhi"},
            "u3": {"name": "Carol", "status": "happy", "age": 28, "location": "Bangalore"}
        },
        "ads.json": [
            {"title": "Budget Smartphone", "category": "tech", "target_audience": "neutral", "explanation": "Great value for money"},
            {"title": "Luxury Watch", "category": "luxury", "target_audience": "stressed", "explanation": "Treat yourself"},
            {"title": "Meditation App", "category": "wellness", "target_audience": "anxious", "explanation": "Find your peace"}
        ],
        "feedback.json": {},
        "blocked_ads.json": [],
        "user_blocked_ads.json": {},
        "user_preferences.json": {}
    }
    return defaults.get(filename, {})

def load_json(file: str, default=None):
    """Load JSON with better error handling and default data"""
    if default is None:
        default = get_default_data(file)
    
    file_path = BASE_DIR / file
    logger.info(f"Trying to load file: {file_path}")
    
    if file_path.exists():
        logger.info(f"File {file_path} exists, attempting to read")
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                logger.info(f"Successfully loaded {file_path}")
                return data
        except Exception as e:
            logger.error(f"Error reading {file_path}: {e}")
            logger.info(f"Using default data for {file}")
            return default
    else:
        logger.warning(f"File {file_path} does not exist, using default data")
        # Try to create the file with default data
        save_success = save_json(file, default)
        if save_success:
            logger.info(f"Created {file_path} with default data")
        else:
            logger.warning(f"Could not create {file_path}, using in-memory default")
        return default

def save_json(file: str, data) -> bool:
    """Save JSON with proper error handling"""
    file_path = BASE_DIR / file
    try:
        # Ensure directory exists
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write to temporary file first, then move (atomic operation)
        temp_file = file_path.with_suffix('.tmp')
        with open(temp_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        # Move temp file to actual file
        temp_file.replace(file_path)
        
        logger.info(f"Successfully saved {file_path}")
        return True
    except Exception as e:
        logger.error(f"Failed to save {file_path}: {e}")
        logger.error(f"Error type: {type(e).__name__}")
        logger.error(f"Current working directory: {os.getcwd()}")
        logger.error(f"Base directory exists: {BASE_DIR.exists()}")
        logger.error(f"Base directory writable: {os.access(BASE_DIR, os.W_OK)}")
        return False

# ================================
# DEBUG ENDPOINTS
# ================================
@app.get("/debug/files")
def debug_files():
    try:
        files_status = {}
        files_to_check = ["users.json", "ads.json", "blocked_ads.json", "user_blocked_ads.json", "feedback.json", "user_preferences.json"]
        
        for file in files_to_check:
            file_path = BASE_DIR / file
            files_status[file] = {
                "exists": file_path.exists(),
                "size": file_path.stat().st_size if file_path.exists() else 0,
                "readable": os.access(file_path, os.R_OK) if file_path.exists() else False,
                "writable": os.access(file_path, os.W_OK) if file_path.exists() else False,
                "full_path": str(file_path)
            }
        
        return {
            "is_render": IS_RENDER,
            "current_directory": os.getcwd(),
            "base_directory": str(BASE_DIR),
            "base_dir_exists": BASE_DIR.exists(),
            "base_dir_writable": os.access(BASE_DIR, os.W_OK),
            "files_in_base_directory": [str(p.name) for p in BASE_DIR.iterdir()] if BASE_DIR.exists() else [],
            "files_status": files_status
        }
    except Exception as e:
        return {"error": str(e)}

@app.get("/debug/users")
def debug_users():
    try:
        users = load_json("users.json", {})
        return {
            "users_data": users,
            "user_count": len(users),
            "user_ids": list(users.keys())
        }
    except Exception as e:
        return {"error": str(e)}

@app.get("/debug/write-test")
def test_write():
    """Test if we can write to the file system"""
    try:
        test_file = BASE_DIR / "test_write.json"
        test_data = {"test": "data", "timestamp": str(datetime.now())}
        
        success = save_json("test_write.json", test_data)
        
        if success and test_file.exists():
            # Try to read it back
            with open(test_file, "r") as f:
                data = json.load(f)
            
            return {
                "success": True, 
                "data": data, 
                "path": str(test_file),
                "message": "Write test successful"
            }
        else:
            return {
                "success": False, 
                "error": "Could not write file",
                "path": str(test_file)
            }
    except Exception as e:
        return {"success": False, "error": str(e)}

# ================================
# MAIN ENDPOINTS
# ================================
@app.get("/")
def root():
    return {"message": "TrustGuard AI Backend v1.1", "status": "running"}

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "is_render": IS_RENDER,
        "base_dir": str(BASE_DIR)
    }

@app.get("/ads/{user_id}")
def get_ad_with_ai(user_id: str):
    try:
        users = load_json("users.json", {})
        ads = load_json("ads.json", [])
        blocked_ads = load_json("blocked_ads.json", [])
        user_blocked_ads = load_json("user_blocked_ads.json", {})
        user_preferences = load_json("user_preferences.json", {})

        user = users.get(user_id)
        if not user:
            return {"error": "User not found"}

        prefs = user_preferences.get(user_id, {
            "emotion_filter": True,
            "personalization": True,
            "explanations": True
        })

        # Empathy Engine
        vulnerability = empathy_engine.analyze_user_vulnerability(user)
        emotionally_safe_ads = empathy_engine.filter_ads_by_emotion(ads, vulnerability) if prefs["emotion_filter"] else ads

        # Apply blocklists
        user_blocked = user_blocked_ads.get(user_id, [])
        final_ads = [ad for ad in emotionally_safe_ads if ad["title"] not in blocked_ads and ad["title"] not in user_blocked]

        if not final_ads:
            return {"error": "No suitable ads available."}

        selected_ad = random.choice(final_ads)

        # Handle personalization logic
        if prefs["personalization"]:
            trust_analysis = trustflow_plus.predict_ad_expectation(user, selected_ad)
            explanation = trustflow_plus.generate_explanation(user, selected_ad) if prefs["explanations"] and trust_analysis["explanation_needed"] else ""
        else:
            trust_analysis = {
                "expectation_score": "N/A",
                "reason": "Personalization disabled"
            }
            explanation = ""

        return {
            "ad": selected_ad,
            "explanation_needed": prefs["explanations"] and trust_analysis.get("explanation_needed", False),
            "explanation": explanation,
            "empathy_analysis": {
                "vulnerability_level": vulnerability["level"],
                "vulnerability_score": vulnerability["score"],
                "filtered_by_emotion": prefs["emotion_filter"] and vulnerability["level"] == "high"
            },
            "trust_analysis": {
                "expectation_score": trust_analysis["expectation_score"],
                "reason": trust_analysis["reason"]
            }
        }

    except Exception as e:
        return {"error": str(e)}

@app.post("/feedback")
async def receive_feedback(request: Request):
    try:
        data = await request.json()
        user_id, ad_title, feedback = data["user_id"], data["ad_title"], data["feedback"]
        emotion = data.get("emotion", "neutral")

        # Check if user opted out of data collection
        user_preferences = load_json("user_preferences.json", {})
        prefs = user_preferences.get(user_id, {
            "data_collection": True
        })

        if not prefs.get("data_collection", True):
            return {
                "status": "opted_out",
                "message": "User has opted out of data collection. Feedback not saved."
            }

        # Continue as usual
        ads = load_json("ads.json", [])
        ad = next((a for a in ads if a["title"] == ad_title), None)
        if ad and not emotion:
            emotion = ad.get("target_audience", "neutral")

        feedback_data = load_json("feedback.json", {})
        feedback_data.setdefault(user_id, [])

        if any(entry["ad_title"] == ad_title for entry in feedback_data[user_id]):
            up = down = block = 0
            for entries in feedback_data.values():
                for entry in entries:
                    if entry["ad_title"] == ad_title:
                        if entry["feedback"] == "up": up += 1
                        if entry["feedback"] == "down": down += 1
                        if entry["feedback"] == "block": block += 1
            return {
                "status": "duplicate",
                "message": "Feedback already submitted.",
                "stats": {"up": up, "down": down, "block": block}
            }

        feedback_data[user_id].append({
            "ad_title": ad_title,
            "feedback": feedback,
            "timestamp": datetime.now().isoformat(),
            "emotion": emotion
        })
        
        save_success = save_json("feedback.json", feedback_data)
        if not save_success:
            logger.error("Failed to save feedback data")
            return {"error": "Failed to save feedback data"}

        if feedback == "block":
            blocked = load_json("user_blocked_ads.json", {})
            blocked.setdefault(user_id, [])
            if ad_title not in blocked[user_id]:
                blocked[user_id].append(ad_title)
            save_json("user_blocked_ads.json", blocked)

        up = down = block = 0
        for entries in feedback_data.values():
            for entry in entries:
                if entry["ad_title"] == ad_title:
                    if entry["feedback"] == "up": up += 1
                    if entry["feedback"] == "down": down += 1
                    if entry["feedback"] == "block": block += 1

        return {
            "status": "success",
            "message": "Feedback recorded.",
            "stats": {"up": up, "down": down, "block": block},
            "save_success": save_success
        }

    except Exception as e:
        logger.error(f"Error in feedback endpoint: {e}")
        return {"error": str(e)}

@app.post("/set_preferences")
async def set_user_preferences(request: Request):
    try:
        data = await request.json()
        user_id = data["user_id"]
        preferences = data.get("preferences", {})

        # Extract preferences from nested object
        emotion_filter = preferences.get("emotion_filter", True)
        personalization = preferences.get("personalization", True)
        explanations = preferences.get("explanations", True)
        data_collection = preferences.get("data_collection", True)

        prefs = load_json("user_preferences.json", {})
        prefs[user_id] = {
            "emotion_filter": emotion_filter,
            "personalization": personalization,
            "explanations": explanations,
            "data_collection": data_collection
        }

        save_success = save_json("user_preferences.json", prefs)
        if not save_success:
            logger.error("Failed to save user preferences")
            return {"error": "Failed to save user preferences"}

        return {
            "status": "success", 
            "preferences": prefs[user_id],
            "save_success": save_success
        }
    except Exception as e:
        logger.error(f"Error in set_preferences endpoint: {e}")
        return {"error": str(e)}

@app.get("/get_preferences/{user_id}")
def get_user_preferences(user_id: str):
    prefs = load_json("user_preferences.json", {})
    return prefs.get(user_id, {
        "emotion_filter": True,
        "personalization": True,
        "explanations": True,
        "data_collection": True
    })

# ================================
# ANALYTICS & ADMIN
# ================================
@app.get("/analytics/user/{user_id}")
def get_user_analytics(user_id: str):
    try:
        feedback_data = load_json("feedback.json", {})
        user_feedback = feedback_data.get(user_id, [])

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
        return {"error": str(e)}

@app.get("/feedback")
def get_all_feedback():
    return load_json("feedback.json", {})

@app.get("/blocked_ads")
def get_blocked_ads():
    return load_json("blocked_ads.json", [])

@app.post("/block_ad")
async def block_ad_globally(request: Request):
    try:
        data = await request.json()
        ad_title = data["ad_title"]
        blocked = load_json("blocked_ads.json", [])
        if ad_title not in blocked:
            blocked.append(ad_title)
            save_success = save_json("blocked_ads.json", blocked)
            if not save_success:
                return {"error": "Failed to save blocked ads"}
        return {"status": "success", "blocked": ad_title}
    except Exception as e:
        return {"error": str(e)}

@app.post("/block_ad_user")
async def block_ad_for_user(request: Request):
    try:
        data = await request.json()
        user_id, ad_title = data["user_id"], data["ad_title"]
        user_blocked = load_json("user_blocked_ads.json", {})
        user_blocked.setdefault(user_id, [])
        if ad_title not in user_blocked[user_id]:
            user_blocked[user_id].append(ad_title)
        save_success = save_json("user_blocked_ads.json", user_blocked)
        if not save_success:
            return {"error": "Failed to save user blocked ads"}
        return {"status": "success", "user_id": user_id, "blocked": ad_title}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)