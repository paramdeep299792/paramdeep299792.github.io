import json
import os
from google import genai
from google.genai import types
from pathlib import Path
import logging

from .core.utils.load import GEMINI_API_KEY
from .core.utils.general import exception_handler
from .core.utils.logging_config import setup_logging

logger = logging.getLogger(__name__)

def load_data(json_file):
    with open(json_file, 'r', encoding='utf-8') as f:
        return json.load(f)

SYSTEM_PROMPT = """
You are an expert personal branding copywriter and career strategist for tech professionals. Your task is to generate highly optimized, platform-specific profile bios and summaries based strictly on the provided JSON resume data.

### INPUTS PROVIDED BY USER
1. TARGET PLATFORM: The specific social media or developer platform (e.g., LinkedIn, GitHub, X, Instagram).
2. JSON DATA: The user's career, education, and project history.

### GENERATION RULES
1. Strict Factuality: DO NOT hallucinate, invent, or embellish skills, metrics, or roles. Extract facts only from the provided JSON.
2. Prioritization: Always highlight the most current education (e.g., M.Tech at NIT Jalandhar), highest-prestige recent experiences (e.g., IIT Ropar), and major awards (e.g., SIH Winner).
3. Keyword Optimization: Naturally integrate technical keywords (e.g., XAI, Federated Learning, PyTorch) relevant to the user's research focus.
4. Tone: Professional, forward-looking, and quietly confident. 

### PLATFORM CONSTRAINTS
Automatically apply the following rules based on the TARGET PLATFORM:
* LinkedIn About: Limit to 3-4 short paragraphs. Focus on the narrative connecting the user's education, research interests, and project outcomes. Include a "Technical Expertise" list at the bottom.
* LinkedIn Headline: Max 220 characters. Format as: [Role] | [Key Interest 1] & [Key Interest 2] | [Notable Achievement].
* GitHub README: Output in clean Markdown. Include a brief intro, bulleted list of current focus/research, tech stack, and contact links.
* X / Twitter Bio: Max 160 characters. Use | dividers. Include 1-2 relevant emojis. 
* Instagram / Threads Bio: Max 150 characters. Use vertical stacking (one point per line) with emojis.

### OUTPUT FORMAT
Output ONLY the requested bio/summary text. Do not include conversational filler, meta-commentary, or markdown formatting unless specifically requested by the platform constraint (e.g., GitHub).
"""

def generate_platform_content(client, platform_name, json_string):
    logger.info(f"Generating content for {platform_name}...")
    
    user_prompt = f"TARGET PLATFORM: {platform_name}\n\nJSON DATA:\n{json_string}"
    
    response = client.models.generate_content(
        model='gemini-3.8-flash',
        contents=user_prompt,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            temperature=0.7,
        )
    )
    return response.text.strip()

def main():
    src_dir = Path(__file__).resolve().parent
    root_dir = src_dir.parent
    json_filename =  root_dir / 'params.json'
    output_filename = root_dir / "outputs" / 'bio.txt'

    os.environ["GEMINI_API_KEY"] = GEMINI_API_KEY

    try:
        json_string = load_data(json_filename)
    except FileNotFoundError:
        print(f"Error: Could not find '{json_filename}'")
        return

    client = genai.Client()
    
    platforms = [
        "GitHub README",
        "LinkedIn About Section",
        "LinkedIn Headline",
        "X / Twitter Bio",
        "Instagram / Threads Bio"
    ]
    
    with open(output_filename, 'w', encoding='utf-8') as f:
        f.write("=== AI-GENERATED PUBLIC PROFILES ===\n\n")

    for platform in platforms:
        content = generate_platform_content(client, platform, json_string)
        
        with open(output_filename, 'a', encoding='utf-8') as f:
            f.write(f"--- {platform.upper()} ---\n")
            f.write(content + "\n\n")
            
    print(f"\nSuccess! All profiles generated and saved to {output_filename}")

if __name__ == "__main__":
    main()