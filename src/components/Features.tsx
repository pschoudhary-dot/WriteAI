import { motion } from 'framer-motion';
import { useRef } from 'react';
import { ChevronLeft, ChevronRight, Zap, Brain, Globe, Shield, Clock, Palette } from 'lucide-react';

const features = [
  {
    icon: Zap,
    title: 'Lightning Fast',
    description: 'Generate content in seconds with our optimized AI pipeline',
  },
  {
    icon: Brain,
    title: 'Multiple Models',
    description: 'Choose from various AI models to suit your specific needs',
  },
  {
    icon: Globe,
    title: 'Cross-Platform',
    description: 'Create content optimized for different platforms and formats',
  },
  {
    icon: Shield,
    title: 'Secure',
    description: 'Your API keys and data are never stored or shared',
  },
  {
    icon: Clock,
    title: 'Time-Saving',
    description: 'Automate your content creation workflow efficiently',
  },
  {
    icon: Palette,
    title: 'Customizable',
    description: 'Fine-tune outputs to match your brand voice and style',
  },
];

export default function Features() {
  const carouselRef = useRef<HTMLDivElement>(null);

  const scroll = (direction: 'left' | 'right') => {
    if (carouselRef.current) {
      const scrollAmount = direction === 'left' ? -400 : 400;
      carouselRef.current.scrollBy({ left: scrollAmount, behavior: 'smooth' });
    }
  };

  return (
    <section id="features" className="py-20 relative">
      <div className="max-w-7xl mx-auto px-4">
        <motion.h2
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-3xl font-bold text-center mb-12 bg-gradient-to-r from-purple-400 to-pink-500 bg-clip-text text-transparent"
        >
          Powerful Features
        </motion.h2>

        <div className="relative">
          <motion.button
            whileHover={{ scale: 1.1 }}
            whileTap={{ scale: 0.9 }}
            onClick={() => scroll('left')}
            className="absolute left-0 top-1/2 -translate-y-1/2 z-10 p-2 rounded-full bg-gray-800/50 backdrop-blur-sm border border-gray-700 hover:bg-gray-700/50 transition-colors"
          >
            <ChevronLeft className="w-6 h-6" />
          </motion.button>

          <motion.button
            whileHover={{ scale: 1.1 }}
            whileTap={{ scale: 0.9 }}
            onClick={() => scroll('right')}
            className="absolute right-0 top-1/2 -translate-y-1/2 z-10 p-2 rounded-full bg-gray-800/50 backdrop-blur-sm border border-gray-700 hover:bg-gray-700/50 transition-colors"
          >
            <ChevronRight className="w-6 h-6" />
          </motion.button>

          <div
            ref={carouselRef}
            className="overflow-x-auto hide-scrollbar flex gap-6 pb-4 px-4"
          >
            {features.map((feature, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.1 }}
                className="flex-shrink-0 w-[300px] bg-gray-900/50 backdrop-blur-xl p-6 rounded-xl border border-gray-800 hover:border-gray-700 transition-colors"
              >
                <feature.icon className="w-10 h-10 text-purple-500 mb-4" />
                <h3 className="text-xl font-semibold mb-2">{feature.title}</h3>
                <p className="text-gray-400">{feature.description}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}