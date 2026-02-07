'use client'

import React from 'react'

import { getUser, logout } from '@/lib/auth'
import { useRouter } from 'next/navigation'

const Navbar = () => {
  const router = useRouter()
  const user = getUser()

  function handleLogout() {
    logout()
    router.push('/login')
  }

  return (
    <nav>
      <a href="/issues">Issues</a>
      {user ? (
        <>
          <span>{user.name} {user.role}</span>
          <button onClick={handleLogout}>Logout</button>
        </>
      ) : (
        <a href="/login">Login</a>
      )}
    </nav>
  )
}

export default Navbar