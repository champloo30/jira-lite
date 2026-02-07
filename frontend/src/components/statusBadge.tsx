import React from 'react'

const StatusBadge = ({ status }: { status: string }) => {
  return (
    <span>{status}</span>
  )
}

export default StatusBadge