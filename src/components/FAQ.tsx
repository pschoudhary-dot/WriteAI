import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { ChevronDown } from 'lucide-react';

const faqs = [
  {
    question: 'How does WriteAI protect my API keys?',
    answer: 'Your API keys are never stored on our servers. They are only used during your active session to make API calls and are immediately discarded when you close the browser.',
  },
  {
    question: 'Which AI models are supported?',
    answer: 'We support major AI providers including OpenAI (GPT-4, GPT-3.5), Anthropic (Claude), Google (Gemini), and Cohere. We regularly add support for new models.',
  },
  {
    question: 'Can I customize the output format?',
    answer: 'Yes! You can select different platforms (blog, social media, email, etc.) and customize your prompts to get content in your desired format and style.',
  },
  {
    question: 'Is there a limit to how much content I can generate?',
    answer: 'The content generation limits depend on your AI providers API limits and pricing. We dont impose any additional restrictions beyond what your chosen API provider sets.',
  },
  {
    question: 'Do you support multiple languages?',
    answer: 'Yes, you can generate content in any language supported by your chosen AI model. Most modern AI models support multiple languages effectively.',
  }
];

export default function FAQ() {
  const [openIndex, setOpenIndex] = useState<number | null>(null);

  return (
    <section id="faq" className="py-20 px-4">
      <div className="max-w-3xl mx-auto">
        <motion.h2
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-3xl font-bold text-center mb-12 bg-gradient-to-r from-purple-400 to-pink-500 bg-clip-text text-transparent"
        >
          Frequently Asked Questions
        </motion.h2>

        <div className="space-y-4">
          {faqs.map((faq, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: index * 0.1 }}
              className="bg-gray-900/50 backdrop-blur-xl border border-gray-800 rounded-lg overflow-hidden"
            >
              <button
                onClick={() => setOpenIndex(openIndex === index ? null : index)}
                className="w-full px-6 py-4 flex items-center justify-between text-left"
              >
                <span className="font-medium">{faq.question}</span>
                <motion.div
                  animate={{ rotate: openIndex === index ? 180 : 0 }}
                  transition={{ duration: 0.2 }}
                >
                  <ChevronDown className="w-5 h-5 text-gray-400" />
                </motion.div>
              </button>
              <AnimatePresence>
                {openIndex === index && (
                  <motion.div
                    initial={{ height: 0, opacity: 0 }}
                    animate={{ height: 'auto', opacity: 1 }}
                    exit={{ height: 0, opacity: 0 }}
                    transition={{ duration: 0.2 }}
                    className="px-6 pb-4"
                  >
                    <p className="text-gray-400">{faq.answer}</p>
                  </motion.div>
                )}
              </AnimatePresence>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}