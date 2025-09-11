import React from 'react';
import { ArrowUp, ArrowDown, FileText, Image, File, X } from 'lucide-react';

const FileList = ({ files, order, onReorder, onRemove }) => {
  const getFileIcon = (fileName) => {
    const extension = fileName.split('.').pop()?.toLowerCase();
    switch (extension) {
      case 'docx':
        return <FileText className="h-5 w-5 text-blue-600" />;
      case 'pdf':
        return <File className="h-5 w-5 text-red-600" />;
      case 'jpg':
      case 'jpeg':
      case 'png':
        return <Image className="h-5 w-5 text-green-600" />;
      default:
        return <File className="h-5 w-5 text-gray-600" />;
    }
  };

  const moveUp = (index) => {
    if (index > 0) {
      const newOrder = [...order];
      [newOrder[index - 1], newOrder[index]] = [newOrder[index], newOrder[index - 1]];
      onReorder(newOrder);
    }
  };

  const moveDown = (index) => {
    if (index < order.length - 1) {
      const newOrder = [...order];
      [newOrder[index], newOrder[index + 1]] = [newOrder[index + 1], newOrder[index]];
      onReorder(newOrder);
    }
  };

  if (files.length === 0) {
    return (
      <div className="card">
        <div className="text-center py-8">
          <FileText className="h-12 w-12 text-gray-400 mx-auto mb-4" />
          <p className="text-gray-500">Файлы не загружены</p>
        </div>
      </div>
    );
  }

  return (
    <div className="card">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">Загруженные файлы</h3>
      <div className="space-y-2">
        {order.map((fileId, index) => {
          const file = files.find(f => f.id === fileId);
          if (!file) return null;

          return (
            <div key={fileId} className="file-item">
              <div className="flex items-center gap-3">
                {getFileIcon(file.name)}
                <div className="flex-1">
                  <p className="font-medium text-gray-900">{file.name}</p>
                  <p className="text-sm text-gray-500">
                    {file.type.toUpperCase()} • {index + 1} в порядке
                  </p>
                </div>
              </div>
              
              <div className="flex items-center gap-2">
                <button
                  onClick={() => moveUp(index)}
                  disabled={index === 0}
                  className="p-1 rounded hover:bg-gray-200 disabled:opacity-50 disabled:cursor-not-allowed"
                  title="Переместить вверх"
                >
                  <ArrowUp className="h-4 w-4" />
                </button>
                <button
                  onClick={() => moveDown(index)}
                  disabled={index === order.length - 1}
                  className="p-1 rounded hover:bg-gray-200 disabled:opacity-50 disabled:cursor-not-allowed"
                  title="Переместить вниз"
                >
                  <ArrowDown className="h-4 w-4" />
                </button>
                <button
                  onClick={() => onRemove(fileId)}
                  className="p-1 rounded hover:bg-red-100 text-red-600"
                  title="Удалить файл"
                >
                  <X className="h-4 w-4" />
                </button>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default FileList;


