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
    <main style={{ background: '#fff', minHeight: '100vh', paddingBottom: '100px' }}>
      <Navbar />
      <Hero />

      {/* AI Recommender Form */}
      <section className="container" style={{ marginTop: '-40px', position: 'relative', zIndex: 10 }}>
        <div style={{
          background: 'white',
          padding: '32px',
          borderRadius: '16px',
          boxShadow: '0 8px 30px rgba(0,0,0,0.12)',
          border: '1px solid #eee'
        }}>
          <div className="flex items-center gap-2 mb-6" style={{ color: 'var(--zomato-red)' }}>
            <Sparkles size={24} />
            <h2 style={{ fontSize: '24px', fontWeight: 600 }}>AI Restaurant Recommender</h2>
          </div>

          <div className="flex gap-4 mb-4" style={{ flexWrap: 'wrap' }}>
            <div style={{ flex: 1, minWidth: '200px' }}>
              <label style={{ display: 'block', fontSize: '14px', color: '#666', marginBottom: '8px' }}>Cuisine Preference</label>
              <select
                style={{ width: '100%', padding: '12px', borderRadius: '8px', border: '1px solid #ddd', outline: 'none', background: 'white' }}
                value={preferences.cuisine}
                onChange={(e) => setPreferences({ ...preferences, cuisine: e.target.value })}
              >
                <option value="">All Cuisines</option>
                <option value="North Indian">North Indian</option>
                <option value="Chinese">Chinese</option>
                <option value="South Indian">South Indian</option>
                <option value="Fast Food">Fast Food</option>
                <option value="Biryani">Biryani</option>
                <option value="Continental">Continental</option>
                <option value="Cafe">Cafe</option>
                <option value="Italian">Italian</option>
                <option value="Bakery">Bakery</option>
                <option value="Seafood">Seafood</option>
                <option value="Mughlai">Mughlai</option>
                <option value="Pizza">Pizza</option>
                <option value="Burger">Burger</option>
              </select>
            </div>

            <div style={{ flex: 1, minWidth: '200px' }}>
              <label style={{ display: 'block', fontSize: '14px', color: '#666', marginBottom: '8px' }}>Budget</label>
              <select
                style={{ width: '100%', padding: '12px', borderRadius: '8px', border: '1px solid #ddd', outline: 'none' }}
                value={preferences.price}
                onChange={(e) => setPreferences({ ...preferences, price: e.target.value })}
              >
                <option value="budget">Budget (Under ₹500)</option>
                <option value="mid">Mid-range (₹500 - ₹1500)</option>
                <option value="premium">Premium (Above ₹1500)</option>
              </select>
            </div>

            <div style={{ flex: 1, minWidth: '200px' }}>
              <label style={{ display: 'block', fontSize: '14px', color: '#666', marginBottom: '8px' }}>Min Rating</label>
              <select
                style={{ width: '100%', padding: '12px', borderRadius: '8px', border: '1px solid #ddd', outline: 'none' }}
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
            style={{ width: '100%', padding: '16px', fontSize: '18px', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '8px' }}
            onClick={handleGetRecommendations}
            disabled={loading}
          >
            {loading ? <Loader2 className="animate-spin" /> : <Sparkles size={20} />}
            {loading ? 'Finding Best Matches...' : 'Get AI Recommendations'}
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
            style={{ marginTop: '48px' }}
          >
            <h3 style={{ fontSize: '28px', marginBottom: '24px' }}>Top Picks for You</h3>
            <div className="flex gap-6" style={{ flexWrap: 'wrap' }}>
              {recommendations.map((res, i) => (
                <div key={i} style={{
                  flex: '1 1 300px',
                  borderRadius: '16px',
                  border: '1px solid #e8e8e8',
                  overflow: 'hidden',
                  background: 'white',
                  boxShadow: '0 4px 6px rgba(0,0,0,0.05)'
                }}>
                  <div style={{ height: '200px', background: '#f8f8f8', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                    <img src={`https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=400&q=80&sig=${i}`} alt={res.name} style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
                  </div>
                  <div style={{ padding: '20px' }}>
                    <div className="flex justify-between items-center mb-2">
                      <h4 style={{ fontSize: '20px', fontWeight: 600 }}>{res.name}</h4>
                      <span style={{ background: '#24963f', color: 'white', padding: '2px 8px', borderRadius: '4px', fontSize: '14px' }}>
                        {res.rate} ★
                      </span>
                    </div>
                    <p style={{ color: '#4f4f4f', fontSize: '14px', marginBottom: '8px' }}>{res.cuisines}</p>
                    <p style={{ color: '#9c9c9c', fontSize: '13px', marginBottom: '16px' }}>{res.location} • Cost for two: ₹{res.approx_cost}</p>
                    <div style={{ background: '#fdf0f1', padding: '12px', borderRadius: '8px', fontSize: '14px', borderLeft: '3px solid var(--zomato-red)' }}>
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
            <p>No recommendations returned. Try relaxing filters.</p>
          </section>
        )}
      </AnimatePresence>

      <CategoryCards />
    </main>
  );
}
