import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './OperationsTable.module.css';

const OperationsTable = ({ type, refresh }) => {
    const [operations, setOperations] = useState([]);

    useEffect(() => {
        const fetchOperations = async () => {
            const response = await axios.get('/api/operations');
            setOperations(response.data);
        };
        fetchOperations();
    }, [refresh]);

    const filteredOperations = operations
        .filter(op => op.operation_type === type)
        .sort((a, b) => new Date(b.started_at) - new Date(a.started_at)); // Sort by started_at in descending order

    return (
        <div className="table-container">
            <table>
                <thead>
                    <tr>
                        <th>Type</th>
                        <th>Status</th>
                        <th>Started At</th>
                        <th>Completed At</th>
                        <th>Duration</th>
                        <th>Details</th>
                    </tr>
                </thead>
                <tbody>
                    {filteredOperations.map((op) => (
                        <tr key={op.id}>
                            <td>{op.operation_type}</td>
                            <td>{op.status}</td>
                            <td>{op.started_at}</td>
                            <td>{op.completed_at}</td>
                            <td>{op.duration}</td>
                            <td>{op.details}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

export default OperationsTable;
