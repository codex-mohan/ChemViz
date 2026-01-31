import { useState, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Upload as UploadIcon, CheckCircle, AlertCircle } from 'lucide-react';
import { Card } from '../components/ui/Card';
import { Button } from '../components/ui/Button';
import { datasetService } from '../services/api';
import clsx from 'clsx';

export const Upload = () => {
    const [file, setFile] = useState<File | null>(null);
    const [isDragging, setIsDragging] = useState(false);
    const [uploading, setUploading] = useState(false);
    const [status, setStatus] = useState<'idle' | 'success' | 'error'>('idle');
    const [message, setMessage] = useState('');
    const fileInputRef = useRef<HTMLInputElement>(null);

    const handleDragOver = (e: React.DragEvent) => {
        e.preventDefault();
        setIsDragging(true);
    };

    const handleDragLeave = (e: React.DragEvent) => {
        e.preventDefault();
        setIsDragging(false);
    };

    const handleDrop = (e: React.DragEvent) => {
        e.preventDefault();
        setIsDragging(false);
        if (e.dataTransfer.files && e.dataTransfer.files[0]) {
            validateAndSetFile(e.dataTransfer.files[0]);
        }
    };

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files && e.target.files[0]) {
            validateAndSetFile(e.target.files[0]);
        }
    };

    const validateAndSetFile = (uploadedFile: File) => {
        if (uploadedFile.type === 'text/csv' || uploadedFile.name.endsWith('.csv')) {
            setFile(uploadedFile);
            setStatus('idle');
            setMessage('');
        } else {
            setStatus('error');
            setMessage('Please upload a valid CSV file.');
        }
    };

    const handleUpload = async () => {
        if (!file) return;

        setUploading(true);
        setStatus('idle');
        try {
            await datasetService.upload(file);
            setStatus('success');
            setMessage('File uploaded and processed successfully!');
            setFile(null);
        } catch (error) {
            console.error(error);
            setStatus('error');
            setMessage('Failed to upload file. Please try again.');
        } finally {
            setUploading(false);
        }
    };

    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="max-w-2xl mx-auto"
        >
            <Card className="p-8 text-center space-y-8">
                <div className="space-y-2">
                    <h2 className="text-2xl font-heading font-bold text-white">Upload Equipment Data</h2>
                    <p className="text-text-secondary">
                        Drag and drop your CSV file here, or click to browse.
                    </p>
                </div>

                <div
                    className={clsx(
                        "relative border-2 border-dashed rounded-2xl p-12 transition-all duration-300 cursor-pointer group",
                        isDragging ? "border-accent bg-accent/5 scale-[1.02]" : "border-border hover:border-accent/50 hover:bg-bg-tertiary",
                        status === 'error' && "border-status-error/50 bg-status-error/5"
                    )}
                    onDragOver={handleDragOver}
                    onDragLeave={handleDragLeave}
                    onDrop={handleDrop}
                    onClick={() => fileInputRef.current?.click()}
                >
                    <input
                        type="file"
                        ref={fileInputRef}
                        className="hidden"
                        accept=".csv"
                        onChange={handleChange}
                    />

                    <div className="flex flex-col items-center justify-center space-y-4">
                        <div className={clsx(
                            "w-16 h-16 rounded-full flex items-center justify-center transition-colors duration-300",
                            isDragging ? "bg-accent/20 text-accent" : "bg-bg-tertiary text-text-muted group-hover:bg-accent/10 group-hover:text-accent"
                        )}>
                            <UploadIcon size={32} />
                        </div>
                        <div className="space-y-1">
                            <p className="text-lg font-medium text-text-primary group-hover:text-accent transition-colors">
                                {file ? file.name : "Drop your CSV here"}
                            </p>
                            <p className="text-sm text-text-muted">
                                {file ? `${(file.size / 1024).toFixed(2)} KB` : "Supports: CSV files only"}
                            </p>
                        </div>
                    </div>
                </div>

                <AnimatePresence>
                    {status === 'error' && (
                        <motion.div
                            initial={{ opacity: 0, height: 0 }}
                            animate={{ opacity: 1, height: 'auto' }}
                            exit={{ opacity: 0, height: 0 }}
                            className="bg-status-error/10 text-status-error px-4 py-3 rounded-xl flex items-center gap-3"
                        >
                            <AlertCircle size={20} />
                            <span>{message}</span>
                        </motion.div>
                    )}

                    {status === 'success' && (
                        <motion.div
                            initial={{ opacity: 0, height: 0 }}
                            animate={{ opacity: 1, height: 'auto' }}
                            exit={{ opacity: 0, height: 0 }}
                            className="bg-accent/10 text-accent px-4 py-3 rounded-xl flex items-center gap-3"
                        >
                            <CheckCircle size={20} />
                            <span>{message}</span>
                        </motion.div>
                    )}
                </AnimatePresence>

                <div className="flex justify-end pt-4">
                    <Button
                        size="lg"
                        isLoading={uploading}
                        disabled={!file}
                        onClick={(e) => { e.stopPropagation(); handleUpload(); }}
                        className="w-full sm:w-auto"
                    >
                        {uploading ? 'Processing...' : 'Upload Data'}
                    </Button>
                </div>
            </Card>
        </motion.div>
    );
};
