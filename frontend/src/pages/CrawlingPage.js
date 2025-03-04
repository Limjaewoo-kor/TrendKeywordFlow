import React, { useState } from 'react';
import api from '../api/axios';
import { TextField, Button, Typography, Card, CardContent } from '@mui/material';

const CrawlingPage = () => {
  const [keyword, setKeyword] = useState('');
  const [posts, setPosts] = useState([]);

  const handleCrawl = async () => {
    try {
      const res = await api.post('/crawl-and-save', null, {
        params: { keyword: keyword }
      });
      setPosts(res.data.posts);
      alert(res.data.message);
    } catch (err) {
      console.error('크롤링 실패:', err.response?.data || err.message);
      alert(`크롤링 실패: ${err.response?.data.detail || err.message}`);
    }
  };

  return (
    <div style={{ padding: 20 }}>
      <Typography variant="h4" gutterBottom>🔍 블로그 크롤링 및 저장</Typography>
      <TextField
        label="검색어 입력"
        value={keyword}
        onChange={(e) => setKeyword(e.target.value)}
        fullWidth
        margin="normal"
      />
      <Button variant="contained" color="primary" onClick={handleCrawl}>
        🔄 크롤링 시작
      </Button>

      {posts.map((post, index) => (
        <Card key={index} style={{ marginTop: 20 }}>
          <CardContent>
            <Typography variant="h6">{post.title || "제목 없음"}</Typography>
            <Typography variant="body2" color="textSecondary">{post.platform || "플랫폼 미상"}</Typography>
            <Typography variant="body1">
              {(post.content || "내용 없음").slice(0, 100)}...
            </Typography>
          </CardContent>
        </Card>
      ))}
    </div>
  );
};

export default CrawlingPage;
