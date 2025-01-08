# WriteAI - AI Content Generator

WriteAI is a modern web application that leverages various AI models to generate optimized content for different platforms. With a beautiful and intuitive user interface, it provides a seamless experience for content creation across multiple platforms.
-  [Access WriteAI](https://writeai-new.netlify.app/)
## Features

- 🚀 **Lightning Fast Generation** - Generate content in seconds with our optimized AI pipeline
- 🧠 **Multiple AI Models** - Choose from various AI models to suit your specific needs
- 🌐 **Cross-Platform Support** - Create content optimized for different platforms and formats
- 🔒 **Secure** - Your API keys and data are never stored or shared
- ⏰ **Time-Saving** - Automate your content creation workflow efficiently
- 🎨 **Customizable** - Fine-tune outputs to match your brand voice and style

## Usage Guide

### Landing Page
![Landing Page](https://github.com/user-attachments/assets/f6a2313f-a489-42d0-a53a-a02b8d30b727)
The landing page showcases our modern, intuitive interface with key features and benefits.

### Step 1: Select Provider
![Select Provider](https://github.com/user-attachments/assets/38befbc9-8d06-4f2c-8aa8-e2c7c9b72ef1)
Choose your preferred AI provider from the dropdown menu. We support multiple leading AI providers.

### Step 2: Select Model
![Select Model](https://github.com/user-attachments/assets/bd8df284-6fa6-4035-870f-017d5cc4ebeb)
Pick the specific AI model you want to use. Different models are optimized for different types of content.

### Step 3: Enter API Key
![Enter API Key](https://github.com/user-attachments/assets/09944fed-5326-439c-816d-56214810ce21)
Enter your API key for the selected provider. Your key is never stored and is used only for the current session.

### Step 4: Generate Content
![Generate Content](https://github.com/user-attachments/assets/e3ea497a-7941-4110-ab38-295f8ed65e9b)
Write your prompt or input text, and click the "Generate" button to create your AI-powered content.

## Tech Stack

### Frontend
- React 18 with TypeScript
- Vite for build tooling
- TailwindCSS for styling
- Framer Motion for animations
- Lucide React for icons

### Backend
- Python FastAPI server
- Environment-based configuration
- Multiple AI provider integrations

## Prerequisites

- Node.js (v18 or higher)
- Python (v3.8 or higher)
- npm or yarn package manager

## Setup Instructions

### Frontend Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the development server:
   ```bash
   npm run dev
   ```

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend/python
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file in the backend/python directory with your API keys:
   ```
   OPENAI_API_KEY=your_openai_key
   ANTHROPIC_API_KEY=your_anthropic_key
   SERPER_API_KEY=your_serper_key
   ```
5. Start the backend server:
   ```bash
   uvicorn api:app --reload
   ```

## Development

- Frontend runs on `http://localhost:5173` by default
- Backend API runs on `http://localhost:8000`
- API documentation available at `http://localhost:8000/docs`

## Available Scripts

### Frontend
- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 
