import { useState } from 'react'
import { ZoomIn, ZoomOut, Download, Maximize2, X } from 'lucide-react'

export default function CircuitViewer({ svg }) {
  const [zoom, setZoom] = useState(1)
  const [fullscreen, setFullscreen] = useState(false)

  if (!svg) return null

  const handleDownload = () => {
    const blob = new Blob([svg], { type: 'image/svg+xml' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = 'circuit.svg'
    a.click()
    URL.revokeObjectURL(url)
  }

  const CircuitContent = () => (
    <div
      className="circuit-container overflow-auto"
      style={{ transform: `scale(${zoom})`, transformOrigin: 'top left', transition: 'transform 0.2s' }}
      dangerouslySetInnerHTML={{ __html: svg }}
    />
  )

  return (
    <>
      {/* Inline viewer */}
      <div className="mt-3 bg-dark-900 border border-dark-600 rounded-xl overflow-hidden">
        {/* Toolbar */}
        <div className="flex items-center justify-between px-3 py-2 border-b border-dark-600 bg-dark-800">
          <span className="text-xs font-medium text-primary-400 flex items-center gap-1.5">
            <svg className="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <rect x="2" y="3" width="20" height="14" rx="2" />
              <path d="M8 21h8M12 17v4" />
            </svg>
            Circuit Diagram
          </span>
          <div className="flex items-center gap-1">
            <button
              onClick={() => setZoom(z => Math.max(0.5, z - 0.25))}
              className="btn-ghost p-1.5 rounded"
              aria-label="Zoom out"
            >
              <ZoomOut className="w-3.5 h-3.5" />
            </button>
            <span className="text-xs text-gray-500 w-10 text-center">{Math.round(zoom * 100)}%</span>
            <button
              onClick={() => setZoom(z => Math.min(3, z + 0.25))}
              className="btn-ghost p-1.5 rounded"
              aria-label="Zoom in"
            >
              <ZoomIn className="w-3.5 h-3.5" />
            </button>
            <button
              onClick={handleDownload}
              className="btn-ghost p-1.5 rounded"
              aria-label="Download SVG"
            >
              <Download className="w-3.5 h-3.5" />
            </button>
            <button
              onClick={() => setFullscreen(true)}
              className="btn-ghost p-1.5 rounded"
              aria-label="Fullscreen"
            >
              <Maximize2 className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>

        {/* SVG display */}
        <div className="p-4 overflow-auto max-h-80">
          <CircuitContent />
        </div>
      </div>

      {/* Fullscreen modal */}
      {fullscreen && (
        <div
          className="fixed inset-0 z-50 bg-black/90 flex items-center justify-center p-4"
          onClick={() => setFullscreen(false)}
        >
          <div
            className="bg-dark-800 rounded-xl border border-dark-600 max-w-5xl w-full max-h-[90vh] overflow-auto"
            onClick={e => e.stopPropagation()}
          >
            <div className="flex items-center justify-between px-4 py-3 border-b border-dark-600">
              <span className="text-sm font-medium text-primary-400">Circuit Diagram</span>
              <div className="flex items-center gap-2">
                <button onClick={handleDownload} className="btn-ghost p-1.5 rounded text-xs flex items-center gap-1">
                  <Download className="w-3.5 h-3.5" /> Download SVG
                </button>
                <button onClick={() => setFullscreen(false)} className="btn-ghost p-1.5 rounded" aria-label="Close">
                  <X className="w-4 h-4" />
                </button>
              </div>
            </div>
            <div className="p-6 overflow-auto" dangerouslySetInnerHTML={{ __html: svg }} />
          </div>
        </div>
      )}
    </>
  )
}
