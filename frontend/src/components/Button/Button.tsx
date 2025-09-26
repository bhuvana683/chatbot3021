/* frontend/src/components/Button/Button.tsx */
import React from 'react';

const Button = ({ children, onClick }: { children: React.ReactNode, onClick?: () => void }) => {
    return <button onClick={onClick}>{children}</button>;
};

export default Button;
