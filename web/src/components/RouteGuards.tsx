
import { Navigate, Outlet } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Layout } from '../layouts/Layout';

export const PrivateRoute = () => {
    const { isAuthenticated } = useAuth();

    return isAuthenticated ? <Layout /> : <Navigate to="/login" replace />;
};

export const PublicRoute = () => {
    const { isAuthenticated } = useAuth();

    return !isAuthenticated ? <Outlet /> : <Navigate to="/dashboard" replace />;
};
