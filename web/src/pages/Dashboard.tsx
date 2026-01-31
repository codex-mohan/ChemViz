import { useEffect, useState } from 'react';
// import { motion } from 'framer-motion';
import { Card } from '../components/ui/Card';
import { Button } from '../components/ui/Button';
import { BarChart } from '../components/charts/BarChart';
import { PieChart } from '../components/charts/PieChart';
import { ScatterChart } from '../components/charts/ScatterChart';
import { HistogramChart } from '../components/charts/HistogramChart';
import { CorrelationMatrix } from '../components/charts/CorrelationMatrix';
import { Activity, Thermometer, Droplets, Wind, FileText, Download } from 'lucide-react';
import { datasetService } from '../services/api';
import type { Dataset } from '../services/api';

export const Dashboard = () => {
    const [dataset, setDataset] = useState<Dataset | null>(null);
    const [loading, setLoading] = useState(true);
    const [downloading, setDownloading] = useState(false);

    useEffect(() => {
        loadLatestDataset();
    }, []);

    const loadLatestDataset = async () => {
        try {
            const history = await datasetService.getHistory();
            if (history.length > 0) {
                // Fetch full details of the latest dataset
                const fullData = await datasetService.getById(history[0].id);
                setDataset(fullData);
            }
        } catch (error) {
            console.error("Failed to load data", error);
        } finally {
            setLoading(false);
        }
    };

    const handleDownloadReport = async () => {
        if (!dataset) return;
        setDownloading(true);
        try {
            await datasetService.downloadReport(dataset.id, `${dataset.name}_report.pdf`);
        } catch (error) {
            console.error("Download failed", error);
        } finally {
            setDownloading(false);
        }
    };

    if (loading) {
        return (
            <div className="flex items-center justify-center h-full">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-accent"></div>
            </div>
        );
    }

    if (!dataset || !dataset.summary || !dataset.equipment) {
        return (
            <div className="flex flex-col items-center justify-center h-full text-text-secondary">
                <FileText className="w-16 h-16 mb-4 opacity-50" />
                <h2 className="text-xl font-semibold mb-2">No Data Available</h2>
                <p>Upload a CSV file to view analytics.</p>
                <Button className="mt-4" onClick={() => window.location.href = '/upload'}>
                    Go to Upload
                </Button>
            </div>
        );
    }

    const { summary, equipment } = dataset;

    return (
        <div className="space-y-6">
            {/* Header Section */}
            <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
                <div>
                    <h1 className="text-3xl font-heading font-bold text-white mb-2">Dashboard</h1>
                    <p className="text-text-secondary">Real-time analysis of <span className="text-accent font-semibold">{dataset.name}</span></p>
                </div>
                <Button
                    onClick={handleDownloadReport}
                    isLoading={downloading}
                    leftIcon={<Download size={18} />}
                >
                    Download Report
                </Button>
            </div>

            {/* Quick Stats */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                <StatsCard
                    title="Total Equipment"
                    value={summary.total_count}
                    icon={<Activity className="text-accent" />}
                />
                <StatsCard
                    title="Avg Flowrate"
                    value={summary.avg_flowrate.toFixed(2)}
                    unit="m³/h"
                    icon={<Wind className="text-status-warning" />}
                />
                <StatsCard
                    title="Avg Pressure"
                    value={summary.avg_pressure.toFixed(2)}
                    unit="bar"
                    icon={<Droplets className="text-status-info" />}
                />
                <StatsCard
                    title="Avg Temperature"
                    value={summary.avg_temperature.toFixed(2)}
                    unit="°C"
                    icon={<Thermometer className="text-status-error" />}
                />
            </div>

            {/* Charts Grid */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* Row 1: Bar & Pie */}
                <BarChart data={equipment} />
                <PieChart distribution={summary.type_distribution} />

                {/* Row 2: Scatter & Correlation */}
                <ScatterChart data={equipment} />
                <CorrelationMatrix data={equipment} />

                {/* Row 3: Histograms */}
                <div className="lg:col-span-2 grid grid-cols-1 md:grid-cols-3 gap-6">
                    <HistogramChart data={equipment} parameter="flowrate" label="Flowrate" color="#00D9A5" />
                    <HistogramChart data={equipment} parameter="pressure" label="Pressure" color="#FF6B35" />
                    <HistogramChart data={equipment} parameter="temperature" label="Temperature" color="#00A8E8" />
                </div>
            </div>
        </div>
    );
};

const StatsCard = ({ title, value, unit, icon }: { title: string, value: string | number, unit?: string, icon: React.ReactNode }) => (
    <Card hoverEffect className="p-5 flex items-center justify-between bg-bg-secondary">
        <div>
            <p className="text-text-secondary text-sm font-medium mb-1">{title}</p>
            <h3 className="text-2xl font-bold text-white flex items-end gap-1">
                {value}
                {unit && <span className="text-sm font-normal text-text-secondary mb-1">{unit}</span>}
            </h3>
        </div>
        <div className="p-3 bg-bg-tertiary rounded-xl">
            {icon}
        </div>
    </Card>
);
