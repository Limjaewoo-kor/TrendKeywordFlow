import React, { useState } from 'react';
import api from '../api/axios';
import { TextField, Button, Typography } from '@mui/material';

const AddPost = () => {
  const [form, setForm] = useState({ title: '', url: '', content: '', platform: '' });

  const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async () => {
    try {
      await api.post('/posts', form);
      alert('게시글이 성공적으로 저장되었습니다!');
    } catch (error) {
      console.error('게시글 저장 실패:', error);
    }
  };

  return (
    <div style={{ padding: 20 }}>
      <Typography variant="h4" gutterBottom>📝 게시글 등록</Typography>
      {['title', 'url', 'platform', 'content'].map((field) => (
        <TextField
          key={field}
          label={field.toUpperCase()}
          name={field}
          fullWidth
          margin="normal"
          value={form[field]}
          onChange={handleChange}
        />
      ))}
      <Button variant="contained" color="primary" onClick={handleSubmit}>
        저장하기
      </Button>
    </div>
  );
};

export default AddPost;
