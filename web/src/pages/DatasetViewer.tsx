
import { useState, useEffect, useMemo } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
    ArrowLeft,
    ArrowUpDown,
    Search,
    Filter,
    Download,
    ChevronLeft,
    ChevronRight,
    ArrowUp,
    ArrowDown
} from 'lucide-react';
import { datasetService, type Dataset, type Equipment } from '../services/api';
import { Button } from '../components/ui/Button';
import { Card } from '../components/ui/Card';

type SortConfig = {
    key: keyof Equipment | null;
    direction: 'asc' | 'desc';
};

export const DatasetViewer = () => {
    const { id } = useParams<{ id: string }>();
    const navigate = useNavigate();
    const [dataset, setDataset] = useState<Dataset | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [searchTerm, setSearchTerm] = useState('');
    const [sortConfig, setSortConfig] = useState<SortConfig>({ key: null, direction: 'asc' });
    const [page, setPage] = useState(1);
    const rowsPerPage = 10;

    useEffect(() => {
        const fetchDataset = async () => {
            if (!id) return;
            try {
                setLoading(true);
                const data = await datasetService.getById(parseInt(id));
                setDataset(data);
            } catch (err) {
                console.error("Failed to fetch dataset:", err);
                setError("Failed to load dataset. Please try again.");
            } finally {
                setLoading(false);
            }
        };

        fetchDataset();
    }, [id]);

    const handleSort = (key: keyof Equipment) => {
        let direction: 'asc' | 'desc' = 'asc';
        if (sortConfig.key === key && sortConfig.direction === 'asc') {
            direction = 'desc';
        }
        setSortConfig({ key, direction });
    };

    const sortedAndFilteredData = useMemo(() => {
        if (!dataset?.equipment) return [];

        let filtered = dataset.equipment;

        // Filter
        if (searchTerm) {
            const lowerTerm = searchTerm.toLowerCase();
            filtered = filtered.filter(item =>
                item.equipment_name.toLowerCase().includes(lowerTerm) ||
                item.equipment_type.toLowerCase().includes(lowerTerm) ||
                item.flowrate.toString().includes(lowerTerm) ||
                item.pressure.toString().includes(lowerTerm) ||
                item.temperature.toString().includes(lowerTerm)
            );
        }

        // Sort
        if (sortConfig.key) {
            filtered = [...filtered].sort((a, b) => {
                const aValue = a[sortConfig.key!];
                const bValue = b[sortConfig.key!];

                if (aValue < bValue) return sortConfig.direction === 'asc' ? -1 : 1;
                if (aValue > bValue) return sortConfig.direction === 'asc' ? 1 : -1;
                return 0;
            });
        }

        return filtered;
    }, [dataset, searchTerm, sortConfig]);

    // Pagination
    const totalPages = Math.ceil(sortedAndFilteredData.length / rowsPerPage);
    const displayedData = sortedAndFilteredData.slice(
        (page - 1) * rowsPerPage,
        page * rowsPerPage
    );

    if (loading) {
        return (
            <div className="flex items-center justify-center min-h-[50vh]">
                <div className="text-text-secondary animate-pulse">Loading dataset...</div>
            </div>
        );
    }

    if (error || !dataset) {
        return (
            <div className="flex flex-col items-center justify-center min-h-[50vh] gap-4">
                <div className="text-red-500">{error || "Dataset not found"}</div>
                <Button onClick={() => navigate('/history')} variant="outline">
                    Back to History
                </Button>
            </div>
        );
    }

    return (
        <div className="space-y-6 animate-fade-in">
            {/* Header */}
            <div className="flex flex-col sm:flex-row gap-4 justify-between items-start sm:items-center">
                <div className="space-y-1">
                    <Button
                        variant="ghost"
                        size="sm"
                        className="pl-0 hover:pl-2 transition-all text-text-muted hover:text-text-primary mb-2"
                        onClick={() => navigate('/history')}
                        leftIcon={<ArrowLeft size={16} />}
                    >
                        Back to History
                    </Button>
                    <h1 className="text-3xl font-heading font-bold text-text-primary">
                        {dataset.name}
                    </h1>
                    <p className="text-text-secondary text-sm">
                        Uploaded on {new Date(dataset.created_at).toLocaleDateString()} • {dataset.row_count} records
                    </p>
                </div>
                <Button
                    variant="primary"
                    rightIcon={<Download size={16} />}
                    onClick={() => datasetService.downloadReport(dataset.id, `Report_${dataset.name}.pdf`)}
                >
                    Download Report
                </Button>
            </div>

            {/* Controls */}
            <Card className="p-4">
                <div className="flex flex-col sm:flex-row gap-4 justify-between">
                    <div className="relative w-full sm:w-96">
                        <div className="absolute inset-y-0 left-3 flex items-center pointer-events-none text-text-muted">
                            <Search size={18} />
                        </div>
                        <input
                            type="text"
                            placeholder="Search equipment, type, or values..."
                            className="w-full pl-10 pr-4 py-2 bg-bg-secondary border border-border rounded-lg text-text-primary focus:outline-none focus:ring-2 focus:ring-accent/50 focus:border-accent transition-all"
                            value={searchTerm}
                            onChange={(e) => setSearchTerm(e.target.value)}
                        />
                    </div>
                    <div className="flex items-center gap-2 text-sm text-text-secondary">
                        <Filter size={16} />
                        <span>Showing {displayedData.length} of {dataset.row_count} records</span>
                    </div>
                </div>
            </Card>

            {/* Table */}
            <div className="bg-bg-secondary border border-border rounded-xl overflow-hidden shadow-sm">
                <div className="overflow-x-auto">
                    <table className="w-full text-left text-sm text-text-primary">
                        <thead className="bg-bg-tertiary border-b border-border">
                            <tr>
                                <SortableHeader label="Equipment Name" sortKey="equipment_name" currentSort={sortConfig} onSort={handleSort} />
                                <SortableHeader label="Type" sortKey="equipment_type" currentSort={sortConfig} onSort={handleSort} />
                                <SortableHeader label="Flowrate (m³/h)" sortKey="flowrate" currentSort={sortConfig} onSort={handleSort} />
                                <SortableHeader label="Pressure (bar)" sortKey="pressure" currentSort={sortConfig} onSort={handleSort} />
                                <SortableHeader label="Temperature (°C)" sortKey="temperature" currentSort={sortConfig} onSort={handleSort} />
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-border/50">
                            {displayedData.length > 0 ? (
                                displayedData.map((item) => (
                                    <tr key={item.id} className="hover:bg-bg-tertiary/50 transition-colors">
                                        <td className="px-6 py-4 font-medium">{item.equipment_name}</td>
                                        <td className="px-6 py-4">
                                            <span className="px-2 py-1 rounded-full bg-accent/10 text-accent text-xs font-medium">
                                                {item.equipment_type}
                                            </span>
                                        </td>
                                        <td className="px-6 py-4">{item.flowrate}</td>
                                        <td className="px-6 py-4">{item.pressure}</td>
                                        <td className="px-6 py-4">{item.temperature}</td>
                                    </tr>
                                ))
                            ) : (
                                <tr>
                                    <td colSpan={5} className="px-6 py-12 text-center text-text-muted">
                                        No matching records found.
                                    </td>
                                </tr>
                            )}
                        </tbody>
                    </table>
                </div>

                {/* Pagination Footer */}
                {totalPages > 1 && (
                    <div className="px-6 py-4 border-t border-border flex items-center justify-between bg-bg-secondary">
                        <div className="text-xs text-text-muted">
                            Page {page} of {totalPages}
                        </div>
                        <div className="flex items-center gap-2">
                            <Button
                                variant="outline"
                                size="sm"
                                disabled={page === 1}
                                onClick={() => setPage(p => Math.max(1, p - 1))}
                            >
                                <ChevronLeft size={16} />
                            </Button>
                            <Button
                                variant="outline"
                                size="sm"
                                disabled={page === totalPages}
                                onClick={() => setPage(p => Math.min(totalPages, p + 1))}
                            >
                                <ChevronRight size={16} />
                            </Button>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
};

const SortableHeader = ({
    label,
    sortKey,
    currentSort,
    onSort
}: {
    label: string,
    sortKey: keyof Equipment,
    currentSort: SortConfig,
    onSort: (key: keyof Equipment) => void
}) => {
    const isSorted = currentSort.key === sortKey;

    return (
        <th
            className="px-6 py-4 font-semibold cursor-pointer select-none hover:text-accent transition-colors group"
            onClick={() => onSort(sortKey)}
        >
            <div className="flex items-center gap-2">
                {label}
                <span className={`transition-opacity ${isSorted ? 'opacity-100' : 'opacity-0 group-hover:opacity-50'}`}>
                    {isSorted && currentSort.direction === 'desc' ? (
                        <ArrowDown size={14} />
                    ) : isSorted && currentSort.direction === 'asc' ? (
                        <ArrowUp size={14} />
                    ) : (
                        <ArrowUpDown size={14} />
                    )}
                </span>
            </div>
        </th>
    );
};
