import json
import re
import logging
from typing import List, Optional, Dict
import google.generativeai as genai
from backend.app.config import settings

logger = logging.getLogger(__name__)

class TextGenerator:
    @staticmethod
    def generate_fallback(themes: List[str], event_desc: str, interests: str) -> List[str]:
        """
        Generates conversation starters using pre-defined professional templates.
        """
        starters = []
        t_len = len(themes)
        
        # Primary templates
        if t_len >= 2:
            t1, t2 = themes[0], themes[1]
            starters.append(f"Hi! I was thinking about the event topic, and it got me wondering: how do you see the intersection of {t1} and {t2} evolving in the next couple of years?")
            starters.append(f"It's fascinating how {t1} is impacting the industry. What do you think is the biggest bottleneck professionals face when integrating it with {t2}?")
            starters.append(f"I'm really interested in both {t1} and {t2}. Are you currently working on any projects that bring these two areas together?")
        elif t_len == 1:
            t1 = themes[0]
            starters.append(f"Hi! What got you interested in the {t1} space? I've been following it closely and wanted to hear how others are approaching it.")
            starters.append(f"Regarding the event theme of {t1}, do you think the current industry standards are ready for the sudden wave of new developments?")
            starters.append(f"I find {t1} to be incredibly dynamic. In your experience, what is a common misconception people have about it?")
        else:
            # Fallback if no themes could be extracted
            starters.append(f"Hi! What brought you to this event today? I'm hoping to learn more about how different industries are adapting to these topics.")
            starters.append(f"It's great to connect! What are your main takeaways or expectations from the presentations today?")
            starters.append(f"Hello! I'm exploring new perspectives on these event topics. How does this align with the work you do daily?")

        return starters[:3]

    @classmethod
    def generate_starters(
        cls, 
        event_desc: str, 
        interests: str, 
        themes: List[str], 
        few_shot_examples: Optional[List[str]] = None,
        api_key: Optional[str] = None
    ) -> List[str]:
        """
        Generates 2-3 conversation starters. Integrates with Gemini if API key is present.
        """
        effective_key = api_key or settings.GEMINI_API_KEY
        if not effective_key:
            logger.info("GEMINI_API_KEY not found. Running starter generation in fallback mode.")
            return cls.generate_fallback(themes, event_desc, interests)

        try:
            genai.configure(api_key=effective_key)
            model = genai.GenerativeModel("gemini-1.5-flash")
            
            # Setup prompt and feed positive feedback examples if available
            few_shot_str = ""
            if few_shot_examples:
                few_shot_str = "Here are examples of conversation starters that the user previously liked (thumbs-up):\n"
                for i, ex in enumerate(few_shot_examples, 1):
                    few_shot_str += f"- \"{ex}\"\n"
                few_shot_str += "\nTry to mimic the professional, engaging, and context-appropriate tone of these examples while applying them to the new event.\n\n"

            prompt = (
                "You are an expert communications coach and professional networking strategist. "
                "Your goal is to generate 2 to 3 engaging, personalized, and context-aware conversation starters "
                "for a networking event based on the event description and the user's interests.\n\n"
                f"Event Description: {event_desc}\n"
                f"User Interests: {interests}\n"
                f"Extracted Themes: {', '.join(themes)}\n\n"
                f"{few_shot_str}"
                "Instructions:\n"
                "1. Generate exactly 3 conversation starters.\n"
                "2. Ensure they are natural, professional, easy to say, and encourage open-ended discussion.\n"
                "3. Keep each starter concise (1-2 sentences).\n"
                "4. Output ONLY a valid JSON list of strings. Do not include markdown code block styling or extra text.\n"
                "Example response structure: [\"Starter 1\", \"Starter 2\", \"Starter 3\"]"
            )

            response = model.generate_content(prompt)
            text = response.text.strip()
            
            # Clean response text if model wrapped it in markdown code blocks
            if text.startswith("```"):
                text = re.sub(r"^```(?:json)?\n", "", text)
                text = re.sub(r"\n```$", "", text)
                text = text.strip()

            starters = json.loads(text)
            if isinstance(starters, list):
                return [str(s) for s in starters][:3]
                
            return cls.generate_fallback(themes, event_desc, interests)
        except Exception as e:
            logger.error(f"Error generating starters with Gemini API: {e}. Falling back.")
            return cls.generate_fallback(themes, event_desc, interests)

TextGeneratorInstance = TextGenerator()
