export type Issue = {
  id: number
  title: string
  description: string
  status: string
  created_by: number
  assigned_to?: number
}

export type Comment = {
  id: number
  content: string
  user_id: number
  issue_id: number
  created_at: string
}