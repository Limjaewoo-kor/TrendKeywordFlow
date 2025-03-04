import React from 'react';
import { Typography, Paper, Button } from '@mui/material';
import { Link, useParams } from "react-router-dom";

const TemplateView = ({ templates }) => {  // templates 배열로 받기
  const { id } = useParams();

  const handleCopy = (template) => {
    navigator.clipboard.writeText(template);
    alert('템플릿이 클립보드에 복사되었습니다!');
  };

  // 템플릿 이름 매핑
  const templateNames = ["bert", "lg", "sk", "kanana"];

  return (
    <>
      {templates.map((template, index) => (
        <Paper key={index} elevation={4} style={{ padding: 20, marginTop: 20 }}>
          <Typography variant="h5" gutterBottom>📝 AI 생성 글 템플릿 {templateNames[index]}</Typography>
          <Typography variant="body1" style={{ whiteSpace: 'pre-wrap' }}>
            {template}
          </Typography>
          <Button
            variant="outlined"
            color="primary"
            onClick={() => handleCopy(template)}
            style={{ marginTop: 10 }}
          >
            템플릿 {templateNames[index]} 복사하기
          </Button>
          <Link
            to={`/posts/${id}/template-edit`}
            state={{ template }}
          >
            <Button variant="contained" color="secondary" style={{ marginTop: 10 }}>
              템플릿 {templateNames[index]} 편집하기(관리자 전용_content 수정)
            </Button>
          </Link>
        </Paper>
      ))}
    </>
  );
};

export default TemplateView;
