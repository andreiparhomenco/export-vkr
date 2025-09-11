import React from 'react';
import { User, BookOpen, Calendar, GraduationCap } from 'lucide-react';

const MetadataForm = ({ metadata, onChange }) => {
  const handleChange = (field, value) => {
    onChange({
      ...metadata,
      [field]: value
    });
  };

  return (
    <div className="card">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">Метаданные работы</h3>
      
      <div className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            <BookOpen className="h-4 w-4 inline mr-1" />
            Заглавие работы *
          </label>
          <input
            type="text"
            value={metadata.title}
            onChange={(e) => handleChange('title', e.target.value)}
            className="input-field"
            placeholder="Введите точное название работы"
            required
          />
        </div>
        
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            <User className="h-4 w-4 inline mr-1" />
            ФИО автора *
          </label>
          <input
            type="text"
            value={metadata.author}
            onChange={(e) => handleChange('author', e.target.value)}
            className="input-field"
            placeholder="Иванов Иван Иванович"
            required
          />
        </div>
        
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            <User className="h-4 w-4 inline mr-1" />
            ФИО научного руководителя
          </label>
          <input
            type="text"
            value={metadata.supervisor}
            onChange={(e) => handleChange('supervisor', e.target.value)}
            className="input-field"
            placeholder="Петров Петр Петрович"
          />
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              <Calendar className="h-4 w-4 inline mr-1" />
              Год *
            </label>
            <input
              type="number"
              value={metadata.year}
              onChange={(e) => handleChange('year', parseInt(e.target.value) || '')}
              className="input-field"
              placeholder="2025"
              min="2000"
              max="2030"
              required
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              <GraduationCap className="h-4 w-4 inline mr-1" />
              Форма обучения
            </label>
            <select
              value={metadata.form}
              onChange={(e) => handleChange('form', e.target.value)}
              className="input-field"
            >
              <option value="">Выберите форму</option>
              <option value="бакалавр">Бакалавр</option>
              <option value="магистр">Магистр</option>
              <option value="специалист">Специалист</option>
              <option value="аспирант">Аспирант</option>
            </select>
          </div>
        </div>
        
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            <GraduationCap className="h-4 w-4 inline mr-1" />
            Факультет/Институт
          </label>
          <input
            type="text"
            value={metadata.faculty}
            onChange={(e) => handleChange('faculty', e.target.value)}
            className="input-field"
            placeholder="Факультет исторических и политических наук"
          />
        </div>
      </div>
    </div>
  );
};

export default MetadataForm;


