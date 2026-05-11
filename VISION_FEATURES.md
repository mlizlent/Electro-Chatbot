# ElectroBot Vision & Image Generation Features

## 🎯 Overview
ElectroBot now has advanced vision capabilities for analyzing circuit images and generating realistic circuit board photos or schematic diagrams.

## 🔍 Vision Analysis Features

### Multi-Model Analysis
When you upload a circuit image, ElectroBot uses **3 different AI models** simultaneously:

1. **General Image Captioning** (`nlpconnect/vit-gpt2-image-captioning`)
   - Provides overall description of the image
   - Quick general understanding

2. **Detailed Description** (`Salesforce/blip-image-captioning-large`)
   - More detailed analysis of the circuit
   - Better component identification

3. **Object Detection** (`facebook/detr-resnet-50`)
   - Detects and counts individual components
   - Provides confidence scores for each detection
   - Groups similar components together

### What You Get
- **General view**: Overall description of the circuit
- **Detailed description**: In-depth analysis of components and layout
- **Detected components**: List of identified components with counts and confidence scores

Example output:
```
General view: a circuit board with electronic components
Detailed description: electronic circuit board with resistors, capacitors, and integrated circuits
Detected components: 3x resistor (0.92 confidence), 2x capacitor (0.87 confidence), 1x integrated circuit (0.95 confidence)
```

## 🎨 Image Generation Features

### Automatic Style Detection
ElectroBot automatically detects whether you want:
- **Schematic diagrams**: Clean technical drawings (keywords: schematic, diagram, draw, sketch)
- **Realistic photos**: Professional circuit board photographs (default)

### Usage Examples

**For Schematics:**
- "Draw a 555 timer circuit schematic"
- "Show me a schematic diagram of an Arduino LED circuit"
- "Sketch a voltage regulator circuit"

**For Realistic Photos:**
- "Show me an Arduino circuit board"
- "Generate a photo of a PCB with LEDs"
- "Create an image of an ESP32 development board"

## 🚀 How to Use

### Analyzing Circuit Images
1. Click the **paperclip icon** 📎 in the chat input
2. Upload your circuit image (JPEG, PNG, GIF, WebP)
3. Ask questions like:
   - "What components do you see?"
   - "Analyze this circuit"
   - "What's wrong with this circuit?"
   - "Identify all the components"

### Generating Circuit Images
Simply ask ElectroBot to create an image:
- "Show me a 555 timer circuit"
- "Generate an Arduino LED circuit board"
- "Draw a schematic of a voltage divider"

## ⚙️ Technical Details

### Models Used
- **Vision**: ViT-GPT2, BLIP, DETR (Facebook)
- **Image Generation**: Stable Diffusion 2.1
- **Text Generation**: Groq (Llama 3.1 8B)

### API Provider
- Hugging Face Inference API (free tier)
- Models may take 10-30 seconds to load on first use
- Subsequent requests are faster

### Limitations
- Free tier has rate limits
- Models may need to "warm up" on first use
- Object detection works best with clear, well-lit images
- Generated images are AI-created and may not be 100% accurate

## 🔧 Configuration

API keys are stored in `backend/.env`:
```env
GROQ_API_KEY=your_groq_key
HF_API_KEY=your_huggingface_key
```

## 📝 Notes
- Vision analysis runs in parallel for faster results
- All models use the Hugging Face Inference API
- Images are analyzed locally and not stored permanently
- Generated images are returned as base64 and displayed inline
