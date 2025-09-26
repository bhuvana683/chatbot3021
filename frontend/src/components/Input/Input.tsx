/* frontend/src/components/Input/Input.tsx */
import React from 'react';

const Input = ({ placeholder, value, onChange }: { placeholder?: string, value: string, onChange: (e: React.ChangeEvent<HTMLInputElement>) => void }) => {
    return <input placeholder={placeholder} value={value} onChange={onChange} />;
};

export default Input;
