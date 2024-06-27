// components/MigrateForm.js
import { useState } from 'react';

const MigrateForm = ({ onSuccess }) => {
    const [formData, setFormData] = useState({
        db_name: '',
        atlas_uri: '',
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
            db_name: '',
            atlas_uri: '',
            mongo_uri: '',
        });

        // Trigger the table refresh
        onSuccess();

        await fetch('/api/migrate', {
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
                name="db_name"
                placeholder="Database Name"
                value={formData.db_name}
                onChange={handleChange}
                required
            />
            <input
                type="text"
                name="atlas_uri"
                placeholder="Atlas URI"
                value={formData.atlas_uri}
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
            <button type="submit">Migrate</button>
        </form>
    );
};

export default MigrateForm;
