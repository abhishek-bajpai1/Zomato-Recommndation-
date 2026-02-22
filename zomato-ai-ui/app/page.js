"use client";
import React, { useState } from 'react';
import Navbar from '../components/Navbar';
import Hero from '../components/Hero';
import CategoryCards from '../components/CategoryCards';
import { motion, AnimatePresence } from 'framer-motion';
import { Loader2, Sparkles } from 'lucide-react';

export default function Home() {
  const [loading, setLoading] = useState(false);
  const [preferences, setPreferences] = useState({
    price: 'mid',
    location: '',
    cuisine: '',
    rating: '4.0'
  });
  const [recommendations, setRecommendations] = useState([]);

  const handleGetRecommendations = async () => {
    setLoading(true);
    setRecommendations([]);
    try {
      const res = await fetch('/api/recommend', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(preferences)
      });
      const data = await res.json();
      if (data.recommendations && data.recommendations.length > 0) {
        setRecommendations(data.recommendations);
      } else {
        setRecommendations([]);
      }
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main style={{ background: '#0d0d0d', minHeight: '100vh', paddingBottom: '100px', color: 'white' }}>
      <Navbar />
      <Hero />

      {/* AI Recommender Form - Clean Pill Style */}
      <section className="container" style={{ marginTop: '-50px', position: 'relative', zIndex: 10 }}>
        <div style={{
          background: '#1a1a1a',
          padding: '40px',
          borderRadius: '24px',
          boxShadow: '0 20px 50px rgba(0,0,0,0.5)',
          border: '1px solid #222'
        }}>
          <div className="flex items-center gap-2 mb-8" style={{ color: '#ff5722' }}>
            <Sparkles size={28} />
            <h2 style={{ fontSize: '26px', fontWeight: 600, color: 'white' }}>AI Recommendation Engine</h2>
          </div>

          <div className="flex gap-6 mb-8" style={{ flexWrap: 'wrap' }}>
            <div style={{ flex: 1, minWidth: '250px' }}>
              <label style={{ display: 'block', fontSize: '14px', color: '#aaa', marginBottom: '10px' }}>What are you craving?</label>
              <select
                style={{ width: '100%', padding: '14px', borderRadius: '12px', border: '1px solid #333', outline: 'none', background: '#222', color: 'white' }}
                value={preferences.cuisine}
                onChange={(e) => setPreferences({ ...preferences, cuisine: e.target.value })}
              >
                <option value="">All Cuisines</option>
                <option value="North Indian">North Indian</option>
                <option value="Chinese">Chinese</option>
                <option value="South Indian">South Indian</option>
                <option value="Fast Food">Fast Food</option>
                <option value="Biryani">Biryani</option>
                <option value="Cafe">Cafe</option>
                <option value="Pizza">Pizza</option>
              </select>
            </div>

            <div style={{ flex: 1, minWidth: '200px' }}>
              <label style={{ display: 'block', fontSize: '14px', color: '#aaa', marginBottom: '10px' }}>Budget</label>
              <select
                style={{ width: '100%', padding: '14px', borderRadius: '12px', border: '1px solid #333', outline: 'none', background: '#222', color: 'white' }}
                value={preferences.price}
                onChange={(e) => setPreferences({ ...preferences, price: e.target.value })}
              >
                <option value="budget">Under ₹500</option>
                <option value="mid">₹500 - ₹1500</option>
                <option value="premium">Above ₹1500</option>
              </select>
            </div>

            <div style={{ flex: 1, minWidth: '150px' }}>
              <label style={{ display: 'block', fontSize: '14px', color: '#aaa', marginBottom: '10px' }}>Min Rating</label>
              <select
                style={{ width: '100%', padding: '14px', borderRadius: '12px', border: '1px solid #333', outline: 'none', background: '#222', color: 'white' }}
                value={preferences.rating}
                onChange={(e) => setPreferences({ ...preferences, rating: e.target.value })}
              >
                <option value="3.0">3.0+</option>
                <option value="3.5">3.5+</option>
                <option value="4.0">4.0+</option>
                <option value="4.5">4.5+</option>
              </select>
            </div>
          </div>

          <button
            className="btn-primary"
            style={{
              width: '100%',
              padding: '18px',
              fontSize: '18px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              gap: '10px',
              background: '#ff5722', // Match accent
              borderRadius: '12px',
              fontWeight: 700
            }}
            onClick={handleGetRecommendations}
            disabled={loading}
          >
            {loading ? <Loader2 className="animate-spin" /> : <Sparkles size={22} />}
            {loading ? 'Finding Best Matches...' : 'Search for AI Recommendations'}
          </button>
        </div>
      </section>

      {/* Recommendations Results */}
      <AnimatePresence>
        {recommendations.length > 0 && (
          <motion.section
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="container"
            style={{ marginTop: '64px' }}
          >
            <h3 style={{ fontSize: '32px', marginBottom: '32px', fontWeight: 700 }}>Top Picks for You</h3>
            <div className="flex gap-8" style={{ flexWrap: 'wrap' }}>
              {recommendations.map((res, i) => (
                <div key={i} style={{
                  flex: '1 1 340px',
                  borderRadius: '20px',
                  border: '1px solid #222',
                  overflow: 'hidden',
                  background: '#1a1a1a',
                  transition: '0.3s'
                }}>
                  <div style={{ height: '220px', overflow: 'hidden' }}>
                    <img src={`https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=400&q=80&sig=${i}`} alt={res.name} style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
                  </div>
                  <div style={{ padding: '24px' }}>
                    <div className="flex justify-between items-center mb-3">
                      <h4 style={{ fontSize: '22px', fontWeight: 700, color: 'white' }}>{res.name}</h4>
                      <span style={{ background: '#ff5722', color: 'white', padding: '4px 10px', borderRadius: '6px', fontSize: '14px', fontWeight: 700 }}>
                        {res.rate} ★
                      </span>
                    </div>
                    <p style={{ color: '#aaa', fontSize: '15px', marginBottom: '10px' }}>{res.cuisines}</p>
                    <p style={{ color: '#666', fontSize: '14px', marginBottom: '20px' }}>{res.location} • Cost for two: ₹{res.approx_cost}</p>
                    <div style={{ background: 'rgba(255, 87, 34, 0.08)', padding: '16px', borderRadius: '12px', fontSize: '15px', borderLeft: '4px solid #ff5722', color: '#eee' }}>
                      <strong>AI Insight:</strong> {res.description}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </motion.section>
        )}

        {!loading && recommendations.length === 0 && (
          <section className="container mt-8 text-center" style={{ color: '#666', padding: '40px' }}>
            <p>Ready to discover something delicious?</p>
          </section>
        )}
      </AnimatePresence>

      <CategoryCards />
    </main>
  );
}
