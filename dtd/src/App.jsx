import { useState } from 'react'
import './App.css'

import { FlightDataProvider } from './modules/contexts/flightdata'
import Presentation from './modules/presentation/presentation'
import TempSlide from './modules/slides/tempslide'
import Title from './modules/slides/001_title'
import Data from './modules/slides/002_data'
import Timeline from './modules/slides/003_timeline'
import Friend from './modules/slides/004_friend'
import Stats from './modules/slides/0035_stats'

function App() {
  return (
    <FlightDataProvider>
      <Presentation>
        <Title />
        <Data />
        <Timeline />
        <TempSlide />
        <Stats />
        <TempSlide />
        <Friend />
      </Presentation>
    </FlightDataProvider>
  )
}

export default App