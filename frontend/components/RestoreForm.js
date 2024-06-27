// components/RestoreForm.js
import { useState } from 'react';

const RestoreForm = ({ onSuccess }) => {
    const [formData, setFormData] = useState({
        backup_name: '',
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
        setFormData({
            backup_name: '',
            mongo_uri: '',
        });

        // Trigger the table refresh
        onSuccess();

        await fetch('/api/restore', {
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
                name="backup_name"
                placeholder="Backup Name"
                value={formData.backup_name}
                onChange={handleChange}
                required
            />
            <input
                type="text"
                name="mongo_uri"
                placeholder="Mongo URI"
                value={formData.mongo_uri}
                onChange={handleChange}
                required
            />
            <button type="submit">Restore</button>
        </form>
    );
};

export default RestoreForm;