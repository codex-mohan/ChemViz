import { createContext, useContext, useState, type ReactNode, useEffect } from 'react';
import { authService } from '../services/api';

interface User {
    id: number;
    username: string;
}

interface AuthContextType {
    user: User | null;
    token: string | null;
    isLoading: boolean;
    login: (token: string, user: User) => void;
    logout: () => void;
    isAuthenticated: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
    const [user, setUser] = useState<User | null>(null);
    const [token, setToken] = useState<string | null>(localStorage.getItem('token'));
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        // Validate stored token on app startup
        const validateStoredToken = async () => {
            const storedToken = localStorage.getItem('token');
            const storedUser = localStorage.getItem('user');

            if (!storedToken || !storedUser) {
                setIsLoading(false);
                return;
            }

            try {
                // Validate token with backend
                await authService.validateToken();
                // Token is valid, restore user
                setToken(storedToken);
                setUser(JSON.parse(storedUser));
            } catch (error) {
                // Token is invalid or expired, clear storage
                console.log('Session expired or invalid, logging out');
                localStorage.removeItem('token');
                localStorage.removeItem('user');
                setToken(null);
                setUser(null);
            } finally {
                setIsLoading(false);
            }
        };

        validateStoredToken();
    }, []);

    const login = (newToken: string, newUser: User) => {
        setToken(newToken);
        setUser(newUser);
        localStorage.setItem('token', newToken);
        localStorage.setItem('user', JSON.stringify(newUser));
    };

    const logout = () => {
        setToken(null);
        setUser(null);
        localStorage.removeItem('token');
        localStorage.removeItem('user');
    };

    return (
        <AuthContext.Provider value={{ user, token, isLoading, login, logout, isAuthenticated: !!token && !isLoading }}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => {
    const context = useContext(AuthContext);
    if (context === undefined) {
        throw new Error('useAuth must be used within an AuthProvider');
    }
    return context;
};
