import React from 'react'

import { Issue } from '@/lib/types'

import StatusBadge from './statusBadge'

const IssueCard = ({ issue }: { issue: Issue }) => {
  return (
    <div>
      <a href={`/issues/${issue.id}`}>
        <h3>{issue.title}</h3>
      </a>
      <StatusBadge status={issue.status} />
    </div>
  )
}

export default IssueCard