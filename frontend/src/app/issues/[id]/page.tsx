'use client'

import React from 'react'
import { useParams, useRouter } from 'next/navigation'

import { isAuthenticated } from '@/lib/auth'
import { apiFetch } from '@/lib/api'
import { useLoadingStore } from '@/stores/loadingStore'

import LoadingScreen from '@/components/loadingScreen'
import { StatusActions } from '@/components/statusActions'
import CommentList from '@/components/commentList'
import { Comment, Issue } from '@/lib/types'

const IssuesDetailsPage = () => {
  const router = useRouter()
  const { id } = useParams()
  const [isLoading, setLoading] = useLoadingStore((state) => [state.isLoading, state.setLoading])

  const [issue, setIssue] = React.useState<Issue | null>(null)
  const [comments, setComments] = React.useState<Comment[]>([])

  // check if user os authenticated

  React.useEffect(() => {
    if (!isAuthenticated()) {
      router.push('/login')
    }
  }, [router])

  // fetch issue details and comments

  React.useEffect(() => {
    try {
      setLoading(true)
      apiFetch(`/issues/${id}`).then(setIssue)
      apiFetch(`/issues/${id}/comments`).then(setComments)
    } catch (error) {
      throw new Error(`Failed to fetch issue details: ${error instanceof Error ? error.message : "Unknown error"}`, { cause: { status: (error as Error & { status?: number })?.status || 500 } })
    } finally {
      setLoading(false)
    }
  }, [id, setLoading])

  // if not issue, redirect to issues page

  React.useEffect(() => {
    if (!issue) {
      router.push('/issues')
    }
  }, [issue, router])

  // if loading, show loading screen

  if (isLoading) return <LoadingScreen />

  return (
    <div>
      <h1>{issue?.title}</h1>
      <p>{issue?.description}</p>
      {issue && <StatusActions issue={issue} onUpdate={() => router.refresh()} />}
      <h2>Comments</h2>
      {comments.map(c => (
        <CommentList key={c.id} comments={comments} refresh={() => router.refresh()} />
      ))}
    </div>
  )
}

export default IssuesDetailsPage