"use client";
import React from 'react';
import { motion } from 'framer-motion';

export default function Hero() {
    return (
        <section style={{
            position: 'relative',
            height: '420px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: 'white',
            overflow: 'hidden'
        }}>
            <div style={{
                position: 'absolute',
                top: 0,
                left: 0,
                right: 0,
                bottom: 0,
                background: 'url(/hero-bg.png) center/cover no-repeat',
                filter: 'brightness(0.6)'
            }} />

            <div className="container" style={{ position: 'relative', textAlign: 'center' }}>
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.8 }}
                >
                    <img
                        src="https://b.zmtcdn.com/web_assets/8313a97515fcb0447d2e77c276b9730c1605039324.png"
                        alt="Zomato"
                        style={{ width: '300px', marginBottom: '20px' }}
                    />
                    <h1 style={{ fontSize: '48px', fontWeight: 700, marginBottom: '32px', letterSpacing: '-1.5px' }}>
                        Discover the best food & drinks in Bangalore
                    </h1>
                </motion.div>
            </div>
        </section>
    );
}
