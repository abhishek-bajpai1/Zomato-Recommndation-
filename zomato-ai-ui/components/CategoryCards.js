"use client";
import React from 'react';
import { motion } from 'framer-motion';

const categories = [
    {
        title: 'Order Online',
        subtitle: 'Stay home and order to your doorstep',
        image: 'https://b.zmtcdn.com/webFrontend/e5b8785c257af2a7f354f1addaf37e4e1647364814.jpeg',
        link: '#'
    },
    {
        title: 'Dining',
        subtitle: "View the city's favourite dining venues",
        image: 'https://b.zmtcdn.com/webFrontend/d026b357feb0d63c997549f6398da8cc1647364915.jpeg',
        link: '#'
    },
    {
        title: 'Live Events',
        subtitle: "Discover India's best events & concerts",
        image: 'https://b.zmtcdn.com/webFrontend/d9d80ef91cb552e3fdfadb3d4f4379761647365057.jpeg',
        link: '#'
    }
];

export default function CategoryCards() {
    return (
        <section className="container mt-8 flex gap-4" style={{ padding: '40px 20px' }}>
            {categories.map((cat, index) => (
                <motion.div
                    key={index}
                    whileHover={{ scale: 1.05 }}
                    style={{
                        flex: 1,
                        borderRadius: '12px',
                        overflow: 'hidden',
                        border: '1px solid #e8e8e8',
                        cursor: 'pointer',
                        background: 'white',
                        transition: 'box-shadow 0.2s ease'
                    }}
                    className="category-card"
                >
                    <div style={{ height: '160px', overflow: 'hidden' }}>
                        <img src={cat.image} alt={cat.title} style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
                    </div>
                    <div style={{ padding: '12px 20px' }}>
                        <h3 style={{ fontSize: '20px', fontWeight: 500, color: '#1c1c1c' }}>{cat.title}</h3>
                        <p style={{ fontSize: '14px', color: '#4f4f4f', marginTop: '4px' }}>{cat.subtitle}</p>
                    </div>
                </motion.div>
            ))}
        </section>
    );
}
