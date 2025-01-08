import { motion } from 'framer-motion';
import { Github, Heart } from 'lucide-react';

export default function Contribute() {
  return (
    <section id="contribute" className="py-20 px-4">
      <div className="max-w-4xl mx-auto text-center">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="bg-gray-900/50 backdrop-blur-xl p-8 rounded-2xl border border-gray-800"
        >
          <Heart className="w-12 h-12 text-pink-500 mx-auto mb-6" />
          <h2 className="text-3xl font-bold mb-4 bg-gradient-to-r from-purple-400 to-pink-500 bg-clip-text text-transparent">
            Contribute to WriteAI
          </h2>
          <p className="text-gray-400 mb-8 max-w-2xl mx-auto">
            WriteAI is an open-source project, and we welcome contributions from developers
            around the world. Help us make content generation more accessible and powerful.
          </p>
          <motion.a
            href="https://github.com/pschoudhary-dot/WriteAI"
            target="_blank"
            rel="noopener noreferrer"
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            className="inline-flex items-center gap-2 px-6 py-3 bg-gray-800 rounded-lg hover:bg-gray-700 transition-colors"
          >
            <Github className="w-5 h-5" />
            <span>View on GitHub</span>
          </motion.a>
        </motion.div>
      </div>
    </section>
  );
}
