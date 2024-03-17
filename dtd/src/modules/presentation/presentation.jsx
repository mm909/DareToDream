import React, { useEffect, useState } from 'react';

const Presentation = ({ children }) => {

    const [currentSlide, setCurrentSlide] = useState(2);
    console.log(currentSlide)

    // const maxSlide = 10

    // useEffect(() => {
    //     const handleKeyDown = (event) => {
    //         if (event.key === 'ArrowLeft') {
    //             setCurrentSlide((prev) => prev > 0 ? prev - 1 : prev)
    //             window.scrollTo({
    //                 top: window.innerHeight * currentSlide,
    //                 behavior: 'smooth',
    //             });
    //         } else if (event.key === 'ArrowRight') {
    //             setCurrentSlide((prev) => prev < maxSlide - 1 ? prev + 1 : prev)
    //             window.scrollTo({
    //                 top: window.innerHeight * currentSlide,
    //                 behavior: 'smooth',
    //             });
    //         }
    //     };
    //     document.addEventListener('keydown', handleKeyDown);

    //     return () => {
    //         document.removeEventListener('keydown', handleKeyDown);
    //     };
    // }, [children.length]);

    // useEffect(() => {
    //     window.scrollTo({
    //         top: window.innerHeight * currentSlide,
    //         behavior: 'smooth',
    //     });
    // }, [currentSlide]);

    return (
        <>
            {children}
        </>
    );
};

export default Presentation;