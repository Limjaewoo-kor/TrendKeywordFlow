import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import api from '../api/axios';
import { Typography } from '@mui/material';
import SummaryView from '../components/SummaryView';
import KeywordTag from '../components/KeywordTag';
import TemplateView from '../components/TemplateView';

const PostDetail = () => {
  const { id } = useParams();
  const [post, setPost] = useState({});
  const [summary, setSummary] = useState('');
  const [keywords, setKeywords] = useState([]);
  const [templates, setTemplates] = useState([]);

  //  게시글 정보 조회
  useEffect(() => {
    const fetchPost = async () => {
      try {
        const res = await api.get(`/posts/${id}`);
        setPost(res.data);
      } catch (err) {
        console.error('게시글 조회 실패:', err);
      }
    };
    fetchPost();
  }, [id]);

  // 요약 데이터 생성
  useEffect(() => {
    const fetchSummary = async () => {
      if (post.description) {
        try {
          const res = await api.post('/summarize', { content: post.description });
          setSummary(res.data.summary);
        } catch (err) {
          console.error('요약 실패:', err);
        }
      }
    };
    fetchSummary();
  }, [post.description]);

  //  키워드 추출
  useEffect(() => {
    const fetchKeywords = async () => {
      if (post.description) {
        try {
          const res = await api.post('/keywords', { content: post.description });
          setKeywords(res.data.keywords);
        } catch (err) {
          console.error('키워드 추출 실패:', err);
        }
      }
    };
    fetchKeywords();
  }, [post.description]);

  //  템플릿 생성 (요약과 키워드가 모두 준비된 후 실행)
  useEffect(() => {
    const fetchTemplates = async () => {
      if (post.title && summary && keywords.length > 0) {
        try {
          const promises = [1, 2, 3, 4].map(async (chk) => {
            const res = await api.post(`/generate-template/${chk}`, {
              topic: post.title,
              keywords: keywords,
              summary: summary,
            }, {
              headers: {
                'Content-Type': 'application/json'
              }
            });
            return res.data.template;
          });
          const result = await Promise.all(promises);
          setTemplates(result);  // 4개 템플릿
        } catch (err) {
          console.error('템플릿 생성 실패:', err);
        }
      }
    };
    fetchTemplates();
  }, [post.title, summary, keywords]);

  return (
    <div style={{ padding: 20 }}>
      <Typography variant="h4" gutterBottom>{post.title}</Typography>
      <SummaryView summary={summary} />
      <KeywordTag keywords={keywords} />
      {templates.length > 0 && <TemplateView templates={templates} />}  {/* 배열 전달 */}
    </div>
  );
};

export default PostDetail;
