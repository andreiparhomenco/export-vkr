import React, { useState, useCallback } from 'react';
import { Upload, Download, AlertCircle, CheckCircle, Loader2 } from 'lucide-react';
import FileList from './components/FileList';
import MetadataForm from './components/MetadataForm';
import Instructions from './components/Instructions';

const API_BASE = 'http://127.0.0.1:8000';

function App() {
  const [files, setFiles] = useState([]);
  const [sessionId, setSessionId] = useState(null);
  const [order, setOrder] = useState([]);
  const [metadata, setMetadata] = useState({
    title: '',
    author: '',
    supervisor: '',
    year: '',
    faculty: '',
    form: ''
  });
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [warnings, setWarnings] = useState([]);

  const handleFileUpload = useCallback(async (event) => {
    const selectedFiles = Array.from(event.target.files);
    if (selectedFiles.length === 0) return;

    setLoading(true);
    try {
      const formData = new FormData();
      selectedFiles.forEach(file => {
        formData.append('files', file);
      });

      const response = await fetch(`${API_BASE}/api/upload`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`Upload failed: ${response.statusText}`);
      }

      const data = await response.json();
      setSessionId(data.session_id);
      setFiles(data.files);
      setOrder(data.files.map(f => f.id));
      setResult(null);
      setWarnings([]);
    } catch (error) {
      console.error('Upload error:', error);
      alert(`Ошибка загрузки: ${error.message}`);
    } finally {
      setLoading(false);
    }
  }, []);

  const handleReorder = useCallback((newOrder) => {
    setOrder(newOrder);
  }, []);

  const handleRemoveFile = useCallback((fileId) => {
    const newFiles = files.filter(f => f.id !== fileId);
    const newOrder = order.filter(id => id !== fileId);
    setFiles(newFiles);
    setOrder(newOrder);
  }, [files, order]);

  const handleMetadataChange = useCallback((newMetadata) => {
    setMetadata(newMetadata);
  }, []);

  const handlePrepare = useCallback(async () => {
    if (!sessionId) {
      alert('Сначала загрузите файлы');
      return;
    }

    if (!metadata.title || !metadata.author || !metadata.year) {
      alert('Заполните обязательные поля: заглавие, автор, год');
      return;
    }

    setLoading(true);
    try {
      const payload = {
        session_id: sessionId,
        order: order,
        metadata: metadata
      };

      const response = await fetch(`${API_BASE}/api/prepare`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || `Prepare failed: ${response.statusText}`);
      }

      const data = await response.json();
      setResult(data);
      setWarnings(data.warnings || []);

      // Auto-download files
      if (data.export_id) {
        // Download PDF
        const pdfResponse = await fetch(`${API_BASE}/api/download/${data.export_id}`);
        if (pdfResponse.ok) {
          const pdfBlob = await pdfResponse.blob();
          const pdfUrl = URL.createObjectURL(pdfBlob);
          const pdfLink = document.createElement('a');
          pdfLink.href = pdfUrl;
          pdfLink.download = `export_${data.export_id}.pdf`;
          pdfLink.click();
        }

        // Download JSON metadata
        const jsonResponse = await fetch(`${API_BASE}/api/metadata/${data.export_id}`);
        if (jsonResponse.ok) {
          const jsonBlob = await jsonResponse.blob();
          const jsonUrl = URL.createObjectURL(jsonBlob);
          const jsonLink = document.createElement('a');
          jsonLink.href = jsonUrl;
          jsonLink.download = `export_${data.export_id}.json`;
          jsonLink.click();
        }
      }
    } catch (error) {
      console.error('Prepare error:', error);
      alert(`Ошибка обработки: ${error.message}`);
    } finally {
      setLoading(false);
    }
  }, [sessionId, order, metadata]);

  const handleReset = useCallback(() => {
    setFiles([]);
    setSessionId(null);
    setOrder([]);
    setMetadata({
      title: '',
      author: '',
      supervisor: '',
      year: '',
      faculty: '',
      form: ''
    });
    setResult(null);
    setWarnings([]);
  }, []);

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Экспорт ВКР → PDF (MVP)
          </h1>
          <p className="text-gray-600">
            Простой и надёжный прототип для экспорта выпускных квалификационных работ
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Main Content */}
          <div className="lg:col-span-2 space-y-6">
            {/* File Upload */}
            <div className="card">
              <h2 className="text-xl font-semibold text-gray-900 mb-4">Загрузка файлов</h2>
              <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center hover:border-primary-400 transition-colors">
                <Upload className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                <p className="text-gray-600 mb-4">
                  Перетащите файлы сюда или нажмите для выбора
                </p>
                <input
                  type="file"
                  multiple
                  onChange={handleFileUpload}
                  className="hidden"
                  id="file-upload"
                  accept=".docx,.pdf,.jpg,.jpeg,.png"
                />
                <label
                  htmlFor="file-upload"
                  className="btn-primary cursor-pointer inline-block"
                >
                  Выбрать файлы
                </label>
                <p className="text-sm text-gray-500 mt-2">
                  Поддерживаемые форматы: .docx, .pdf, .jpg, .png (макс. 100 MB)
                </p>
              </div>
            </div>

            {/* File List */}
            <FileList
              files={files}
              order={order}
              onReorder={handleReorder}
              onRemove={handleRemoveFile}
            />

            {/* Metadata Form */}
            {files.length > 0 && (
              <MetadataForm
                metadata={metadata}
                onChange={handleMetadataChange}
              />
            )}

            {/* Actions */}
            {files.length > 0 && (
              <div className="card">
                <div className="flex flex-col sm:flex-row gap-4">
                  <button
                    onClick={handlePrepare}
                    disabled={loading || !sessionId}
                    className="btn-primary flex items-center justify-center gap-2 flex-1"
                  >
                    {loading ? (
                      <>
                        <Loader2 className="h-4 w-4 animate-spin" />
                        Собираем PDF...
                      </>
                    ) : (
                      <>
                        <Download className="h-4 w-4" />
                        Собрать PDF
                      </>
                    )}
                  </button>
                  <button
                    onClick={handleReset}
                    disabled={loading}
                    className="btn-secondary"
                  >
                    Сбросить
                  </button>
                </div>
                {sessionId && (
                  <p className="text-sm text-gray-500 mt-2">
                    Session ID: {sessionId}
                  </p>
                )}
              </div>
            )}

            {/* Results */}
            {result && (
              <div className="card">
                <div className="flex items-center gap-2 mb-4">
                  <CheckCircle className="h-5 w-5 text-green-500" />
                  <h3 className="text-lg font-semibold text-gray-900">
                    Экспорт завершён успешно!
                  </h3>
                </div>
                <div className="bg-green-50 border border-green-200 rounded-lg p-4">
                  <p className="text-green-800">
                    Файлы автоматически скачаны:
                  </p>
                  <ul className="text-green-700 mt-2 space-y-1">
                    <li>• PDF: <code className="bg-green-100 px-1 rounded">export_{result.export_id}.pdf</code></li>
                    <li>• JSON: <code className="bg-green-100 px-1 rounded">export_{result.export_id}.json</code></li>
                  </ul>
                </div>
              </div>
            )}

            {/* Warnings */}
            {warnings.length > 0 && (
              <div className="card">
                <div className="flex items-center gap-2 mb-4">
                  <AlertCircle className="h-5 w-5 text-yellow-500" />
                  <h3 className="text-lg font-semibold text-gray-900">
                    Предупреждения
                  </h3>
                </div>
                <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
                  <ul className="text-yellow-800 space-y-1">
                    {warnings.map((warning, index) => (
                      <li key={index}>• {warning}</li>
                    ))}
                  </ul>
                </div>
              </div>
            )}
          </div>

          {/* Sidebar */}
          <div className="lg:col-span-1">
            <Instructions />
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;


