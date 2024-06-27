// pages/index.js
import Link from 'next/link';

const HomePage = () => (
    <div>
        <h1>Welcome to the Database Management App</h1>
        <nav>
            <ul>
                <li>
                    <Link href="/migrate">
                        <a>Migrate</a>
                    </Link>
                </li>
                <li>
                    <Link href="/backup">
                        <a>Backup</a>
                    </Link>
                </li>
                <li>
                    <Link href="/restore">
                        <a>Restore</a>
                    </Link>
                </li>
            </ul>
        </nav>
    </div>
);

export default HomePage;
