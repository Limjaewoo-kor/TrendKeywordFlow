import React from 'react';
import { Typography, Paper } from '@mui/material';

const SummaryView = ({ summary }) => (
  <Paper elevation={3} style={{ padding: 20, marginTop: 20 }}>
    <Typography variant="h5" gutterBottom>📄 요약 내용</Typography>
    <Typography variant="body1">{summary}</Typography>
  </Paper>
);

export default SummaryView;
