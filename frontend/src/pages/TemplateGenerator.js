import React, { useState } from 'react';
import api from '../api/axios';
import { TextField, Button, Typography, Paper } from '@mui/material';

const TemplateGenerator = () => {
  const [topic, setTopic] = useState('');
  const [keywords, setKeywords] = useState('');
  const [summary, setSummary] = useState('');
  const [template, setTemplate] = useState('');

const handleGenerate = async () => {
  try {
    const res = await api.post('/generate-template', {
      topic: topic,
      keywords: keywords.split(',').map(k => k.trim()),  // 리스트 형태로 변환
      summary: summary
    });
    setTemplate(res.data.template);
  } catch (err) {
    console.error('템플릿 생성 실패:', err.response?.data || err.message);
  }
};

  return (
    <div style={{ padding: 20 }}>
      <Typography variant="h4" gutterBottom>📝 글 작성 템플릿 생성기</Typography>
      <TextField label="주제" value={topic} onChange={(e) => setTopic(e.target.value)} fullWidth margin="normal" />
      <TextField label="키워드 (쉼표로 구분)" value={keywords} onChange={(e) => setKeywords(e.target.value)} fullWidth margin="normal" />
      <TextField label="요약" value={summary} onChange={(e) => setSummary(e.target.value)} fullWidth margin="normal" multiline />
      <Button variant="contained" color="primary" onClick={handleGenerate}>✨ 템플릿 생성</Button>

      {template && (
        <Paper elevation={3} style={{ padding: 20, marginTop: 20 }}>
          <Typography variant="h5">✨ 생성된 템플릿</Typography>
          <Typography variant="body1" style={{ whiteSpace: 'pre-wrap' }}>{template}</Typography>
        </Paper>
      )}
    </div>
  );
};

export default TemplateGenerator;
