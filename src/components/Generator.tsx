import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Wand2, ChevronDown, AlertCircle, Loader2 } from 'lucide-react';

interface Provider {
  name: string;
  models: string[];
}

interface Platform {
  name: string;
  instructions: string;
}

const API_BASE_URL = 'http://localhost:8000'; // Make sure your FastAPI server is running on this port

export default function Generator() {
  const [providers, setProviders] = useState<Provider[]>([]);
  const [platforms, setPlatforms] = useState<Platform[]>([]);
  const [selectedProvider, setSelectedProvider] = useState('');
  const [selectedModel, setSelectedModel] = useState('');
  const [selectedPlatform, setSelectedPlatform] = useState('');
  const [apiKey, setApiKey] = useState('');
  const [serperApiKey, setSerperApiKey] = useState('');
  const [inputText, setInputText] = useState('');
  const [isGenerating, setIsGenerating] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');
  const [generatedContent, setGeneratedContent] = useState('');

  useEffect(() => {
    const initializeData = async () => {
      setIsLoading(true);
      setError('');
      try {
        await Promise.all([fetchProviders(), fetchPlatforms()]);
      } catch (err) {
        setError('Failed to initialize data. Please make sure the API server is running.');
      } finally {
        setIsLoading(false);
      }
    };

    initializeData();
  }, []);

  const fetchProviders = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/providers`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        throw new Error('Failed to fetch providers');
      }

      const data = await response.json();
      setProviders(data.providers);
    } catch (err) {
      console.error('Error fetching providers:', err);
      throw err;
    }
  };

  const fetchPlatforms = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/platforms`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        throw new Error('Failed to fetch platforms');
      }

      const data = await response.json();
      setPlatforms(data.platforms);
    } catch (err) {
      console.error('Error fetching platforms:', err);
      throw err;
    }
  };

  const handleGenerate = async () => {
    // Validate required fields
    if (!selectedProvider || !selectedModel || !selectedPlatform || !apiKey || !inputText) {
      setError('Please fill in all required fields');
      return;
    }

    setIsGenerating(true);
    setError('');
    setGeneratedContent('');

    try {
      const response = await fetch(`${API_BASE_URL}/api/generate`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          provider: selectedProvider,
          model_name: selectedModel,
          api_key: apiKey,
          platform: selectedPlatform,
          input_text: inputText,
          serper_api_key: serperApiKey || undefined,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || 'Generation failed');
      }

      setGeneratedContent(data.content);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Generation failed');
    } finally {
      setIsGenerating(false);
    }
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <Loader2 className="w-8 h-8 animate-spin text-purple-500" />
      </div>
    );
  }

  return (
    <section id="generate" className="py-20 px-4">
      <div className="max-w-4xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="bg-gray-900/50 backdrop-blur-xl p-8 rounded-2xl border border-gray-800"
        >
          <h2 className="text-3xl font-bold mb-8 text-center bg-gradient-to-r from-purple-400 to-pink-500 bg-clip-text text-transparent">
            Generate Content
          </h2>

          <div className="space-y-6">
            {error && (
              <div className="bg-red-500/10 border border-red-500 rounded-lg p-4 flex items-center gap-2">
                <AlertCircle className="w-5 h-5 text-red-500" />
                <p className="text-red-500">{error}</p>
              </div>
            )}

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label className="block text-sm font-medium text-gray-400 mb-2">
                  Provider*
                </label>
                <div className="relative">
                  <select
                    value={selectedProvider}
                    onChange={(e) => {
                      setSelectedProvider(e.target.value);
                      setSelectedModel('');
                    }}
                    className="w-full bg-gray-800/50 border border-gray-700 rounded-lg py-2 px-3 appearance-none cursor-pointer hover:border-gray-600 transition-colors"
                  >
                    <option value="">Select Provider</option>
                    {providers.map((provider) => (
                      <option key={provider.name} value={provider.name}>
                        {provider.name.toUpperCase()}
                      </option>
                    ))}
                  </select>
                  <ChevronDown className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 pointer-events-none" />
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-400 mb-2">
                  Model*
                </label>
                <div className="relative">
                  <select
                    value={selectedModel}
                    onChange={(e) => setSelectedModel(e.target.value)}
                    disabled={!selectedProvider}
                    className="w-full bg-gray-800/50 border border-gray-700 rounded-lg py-2 px-3 appearance-none cursor-pointer hover:border-gray-600 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    <option value="">Select Model</option>
                    {selectedProvider &&
                      providers
                        .find((p) => p.name === selectedProvider)
                        ?.models.map((model) => (
                          <option key={model} value={model}>
                            {model}
                          </option>
                        ))}
                  </select>
                  <ChevronDown className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 pointer-events-none" />
                </div>
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-400 mb-2">
                API Key*
              </label>
              <input
                type="password"
                value={apiKey}
                onChange={(e) => setApiKey(e.target.value)}
                placeholder="Enter your API key"
                className="w-full bg-gray-800/50 border border-gray-700 rounded-lg py-2 px-3 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent"
              />
              <p className="mt-1 text-xs text-gray-500">
                Your API key is never stored and is only used for this session
              </p>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-400 mb-2">
                Serper API Key (Optional)
              </label>
              <input
                type="password"
                value={serperApiKey}
                onChange={(e) => setSerperApiKey(e.target.value)}
                placeholder="Enter your Serper API key for enhanced research"
                className="w-full bg-gray-800/50 border border-gray-700 rounded-lg py-2 px-3 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-400 mb-2">
                Platform*
              </label>
              <div className="relative">
                <select
                  value={selectedPlatform}
                  onChange={(e) => setSelectedPlatform(e.target.value)}
                  className="w-full bg-gray-800/50 border border-gray-700 rounded-lg py-2 px-3 appearance-none cursor-pointer hover:border-gray-600 transition-colors"
                >
                  <option value="">Select Platform</option>
                  {platforms.map((platform) => (
                    <option key={platform.name} value={platform.name}>
                      {platform.name.replace(/_/g, ' ').toUpperCase()}
                    </option>
                  ))}
                </select>
                <ChevronDown className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 pointer-events-none" />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-400 mb-2">
                Input Text*
              </label>
              <textarea
                value={inputText}
                onChange={(e) => setInputText(e.target.value)}
                placeholder="Enter your content prompt..."
                rows={4}
                className="w-full bg-gray-800/50 border border-gray-700 rounded-lg py-2 px-3 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent"
              />
            </div>

            <motion.button
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              onClick={handleGenerate}
              disabled={isGenerating}
              className="w-full py-3 px-4 bg-gradient-to-r from-purple-600 to-pink-600 rounded-lg font-medium text-white hover:opacity-90 transition-opacity disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
            >
              {isGenerating ? (
                <Loader2 className="w-5 h-5 animate-spin" />
              ) : (
                <Wand2 className="w-5 h-5" />
              )}
              {isGenerating ? 'Generating...' : 'Generate Content'}
            </motion.button>

            {generatedContent && (
              <div className="mt-8">
                <h3 className="text-xl font-semibold mb-4">Generated Content:</h3>
                <div className="bg-gray-800/50 border border-gray-700 rounded-lg p-4 whitespace-pre-wrap">
                  {generatedContent}
                </div>
              </div>
            )}
          </div>
        </motion.div>
      </div>
    </section>
  );
}