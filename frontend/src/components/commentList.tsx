'use client'

import React from 'react'

import { Comment } from '@/lib/types'

import CommentItem from './commentItem'

const CommentList = ({ comments, refresh }: { comments: Comment[], refresh: () => void }) => {
  return (
    <div>
      {comments.map(c => (
        <CommentItem 
          key={c.id}
          comment={c}
          onDelete={refresh}
        />
      ))}
    </div>
  )
}

export default CommentList