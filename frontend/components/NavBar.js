// components/Navbar.js
import React from 'react';
import Link from 'next/link';

const Navbar = () => (
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
);

export default Navbar;
