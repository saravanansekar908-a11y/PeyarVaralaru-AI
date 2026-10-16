import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { LanguageProvider } from './services/LanguageContext';
import Navbar from './components/Navbar';
import Sidebar from './components/Sidebar';
import ScrollToTop from './components/ScrollToTop';

import Home from './pages/Home';
import SearchPage from './pages/SearchPage';
import PlaceDetails from './pages/PlaceDetails';
import Timeline from './pages/Timeline';
import SourcesPage from './pages/SourcesPage';
import AskAI from './pages/AskAI';
import RelationshipGraph from './pages/RelationshipGraph';
import DistrictDashboard from './pages/DistrictDashboard';
import HistoricalMapExplorer from './pages/HistoricalMapExplorer';

function AppContent() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  return (
    <div className="min-h-screen lg:h-screen bg-[#F7F4ED] flex flex-col font-sans text-[#172B40]">
      {/* Top Navbar */}
      <Navbar 
        mobileMenuOpen={mobileMenuOpen} 
        setMobileMenuOpen={setMobileMenuOpen} 
      />

      <div className="flex-1 flex overflow-hidden relative min-h-0">
        {/* Desktop Sidebar & Mobile Drawer */}
        <Sidebar 
          mobileMenuOpen={mobileMenuOpen} 
          setMobileMenuOpen={setMobileMenuOpen} 
        />

        {/* Main Content Area */}
        <main id="main-content" className="flex-1 overflow-y-auto min-h-0 p-3 sm:p-5 lg:p-8">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/search" element={<SearchPage />} />
            <Route path="/places" element={<Navigate to="/search" replace />} />
            <Route path="/places/:id" element={<PlaceDetails />} />
            <Route path="/districts" element={<DistrictDashboard />} />
            <Route path="/districts/:id" element={<DistrictDashboard />} />
            <Route path="/timeline" element={<Timeline />} />
            <Route path="/maps" element={<HistoricalMapExplorer />} />
            <Route path="/sources" element={<SourcesPage />} />
            <Route path="/ask" element={<AskAI />} />
            <Route path="/graph" element={<RelationshipGraph />} />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </main>
      </div>
    </div>
  );
}

export default function App() {
  return (
    <LanguageProvider>
      <Router>
        <ScrollToTop />
        <AppContent />
      </Router>
    </LanguageProvider>
  );
}

