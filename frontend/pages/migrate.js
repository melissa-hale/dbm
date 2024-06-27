// pages/migrate.js
import { useState } from 'react';
import MigrateForm from '../components/MigrateForm';
import OperationsTable from '../components/OperationsTable';

const MigratePage = () => {
    const [refresh, setRefresh] = useState(false);

    const handleSuccess = () => {
        setRefresh(prev => !prev);
    };

    return (
        <div>
            <h1>Migrate Database</h1>
            <MigrateForm onSuccess={handleSuccess} />
            <h2>Past Operations</h2>
            <OperationsTable type="migrate" refresh={refresh} />
        </div>
    );
};

export default MigratePage;
