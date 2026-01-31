import { useMemo } from 'react';
import {
    Chart as ChartJS,
    ArcElement,
    Tooltip,
    Legend
} from 'chart.js';
import { Pie } from 'react-chartjs-2';
import { Card } from '../ui/Card';

ChartJS.register(ArcElement, Tooltip, Legend);

interface PieChartProps {
    distribution: Record<string, number>;
}

export const PieChart = ({ distribution }: PieChartProps) => {
    const chartData = useMemo(() => {
        const labels = Object.keys(distribution);
        const values = Object.values(distribution);

        return {
            labels,
            datasets: [
                {
                    data: values,
                    backgroundColor: [
                        '#00D9A5', '#FF6B35', '#00A8E8', '#FFD166', '#EF476F', '#8338EC'
                    ],
                    borderColor: '#0D0D0D',
                    borderWidth: 2,
                },
            ],
        };
    }, [distribution]);

    const options = {
        responsive: true,
        plugins: {
            legend: {
                position: 'right' as const,
                labels: { color: '#E8E8E8' }
            },
        },
    };

    return (
        <Card className="p-4 bg-bg-secondary w-full h-full flex flex-col items-center">
            <h3 className="text-xl font-heading font-semibold text-white mb-4 self-start">Type Distribution</h3>
            <div className="w-64 h-64">
                <Pie data={chartData} options={options} />
            </div>
        </Card>
    );
};
