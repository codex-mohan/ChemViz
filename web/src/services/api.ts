import api from '../api/axios';

export interface Equipment {
    id: number;
    equipment_name: string;
    equipment_type: string;
    flowrate: number;
    pressure: number;
    temperature: number;
}

export interface Dataset {
    id: number;
    name: string;
    created_at: string;
    row_count: number;
    summary?: {
        total_count: number;
        avg_flowrate: number;
        avg_pressure: number;
        avg_temperature: number;
        type_distribution: Record<string, number>;
    };
    equipment?: Equipment[];
}

// Auth Service
export const authService = {
    login: async (username: string, password: string) => {
        const response = await api.post('login/', { username, password });
        return response.data;
    },
    register: async (username: string, password: string, email: string) => {
        const response = await api.post('register/', { username, password, email });
        return response.data;
    },
};

export const datasetService = {

    upload: async (file: File) => {
        const formData = new FormData();
        formData.append('file', file);
        const response = await api.post('upload/', formData, {
            headers: { 'Content-Type': 'multipart/form-data' },
        });
        return response.data;
    },

    getAll: async () => {
        const response = await api.get<Dataset[]>('datasets/');
        return response.data;
    },

    getById: async (id: number) => {
        const response = await api.get<Dataset>(`datasets/${id}/`);
        // Fetch equipment and summary if not included (depending on API design)
        // Desktop app sees them in detail endpoints, but let's assume getById might need extra calls if serializer is minimal.
        // Based on serializers.py, DatasetSerializer includes equipment and summary.
        return response.data;
    },

    getHistory: async () => {
        const response = await api.get<Dataset[]>('history/');
        return response.data;
    },

    downloadReport: async (id: number, filename: string) => {
        const response = await api.get(`datasets/${id}/report/`, {
            responseType: 'blob',
        });

        // Trigger download in browser
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', filename);
        document.body.appendChild(link);
        link.click();
        link.remove();
        window.URL.revokeObjectURL(url);
    },

    clearHistory: async () => {
        const response = await api.delete('history/');
        return response.data;
    }
};
