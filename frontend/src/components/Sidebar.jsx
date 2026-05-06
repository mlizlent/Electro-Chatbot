import { useState } from 'react'
import { Plus, MessageSquare, Trash2, Cpu, LogOut, ChevronLeft, ChevronRight } from 'lucide-react'
import { useAuth } from '../context/AuthContext'
import toast from 'react-hot-toast'
import api from '../api/client'

export default function Sidebar({
  conversations,
  activeConversationId,
  onSelectConversation,
  onNewConversation,
  onDeleteConversation,
  collapsed,
  onToggleCollapse,
}) {
  const { user, logout } = useAuth()
  const [deletingId, setDeletingId] = useState(null)

  const handleDelete = async (e, id) => {
    e.stopPropagation()
    if (!confirm('Delete this conversation?')) return
    setDeletingId(id)
    try {
      await api.delete(`/conversations/${id}`)
      onDeleteConversation(id)
      toast.success('Conversation deleted')
    } catch {
      toast.error('Failed to delete')
    } finally {
      setDeletingId(null)
    }
  }

  return (
    <aside className={`flex flex-col bg-dark-800 dark:bg-dark-800 light:bg-white border-r border-dark-600 dark:border-dark-600 light:border-gray-200 transition-all duration-300 ${
      collapsed ? 'w-14' : 'w-64'
    }`}>
      {/* Header */}
      <div className="flex items-center justify-between p-3 border-b border-dark-600 dark:border-dark-600 light:border-gray-200">
        {!collapsed && (
          <div className="flex items-center gap-2">
            <Cpu className="w-5 h-5 text-primary-400 flex-shrink-0" />
            <span className="font-bold text-white dark:text-white light:text-gray-900 text-sm">ElectroBot</span>
          </div>
        )}
        {collapsed && <Cpu className="w-5 h-5 text-primary-400 mx-auto" />}
        <button
          onClick={onToggleCollapse}
          className="btn-ghost p-1.5 rounded ml-auto"
          aria-label={collapsed ? 'Expand sidebar' : 'Collapse sidebar'}
        >
          {collapsed ? <ChevronRight className="w-4 h-4" /> : <ChevronLeft className="w-4 h-4" />}
        </button>
      </div>

      {/* New Chat button */}
      <div className="p-2">
        <button
          onClick={onNewConversation}
          className={`w-full flex items-center gap-2 bg-primary-600/20 hover:bg-primary-600/30 border border-primary-500/30 text-primary-300 rounded-lg transition-colors duration-200 ${
            collapsed ? 'justify-center p-2' : 'px-3 py-2'
          }`}
          aria-label="New conversation"
        >
          <Plus className="w-4 h-4 flex-shrink-0" />
          {!collapsed && <span className="text-sm font-medium">New Chat</span>}
        </button>
      </div>

      {/* Conversations list */}
      <div className="flex-1 overflow-y-auto py-1">
        {!collapsed && conversations.length === 0 && (
          <p className="text-xs text-gray-600 text-center py-8 px-4">
            No conversations yet. Start a new chat!
          </p>
        )}

        {conversations.map(convo => (
          <div
            key={convo.id}
            onClick={() => onSelectConversation(convo.id)}
            className={`group flex items-center gap-2 mx-2 my-0.5 rounded-lg cursor-pointer transition-colors duration-150 ${
              activeConversationId === convo.id
                ? 'bg-primary-600/20 border border-primary-500/30'
                : 'hover:bg-dark-700 border border-transparent'
            } ${collapsed ? 'justify-center p-2' : 'px-3 py-2'}`}
            role="button"
            tabIndex={0}
            onKeyDown={e => e.key === 'Enter' && onSelectConversation(convo.id)}
            aria-label={`Conversation: ${convo.title}`}
          >
            <MessageSquare className={`w-4 h-4 flex-shrink-0 ${
              activeConversationId === convo.id ? 'text-primary-400' : 'text-gray-500'
            }`} />

            {!collapsed && (
              <>
                <span className={`flex-1 text-sm truncate ${
                  activeConversationId === convo.id ? 'text-gray-100' : 'text-gray-400'
                }`}>
                  {convo.title}
                </span>
                <button
                  onClick={e => handleDelete(e, convo.id)}
                  disabled={deletingId === convo.id}
                  className="opacity-0 group-hover:opacity-100 p-1 rounded hover:bg-red-500/20 hover:text-red-400 text-gray-600 transition-all"
                  aria-label="Delete conversation"
                >
                  <Trash2 className="w-3.5 h-3.5" />
                </button>
              </>
            )}
          </div>
        ))}
      </div>

      {/* User footer */}
      <div className={`border-t border-dark-600 p-3 flex items-center gap-2 ${collapsed ? 'justify-center' : ''}`}>
        <div className="w-7 h-7 rounded-full bg-primary-600/30 border border-primary-500/40 flex items-center justify-center flex-shrink-0">
          <span className="text-xs font-bold text-primary-300">
            {user?.username?.[0]?.toUpperCase()}
          </span>
        </div>
        {!collapsed && (
          <>
            <div className="flex-1 min-w-0">
              <p className="text-sm font-medium text-gray-200 truncate">{user?.username}</p>
              <p className="text-xs text-gray-500 truncate">{user?.email}</p>
            </div>
            <button
              onClick={logout}
              className="btn-ghost p-1.5 rounded"
              aria-label="Sign out"
            >
              <LogOut className="w-4 h-4" />
            </button>
          </>
        )}
      </div>
    </aside>
  )
}
