import React from 'react'

function TimelineFlight({flight}) {

    let BottomSpacing = flight.BottomSpacing ? flight.BottomSpacing : '0px'

    // translate date from 2009-03-18 to March 18, 2009
    let date = new Date(flight.Date)
    let options = { year: 'numeric', month: 'long', day: 'numeric' };
    let formattedDate = date.toLocaleDateString('en-US', options)


    return (
            <li className='
                relative
                flex
                flex-row
                items-center
                justify-center
                mt-[100px]
            ' 
            style={{marginBottom: BottomSpacing}}>
  
                <div className='
                    flex
                    flex-col
                '>
                    <div className='
                        text-[36px]
                        font-semibold
                        px-5
                        py-5
                    '>
                        {flight.Caption}
                    </div>
                    <div className='
                        shadow-md 
                        border-[1px] 
                        rounded-lg
                        ml-5
                        mb-5
                        overflow-hidden
                    '>
                    <div className='
                        text-[24px]
                        font-bold
                        w-full
                        //border-b-[1px]
                        p-[10px]
                        px-5
                        flex
                        flex-row
                        items-center
                        justify-center
                    '>
                        <div className='
                            flex-grow
                        '>
                            {formattedDate}
                        </div>
                        <div className='
                            text-[20px]
                            font-normal
                        '>
                            Flight #{flight.FlightNumber}
                        </div>
                    </div>
                    
                    <div className='
                        flex
                        flex-row
                    '>
                        <img className='max-h-[300px]' src={flight.AirplaneModel+".jpg"} alt="PA28-140" />
                        <div className='
                            flex
                            flex-col
                            flex-grow
                            px-[20px]
                        '>
                            <div className='
                                flex
                                flex-row
                                py-[10px]
                                border-y-[1px]
                            '>
                                <div className='
                                    text-[24px]
                                    flex-grow
                                '>
                                    {flight.AirplaneModel}
                                </div>
                                <div className='
                                    text-[16px]
                                    flex
                                    items-center
                                '>
                                    {flight.TailNumber}
                                </div>
                            </div>
                            <div className='
                                border-b-[1px]
                                text-[18px]
                                py-[5px]
                            '>
                                <p> {flight.Memo}</p>
                            </div>
                            <div className='
                                my-[20px]
                                flex
                                flex-row
                                flex-grow
                                justify-between
                                items-center
                            '>
                                <div className='
                                    w-full
                                    flex
                                    flex-row
                                    justify-between
                                '>
                                    <div className='
                                        p-[10px]
                                        border-[1px]
                                        rounded-[5px]
                                        shadow-md
                                        min-w-[150px]
                                    '>
                                        <span className='
                                            text-[10px]
                                            leading-[10px]
                                        '>
                                            From
                                        </span>
                                        <br />
                                        <span className='
                                            text-[20px]
                                            leading-[20px]
                                        '>
                                            {flight.Departure}
                                        </span>
                                        <br />
                                        <span className='
                                            text-[14px]
                                            leading-[14px]
                                        '>
                                            {flight.DepartureName}
                                        </span>
                                    </div>

                                    <div className='
                                        flex
                                        items-center
                                    '>
                                        <div className='
                                            p-[10px]
                                            min-w-[50px]
                                        '>
                                            <svg className='text-black' xmlns="http://www.w3.org/2000/svg" viewBox="0 0 25 25"><path d="m17.5 5.999-.707.707 5.293 5.293H1v1h21.086l-5.294 5.295.707.707L24 12.499l-6.5-6.5z" data-name="Right"/></svg>
                                        </div>
                                    </div>
                                    <div className='
                                        p-[10px]
                                        border-[1px]
                                        rounded-[5px]
                                        shadow-md
                                        min-w-[150px]
                                    '>
                                        <span className='
                                            text-[10px]
                                            leading-[10px]
                                        '>
                                            To
                                        </span>
                                        <br />
                                        <span className='
                                            text-[20px]
                                            leading-[20px]
                                        '>
                                            {flight.Arrival}
                                        </span>
                                        <br />
                                        <span className='
                                            text-[14px]
                                            leading-[14px]
                                        '>
                                            {flight.ArrivalName}
                                        </span>
                                    </div>
                                    <div className='
                                        min-w-[150px]
                                        flex
                                        items-center
                                        justify-center
                                        text-[24px]
                                    '>
                                        {flight.Hours} Hours
                                    </div>
                                </div>
                      

                                </div>

                        </div>

                    </div>

                </div>
            </div>
                
        </li>
    )
}

export default TimelineFlight
