

import React, { useEffect, useState } from 'react';

const Presentation = ({ children }) => {

    const [currentSlide, setCurrentSlide] = useState(0);

    useEffect(() => {
        const handleKeyDown = (event) => {
            if (event.key === 'ArrowLeft') {
                setCurrentSlide((prev) => prev > 0 ? prev - 1 : prev)
            } else if (event.key === 'ArrowRight') {
                setCurrentSlide((prev) => prev < children.length - 1 ? prev + 1 : prev)
            }
        };
        document.addEventListener('keydown', handleKeyDown);

        return () => {
            document.removeEventListener('keydown', handleKeyDown);
        };
    }, [children.length]);

    useEffect(() => {
        window.scrollTo({
            top: window.innerHeight * currentSlide,
            behavior: 'smooth',
        });
    }, [currentSlide]);

    return (
        <>
            {children.map((child, index) => (
                <div key={index} className="h-screen w-full overflow-hidden">
                    {child}
                </div>
            ))}
        </>
    );
};

export default Presentation;