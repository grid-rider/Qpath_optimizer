'use client'

import { CircularProgress } from '@chakra-ui/progress';
import { Map } from './components/Map';

export default function Home() {
  return (
    <main>
      <h1>Qpath Optimizer</h1>
      <CircularProgress isIndeterminate color='green.300' />
      <Map/>
    </main>
  )
}
