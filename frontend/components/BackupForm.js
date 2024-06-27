// components/BackupForm.js
import { useState } from 'react';

const BackupForm = ({ onSuccess }) => {
    const [formData, setFormData] = useState({
        mongo_uri: '',
    });

    const handleChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value,
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        const currentFormData = { ...formData };

        // Clear the form immediately
        setFormData({ mongo_uri: '' });

        // Trigger the table refresh
        onSuccess();

        await fetch('/api/backup', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(currentFormData),
        });
    };

    return (
        <form onSubmit={handleSubmit}>
            <input
                type="text"
                name="mongo_uri"
                placeholder="Mongo URI"
                value={formData.mongo_uri}
                onChange={handleChange}
                required
            />
            <button type="submit">Backup</button>
        </form>
    );
};

export default BackupForm;
