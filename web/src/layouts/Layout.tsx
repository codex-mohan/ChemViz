import { useState } from 'react';
import { Outlet, NavLink, useLocation } from 'react-router-dom';
import { LayoutDashboard, Upload, History, Menu, X, Database, Table, LogOut } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import clsx from 'clsx';
import { useAuth } from '../context/AuthContext';

export const Layout = () => {
    const [isSidebarOpen, setIsSidebarOpen] = useState(true);
    const location = useLocation();
    const { user, logout } = useAuth();

    // Get initials from username
    const initials = user?.username
        ? user.username.substring(0, 2).toUpperCase()
        : 'US';

    const navItems = [
        { to: '/dashboard', icon: LayoutDashboard, label: 'Dashboard' },
        { to: '/upload', icon: Upload, label: 'Upload Data' },
        { to: '/dataset/latest', icon: Table, label: 'Dataset Viewer' },
        { to: '/history', icon: History, label: 'History' },
    ];

    return (
        <div className="flex h-screen bg-bg-primary text-text-primary overflow-hidden">
            {/* Sidebar */}
            <motion.aside
                initial={{ width: 260 }}
                animate={{ width: isSidebarOpen ? 260 : 80 }}
                transition={{ duration: 0.3, ease: 'easeInOut' }}
                className="relative bg-bg-secondary border-r border-border h-full flex flex-col z-20"
            >
                <div className="p-6 flex items-center justify-between">
                    <AnimatePresence mode="wait">
                        {isSidebarOpen ? (
                            <motion.div
                                initial={{ opacity: 0 }}
                                animate={{ opacity: 1 }}
                                exit={{ opacity: 0 }}
                                className="flex items-center gap-3"
                            >
                                <div className="p-2 bg-accent/10 rounded-lg">
                                    <Database className="w-6 h-6 text-accent" />
                                </div>
                                <span className="font-heading font-semibold text-lg tracking-tight whitespace-nowrap">
                                    CE Visualizer
                                </span>
                            </motion.div>
                        ) : (
                            <motion.div
                                initial={{ opacity: 0 }}
                                animate={{ opacity: 1 }}
                                className="mx-auto"
                            >
                                <Database className="w-6 h-6 text-accent" />
                            </motion.div>
                        )}
                    </AnimatePresence>
                </div>

                <nav className="flex-1 px-4 py-6 space-y-2">
                    {navItems.map((item) => (
                        <NavLink
                            key={item.to}
                            to={item.to}
                            className={({ isActive }) =>
                                clsx(
                                    'flex items-center gap-4 px-4 py-3 rounded-xl transition-all duration-200 group',
                                    isActive
                                        ? 'bg-accent/10 text-accent font-medium shadow-[0_0_20px_rgba(0,217,165,0.1)]'
                                        : 'text-text-secondary hover:bg-bg-tertiary hover:text-text-primary'
                                )
                            }
                        >
                            <item.icon className="w-5 h-5 flex-shrink-0" />
                            {isSidebarOpen && (
                                <motion.span
                                    initial={{ opacity: 0, x: -10 }}
                                    animate={{ opacity: 1, x: 0 }}
                                    transition={{ delay: 0.1 }}
                                    className="whitespace-nowrap"
                                >
                                    {item.label}
                                </motion.span>
                            )}
                        </NavLink>
                    ))}
                </nav>

                {/* Toggle Button */}
                <button
                    onClick={() => setIsSidebarOpen(!isSidebarOpen)}
                    className="absolute -right-3 top-10 bg-bg-tertiary border border-border text-text-muted hover:text-accent rounded-full p-1.5 transition-colors shadow-lg z-50"
                >
                    {isSidebarOpen ? <X size={14} /> : <Menu size={14} />}
                </button>

                <div className={clsx("p-6 border-t border-border", !isSidebarOpen && "text-center")}>
                    <div className="flex items-center gap-3">
                        <div className="w-8 h-8 rounded-full bg-gradient-to-tr from-accent to-blue-500 flex items-center justify-center text-bg-primary font-bold text-xs shrink-0">
                            {initials}
                        </div>
                        {isSidebarOpen && (
                            <div className="flex flex-col min-w-0 flex-1">
                                <span className="text-sm font-medium text-white truncate">
                                    {user?.username || 'User'}
                                </span>
                                <div
                                    className="flex items-center gap-1 text-xs text-text-secondary hover:text-red-400 cursor-pointer transition-colors mt-0.5"
                                    onClick={logout}
                                >
                                    <LogOut size={10} />
                                    <span>Sign Out</span>
                                </div>
                            </div>
                        )}
                    </div>
                </div>
            </motion.aside>

            {/* Main Content */}
            <main className="flex-1 flex flex-col min-w-0 bg-bg-primary relative overflow-hidden">
                {/* Background Decoration */}
                <div className="absolute top-0 left-0 w-full h-[300px] bg-accent/5 blur-[120px] pointer-events-none" />

                <div className="flex-1 overflow-y-auto overflow-x-hidden p-8 scroll-smooth">
                    <div className="max-w-7xl mx-auto space-y-8">
                        <header className="mb-8">
                            <h1 className="text-3xl font-bold text-white mb-2">
                                {navItems.find(i => i.to === location.pathname)?.label || 'Dashboard'}
                            </h1>
                            <p className="text-text-secondary">
                                Manage and analyze your chemical equipment parameters.
                            </p>
                        </header>

                        <AnimatePresence mode="wait">
                            <motion.div
                                key={location.pathname}
                                initial={{ opacity: 0, y: 10 }}
                                animate={{ opacity: 1, y: 0 }}
                                exit={{ opacity: 0, y: -10 }}
                                transition={{ duration: 0.2 }}
                            >
                                <Outlet />
                            </motion.div>
                        </AnimatePresence>
                    </div>
                </div>
            </main>
        </div>
    );
};
