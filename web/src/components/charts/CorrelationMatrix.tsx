import { useMemo } from 'react';
import type { Equipment } from '../../services/api';
import { calculateCorrelation } from '../../utils/analytics';
import { Card } from '../ui/Card';

interface CorrelationMatrixProps {
    data: Equipment[];
}

export const CorrelationMatrix = ({ data }: CorrelationMatrixProps) => {
    const matrix = useMemo(() => {
        const flow = data.map(d => d.flowrate);
        const pressure = data.map(d => d.pressure);
        const temp = data.map(d => d.temperature);

        return [
            [
                calculateCorrelation(flow, flow),
                calculateCorrelation(flow, pressure),
                calculateCorrelation(flow, temp)
            ],
            [
                calculateCorrelation(pressure, flow),
                calculateCorrelation(pressure, pressure),
                calculateCorrelation(pressure, temp)
            ],
            [
                calculateCorrelation(temp, flow),
                calculateCorrelation(temp, pressure),
                calculateCorrelation(temp, temp)
            ]
        ];
    }, [data]);

    const labels = ['Flow', 'Pressure', 'Temp'];

    // Helper to map -1..1 correlation to color
    // -1 -> Blue, 0 -> White/Gray, 1 -> Red
    const getColor = (value: number) => {
        const val = Math.max(-1, Math.min(1, value));
        if (val > 0) {
            // Red scale for positive
            const alpha = Math.abs(val);
            return `rgba(255, 107, 53, ${alpha})`; // Using accent orange
        } else {
            // Blue scale for negative
            const alpha = Math.abs(val);
            return `rgba(0, 168, 232, ${alpha})`; // Using accent blue
        }
    };

    return (
        <Card className="p-4 bg-bg-secondary w-full flex flex-col items-center">
            <h3 className="text-xl font-heading font-semibold text-white mb-6">Correlation Matrix</h3>
            <div className="grid grid-cols-4 gap-1 w-full max-w-md">
                {/* Header Row */}
                <div className="col-span-1"></div>
                {labels.map((label, i) => (
                    <div key={`col-${i}`} className="text-center font-bold text-text-primary text-sm py-2">
                        {label}
                    </div>
                ))}

                {/* Data Rows */}
                {labels.map((rowLabel, i) => (
                    <>
                        {/* Row Label */}
                        <div key={`row-${i}`} className="col-span-1 flex items-center justify-end pr-3 font-bold text-text-primary text-sm">
                            {rowLabel}
                        </div>

                        {/* Cells */}
                        {matrix[i].map((val, j) => (
                            <div
                                key={`cell-${i}-${j}`}
                                className="aspect-square flex items-center justify-center rounded-md font-mono text-sm font-semibold text-white transition-all hover:scale-105"
                                style={{ backgroundColor: getColor(val) }}
                                title={`${rowLabel} vs ${labels[j]}: ${val.toFixed(2)}`}
                            >
                                {val.toFixed(2)}
                            </div>
                        ))}
                    </>
                ))}
            </div>
        </Card>
    );
};
