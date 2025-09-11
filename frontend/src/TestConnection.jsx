import React, { useState } from 'react';

const API_BASE = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000';

function TestConnection() {
  const [status, setStatus] = useState('Не проверено');
  const [loading, setLoading] = useState(false);

  const testConnection = async () => {
    setLoading(true);
    setStatus('Проверяем...');
    
    try {
      console.log('Testing connection to:', API_BASE);
      
      const response = await fetch(`${API_BASE}/health`);
      console.log('Health check response:', response);
      
      if (response.ok) {
        const data = await response.json();
        console.log('Health check data:', data);
        setStatus(`✅ Подключение успешно: ${data.status}`);
      } else {
        setStatus(`❌ Ошибка: ${response.status} ${response.statusText}`);
      }
    } catch (error) {
      console.error('Connection test error:', error);
      setStatus(`❌ Ошибка подключения: ${error.message}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow">
      <h3 className="text-lg font-semibold mb-4">Тест подключения к Backend</h3>
      <div className="space-y-4">
        <div>
          <strong>API URL:</strong> {API_BASE}
        </div>
        <div>
          <strong>Статус:</strong> {status}
        </div>
        <button
          onClick={testConnection}
          disabled={loading}
          className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 disabled:opacity-50"
        >
          {loading ? 'Проверяем...' : 'Проверить подключение'}
        </button>
      </div>
    </div>
  );
}

export default TestConnection;
