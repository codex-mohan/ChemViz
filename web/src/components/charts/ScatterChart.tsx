import { useMemo } from 'react';
import {
    Chart as ChartJS,
    LinearScale,
    PointElement,
    LineElement,
    Tooltip,
    Legend,
} from 'chart.js';
import { Scatter } from 'react-chartjs-2';
import type { Equipment } from '../../services/api';
import { Card } from '../ui/Card';

ChartJS.register(LinearScale, PointElement, LineElement, Tooltip, Legend);

interface ScatterChartProps {
    data: Equipment[];
}

export const ScatterChart = ({ data }: ScatterChartProps) => {
    const chartData = useMemo(() => {
        const datasets: { label: string; data: { x: number; y: number; }[]; backgroundColor: string; }[] = [];
        const types = Array.from(new Set(data.map(d => d.equipment_type)));
        const colors = ['#00D9A5', '#FF6B35', '#00A8E8', '#FFD166', '#EF476F', '#8338EC'];

        types.forEach((type, index) => {
            datasets.push({
                label: type,
                data: data.filter(d => d.equipment_type === type).map(d => ({
                    x: d.temperature,
                    y: d.pressure
                })),
                backgroundColor: colors[index % colors.length],
            });
        });

        return { datasets };
    }, [data]);

    const options = {
        responsive: true,
        plugins: {
            legend: {
                position: 'top' as const,
                labels: { color: '#E8E8E8' }
            },
        },
        scales: {
            x: {
                title: { display: true, text: 'Temperature', color: '#E8E8E8' },
                ticks: { color: '#888888' },
                grid: { color: '#333333' }
            },
            y: {
                title: { display: true, text: 'Pressure', color: '#E8E8E8' },
                ticks: { color: '#888888' },
                grid: { color: '#333333' }
            }
        }
    };

    return (
        <Card className="p-4 bg-bg-secondary w-full">
            <h3 className="text-xl font-heading font-semibold text-white mb-4">Temperature vs Pressure</h3>
            <Scatter options={options} data={chartData} />
        </Card>
    );
};
