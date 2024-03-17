
import React from 'react';

const TempSlide = () => {

    const randomColor = () => {
        return '#' + Math.floor(Math.random()*16777215).toString(16);
    }

    return (
        <div className="h-screen w-full">
            <div className={`
                flex
                flex-col
                justify-center
                items-center
                h-screen
                w-full
            `}
            style = {{
                // backgroundColor: randomColor(),
                backgroundImage: '#fff',
            }}>
            </div>
        </div>
    );
};

export default TempSlide;