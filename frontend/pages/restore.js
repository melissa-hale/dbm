// pages/restore.js
import { useState } from 'react';
import RestoreForm from '../components/RestoreForm';
import OperationsTable from '../components/OperationsTable';

const RestorePage = () => {
    const [refresh, setRefresh] = useState(false);

    const handleSuccess = () => {
        setRefresh(prev => !prev); 
    };

    return (
        <div>
            <h1>Restore Database</h1>
            <RestoreForm onSuccess={handleSuccess} />
            <h2>Past Operations</h2>
            <OperationsTable type="restore" refresh={refresh} />
        </div>
    );
};

export default RestorePage;
