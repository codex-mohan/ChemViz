import type { Equipment } from '../services/api';

export interface AverageByType {
    type: string;
    flowrate: number;
    pressure: number;
    temperature: number;
    count: number;
}

export interface BinData {
    label: string;
    count: number;
}

export const calculateAveragesByType = (data: Equipment[]): AverageByType[] => {
    const groups: Record<string, AverageByType> = {};

    data.forEach(item => {
        if (!groups[item.equipment_type]) {
            groups[item.equipment_type] = {
                type: item.equipment_type,
                flowrate: 0,
                pressure: 0,
                temperature: 0,
                count: 0
            };
        }
        groups[item.equipment_type].flowrate += item.flowrate;
        groups[item.equipment_type].pressure += item.pressure;
        groups[item.equipment_type].temperature += item.temperature;
        groups[item.equipment_type].count += 1;
    });

    return Object.values(groups).map(group => ({
        ...group,
        flowrate: group.flowrate / group.count,
        pressure: group.pressure / group.count,
        temperature: group.temperature / group.count
    }));
};

export const calculateHistogram = (data: number[], bins: number = 10): BinData[] => {
    if (data.length === 0) return [];

    const min = Math.min(...data);
    const max = Math.max(...data);
    const step = (max - min) / bins;

    const result: BinData[] = Array.from({ length: bins }, (_, i) => ({
        label: `${(min + i * step).toFixed(1)}-${(min + (i + 1) * step).toFixed(1)}`,
        count: 0
    }));

    data.forEach(value => {
        const index = Math.min(Math.floor((value - min) / step), bins - 1);
        if (index >= 0) {
            result[index].count++;
        }
    });

    return result;
};

export const calculateCorrelation = (x: number[], y: number[]): number => {
    const n = x.length;
    if (n !== y.length || n === 0) return 0;

    const meanX = x.reduce((a, b) => a + b) / n;
    const meanY = y.reduce((a, b) => a + b) / n;

    const num = x.reduce((sum, xi, i) => sum + (xi - meanX) * (y[i] - meanY), 0);
    const denX = Math.sqrt(x.reduce((sum, xi) => sum + Math.pow(xi - meanX, 2), 0));
    const denY = Math.sqrt(y.reduce((sum, yi) => sum + Math.pow(yi - meanY, 2), 0));

    return (denX * denY) === 0 ? 0 : num / (denX * denY);
};
