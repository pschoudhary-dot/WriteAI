# Content Generation API

A FastAPI-based backend service that generates platform-specific content using various AI providers (Gemini, Groq) with specialized agents for research and writing.

## Table of Contents
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Running the API](#running-the-api)
- [API Endpoints](#api-endpoints)
- [Frontend Integration](#frontend-integration)
- [Common Issues](#common-issues)
- [Error Handling](#error-handling)

## Features

- Multiple AI provider support (Gemini, Groq)
- Platform-specific content generation for:
  - Social Media (Instagram, YouTube, Twitter, etc.)
  - Blogging (Medium, WordPress, Substack)
  - Professional (Website, Landing Pages)
  - Other (Podcast Scripts, Video Scripts)
- Research and writing capabilities
- Automatic content optimization for each platform
- Optional Google Search integration

## Prerequisites

- Python 3.8 or higher
- Node.js and npm (for frontend)
- API keys for chosen providers (Gemini/Groq)
- Optional: Serper API key for Google Search functionality

## Installation

1. Clone the repository:
```bash
git clone <your-repository>
cd <your-repository>
```

2. Create and activate a virtual environment:
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. Install required packages:
```bash
pip install fastapi uvicorn phi-agent python-dotenv
```

4. Create a `.env` file in the root directory:
```env
SERPER_API_KEY=your_serper_api_key_here  # Optional
```

## Running the API

1. Start the server:
```bash
# Option 1: Using python
python main.py

# Option 2: Using uvicorn
uvicorn main:app --reload
```

2. The API will be available at `http://127.0.0.1:8000`
3. Access the API documentation at `http://127.0.0.1:8000/docs`

Note: It's normal to see some asyncio-related messages when stopping the server with Ctrl+C. This is part of the normal shutdown process.

## API Endpoints

### 1. Generate Content
**POST** `/api/generate`

Generate platform-specific content based on input text.

Request Body:
```json
{
  "provider": "gemini",
  "model_name": "gemini-1.5-pro",
  "api_key": "your_api_key",
  "platform": "instagram",
  "input_text": "Your content topic",
  "serper_api_key": "optional_serper_key"
}
```

Response:
```json
{
  "content": "Generated content",
  "summary": "Optional summary",
  "status": "success"
}
```

### 2. Get Providers
**GET** `/api/providers`

Get list of available providers and their models.

Response:
```json
{
  "providers": [
    {
      "name": "gemini",
      "models": ["gemini-1.5-pro", "gemini-1.5-flash", "gemini-1.5-flash-8b"]
    },
    {
      "name": "groq",
      "models": ["llama-3.3-70b-versatile"]
    }
  ]
}
```

### 3. Get Platforms
**GET** `/api/platforms`

Get list of available platforms and their instructions.

Response:
```json
{
  "platforms": [
    {
      "name": "instagram",
      "instructions": "Platform-specific instructions..."
    }
  ]
}
```

## Frontend Integration

1. Install the provided React component:
```bash
# Copy ContentGenerator.jsx to your components folder
```

2. Import and use the component:
```jsx
import ContentGenerator from './components/ContentGenerator';

function App() {
  return (
    <div>
      <ContentGenerator />
    </div>
  );
}
```

3. Make sure your frontend application is configured to make requests to `http://127.0.0.1:8000`

## Common Issues

1. **Server Shutdown Messages**: When stopping the server with Ctrl+C, you may see asyncio-related error messages. This is normal and part of the shutdown process.

2. **CORS Issues**: If you're getting CORS errors:
   - Check that your frontend URL matches the allowed origins in the CORS middleware
   - Update the CORS configuration in main.py if needed

3. **API Key Issues**:
   - Ensure your API keys are valid
   - Check that you're using the correct model for each provider
   - Verify the API key permissions

## Error Handling

The API includes built-in error handling for:
- Invalid requests
- Authentication errors
- Provider-specific errors
- Platform validation
- Content generation failures

Errors are returned in the following format:
```json
{
  "detail": "Error message description"
}
```

## Development Notes

- Use the Swagger UI at `/docs` for testing endpoints
- Monitor the console for detailed logging
- The API uses FastAPI's automatic validation
- All platform-specific content generation includes SEO optimization

## Security Notes

- Never commit API keys to version control
- Use environment variables for sensitive data
- Implement rate limiting in production
- Add proper authentication for production use
