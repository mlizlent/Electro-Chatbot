import { useState, useEffect, useRef, useCallback } from 'react'
import { Send, Paperclip, X, Cpu, Zap, Wifi, Radio } from 'lucide-react'
import Message from './Message'
import api from '../api/client'
import toast from 'react-hot-toast'

const SUGGESTIONS = [
  { icon: <Zap className="w-4 h-4" />, text: 'Explain how a buck converter works' },
  { icon: <Cpu className="w-4 h-4" />, text: 'Design an ESP32 temperature sensor with MQTT' },
  { icon: <Wifi className="w-4 h-4" />, text: 'Compare LoRa vs NB-IoT for remote sensing' },
  { icon: <Radio className="w-4 h-4" />, text: 'Draw a 555 timer astable circuit' },
]

function TypingIndicator() {
  return (
    <div className="flex gap-3 message-enter">
      <div className="w-8 h-8 rounded-full bg-green-600/20 border border-green-500/30 flex items-center justify-center flex-shrink-0">
        <Cpu className="w-4 h-4 text-green-400" />
      </div>
      <div className="bg-dark-800 border border-dark-600 rounded-2xl px-4 py-3">
        <div className="flex gap-1 items-center h-5">
          <span className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
          <span className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
          <span className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
        </div>
      </div>
    </div>
  )
}

export default function Chat({ conversationId, onConversationCreated }) {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [image, setImage] = useState(null)
  const [imagePreview, setImagePreview] = useState(null)
  const [loading, setLoading] = useState(false)
  const [fetching, setFetching] = useState(false)
  const messagesEndRef = useRef(null)
  const fileInputRef = useRef(null)
  const textareaRef = useRef(null)

  // Load messages when conversation changes
  useEffect(() => {
    if (!conversationId) {
      setMessages([])
      return
    }
    setFetching(true)
    api.get(`/conversations/${conversationId}/messages`)
      .then(res => setMessages(res.data))
      .catch(() => toast.error('Failed to load messages'))
      .finally(() => setFetching(false))
  }, [conversationId])

  // Auto-scroll
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, loading])

  const handleImageSelect = (e) => {
    const file = e.target.files?.[0]
    if (!file) return
    if (file.size > 10 * 1024 * 1024) {
      toast.error('Image must be under 10MB')
      return
    }
    setImage(file)
    setImagePreview(URL.createObjectURL(file))
  }

  const clearImage = () => {
    setImage(null)
    setImagePreview(null)
    if (fileInputRef.current) fileInputRef.current.value = ''
  }

  const handleSend = useCallback(async (messageText = input) => {
    const text = messageText.trim()
    if (!text && !image) return
    if (loading) return

    // Optimistic user message
    const userMsg = {
      id: Date.now(),
      role: 'user',
      content: text,
      image_path: imagePreview,
      created_at: new Date().toISOString(),
    }
    setMessages(prev => [...prev, userMsg])
    setInput('')
    clearImage()
    setLoading(true)

    try {
      const formData = new FormData()
      formData.append('message', text)
      if (conversationId) formData.append('conversation_id', conversationId)
      if (image) formData.append('image', image)

      const res = await api.post('/chat', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      })

      const { conversation_id, conversation_title, message: aiMsg } = res.data

      // Notify parent if new conversation was created
      if (!conversationId) {
        onConversationCreated(conversation_id, conversation_title)
      }

      setMessages(prev => [...prev, {
        ...aiMsg,
        created_at: aiMsg.created_at,
        generated_image: aiMsg.generated_image, // Include generated image
      }])
    } catch (err) {
      const detail = err.response?.data?.detail || 'Failed to get response'
      toast.error(detail)
      // Remove optimistic message on error
      setMessages(prev => prev.filter(m => m.id !== userMsg.id))
    } finally {
      setLoading(false)
    }
  }, [input, image, imagePreview, conversationId, loading, onConversationCreated])

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  // Auto-resize textarea
  useEffect(() => {
    const ta = textareaRef.current
    if (!ta) return
    ta.style.height = 'auto'
    ta.style.height = Math.min(ta.scrollHeight, 160) + 'px'
  }, [input])

  const isEmpty = messages.length === 0 && !fetching

  return (
    <div className="flex flex-col h-full">
      {/* Messages area */}
      <div className="flex-1 overflow-y-auto px-4 py-6">
        {fetching && (
          <div className="flex justify-center py-8">
            <span className="w-6 h-6 border-2 border-primary-500/30 border-t-primary-500 rounded-full animate-spin" />
          </div>
        )}

        {/* Empty state */}
        {isEmpty && (
          <div className="flex flex-col items-center justify-center h-full text-center max-w-lg mx-auto">
            <div className="w-16 h-16 bg-primary-600/20 border border-primary-500/30 rounded-2xl flex items-center justify-center mb-4">
              <Cpu className="w-8 h-8 text-primary-400" />
            </div>
            <h2 className="text-xl font-bold text-white mb-2">ElectroBot</h2>
            <p className="text-gray-400 text-sm mb-8">
              Ask me anything about electronics, IoT, sensors, RF, cellular, PCB design, or embedded systems.
              I can also sketch circuits for you.
            </p>

            {/* Suggestion chips */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 w-full">
              {SUGGESTIONS.map((s, i) => (
                <button
                  key={i}
                  onClick={() => handleSend(s.text)}
                  className="flex items-center gap-2 text-left bg-dark-800 hover:bg-dark-700 border border-dark-600 hover:border-primary-500/40 rounded-xl px-4 py-3 text-sm text-gray-300 hover:text-gray-100 transition-all duration-200"
                >
                  <span className="text-primary-400 flex-shrink-0">{s.icon}</span>
                  {s.text}
                </button>
              ))}
            </div>
          </div>
        )}

        {/* Messages */}
        <div className="max-w-3xl mx-auto space-y-6">
          {messages.map(msg => (
            <Message key={msg.id} message={msg} />
          ))}
          {loading && <TypingIndicator />}
          <div ref={messagesEndRef} />
        </div>
      </div>

      {/* Input area */}
      <div className="border-t border-dark-600 bg-dark-800/50 backdrop-blur-sm p-4">
        <div className="max-w-3xl mx-auto">
          {/* Image preview */}
          {imagePreview && (
            <div className="mb-3 relative inline-block">
              <img
                src={imagePreview}
                alt="Upload preview"
                className="h-20 w-auto rounded-lg border border-dark-600 object-cover"
              />
              <button
                onClick={clearImage}
                className="absolute -top-2 -right-2 w-5 h-5 bg-red-500 rounded-full flex items-center justify-center hover:bg-red-600 transition-colors"
                aria-label="Remove image"
              >
                <X className="w-3 h-3 text-white" />
              </button>
            </div>
          )}

          {/* Input row */}
          <div className="flex items-end gap-2 bg-dark-700 border border-dark-600 rounded-2xl px-4 py-3 focus-within:border-primary-500/50 transition-colors">
            {/* File upload */}
            <button
              onClick={() => fileInputRef.current?.click()}
              className="flex-shrink-0 text-gray-500 hover:text-primary-400 transition-colors p-1"
              aria-label="Attach image"
              disabled={loading}
            >
              <Paperclip className="w-5 h-5" />
            </button>
            <input
              ref={fileInputRef}
              type="file"
              accept="image/*"
              onChange={handleImageSelect}
              className="hidden"
              aria-label="Upload image"
            />

            {/* Textarea */}
            <textarea
              ref={textareaRef}
              value={input}
              onChange={e => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Ask about circuits, components, IoT, RF, cellular... or ask me to draw a circuit"
              className="flex-1 bg-transparent text-gray-100 placeholder-gray-600 resize-none outline-none text-sm leading-relaxed min-h-[24px] max-h-40"
              rows={1}
              disabled={loading}
              aria-label="Message input"
            />

            {/* Send button */}
            <button
              onClick={() => handleSend()}
              disabled={loading || (!input.trim() && !image)}
              className="flex-shrink-0 w-8 h-8 bg-primary-600 hover:bg-primary-700 disabled:bg-dark-600 disabled:text-gray-600 text-white rounded-xl flex items-center justify-center transition-colors"
              aria-label="Send message"
            >
              {loading
                ? <span className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                : <Send className="w-4 h-4" />
              }
            </button>
          </div>

          <p className="text-xs text-gray-600 text-center mt-2">
            Press Enter to send · Shift+Enter for new line · Attach images of circuits for analysis
          </p>
        </div>
      </div>
    </div>
  )
}
