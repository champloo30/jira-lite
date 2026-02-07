import { apiFetch } from "@/lib/api"
import { getUser } from "@/lib/auth"
import { Issue } from "@/lib/types"

const transitions: Record<string, string[]> = {
  open: ['in_progress'],
  in_progress: ['done'],
  done: []
}

export function StatusActions({ issue, onUpdate }: { issue: Issue; onUpdate: () => void }) {
  const user = getUser()
  const canChangeStatus = user?.role === 'admin' || issue.assigned_to === user?.sub

  if (!canChangeStatus) return null
  return (
    <div>
      {transitions[issue.status].map(next => (
        <button
          key={next}
          onClick={() =>
            apiFetch(`/issues/${issue.id}/status?status=${next}`, {
              method: 'PUT'
            }).then(onUpdate)
          }
        >
          {`Move to ${next.replace('_', ' ')}`}
        </button>
      ))}
    </div>
  )
}