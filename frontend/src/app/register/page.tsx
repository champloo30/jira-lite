'use client'

import React from 'react'
import { useRouter } from 'next/navigation'

import { login } from '@/lib/auth'
import { useLoadingStore } from '@/stores/loadingStore'

import toast from 'react-hot-toast'
import LoadingScreen from '@/components/loadingScreen'

const RegisterPage = () => {
  const router = useRouter()
  const [isLoading, setLoading] = useLoadingStore((state) => [state.isLoading, state.setLoading])

  const apiUrl = process.env.NEXT_PUBLIC_API_URL

  async function handleSubmit(e: React.SubmitEvent<HTMLFormElement>) {
    e.preventDefault()
    setLoading(true)

    try {
      const fromData = new FormData(e.currentTarget)
      const res = await fetch(`${apiUrl}/auth/register`, {
        method: 'POST',
        body: fromData
      })

      const data = await res.json()
      login(data.access_token)
      toast.success("Register successful and logged in")
      router.push('/issues')
    } catch (error) {
      toast.error("Register failed")
      console.error("Register failed", error)
      throw new Error(`Register failed: ${error instanceof Error ? error.message : "Unknown error"}`, { cause: { status: (error as Error & { status?: number })?.status || 500 } })
    } finally {
      setLoading(false)
    }
  }

  if (isLoading) return <LoadingScreen />

  return (
    <form onSubmit={handleSubmit}>
      <input name='username' type='text' />
      <input name='password' type='password' />
      <button type='submit' disabled={isLoading}>
        {isLoading ? 'Registering...' : 'Register'}
      </button>
    </form>
  )
}

export default RegisterPage