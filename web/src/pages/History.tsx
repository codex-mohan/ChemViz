import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { FileText, Download, Calendar, HardDrive } from 'lucide-react';
import { Card } from '../components/ui/Card';
import { Button } from '../components/ui/Button';
import { datasetService, type Dataset } from '../services/api';

export const History = () => {
    const navigate = useNavigate();
    const [datasets, setDatasets] = useState<Dataset[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const loadHistory = async () => {
            try {
                const data = await datasetService.getHistory();
                setDatasets(data);
            } catch (err) {
                console.error("Failed to load history:", err);
            } finally {
                setLoading(false);
            }
        };
        loadHistory();
    }, []);

    const formatDate = (dateString: string) => {
        return new Date(dateString).toLocaleDateString('en-US', {
            month: 'short', day: 'numeric', year: 'numeric', hour: '2-digit', minute: '2-digit'
        });
    };

    if (loading) return <div className="p-8 text-center text-text-muted">Loading history...</div>;

    return (
        <div className="space-y-6 animate-fade-in">
            <div className="flex items-center justify-between">
                <h2 className="text-2xl font-heading font-bold text-white">Upload History</h2>
            </div>

            <div className="grid gap-4">
                {datasets.length > 0 ? (
                    datasets.map((dataset) => (
                        <Card
                            key={dataset.id}
                            className="p-4 flex flex-col sm:flex-row items-start sm:items-center gap-4 hover:bg-bg-tertiary/30 transition-colors group cursor-pointer"
                            onClick={() => navigate(`/dataset/${dataset.id}`)}
                        >
                            <div className="w-12 h-12 rounded-xl bg-bg-tertiary flex items-center justify-center text-accent shrink-0">
                                <FileText size={24} />
                            </div>

                            <div className="flex-1 min-w-0">
                                <h3 className="text-lg font-medium text-text-primary mb-1 group-hover:text-accent transition-colors">
                                    {dataset.name}
                                </h3>
                                <div className="flex items-center gap-4 text-xs text-text-secondary">
                                    <span className="flex items-center gap-1">
                                        <Calendar size={12} /> {formatDate(dataset.created_at)}
                                    </span>
                                    <span className="flex items-center gap-1">
                                        <HardDrive size={12} /> {dataset.row_count} Records
                                    </span>
                                </div>
                            </div>

                            <div className="flex items-center gap-2 mt-2 sm:mt-0 w-full sm:w-auto justify-end">
                                <Button
                                    variant="ghost"
                                    size="sm"
                                    className="hidden sm:flex"
                                    onClick={(e) => {
                                        e.stopPropagation();
                                        navigate(`/dataset/${dataset.id}`);
                                    }}
                                >
                                    View Analysis
                                </Button>
                                <Button
                                    variant="secondary"
                                    size="sm"
                                    rightIcon={<Download size={14} />}
                                    onClick={(e) => {
                                        e.stopPropagation();
                                        datasetService.downloadReport(dataset.id, `Report_${dataset.name}.pdf`);
                                    }}
                                >
                                    Download
                                </Button>
                            </div>
                        </Card>
                    ))
                ) : (
                    <div className="text-center p-8 text-text-muted bg-bg-secondary rounded-xl border border-border">
                        No datasets uploaded yet. Go to Upload to add one.
                    </div>
                )}
            </div>
        </div>
    );
};
