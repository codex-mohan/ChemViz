import { useMemo } from 'react';
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    Tooltip,
    Legend,
} from 'chart.js';
import { Bar } from 'react-chartjs-2';
import type { Equipment } from '../../services/api';
import { calculateHistogram } from '../../utils/analytics';
import { Card } from '../ui/Card';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

interface HistogramChartProps {
    data: Equipment[];
    parameter: 'flowrate' | 'pressure' | 'temperature';
    label: string;
    color: string;
}

export const HistogramChart = ({ data, parameter, label, color }: HistogramChartProps) => {
    const chartData = useMemo(() => {
        const values = data.map(d => d[parameter]);
        const bins = calculateHistogram(values, 10);

        return {
            labels: bins.map(b => b.label),
            datasets: [
                {
                    label: label,
                    data: bins.map(b => b.count),
                    backgroundColor: color,
                    barPercentage: 1.0,
                    categoryPercentage: 1.0,
                },
            ],
        };
    }, [data, parameter, label, color]);

    const options = {
        responsive: true,
        plugins: {
            legend: { display: false },
            title: { display: false },
        },
        scales: {
            y: {
                ticks: { color: '#888888' },
                grid: { color: '#333333' }
            },
            x: {
                ticks: {
                    color: '#888888',
                    maxRotation: 45,
                    minRotation: 45
                },
                grid: { display: false }
            }
        }
    };

    return (
        <Card className="p-4 bg-bg-secondary w-full">
            <h3 className="text-lg font-heading font-semibold text-white mb-2">{label} Distribution</h3>
            <Bar options={options} data={chartData} />
        </Card>
    );
};
