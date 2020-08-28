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
      <section>
        <a
          href="https://www.finddx.org/covid-19/dx-imp-sim/about/"
          target="_parent"
        >
          <button className="btn simple">
            About the Dx Implementation Sim
          </button>
        </a>
      </section>
      {children}
      <Footer />
    </main>
    <ScrollToTop />
  </div>
);

export default MainLayout;
