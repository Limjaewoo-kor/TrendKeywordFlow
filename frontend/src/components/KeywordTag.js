import React from 'react';
import { Chip } from '@mui/material';

const KeywordTag = ({ keywords }) => (
  <div style={{ display: 'flex', flexWrap: 'wrap', gap: '10px' }}>
    {keywords.map((keyword, index) => (
      <Chip key={index} label={keyword} color="primary" />
    ))}
  </div>
);

export default KeywordTag;
