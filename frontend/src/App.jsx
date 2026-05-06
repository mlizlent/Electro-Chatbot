import { useState, useEffect } from 'react'
import { Toaster } from 'react-hot-toast'
import { AuthProvider, useAuth } from './context/AuthContext'
import { ThemeProvider } from './context/ThemeContext'
import Auth from './components/Auth'
import Chat from './components/Chat'
import Sidebar from './components/Sidebar'
import api from './api/client'

function AppContent() {
  const { user, loading } = useAuth()
  const [conversations, setConversations] = useState([])
  const [activeConversationId, setActiveConversationId] = useState(null)
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false)

  console.log('AppContent rendering:', { user, loading })

  // Load conversations when user logs in
  useEffect(() => {
    if (!user) {
      setConversations([])
      setActiveConversationId(null)
      return
    }
    api.get('/conversations')
      .then(res => setConversations(res.data))
      .catch((err) => {
        console.error('Failed to load conversations:', err)
      })
  }, [user])

  const handleNewConversation = () => {
    setActiveConversationId(null)
  }

  const handleSelectConversation = (id) => {
    setActiveConversationId(id)
  }

  const handleConversationCreated = (id, title) => {
    const newConvo = {
      id,
      title,
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
    }
    setConversations(prev => [newConvo, ...prev])
    setActiveConversationId(id)
  }

  const handleDeleteConversation = (id) => {
    setConversations(prev => prev.filter(c => c.id !== id))
    if (activeConversationId === id) {
      setActiveConversationId(null)
    }
  }

  if (loading) {
    console.log('Showing loading screen')
    return (
      <div className="min-h-screen bg-dark-900 dark:bg-dark-900 light:bg-gray-50 flex items-center justify-center">
        <div className="flex flex-col items-center gap-3">
          <span className="w-8 h-8 border-2 border-primary-500/30 border-t-primary-500 rounded-full animate-spin" />
          <span className="text-gray-500 dark:text-gray-500 light:text-gray-600 text-sm">Loading ElectroBot...</span>
        </div>
      </div>
    )
  }

  if (!user) {
    console.log('Showing auth screen')
    return <Auth />
  }

  console.log('Showing main app')
  return (
    <div className="flex h-screen bg-dark-900 dark:bg-dark-900 light:bg-gray-50 overflow-hidden">
      <Sidebar
        conversations={conversations}
        activeConversationId={activeConversationId}
        onSelectConversation={handleSelectConversation}
        onNewConversation={handleNewConversation}
        onDeleteConversation={handleDeleteConversation}
        collapsed={sidebarCollapsed}
        onToggleCollapse={() => setSidebarCollapsed(v => !v)}
      />

      <main className="flex-1 flex flex-col overflow-hidden">
        <Chat
          key={activeConversationId ?? 'new'}
          conversationId={activeConversationId}
          onConversationCreated={handleConversationCreated}
        />
      </main>
    </div>
  )
}

export default function App() {
  console.log('App component rendering')
  return (
    <ThemeProvider>
      <AuthProvider>
        <AppContent />
        <Toaster
          position="top-right"
          toastOptions={{
            style: {
              background: '#21262d',
              color: '#e6edf3',
              border: '1px solid #30363d',
              fontSize: '14px',
            },
            success: { iconTheme: { primary: '#2aa5ff', secondary: '#0d1117' } },
            error: { iconTheme: { primary: '#f85149', secondary: '#0d1117' } },
          }}
        />
      </AuthProvider>
    </ThemeProvider>
  )
}
