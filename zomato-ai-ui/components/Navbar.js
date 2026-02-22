"use client";
import React from 'react';
import { MapPin, Search, ChevronDown, LogOut, User } from 'lucide-react';
import Link from 'next/link';
import { useAuth } from '../context/AuthContext';

export default function Navbar() {
    const { user, logout } = useAuth();

    return (
        <nav style={{
            padding: '16px 0',
            background: '#0d0d0d', // Match dark theme
            borderBottom: '1px solid #1a1a1a',
            position: 'sticky',
            top: 0,
            zIndex: 100
        }}>
            <div className="container flex items-center justify-between">
                <div className="flex items-center gap-8" style={{ flex: 1 }}>
                    <Link href="/">
                        <div style={{ color: 'white', fontSize: '24px', fontWeight: 800, letterSpacing: '1px' }}>
                            ZOMATO<span style={{ color: '#ff5722' }}>AI</span>
                        </div>
                    </Link>

                    {/* Clean Pill Nav for Desktop */}
                    <div style={{
                        display: 'flex',
                        background: 'rgba(255,255,255,0.95)',
                        borderRadius: '100px',
                        padding: '8px 24px',
                        gap: '24px',
                        alignItems: 'center',
                        marginLeft: '32px'
                    }}>
                        <span style={{ color: '#1c1c1c', fontWeight: 600, fontSize: '14px', cursor: 'pointer' }}>Home</span>
                        <span style={{ color: '#1c1c1c', fontWeight: 600, fontSize: '14px', cursor: 'pointer' }}>Dining</span>
                        <span style={{ color: '#1c1c1c', fontWeight: 600, fontSize: '14px', cursor: 'pointer' }}>Nightlife</span>
                    </div>
                </div>

                <div className="flex items-center gap-6" style={{ color: '#ddd', fontSize: '16px', marginLeft: '32px' }}>
                    {user ? (
                        <div className="flex items-center gap-4">
                            <div className="flex items-center gap-2" style={{ cursor: 'pointer' }}>
                                {user.photoURL ? (
                                    <img src={user.photoURL} alt="Profile" style={{ width: '32px', height: '32px', borderRadius: '50%', border: '2px solid #ff5722' }} />
                                ) : (
                                    <div style={{ background: '#333', padding: '6px', borderRadius: '50%', border: '2px solid #ff5722' }}>
                                        <User size={18} color="white" />
                                    </div>
                                )}
                                <span style={{ color: 'white' }}>{user.displayName || user.email.split('@')[0]}</span>
                            </div>
                            <button onClick={logout} style={{ background: 'transparent', display: 'flex', alignItems: 'center', gap: '4px', color: '#aaa' }}>
                                <LogOut size={18} />
                                <span>Logout</span>
                            </button>
                        </div>
                    ) : (
                        <div className="flex items-center gap-6">
                            <Link href="/login" style={{ cursor: 'pointer' }}>Log in</Link>
                            <Link href="/signup" style={{
                                background: '#cb202d',
                                color: 'white',
                                padding: '8px 20px',
                                borderRadius: '8px',
                                fontWeight: 500
                            }}>Sign up</Link>
                        </div>
                    )}
                </div>
            </div>
        </nav>
    );
}
