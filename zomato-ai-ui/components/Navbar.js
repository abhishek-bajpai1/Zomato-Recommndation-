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
            background: 'white',
            borderBottom: '1px solid #e8e8e8',
            position: 'sticky',
            top: 0,
            zIndex: 100
        }}>
            <div className="container flex items-center justify-between">
                <div className="flex items-center gap-4" style={{ flex: 1 }}>
                    <Link href="/">
                        <img
                            src="https://b.zmtcdn.com/web_assets/b40b97e677bc7b2ca77c58c61db266fe1603954218.png"
                            alt="Zomato"
                            style={{ height: '28px', cursor: 'pointer' }}
                        />
                    </Link>

                    <div style={{
                        display: 'flex',
                        alignItems: 'center',
                        background: 'white',
                        border: '1px solid #e8e8e8',
                        borderRadius: '8px',
                        padding: '8px 16px',
                        boxShadow: 'var(--zomato-shadow)',
                        marginLeft: '20px',
                        width: '100%',
                        maxWidth: '700px'
                    }}>
                        <div className="flex items-center gap-4" style={{ borderRight: '1px solid #e8e8e8', paddingRight: '16px', minWidth: '180px' }}>
                            <MapPin size={20} color="#ff7e8b" />
                            <select
                                style={{ border: 'none', outline: 'none', fontSize: '14px', width: '100%', background: 'transparent', cursor: 'pointer' }}
                            >
                                <option value="">Select Location</option>
                                <option value="Bellandur">Bellandur</option>
                                <option value="Marathahalli">Marathahalli</option>
                                <option value="Whitefield">Whitefield</option>
                                <option value="Banashankari">Banashankari</option>
                                <option value="Indiranagar">Indiranagar</option>
                                <option value="Electronic City">Electronic City</option>
                                <option value="Basavanagudi">Basavanagudi</option>
                                <option value="Bannerghatta Road">Bannerghatta Road</option>
                            </select>
                        </div>
                        <div className="flex items-center gap-4" style={{ paddingLeft: '16px', flex: 1 }}>
                            <Search size={20} color="#696969" />
                            <input
                                type="text"
                                placeholder="Search for restaurant, cuisine or a dish"
                                style={{ border: 'none', outline: 'none', fontSize: '14px', width: '100%' }}
                            />
                        </div>
                    </div>
                </div>

                <div className="flex items-center gap-6" style={{ color: '#696969', fontSize: '18px', marginLeft: '32px' }}>
                    {user ? (
                        <div className="flex items-center gap-4">
                            <div className="flex items-center gap-2" style={{ cursor: 'pointer' }}>
                                {user.photoURL ? (
                                    <img src={user.photoURL} alt="Profile" style={{ width: '32px', height: '32px', borderRadius: '50%' }} />
                                ) : (
                                    <div style={{ background: '#eee', padding: '6px', borderRadius: '50%' }}>
                                        <User size={18} />
                                    </div>
                                )}
                                <span style={{ fontSize: '16px', color: '#1c1c1c' }}>{user.displayName || user.email.split('@')[0]}</span>
                            </div>
                            <button onClick={logout} style={{ background: 'transparent', display: 'flex', alignItems: 'center', gap: '4px', color: '#696969' }}>
                                <LogOut size={18} />
                                <span style={{ fontSize: '16px' }}>Logout</span>
                            </button>
                        </div>
                    ) : (
                        <>
                            <Link href="/login">Log in</Link>
                            <Link href="/signup">Sign up</Link>
                        </>
                    )}
                </div>
            </div>
        </nav>
    );
}
