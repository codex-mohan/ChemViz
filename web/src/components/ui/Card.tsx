import { forwardRef } from 'react';
import { twMerge } from 'tailwind-merge';
import { motion, type HTMLMotionProps } from 'framer-motion';

interface CardProps extends HTMLMotionProps<"div"> {
    hoverEffect?: boolean;
}

export const Card = forwardRef<HTMLDivElement, CardProps>(
    ({ className, children, hoverEffect = false, ...props }, ref) => {
        return (
            <motion.div
                ref={ref}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className={twMerge(
                    'bg-bg-secondary border border-border rounded-2xl p-6 shadow-sm',
                    hoverEffect && 'hover:border-accent/40 hover:shadow-[0_0_30px_rgba(0,0,0,0.3)] transition-all duration-300',
                    className
                )}
                {...props}
            >
                {children}
            </motion.div>
        );
    }
);

Card.displayName = 'Card';
