import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { LanguageProvider } from './services/LanguageContext';
import Navbar from './components/Navbar';
import Sidebar from './components/Sidebar';

import Home from './pages/Home';
import SearchPage from './pages/SearchPage';
import PlaceDetails from './pages/PlaceDetails';
import SourcesPage from './pages/SourcesPage';
import AskAI from './pages/AskAI';
import RelationshipGraph from './pages/RelationshipGraph';

function AppContent() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  return (
    <div className="min-h-screen bg-[#F7F4ED] flex flex-col font-sans text-[#172B40]">
      {/* Top Navbar */}
      <Navbar 
        mobileMenuOpen={mobileMenuOpen} 
        setMobileMenuOpen={setMobileMenuOpen} 
      />

      <div className="flex-1 flex overflow-hidden">
        {/* Desktop Sidebar & Mobile Drawer */}
        <Sidebar 
          mobileMenuOpen={mobileMenuOpen} 
          setMobileMenuOpen={setMobileMenuOpen} 
        />

        {/* Main Content Area */}
        <main className="flex-1 overflow-y-auto p-4 sm:p-6 lg:p-8">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/search" element={<SearchPage />} />
            <Route path="/places" element={<Navigate to="/search" replace />} />
            <Route path="/places/:id" element={<PlaceDetails />} />
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
        <AppContent />
      </Router>
    </LanguageProvider>
  );
}
