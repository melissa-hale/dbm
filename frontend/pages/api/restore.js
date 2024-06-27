// pages/api/restore.js
import axios from 'axios';

export default async function handler(req, res) {
    if (req.method === 'POST') {
        const { backup_name, mongo_uri } = req.body;

        try {
            const response = await axios.post(`${process.env.API_URL}/restore/${backup_name}`, {
                mongo_uri,
            }, {
                headers: {
                    'Content-Type': 'application/json',
                    'X-API-KEY': process.env.API_KEY,
                }
            });

            res.status(200).json(response.data);
        } catch (error) {
            res.status(error.response?.status || 500).json({ error: error.message });
        }
    } else {
        res.setHeader('Allow', ['POST']);
        res.status(405).end(`Method ${req.method} Not Allowed`);
    }
}
