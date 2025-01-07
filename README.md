# WriteAI - AI Content Generator

WriteAI is a modern web application that leverages various AI models to generate optimized content for different platforms. With a beautiful and intuitive user interface, it provides a seamless experience for content creation across multiple platforms.

## Features

- 🚀 **Lightning Fast Generation** - Generate content in seconds with our optimized AI pipeline
- 🧠 **Multiple AI Models** - Choose from various AI models to suit your specific needs
- 🌐 **Cross-Platform Support** - Create content optimized for different platforms and formats
- 🔒 **Secure** - Your API keys and data are never stored or shared
- ⏰ **Time-Saving** - Automate your content creation workflow efficiently
- 🎨 **Customizable** - Fine-tune outputs to match your brand voice and style

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