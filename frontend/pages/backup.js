// pages/backup.js
import { useState } from 'react';
import BackupForm from '../components/BackupForm';
import OperationsTable from '../components/OperationsTable';

const BackupPage = () => {
    const [refresh, setRefresh] = useState(false);

    const handleSuccess = () => {
        setRefresh(prev => !prev);
    };

    return (
        <div>
            <h1>Backup Database</h1>
            <BackupForm onSuccess={handleSuccess} />
            <h2>Past Operations</h2>
            <OperationsTable type="backup" refresh={refresh} />
        </div>
    );
};

export default BackupPage;
