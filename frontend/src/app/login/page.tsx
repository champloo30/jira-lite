'use client'

import React from 'react'
import { useRouter } from 'next/navigation'
import { login } from '@/lib/auth'
import { useLoadingStore } from '@/stores/loadingStore'

const LoginPage = () => {
  const router = useRouter()
  const [isLoading, setLoading] = useLoadingStore((state) => [state.isLoading, state.setLoading])


  const apiUrl = process.env.NEXT_PUBLIC_API_URL

  async function handleSubmit(e: React.SubmitEvent<HTMLFormElement>) {
    e.preventDefault()
    setLoading(true)

    try {
      const fromData = new FormData(e.currentTarget)
      const res = await fetch(`${apiUrl}/auth/login`, {
        method: 'POST',
        body: fromData
      })

      const data = await res.json()
      login(data.access_token)
      router.push('/issues')
    } catch (error) {
      console.error("Login failed", error)
      throw new Error(`Login failed: ${error instanceof Error ? error.message : "Unknown error"}`)
    } finally {
      setLoading(false)
    }

  }
  return (
    <form onSubmit={handleSubmit}>
      <input name='username' type='text' />
      <input name='password' type='password' />
      <button type='submit' disabled={isLoading}>
        {isLoading ? 'Logging in...' : 'Login'}
      </button>
    </form>
  )
}

export default LoginPage