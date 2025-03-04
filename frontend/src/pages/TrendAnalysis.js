import React, { useState } from 'react';
import api from '../api/axios';
import { TextField, Button, Typography } from '@mui/material';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';

const TrendAnalysis = () => {
  const [keywordInput, setKeywordInput] = useState('');
  const [keywords, setKeywords] = useState([]);  //  여러 키워드를 저장
  const [data, setData] = useState([]);
  const colors = ["#8884d8", "#82ca9d", "#ffc658", "#ff7300"];  //  키워드별 색상

  const handleSubmit = async () => {
    const keywordList = keywordInput.split(',').map((kw) => kw.trim()).filter(Boolean);  // ✅ 콤마로 구분해 키워드 리스트 생성
    setKeywords(keywordList);  //  키워드 저장

    try {
      const res = await api.post('/trend-analysis', { keywords: keywordList });  // ✅ 여러 키워드 전송
      const trendData = res.data.results.reduce((acc, group, index) => {
        group.data.forEach((item, i) => {
          if (!acc[i]) acc[i] = { period: item.period };
          acc[i][group.keyword] = item.ratio;  //  키워드별 데이터 저장
        });
        return acc;
      }, []);
      setData(trendData);  // 데이터 저장
    } catch (err) {
      console.error('트렌드 분석 실패:', err);
    }
  };

  return (
    <div style={{ padding: 20 }}>
      <Typography variant="h4" gutterBottom>📊 트렌드 분석</Typography>
      <TextField
        label="검색어 입력 (콤마로 구분)"
        value={keywordInput}
        onChange={(e) => setKeywordInput(e.target.value)}
        fullWidth
        margin="normal"
        placeholder="예: 인공지능, 블록체인, 메타버스"
      />
      <Button variant="contained" color="primary" onClick={handleSubmit}>
        🔍 트렌드 분석하기
      </Button>

      {data.length > 0 && (
        <LineChart width={800} height={400} data={data} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="period" />
          <YAxis />
          <Tooltip />
          <Legend />
          {keywords.map((keyword, index) => (
            <Line
              key={keyword}
              type="monotone"
              dataKey={keyword}
              stroke={colors[index % colors.length]}  // 키워드별 색상 적용
              activeDot={{ r: 8 }}
            />
          ))}
        </LineChart>
      )}
    </div>
  );
};

export default TrendAnalysis;
