import React from 'react';

export const Card = ({ children, className }) => (
  <div className={`border rounded-md shadow-md ${className}`}>{children}</div>
);

export const CardContent = ({ children }) => <div>{children}</div>;
