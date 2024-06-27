// pages/_app.js
import '../styles/globals.css';
import Navbar from '@/components/NavBar';

function MyApp({ Component, pageProps }) {
    return (
        <>
            <Navbar />
            <div className="container">
                <Component {...pageProps} />
            </div>
        </>
    );
}

export default MyApp;
