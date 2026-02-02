
import { Navigate, Outlet } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Layout } from '../layouts/Layout';

export const PrivateRoute = () => {
    const { isAuthenticated, isLoading } = useAuth();

    // Show loading state while validating token
    if (isLoading) {
        return (
            <div className="flex items-center justify-center h-screen bg-bg-primary">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-accent"></div>
            </div>
        );
    }

    return isAuthenticated ? <Layout /> : <Navigate to="/login" replace />;
};

export const PublicRoute = () => {
    const { isAuthenticated, isLoading } = useAuth();

    // Show loading state while validating token
    if (isLoading) {
        return (
            <div className="flex items-center justify-center h-screen bg-bg-primary">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-accent"></div>
            </div>
        );
    }

    return !isAuthenticated ? <Outlet /> : <Navigate to="/dashboard" replace />;
};
