import { useState } from 'react';
import Navbar from './components/Navbar';
import Hero from './components/Hero';
import Generator from './components/Generator';
import Features from './components/Features';
import Reviews from './components/Reviews';
import Contribute from './components/Contribute';
import Newsletter from './components/Newsletter';
import FAQ from './components/FAQ';
import Footer from './components/Footer';

function App() {
  const [theme, setTheme] = useState<'dark' | 'light'>('dark');

  const toggleTheme = () => {
    setTheme(theme === 'dark' ? 'light' : 'dark');
  };

  return (
    <div className={`${theme} min-h-screen bg-gray-900 text-white`}>
      <Navbar theme={theme} toggleTheme={toggleTheme} />
      <Hero />
      <Generator />
      <Features />
      <Reviews />
      <Contribute />
      <Newsletter />
      <FAQ />
      <Footer />
    </div>
  );
}

export default App;