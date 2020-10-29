import * as React from 'react';

import TopSection from '../components/TopSection';
import Header from '../components/Header';
import Hero from '../components/Hero';
import ScrollToTop from '../components/ScrollToTop';
import Footer from '../components/Footer';

const MainLayout: React.FC = ({ children }) => (
  <div>
    <Header />
    <Hero />
    <main>
      <TopSection />
      {children}
      <Footer />
    </main>
    <ScrollToTop />
  </div>
);

export default MainLayout;
