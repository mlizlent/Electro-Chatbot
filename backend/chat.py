import os
import base64
from pathlib import Path
from typing import Optional, Tuple
import httpx
import asyncio
from dotenv import load_dotenv
from circuit import CIRCUIT_SYSTEM_PROMPT, extract_and_render_circuit
from circuit_animator import generate_animated_circuit

# Load .env from the same directory as this file
load_dotenv(dotenv_path=Path(__file__).parent / ".env")

# Groq configuration (free API)
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")

# Hugging Face for vision and image generation
HF_API_KEY = os.getenv("HF_API_KEY", "")

# Multiple vision models for comprehensive analysis
VISION_MODELS = {
    "caption": "nlpconnect/vit-gpt2-image-captioning",  # General image captioning
    "detailed": "Salesforce/blip-image-captioning-large",  # Detailed descriptions
    "objects": "facebook/detr-resnet-50",  # Object detection (DETR)
}

# Image generation model
IMAGE_GEN_MODEL = "runwayml/stable-diffusion-v1-5"  # SD 1.5 - more reliable on Inference API

SYSTEM_PROMPT = """You are ElectroBot, an electronics expert specializing in circuits, IoT, and embedded systems.

VISION: You analyze circuit images using AI models that provide:
- General description
- Detailed component view  
- Detected objects with confidence scores

Use this to identify components, explain functionality, and troubleshoot issues.

Provide clear answers with component values and part numbers. Include safety warnings for high voltage/current.

{CIRCUIT_SYSTEM_PROMPT}
"""


async def detect_objects_in_image(image_bytes: bytes) -> list:
    """Detect objects/components in image using DETR object detection."""
    if not HF_API_KEY:
        return []
    
    try:
        api_url = f"https://api-inference.huggingface.co/models/{VISION_MODELS['objects']}"
        
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                api_url,
                headers={
                    "Authorization": f"Bearer {HF_API_KEY}",
                    "Content-Type": "application/octet-stream"
                },
                content=image_bytes
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"Object detection result: {result}")
                
                # DETR returns list of detected objects with labels and scores
                if isinstance(result, list):
                    # Filter objects with confidence > 0.5
                    detected = [obj for obj in result if obj.get('score', 0) > 0.5]
                    return detected
            elif response.status_code == 503:
                print("Object detection model is loading")
            else:
                print(f"Object detection error: {response.text[:200]}")
                
        return []
    except Exception as e:
        print(f"Object detection error: {e}")
        return []


async def get_image_caption(image_bytes: bytes, model_key: str) -> str:
    """Get image caption from a specific vision model."""
    if not HF_API_KEY:
        return ""
    
    try:
        api_url = f"https://api-inference.huggingface.co/models/{VISION_MODELS[model_key]}"
        
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                api_url,
                headers={
                    "Authorization": f"Bearer {HF_API_KEY}",
                    "Content-Type": "application/octet-stream"
                },
                content=image_bytes
            )
            
            if response.status_code == 200:
                result = response.json()
                
                if isinstance(result, list) and len(result) > 0:
                    return result[0].get("generated_text", "")
                elif isinstance(result, dict) and "generated_text" in result:
                    return result["generated_text"]
            elif response.status_code == 503:
                print(f"{model_key} model is loading")
            else:
                print(f"{model_key} caption error: {response.text[:200]}")
                
        return ""
    except Exception as e:
        print(f"{model_key} caption error: {e}")
        return ""


async def analyze_circuit_image(image_data_b64: str) -> str:
    """Comprehensive circuit image analysis using multiple vision models."""
    if not HF_API_KEY:
        print("Vision analysis skipped: HF_API_KEY not set")
        return "[Vision analysis unavailable - HF_API_KEY not set]"
    
    try:
        print(f"Starting comprehensive vision analysis...")
        # Decode base64 to bytes
        image_bytes = base64.b64decode(image_data_b64)
        print(f"Image size: {len(image_bytes)} bytes")
        
        # Run multiple analyses in parallel
        caption_task = get_image_caption(image_bytes, "caption")
        detailed_task = get_image_caption(image_bytes, "detailed")
        objects_task = detect_objects_in_image(image_bytes)
        
        # Wait for all analyses to complete
        caption, detailed_caption, detected_objects = await asyncio.gather(
            caption_task, detailed_task, objects_task, return_exceptions=True
        )
        
        # Build concise analysis to save tokens
        analysis_parts = []
        
        if detailed_caption and not isinstance(detailed_caption, Exception):
            # Use only detailed caption, skip general one to save tokens
            analysis_parts.append(f"View: {detailed_caption[:150]}")
            print(f"Detailed caption: {detailed_caption}")
        elif caption and not isinstance(caption, Exception):
            analysis_parts.append(f"View: {caption[:150]}")
            print(f"Caption: {caption}")
        
        if detected_objects and not isinstance(detected_objects, Exception) and len(detected_objects) > 0:
            # Group objects by label
            object_counts = {}
            for obj in detected_objects:
                label = obj.get('label', 'unknown')
                score = obj.get('score', 0)
                if label in object_counts:
                    object_counts[label]['count'] += 1
                    object_counts[label]['max_score'] = max(object_counts[label]['max_score'], score)
                else:
                    object_counts[label] = {'count': 1, 'max_score': score}
            
            # Format detected objects (top 5 only to save tokens)
            top_objects = sorted(object_counts.items(), key=lambda x: x[1]['max_score'], reverse=True)[:5]
            objects_str = ", ".join([
                f"{count['count']}x {label}"
                for label, count in top_objects
            ])
            analysis_parts.append(f"Components: {objects_str}")
            print(f"Detected objects: {objects_str}")
        
        if analysis_parts:
            full_analysis = " | ".join(analysis_parts)
            return f"IMAGE: {full_analysis}. Analyze this circuit."
        else:
            return "[Image uploaded - models loading, retry in 30s]"
            
    except Exception as e:
        print(f"Image analysis error: {str(e)}")
        import traceback
        traceback.print_exc()
        return f"[Image error: {str(e)[:50]}]"


async def generate_circuit_image(circuit_description: str) -> Optional[str]:
    """Generate realistic circuit/schematic images using Stable Diffusion."""
    if not HF_API_KEY:
        print("Image generation skipped: HF_API_KEY not set")
        return None
    
    try:
        # Determine if user wants schematic or realistic photo
        is_schematic = any(word in circuit_description.lower() for word in ['schematic', 'diagram', 'draw', 'sketch'])
        
        if is_schematic:
            # Generate schematic-style diagram
            prompt = f"clean electronic circuit schematic diagram, {circuit_description}, technical drawing, black lines on white background, labeled components, professional engineering diagram"
        else:
            # Generate realistic circuit board photo
            prompt = f"professional photograph of electronic circuit board, {circuit_description}, detailed PCB with components, realistic electronics, high quality, well-lit"
        
        print(f"Generating {'schematic' if is_schematic else 'realistic'} image...")
        print(f"Prompt: {prompt[:100]}...")
        
        # Use correct Inference API endpoint
        api_url = f"https://api-inference.huggingface.co/models/{IMAGE_GEN_MODEL}"
        
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                api_url,
                headers={
                    "Authorization": f"Bearer {HF_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={"inputs": prompt},
                timeout=120.0
            )
            
            print(f"Image generation API response status: {response.status_code}")
            
            if response.status_code == 200:
                # Check if response is JSON (error/loading) or binary (image)
                content_type = response.headers.get('content-type', '')
                print(f"Content-Type: {content_type}")
                
                if 'application/json' in content_type:
                    error_data = response.json()
                    print(f"Image generation API returned JSON: {error_data}")
                    # Model might be loading
                    if 'error' in error_data:
                        error_msg = error_data.get('error', '')
                        if 'loading' in error_msg.lower():
                            print("Image generation model is loading")
                        if 'estimated_time' in error_data:
                            print(f"Estimated time: {error_data.get('estimated_time')}s")
                    return None
                
                # Return base64 encoded image
                image_bytes = response.content
                print(f"Successfully generated image: {len(image_bytes)} bytes")
                image_b64 = base64.b64encode(image_bytes).decode('utf-8')
                return image_b64
            elif response.status_code == 503:
                # Model is loading
                try:
                    error_data = response.json()
                    print(f"Image generation model loading: {error_data}")
                    if "estimated_time" in error_data:
                        print(f"Estimated time: {error_data['estimated_time']}s")
                except:
                    print("Image generation model is currently loading")
                return None
            else:
                print(f"Image generation API error: {response.text[:500]}")
            
            return None
    except Exception as e:
        print(f"Image generation error: {e}")
        import traceback
        traceback.print_exc()
        return None


async def build_messages(conversation_history: list, user_message: str, image_data: Optional[str] = None, image_analysis: Optional[str] = None) -> list:
    """Build the messages array for Groq API."""
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    # Add conversation history
    for msg in conversation_history:
        messages.append({"role": msg["role"], "content": msg["content"]})

    # Build current user message
    if image_data and image_analysis:
        content = f"{user_message or 'Please analyze this circuit/schematic diagram.'}\n\n{image_analysis}"
        messages.append({"role": "user", "content": content})
    else:
        messages.append({"role": "user", "content": user_message})

    return messages


async def get_ai_response(
    conversation_history: list,
    user_message: str,
    image_data: Optional[str] = None
) -> tuple[str, Optional[str], Optional[str]]:
    """
    Get response from Groq API with optional vision and image generation.
    Returns (text_response, circuit_svg_or_none, generated_image_b64_or_none)
    """
    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY not set. Get a free key at https://console.groq.com")
    
    # Analyze uploaded image if provided
    image_analysis = None
    if image_data:
        image_analysis = await analyze_circuit_image(image_data)
    
    messages = await build_messages(conversation_history, user_message, image_data, image_analysis)

    # Call Groq API
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {GROQ_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": GROQ_MODEL,
                    "messages": messages,
                    "max_tokens": 2048,  # Reduced to stay within rate limits
                    "temperature": 0.3,
                }
            )
            
            if response.status_code != 200:
                error_detail = response.text
                raise ValueError(f"Groq API error: {error_detail}")
            
            result = response.json()
    except httpx.HTTPStatusError as e:
        raise ValueError(f"Groq API HTTP error: {e.response.text}")
    except Exception as e:
        raise ValueError(f"Groq API error: {str(e)}")

    raw_response = result["choices"][0]["message"]["content"]

    # Check if response contains a circuit block and render it
    text_response, circuit_svg = extract_and_render_circuit(raw_response)

    # Only generate animated circuit when the user EXPLICITLY asks for one.
    # Trigger words: draw, show, generate, create, design, display, visualize + circuit/diagram/schematic
    DRAW_VERBS = [
        'draw', 'show me', 'generate', 'create', 'design', 'display',
        'visualize', 'make', 'build', 'sketch', 'diagram', 'animate',
        'give me a circuit', 'circuit diagram', 'circuit for', 'schematic for',
        'schematic of', 'wiring diagram', 'circuit of',
    ]

    message_lower = user_message.lower()
    user_wants_diagram = any(verb in message_lower for verb in DRAW_VERBS)

    # Also trigger if the AI itself rendered a circuit SVG block (explicit circuit in response)
    generated_image = None
    if user_wants_diagram or circuit_svg:
        circuit_desc = f"{user_message} {text_response[:200]}"
        print(f"User requested diagram — generating animated circuit for: {circuit_desc[:80]}...")
        animated_svg = generate_animated_circuit(circuit_desc)
        if animated_svg:
            animated_svg_b64 = base64.b64encode(animated_svg.encode('utf-8')).decode('utf-8')
            generated_image = f"svg:{animated_svg_b64}"
            print("Successfully generated animated circuit SVG")
        else:
            print("Animated circuit generation returned None")
    else:
        print("No diagram requested — skipping animation")

    return text_response, circuit_svg, generated_image


def generate_conversation_title(first_message: str) -> str:
    """Generate a short title from the first user message."""
    words = first_message.strip().split()
    title = " ".join(words[:8])
    if len(words) > 8:
        title += "..."
    return title[:100]
