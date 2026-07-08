import requests
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class FactVerifier:
    @staticmethod
    def verify_fact(topic: str) -> Dict[str, Any]:
        """
        Searches Wikipedia for the topic, retrieves the top search match,
        and fetches a concise summary using the Wikipedia REST API.
        """
        # Step 1: Search for the topic to get the best-matching title
        search_url = "https://en.wikipedia.org/w/api.php"
        search_params = {
            "action": "query",
            "list": "search",
            "srsearch": topic,
            "format": "json",
            "utf8": 1,
            "srlimit": 1
        }
        
        headers = {
            "User-Agent": "PersonalizedNetworkingAssistant/1.0 (contact: suren.gemini@gmail.com)"
        }
        
        try:
            response = requests.get(search_url, params=search_params, headers=headers, timeout=10)
            response.raise_for_status()
            search_data = response.json()
            
            search_results = search_data.get("query", {}).get("search", [])
            if not search_results:
                return {
                    "topic": topic,
                    "summary": f"Could not find any Wikipedia articles matching '{topic}'. Please try a different query.",
                    "source_url": None,
                    "found": False
                }
            
            # Extract page title of the top match
            top_match = search_results[0]
            title = top_match["title"]
            
            # Step 2: Fetch the page summary using Wikipedia REST API
            # Encode spaces and special characters
            encoded_title = requests.utils.quote(title)
            summary_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{encoded_title}"
            
            summary_response = requests.get(summary_url, headers=headers, timeout=10)
            if summary_response.status_code == 200:
                summary_data = summary_response.json()
                
                extract = summary_data.get("extract", "")
                source_url = summary_data.get("content_urls", {}).get("desktop", {}).get("page", None)
                display_title = summary_data.get("title", title)
                
                if not extract:
                    extract = f"Wikipedia article found: '{display_title}', but no text summary was available."
                
                return {
                    "topic": display_title,
                    "summary": extract,
                    "source_url": source_url,
                    "found": True
                }
            else:
                # Fallback to MediaWiki API if REST API fails
                logger.warning(f"REST API failed with code {summary_response.status_code}. Using action=query fallback.")
                fallback_url = "https://en.wikipedia.org/w/api.php"
                fallback_params = {
                    "action": "query",
                    "prop": "extracts",
                    "exintro": 1,
                    "explaintext": 1,
                    "titles": title,
                    "format": "json"
                }
                fallback_res = requests.get(fallback_url, params=fallback_params, headers=headers, timeout=10)
                fallback_res.raise_for_status()
                pages = fallback_res.json().get("query", {}).get("pages", {})
                page_id = list(pages.keys())[0]
                
                if page_id != "-1":
                    extract = pages[page_id].get("extract", "")
                    page_title = pages[page_id].get("title", title)
                    source_url = f"https://en.wikipedia.org/wiki/{requests.utils.quote(page_title)}"
                    return {
                        "topic": page_title,
                        "summary": extract or f"Article found but extract is empty.",
                        "source_url": source_url,
                        "found": True
                    }
                    
                return {
                    "topic": topic,
                    "summary": f"Found match '{title}' but failed to retrieve its summary.",
                    "source_url": None,
                    "found": False
                }
                
        except Exception as e:
            logger.error(f"Error checking Wikipedia for '{topic}': {e}")
            return {
                "topic": topic,
                "summary": f"Error connecting to Wikipedia API: {str(e)}. Please check your internet connection and try again.",
                "source_url": None,
                "found": False
            }

FactVerifierInstance = FactVerifier()
