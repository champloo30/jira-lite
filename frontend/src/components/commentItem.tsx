'use client'

import { apiFetch } from '@/lib/api'
import { getUser } from '@/lib/auth'
import { Comment } from '@/lib/types'
import React from 'react'

const CommentItem = ({ comment, onDelete }: { comment: Comment, onDelete: () => void }) => {
  const user = getUser()

  const canEdit = user?.role === 'admin' || comment.user_id === user?.sub

  return (
    <div>
      <p>{comment.content}</p>
      {canEdit && (
        <button
          onClick={() =>
            apiFetch(
              `/issues/${comment.issue_id}/comments/${comment.id}`,
              { method: 'DELETE' }
            ).then(onDelete)
          }
        >Delete</button>
      )}
    </div>
  )
}

export default CommentItem