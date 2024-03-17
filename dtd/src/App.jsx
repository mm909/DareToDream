import { useState } from 'react'
import './App.css'

import { FlightDataProvider } from './modules/contexts/flightdata'
import Presentation from './modules/presentation/presentation'
import TempSlide from './modules/slides/tempslide'
import Introduction from './modules/slides/1_introduction'

function App() {
  return (
    <FlightDataProvider>
      <Presentation>
        <Introduction />
        <TempSlide />
      </Presentation>
    </FlightDataProvider>
  )
}

export default App