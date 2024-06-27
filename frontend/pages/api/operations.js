// pages/api/operations.js
import axios from 'axios';

export default async function handler(req, res) {
    if (req.method === 'GET') {
        try {
            const response = await axios.get(`${process.env.API_URL}/operations`, {
                headers: {
                    'X-API-KEY': process.env.API_KEY,
                },
            });

            res.status(200).json(response.data);
        } catch (error) {
            res.status(error.response?.status || 500).json({ error: error.message });
        }
    } else {
        res.setHeader('Allow', ['GET']);
        res.status(405).end(`Method ${req.method} Not Allowed`);
    }
}
