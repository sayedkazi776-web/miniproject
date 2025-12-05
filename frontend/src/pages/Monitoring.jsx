import React, { useState, useEffect, useRef, useCallback, useMemo } from 'react';
import { useParams, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import api from '../services/api'
import { io } from 'socket.io-client'
import { Line } from 'react-chartjs-2'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
} from 'chart.js'
import { ArrowLeft, AlertTriangle, Settings } from 'lucide-react'

// Register Chart.js components
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
)

const Monitoring = () => {
  const { cameraId } = useParams()
  const navigate = useNavigate()
  const { user } = useAuth()
  const [camera, setCamera] = useState(null)
  const [streaming, setStreaming] = useState(false)
  const [density, setDensity] = useState({ person_count: 0, density_value: 0, density_per_sqm: 0 })
  const [alert, setAlert] = useState(false)
  const [threshold, setThreshold] = useState(0.65)
  const [densityHistory, setDensityHistory] = useState([])
  const [chartData, setChartData] = useState({ labels: [], datasets: [] })
  const videoRef = useRef(null)
  const socketRef = useRef(null)
  const [showSettings, setShowSettings] = useState(false)

  const fetchCameraInfo = useCallback(async () => {
    try {
      const response = await api.get(`/cameras/${cameraId}`)
      setCamera(response.data.camera)
    } catch (error) {
      console.error('Failed to fetch camera info:', error)
      window.alert('Camera not found')
      navigate('/dashboard')
    }
  }, [cameraId, navigate])

  // FIX APPLIED HERE: Removed the extra '})', '}', and ')' at the end of this useCallback.
  const fetchDensityHistory = useCallback(async () => {
    try {
      // Fetch historical data for the last 60 minutes
      const response = await api.get(`/monitoring/density/${cameraId}?minutes=60`)
      // Reverse to show chronological order
      const logs = response.data.logs.reverse() 
      setDensityHistory(logs)
    } catch (error) {
      console.error('Failed to fetch density history:', error)
    }
  }, [cameraId]) 

  useEffect(() => {
    fetchCameraInfo()
    fetchDensityHistory()

    // This effect should only run when streaming is toggled.
    // NOTE: The dependencies for this useEffect should likely include 'streaming', 
    // 'startStream', and 'stopStream' to ensure correct behavior when 'streaming' changes.
    // However, since 'startStream' and 'stopStream' rely on state/refs that update 
    // outside of the effect, we'll keep the cleanup but add the toggle logic 
    // inside the return from the toggle button handler for simplicity, or 
    // better yet, define startStream/stopStream inside the component and include 
    // them as dependencies if they change state. 
    // For now, let's include the logic here but be mindful of the dependency array.

    // The startStream/stopStream logic should ideally be triggered by the 
    // button handler to avoid re-running on every render, but since you 
    // are toggling streaming state, this useEffect with 'streaming' as a 
    // dependency (which isn't currently in the list) is what you likely intended.
    // For now, we will assume you meant to run the stream logic when the 
    // component mounts and streaming is initially true (which it isn't), 
    // OR that you are missing `streaming` in the dependency array.

    if (streaming) {
      startStream()
    } else {
      stopStream()
    }

    // Cleanup function to disconnect socket when component unmounts or streaming stops
    return () => {
      stopStream()
    }
    // Dependency array should include `streaming` if it's meant to trigger stream changes.
  }, [fetchCameraInfo, fetchDensityHistory, streaming]) // Added 'streaming' to dependencies

  // Define stream functions (now including 'threshold' in startStream)

  const startStream = useCallback(() => {
    if (!socketRef.current) {
      const socketUrl = import.meta.env.VITE_SOCKET_URL || window.location.origin
      socketRef.current = io(socketUrl, {
        transports: ['websocket', 'polling'],
        path: '/socket.io/',
        reconnection: true,
        reconnectionDelay: 1000,
        reconnectionAttempts: 5
      })

      socketRef.current.on('connect', () => {
        console.log('✓ Socket.IO connected successfully')
        console.log('Requesting stream for camera:', cameraId)
        // Pass the current threshold to the backend on connection
        socketRef.current.emit('start_stream', {
          camera_id: cameraId,
          threshold: threshold 
        })
      })

      socketRef.current.on('connected', (data) => {
        console.log('✓ Video streamer ready:', data?.message || 'Connected')
      })

      socketRef.current.on('frame', (data) => {
        if (data && data.camera_id === cameraId && videoRef.current) {
          try {
            if (data.frame) {
              videoRef.current.src = `data:image/jpeg;base64,${data.frame}`
            }
            if (data.density) {
              setDensity(data.density)
            }
            if (data.alert !== undefined) {
              setAlert(data.alert)
            }
          
            // Update history
            if (data.density) {
              const newEntry = {
                timestamp: new Date().toISOString(),
                density_value: data.density.density_value || 0,
                person_count: data.density.person_count || 0
              }
              setDensityHistory(prev => {
                const updated = [...prev, newEntry]
                // Keep only last 100 entries
                return updated.slice(-100)
              })
            }
          } catch (error) {
            console.error('Error processing frame:', error)
          }
        }
      })

      socketRef.current.on('error', (error) => {
        console.error('Socket error:', error)
        let errorMessage = 'Streaming error occurred'
        if (error && typeof error === 'object') {
          errorMessage = error.message || error.error || JSON.stringify(error)
        } else if (error) {
          errorMessage = String(error)
        }
        console.error('Full error details:', error)
        window.alert(`Streaming error: ${errorMessage}`)
        setStreaming(false)
      })

      socketRef.current.on('connect_error', (error) => {
        console.error('Socket connection error:', error)
        window.alert(`Cannot connect to video server. Make sure backend is running on ${socketUrl}`)
        setStreaming(false)
      })

      socketRef.current.on('disconnect', () => {
        console.log('Socket disconnected')
      })
    }
  }, [cameraId, threshold]) // Added 'threshold' and 'cameraId' as dependencies for startStream

  const stopStream = useCallback(() => {
    if (socketRef.current) {
      socketRef.current.emit('stop_stream', { camera_id: cameraId })
      socketRef.current.disconnect()
      socketRef.current = null
    }
    if (videoRef.current) {
      videoRef.current.src = ''
    }
  }, [cameraId]) // Added 'cameraId' as a dependency for stopStream

  // Handler for the Start/Stop button
  const handleStreamToggle = () => {
    if (streaming) {
      // If currently streaming, stop it
      setStreaming(false)
    } else {
      // If not streaming, start it
      setStreaming(true)
    }
  }

  // Effect to update the chart data when density history changes
  useEffect(() => {
    const labels = densityHistory.map((entry) => {
      const date = new Date(entry.timestamp)
      return date.toLocaleTimeString()
    })

    const densityValues = densityHistory.map(entry => entry.density_value || 0)
    const personCounts = densityHistory.map(entry => entry.person_count || 0)

    setChartData({
      labels: labels,
      datasets: [
        {
          label: 'Density Value',
          data: densityValues,
          borderColor: 'rgb(59, 130, 246)',
          backgroundColor: 'rgba(59, 130, 246, 0.1)',
          fill: true,
          tension: 0.4,
          yAxisID: 'y'
        },
        {
          label: 'Person Count',
          data: personCounts,
          borderColor: 'rgb(34, 197, 94)',
          backgroundColor: 'rgba(34, 197, 94, 0.1)',
          fill: true,
          tension: 0.4,
          yAxisID: 'y1'
        }
      ]
    })
  }, [densityHistory])

  // Chart configuration options
  const chartOptions = useMemo(() => ({
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top',
        labels: {
          color: '#ffffff'
        }
      },
      title: {
        display: true,
        text: 'Crowd Density History (Last Hour)',
        color: '#ffffff'
      }
    },
    scales: {
      x: {
        ticks: { color: '#ffffff' },
        grid: { color: 'rgba(255, 255, 255, 0.1)' }
      },
      y: {
        type: 'linear',
        display: true,
        position: 'left',
        min: 0,
        max: 1,
        ticks: { color: '#ffffff' },
        grid: { color: 'rgba(255, 255, 255, 0.1)' },
        title: {
          display: true,
          text: 'Density (0-1)',
          color: '#ffffff'
        }
      },
      y1: {
        type: 'linear',
        display: true,
        position: 'right',
        ticks: { color: '#ffffff' },
        grid: { drawOnChartArea: false },
        title: {
          display: true,
          text: 'Person Count',
          color: '#ffffff'
        }
      }
    }
  }), []);

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-900 via-blue-800 to-blue-900">
      {/* Header */}
      <header className="bg-white/10 backdrop-blur-md border-b border-white/20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <button
                onClick={() => navigate('/dashboard')}
                className="p-2 hover:bg-white/20 rounded-lg transition"
              >
                <ArrowLeft className="w-6 h-6 text-white" />
              </button>
              <div>
                <h1 className="text-2xl font-bold text-white">{camera?.name || 'Monitoring'}</h1>
                <p className="text-blue-200 text-sm">{camera?.location || 'No location'}</p>
              </div>
            </div>
            <div className="flex items-center gap-4">
              <button
                onClick={() => setShowSettings(true)}
                className="p-2 hover:bg-white/20 rounded-lg transition"
              >
                <Settings className="w-6 h-6 text-white" />
              </button>
              <button
                onClick={handleStreamToggle} // Use the new toggle handler
                className={`px-6 py-2 rounded-lg font-semibold transition ${
                  streaming
                    ? 'bg-red-600 hover:bg-red-700 text-white'
                    : 'bg-green-600 hover:bg-green-700 text-white'
                }`}
              >
                {streaming ? 'Stop Stream' : 'Start Stream'}
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Video Feed */}
          <div className="lg:col-span-2">
            <div className={`bg-white/10 backdrop-blur-md rounded-xl p-6 border-2 transition-all ${
              alert ? 'border-red-500 animate-pulse' : 'border-white/20'
            }`}>
              {alert && (
                <div className="mb-4 p-4 bg-red-600/90 rounded-lg flex items-center gap-3 animate-pulse">
                  <AlertTriangle className="w-6 h-6 text-white" />
                  <div>
                    <h3 className="text-white font-bold text-lg">OVERCROWDING ALERT!</h3>
                    <p className="text-red-100 text-sm">Density threshold exceeded</p>
                  </div>
                </div>
              )}
              
              <div className="relative bg-black rounded-lg overflow-hidden" style={{ aspectRatio: '16/9' }}>
                <img
                  ref={videoRef}
                  alt="Video feed"
                  className="w-full h-full object-contain"
                  // Style is controlled by the `frame` event handler, but display 'block' when streaming
                  style={{ display: streaming ? 'block' : 'none' }}
                />
                {!streaming && (
                  <div className="absolute inset-0 flex items-center justify-center text-white">
                    <div className="text-center">
                      <div className="text-4xl mb-4">📹</div>
                      <p className="text-xl">Stream not started</p>
                      <p className="text-blue-300 mt-2">Click "Start Stream" to begin monitoring</p>
                    </div>
                  </div>
                )}
              </div>

              {/* Density Stats Overlay */}
              {streaming && (
                <div className="mt-4 grid grid-cols-3 gap-4">
                  <div className="bg-blue-600/80 backdrop-blur-sm rounded-lg p-4 text-center">
                    <div className="text-3xl font-bold text-white">{density.person_count}</div>
                    <div className="text-blue-100 text-sm mt-1">People Detected</div>
                  </div>
                  <div className={`${
                    alert ? 'bg-red-600/80' : 'bg-green-600/80'
                  } backdrop-blur-sm rounded-lg p-4 text-center`}>
                    <div className="text-3xl font-bold text-white">
                      {(density.density_value * 100).toFixed(1)}%
                    </div>
                    <div className="text-white/90 text-sm mt-1">Density</div>
                  </div>
                  <div className="bg-purple-600/80 backdrop-blur-sm rounded-lg p-4 text-center">
                    <div className="text-3xl font-bold text-white">
                      {density.density_per_sqm.toFixed(2)}
                    </div>
                    <div className="text-purple-100 text-sm mt-1">Per sqm</div>
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            {/* Current Status */}
            <div className="bg-white/10 backdrop-blur-md rounded-xl p-6 border border-white/20">
              <h2 className="text-xl font-bold text-white mb-4">Current Status</h2>
              <div className="space-y-3">
                <div className="flex justify-between items-center">
                  <span className="text-blue-200">Status</span>
                  <span className={`px-3 py-1 rounded-full text-sm font-semibold ${
                    streaming ? 'bg-green-600 text-white' : 'bg-gray-600 text-white'
                  }`}>
                    {streaming ? 'Active' : 'Inactive'}
                  </span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-blue-200">Threshold</span>
                  <span className="text-white font-semibold">{(threshold * 100).toFixed(0)}%</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-blue-200">Alert Status</span>
                  <span className={`px-3 py-1 rounded-full text-sm font-semibold ${
                    alert ? 'bg-red-600 text-white' : 'bg-green-600 text-white'
                  }`}>
                    {alert ? 'Alert' : 'Normal'}
                  </span>
                </div>
              </div>
            </div>

            {/* Density Chart */}
            <div className="bg-white/10 backdrop-blur-md rounded-xl p-6 border border-white/20">
              <div style={{ height: '300px' }}>
                {chartData.labels.length > 0 ? (
                  <Line data={chartData} options={chartOptions} />
                ) : (
                  <div className="flex items-center justify-center h-full text-blue-200">
                    No data available yet
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      </main>

      {/* Settings Modal */}
      {showSettings && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-2xl shadow-2xl w-full max-w-md p-6">
            <h2 className="text-2xl font-bold text-gray-800 mb-4">Alert Settings</h2>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Density Threshold: {(threshold * 100).toFixed(0)}%
                </label>
                <input
                  type="range"
                  min="0"
                  max="1"
                  step="0.05"
                  value={threshold}
                  onChange={(e) => setThreshold(parseFloat(e.target.value))}
                  className="w-full"
                />
                <div className="flex justify-between text-xs text-gray-500 mt-1">
                  <span>0%</span>
                  <span>50%</span>
                  <span>100%</span>
                </div>
              </div>
              <div className="pt-4">
                <button
                  // When settings are saved, you might want to restart the stream if active 
                  // to apply the new threshold immediately. 
                  onClick={() => {
                    setShowSettings(false);
                    // If streaming is active, stop and start to send new threshold to socket
                    if (streaming) {
                      stopStream();
                      startStream();
                    }
                  }}
                  className="w-full px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-semibold transition"
                >
                  Save Settings
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default Monitoring