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
import { calculateAveragesByType } from '../../utils/analytics';
import { Card } from '../ui/Card';

ChartJS.register(
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    Tooltip,
    Legend
);

interface BarChartProps {
    data: Equipment[];
}

export const BarChart = ({ data }: BarChartProps) => {
    const chartData = useMemo(() => {
        const averages = calculateAveragesByType(data);
        const labels = averages.map(a => a.type);

        return {
            labels,
            datasets: [
                {
                    label: 'Avg Flowrate',
                    data: averages.map(a => a.flowrate),
                    backgroundColor: '#00D9A5',
                },
                {
                    label: 'Avg Pressure',
                    data: averages.map(a => a.pressure),
                    backgroundColor: '#FF6B35',
                },
                {
                    label: 'Avg Temperature',
                    data: averages.map(a => a.temperature),
                    backgroundColor: '#00A8E8',
                },
            ],
        };
    }, [data]);

    const options = {
        responsive: true,
        plugins: {
            legend: {
                position: 'top' as const,
                labels: { color: '#E8E8E8' }
            },
            title: {
                display: false,
            },
        },
        scales: {
            y: {
                ticks: { color: '#888888' },
                grid: { color: '#333333' }
            },
            x: {
                ticks: { color: '#888888' },
                grid: { display: false }
            }
        }
    };

    return (
        <Card className="p-4 bg-bg-secondary w-full">
            <h3 className="text-xl font-heading font-semibold text-white mb-4">Averages by Type</h3>
            <Bar options={options} data={chartData} />
        </Card>
    );
};
