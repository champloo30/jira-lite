'use client'

import React from 'react'
import { useRouter } from 'next/navigation'

import { apiFetch } from '@/lib/api'
import { isAuthenticated } from '@/lib/auth'
import { Issue } from '@/lib/types'

import { useLoadingStore } from '@/stores/loadingStore'

import DefaultLanding from '@/components/defaultLanding'
import LoadingScreen from '@/components/loadingScreen'
import IssueCard from '@/components/issueCard'

const IssuesPage = () => {
  const router = useRouter()
  const [isLoading, setLoading] = useLoadingStore((state) => [state.isLoading, state.setLoading])

  const [issues, setIssues] = React.useState<Issue[]>([])

  // check if user os authenticated

  React.useEffect(() => {
    if (!isAuthenticated()) {
      router.push('/login')
    }
  }, [router])

  // fetch issues

  React.useEffect(() => {
    try {
      setLoading(true)
      apiFetch('/issues').then(setIssues)
    } catch (error) {
      throw new Error(`Failed to fetch issue details: ${error instanceof Error ? error.message : "Unknown error"}`, { cause: { status: (error as Error & { status?: number })?.status || 500 } })
    } finally {
      setLoading(false)
    }
  }, [setLoading])

  // if no issues, set default landing page

  if (issues.length === 0) return <DefaultLanding />

  // if loading, show loading screen

  if (isLoading) return <LoadingScreen />

  return (
    <div>
      <h1>Issues</h1>
      {issues.map(issue => (
        <IssueCard key={issue.id} issue={issue} />
      ))}
    </div>
  )
}

export default IssuesPage