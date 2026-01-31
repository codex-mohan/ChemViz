
import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Upload, FileSpreadsheet } from 'lucide-react';
import { Button } from '../components/ui/Button';
import { datasetService } from '../services/api';

export const LatestDataset = () => {
    const navigate = useNavigate();
    const [loading, setLoading] = useState(true);
    const [hasData, setHasData] = useState(false);

    useEffect(() => {
        const checkLatest = async () => {
            try {
                const history = await datasetService.getHistory(); // Assuming this returns sorted list
                if (history && history.length > 0) {
                    // Navigate to the most recent one (assuming index 0 is newest or check created_at)
                    // The backend API for history doesn't explicitly guarantee order in the mock, 
                    // but usually APIs return newest first. Let's assume index 0.
                    // If your API returns oldest first, you might need history[history.length - 1]
                    const latestId = history[0].id;
                    navigate(`/dataset/${latestId}`, { replace: true });
                } else {
                    setHasData(false);
                }
            } catch (error) {
                console.error("Failed to fetch history for latest dataset:", error);
                setHasData(false);
            } finally {
                setLoading(false);
            }
        };

        checkLatest();
    }, [navigate]);

    if (loading) {
        return (
            <div className="flex h-full items-center justify-center">
                <div className="text-text-secondary animate-pulse">Finding latest dataset...</div>
            </div>
        );
    }

    if (!hasData) {
        return (
            <div className="flex flex-col items-center justify-center h-[60vh] text-center space-y-6 animate-fade-in">
                <div className="p-6 rounded-full bg-bg-tertiary text-text-muted">
                    <FileSpreadsheet size={48} strokeWidth={1.5} />
                </div>
                <div className="space-y-2 max-w-md">
                    <h2 className="text-2xl font-bold text-text-primary">No Datasets Found</h2>
                    <p className="text-text-secondary">
                        There isn't any data loaded yet. Upload a CSV file to get started with the viewer.
                    </p>
                </div>
                <Button
                    variant="primary"
                    size="lg"
                    leftIcon={<Upload size={20} />}
                    onClick={() => navigate('/upload')}
                >
                    Upload New Dataset
                </Button>
            </div>
        );
    }

    return null; // Should have navigated away
};
