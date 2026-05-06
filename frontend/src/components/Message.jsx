import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter'
import { oneDark } from 'react-syntax-highlighter/dist/esm/styles/prism'
import CircuitViewer from './CircuitViewer'
import { Cpu, User, Copy, Check } from 'lucide-react'
import { useState } from 'react'

function CopyButton({ text }) {
  const [copied, setCopied] = useState(false)

  const handleCopy = async () => {
    await navigator.clipboard.writeText(text)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  return (
    <button
      onClick={handleCopy}
      className="absolute top-2 right-2 p-1.5 rounded bg-dark-600 hover:bg-dark-500 text-gray-400 hover:text-gray-200 transition-colors"
      aria-label="Copy code"
    >
      {copied ? <Check className="w-3.5 h-3.5 text-green-400" /> : <Copy className="w-3.5 h-3.5" />}
    </button>
  )
}

const markdownComponents = {
  code({ node, inline, className, children, ...props }) {
    const match = /language-(\w+)/.exec(className || '')
    const codeString = String(children).replace(/\n$/, '')

    if (!inline && match) {
      return (
        <div className="relative group">
          <CopyButton text={codeString} />
          <SyntaxHighlighter
            style={oneDark}
            language={match[1]}
            PreTag="div"
            customStyle={{
              margin: 0,
              borderRadius: '8px',
              fontSize: '0.85rem',
              background: '#0d1117',
              border: '1px solid #30363d',
            }}
            {...props}
          >
            {codeString}
          </SyntaxHighlighter>
        </div>
      )
    }

    return (
      <code className="bg-dark-700 text-primary-300 px-1.5 py-0.5 rounded text-sm font-mono" {...props}>
        {children}
      </code>
    )
  },
  table({ children }) {
    return (
      <div className="overflow-x-auto my-4">
        <table className="min-w-full border-collapse text-sm">{children}</table>
      </div>
    )
  },
  th({ children }) {
    return <th className="border border-dark-600 bg-dark-700 px-3 py-2 text-left font-semibold text-gray-200">{children}</th>
  },
  td({ children }) {
    return <td className="border border-dark-600 px-3 py-2 text-gray-300">{children}</td>
  },
  blockquote({ children }) {
    return (
      <blockquote className="border-l-4 border-primary-500 pl-4 my-3 text-gray-400 italic">
        {children}
      </blockquote>
    )
  },
  a({ href, children }) {
    return (
      <a href={href} target="_blank" rel="noopener noreferrer" className="text-primary-400 hover:text-primary-300 underline">
        {children}
      </a>
    )
  },
}

export default function Message({ message }) {
  const isUser = message.role === 'user'
  const time = new Date(message.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })

  return (
    <div className={`flex gap-3 message-enter ${isUser ? 'flex-row-reverse' : 'flex-row'}`}>
      {/* Avatar */}
      <div className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${
        isUser
          ? 'bg-primary-600/30 border border-primary-500/40'
          : 'bg-green-600/20 border border-green-500/30'
      }`}>
        {isUser
          ? <User className="w-4 h-4 text-primary-400" />
          : <Cpu className="w-4 h-4 text-green-400" />
        }
      </div>

      {/* Bubble */}
      <div className={`max-w-[80%] flex flex-col gap-2 ${isUser ? 'items-end' : 'items-start'}`}>
        {/* Image preview */}
        {message.image_path && (
          <div className="rounded-xl overflow-hidden border border-dark-600 max-w-sm">
            <img
              src={message.image_path}
              alt="Uploaded circuit"
              className="max-w-full h-auto max-h-64 object-contain bg-dark-900"
            />
          </div>
        )}

        {/* Text content */}
        <div className={`rounded-2xl px-4 py-3 ${
          isUser
            ? 'bg-primary-600/20 border border-primary-500/30 text-gray-100'
            : 'bg-dark-800 border border-dark-600 text-gray-100'
        }`}>
          {isUser ? (
            <p className="text-sm whitespace-pre-wrap">{message.content}</p>
          ) : (
            <div className="prose-dark text-sm">
              <ReactMarkdown
                remarkPlugins={[remarkGfm]}
                components={markdownComponents}
              >
                {message.content}
              </ReactMarkdown>
            </div>
          )}
        </div>

        {/* Circuit diagram */}
        {message.circuit_svg && (
          <div className="w-full max-w-2xl">
            <CircuitViewer svg={message.circuit_svg} />
          </div>
        )}

        {/* Generated circuit animation */}
        {message.generated_image && (
          <div className="w-full max-w-4xl">
            <div className="rounded-xl overflow-hidden border border-dark-600 bg-dark-900">
              <div className="px-3 py-2 bg-dark-800 border-b border-dark-600 flex items-center gap-2">
                <span className="w-2 h-2 rounded-full bg-green-400 animate-pulse" />
                <span className="text-xs text-gray-400">
                  {message.generated_image.startsWith('svg:')
                    ? (() => {
                        try {
                          const svg = atob(message.generated_image.substring(4))
                          const match = svg.match(/<text[^>]*>([^<]+)<\/text>/)
                          return match ? match[1].trim() : 'Circuit Diagram'
                        } catch { return 'Circuit Diagram' }
                      })()
                    : 'AI-Generated Circuit Image'
                  }
                </span>
              </div>
              {message.generated_image.startsWith('svg:') ? (
                <div
                  className="w-full overflow-x-auto overflow-y-auto max-h-[600px] bg-dark-900"
                  style={{ scrollbarWidth: 'thin' }}
                  dangerouslySetInnerHTML={{
                    __html: atob(message.generated_image.substring(4))
                  }}
                />
              ) : (
                <img
                  src={`data:image/png;base64,${message.generated_image}`}
                  alt="AI-generated circuit"
                  className="w-full h-auto"
                />
              )}
            </div>
          </div>
        )}

        {/* Timestamp */}
        <span className="text-xs text-gray-600 px-1">{time}</span>
      </div>
    </div>
  )
}
