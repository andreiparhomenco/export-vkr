import React from 'react';
import { FileText, CheckCircle, AlertCircle, Info } from 'lucide-react';

const Instructions = () => {
  return (
    <div className="card">
      <div className="flex items-center gap-2 mb-4">
        <Info className="h-5 w-5 text-primary-600" />
        <h3 className="text-lg font-semibold text-gray-900">
          Что должно быть внутри загружаемых файлов
        </h3>
      </div>
      
      <div className="space-y-4">
        <div className="flex items-start gap-3">
          <CheckCircle className="h-5 w-5 text-green-500 mt-0.5 flex-shrink-0" />
          <div>
            <h4 className="font-medium text-gray-900">Титульный лист</h4>
            <p className="text-sm text-gray-600">
              Скан/фото ТОЛЬКО в формате A4, читаемый, подпись и печать (если требуется).
              Название работы — <em>ровно</em> так, как будет в метаданных (без КАПСЛОКА).
            </p>
          </div>
        </div>
        
        <div className="flex items-start gap-3">
          <CheckCircle className="h-5 w-5 text-green-500 mt-0.5 flex-shrink-0" />
          <div>
            <h4 className="font-medium text-gray-900">Текст работы</h4>
            <p className="text-sm text-gray-600">
              Основной файл: <code className="bg-gray-100 px-1 rounded">.docx</code> или <code className="bg-gray-100 px-1 rounded">.pdf</code>.
              Если <code className="bg-gray-100 px-1 rounded">.docx</code> — он будет автоматически конвертирован в PDF.
            </p>
          </div>
        </div>
        
        <div className="flex items-start gap-3">
          <CheckCircle className="h-5 w-5 text-green-500 mt-0.5 flex-shrink-0" />
          <div>
            <h4 className="font-medium text-gray-900">Отчёт проверки на заимствования</h4>
            <p className="text-sm text-gray-600">
              Скан или PDF отчёта с подписью научного руководителя (если регламент требует).
            </p>
          </div>
        </div>
        
        <div className="flex items-start gap-3">
          <CheckCircle className="h-5 w-5 text-green-500 mt-0.5 flex-shrink-0" />
          <div>
            <h4 className="font-medium text-gray-900">Дополнительные материалы</h4>
            <p className="text-sm text-gray-600">
              Приложения прикладывайте отдельно и указывайте в порядке (они войдут в итоговый PDF после основного текста).
            </p>
          </div>
        </div>
        
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
          <div className="flex items-start gap-2">
            <AlertCircle className="h-5 w-5 text-blue-600 mt-0.5 flex-shrink-0" />
            <div>
              <h4 className="font-medium text-blue-900">Требования к файлам</h4>
              <ul className="text-sm text-blue-800 mt-1 space-y-1">
                <li>• Форматы: A4, разрешение не менее 300 dpi</li>
                <li>• Именование: <code className="bg-blue-100 px-1 rounded">01_Titul.jpg</code>, <code className="bg-blue-100 px-1 rounded">02_VKR.docx</code></li>
                <li>• Максимальный размер файла: 100 MB</li>
                <li>• Поддерживаемые форматы: .docx, .pdf, .jpg, .png</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Instructions;




