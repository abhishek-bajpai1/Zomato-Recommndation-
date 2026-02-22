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
        <section className="container mt-8 flex gap-8" style={{ padding: '60px 20px' }}>
            {categories.map((cat, index) => (
                <motion.div
                    key={index}
                    whileHover={{ scale: 1.05, translateY: -10 }}
                    style={{
                        flex: 1,
                        borderRadius: '24px',
                        overflow: 'hidden',
                        border: '1px solid #222',
                        cursor: 'pointer',
                        background: '#1a1a1a',
                        transition: '0.3s'
                    }}
                    className="category-card"
                >
                    <div style={{ height: '200px', overflow: 'hidden' }}>
                        <img src={cat.image} alt={cat.title} style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
                    </div>
                    <div style={{ padding: '24px' }}>
                        <h3 style={{ fontSize: '24px', fontWeight: 600, color: 'white' }}>{cat.title}</h3>
                        <p style={{ fontSize: '15px', color: '#888', marginTop: '10px' }}>{cat.subtitle}</p>
                    </div>
                </motion.div>
            ))}
        </section>
    );
}
