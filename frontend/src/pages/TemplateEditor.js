import React, { useEffect, useState } from 'react';
import ReactQuill from 'react-quill';
import 'react-quill/dist/quill.snow.css';
import api from '../api/axios';
import { Button, Typography } from '@mui/material';
import { useParams, useLocation } from 'react-router-dom';

const TemplateEditor = () => {
  const { id } = useParams();                 // URL에서 id 수신
  const location = useLocation();             // TemplateView에서 전달된 상태 수신
  const [template, setTemplate] = useState(location.state?.template || '');  //  상태 초기화

  console.log("현재 ID:", id);                //  id 확인

  const handleSave = async () => {
    try {
      await api.put(`/posts/${id}/template`, { template });
      alert(' 템플릿 저장이 완료되었습니다!');
    } catch (err) {
      console.error('템플릿 저장 실패:', err);
      alert(' 템플릿 저장 중 오류 발생');
    }
  };

  return (
    <div style={{ padding: 20 }}>
      <Typography variant="h4" gutterBottom>📝 템플릿 편집기</Typography>
      <ReactQuill
        theme="snow"
        value={template}
        onChange={setTemplate}
        style={{ height: '400px', marginBottom: '20px' }}
      />
      <Button variant="contained" color="primary" onClick={handleSave}>
        💾 저장하기
      </Button>
    </div>
  );
};

export default TemplateEditor;
