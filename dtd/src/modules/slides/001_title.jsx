
import React from 'react'

function Title() {

  return (
    <>
      <div className="h-screen w-full">
        <div className='
          h-full
          w-full
          bg-white
          text-black
          overflow-hidden
        '>
          <div className='
            flex
            flex-row
            h-full
            w-full
          '>
            <div className='
              flex
              flex-col
              justify-center
            '>
              <div className='
                  px-[50px]
                  text-[100px]
                  leading-[100px]
                  text-nowrap
              '>
                265 Hours
                <div className='
                    ml-[5px]
                    text-[20px]
                    leading-[20px]
                '>
                  A short story about <span> daring to dream </span>
                </div>
              </div>
            </div>
            <div className='
              flex
              items-center
              justify-center
            '>
              <img src="wings.jpg" alt="Wings"/>
            </div>
          </div>
        </div>
      </div>
    </>
  )
}

export default Title
