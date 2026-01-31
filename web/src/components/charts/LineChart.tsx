import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend,
    Filler,
} from 'chart.js';
import { Line } from 'react-chartjs-2';

ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend,
    Filler
);

interface LineChartProps {
    data: {
        labels: string[];
        datasets: {
            label: string;
            data: number[];
            borderColor?: string;
            backgroundColor?: string;
        }[];
    };
    title?: string;
}

export const LineChart = ({ data, title }: LineChartProps) => {
    const options = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                labels: {
                    color: '#888888',
                    font: { family: 'Plus Jakarta Sans' }
                }
            },
            title: {
                display: !!title,
                text: title,
                color: '#E8E8E8',
                font: { family: 'Outfit', size: 16 }
            },
            tooltip: {
                backgroundColor: '#1A1A1A',
                titleColor: '#E8E8E8',
                bodyColor: '#CCCCCC',
                borderColor: '#333333',
                borderWidth: 1,
                padding: 10,
            }
        },
        scales: {
            y: {
                grid: { color: '#252525' },
                ticks: { color: '#888888' }
            },
            x: {
                grid: { color: '#252525' },
                ticks: { color: '#888888' }
            }
        }
    };

    return <Line options={options} data={data} />;
};
