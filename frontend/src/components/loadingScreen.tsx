import React from 'react'
import { LoaderCircle } from 'lucide-react'

const LoadingScreen = () => {
  return (
    <div className='absolute inset-0 flex flex-col justify-center items-center gap-4 bg-white/50 backdrop-blur-sm'>
      Loading...<LoaderCircle className='animate-spin' />
    </div>
  )
}

export default LoadingScreen