export function login(token: string) {
  localStorage.setItem('token', token)
}

export function logout() {
  localStorage.removeItem('token')
}

export function isAuthenticated() {
  return !!localStorage.getItem('token')
}

export function getUser() {
  const token = localStorage.getItem('token')
  if (!token) return null

  return JSON.parse(atob(token.split('.')[1]))
}