import { initializeApp, getApps, getApp } from "firebase/app";
import { getAuth } from "firebase/auth";

// Your web app's Firebase configuration
const firebaseConfig = {
    apiKey: "AIzaSyDRJ7W10gM2ZFUetfmAo6QF2Lgcdq0E1Vk",
    authDomain: "zomatoai-3cf37.firebaseapp.com",
    projectId: "zomatoai-3cf37",
    storageBucket: "zomatoai-3cf37.firebasestorage.app",
    messagingSenderId: "578592166445",
    appId: "1:578592166445:web:8c2e5c67a1c226bb7ddea4",
    measurementId: "G-M1HC7WWPTM"
};

// Initialize Firebase
const app = !getApps().length ? initializeApp(firebaseConfig) : getApp();
const auth = getAuth(app);

export { auth };
