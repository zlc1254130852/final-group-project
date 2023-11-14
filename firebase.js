// Import the functions you need from the SDKs you need
import { initializeApp } from 'firebase/app';
import { getAuth, createUserWithEmailAndPassword, signInWithEmailAndPassword } from 'firebase/auth';
// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyCr1FDh_dqPjsRRuiYMF-Js6Po3ogm4g3o",
  authDomain: "fir-auth-24005.firebaseapp.com",
  projectId: "fir-auth-24005",
  storageBucket: "fir-auth-24005.appspot.com",
  messagingSenderId: "691326477105",
  appId: "1:691326477105:web:0aa6c67196c91d96b84610"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);

// Get the auth instance
const auth = getAuth(app);

// Export the auth instance
export { auth, createUserWithEmailAndPassword, signInWithEmailAndPassword };
