import React, { useEffect, useState } from 'react';
import api from '../api/axios';
import { Card, CardContent, Typography } from '@mui/material';
import { useNavigate } from 'react-router-dom'; // 라우터 내비게이션

const PostList = () => {
  const [posts, setPosts] = useState([]);
  const navigate = useNavigate(); //  페이지 이동 함수

  useEffect(() => {
    api.get('/posts')
      .then((res) => setPosts(res.data.posts))
      .catch((err) => console.error('게시글 조회 실패:', err));
  }, []);

  const handlePostClick = (id) => {
    navigate(`/posts/${id}`); //  게시글 클릭 시 상세 페이지로 이동
  };

  return (
    <div style={{ padding: 20 }}>
      <Typography variant="h4" gutterBottom>📚 저장된 게시글 목록</Typography>
      {posts.map((post) => (
        <Card
          key={post.id}
          style={{ marginBottom: 15, cursor: 'pointer' }}
          onClick={() => handlePostClick(post.id)}       //  클릭 이벤트
        >
          <CardContent>
            <Typography variant="h6">{post.title}</Typography>
            <Typography variant="body2" color="textSecondary">{post.platform}</Typography>
            <Typography variant="body1">{post.content.slice(0, 100)}...</Typography>
          </CardContent>
        </Card>
      ))}
    </div>
  );
};

export default PostList;
