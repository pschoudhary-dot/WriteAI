import { motion } from 'framer-motion';
import { Mail } from 'lucide-react';

export default function Newsletter() {
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // Handle newsletter subscription
    alert('Thank you for subscribing! (This is a demo)');
  };

  return (
    <section className="py-20 px-4">
      <div className="max-w-4xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="bg-gradient-to-br from-purple-900/50 to-pink-900/50 backdrop-blur-xl p-8 rounded-2xl border border-gray-800"
        >
          <div className="text-center mb-8">
            <Mail className="w-12 h-12 mx-auto mb-4 text-purple-400" />
            <h2 className="text-3xl font-bold mb-4 bg-gradient-to-r from-purple-400 to-pink-500 bg-clip-text text-transparent">
              Stay Updated
            </h2>
            <p className="text-gray-400">
              Subscribe to our newsletter for the latest updates, tips, and features.
            </p>
          </div>

          <form onSubmit={handleSubmit} className="max-w-md mx-auto">
            <div className="flex gap-4">
              <input
                type="email"
                placeholder="Enter your email"
                required
                className="flex-1 bg-gray-800/50 border border-gray-700 rounded-lg py-2 px-4 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent"
              />
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                type="submit"
                className="px-6 py-2 bg-gradient-to-r from-purple-600 to-pink-600 rounded-lg font-medium text-white hover:opacity-90 transition-opacity"
              >
                Subscribe
              </motion.button>
            </div>
          </form>
        </motion.div>
      </div>
    </section>
  );
}