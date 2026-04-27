import React from "react";
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Layout from '../components/Layout';
import AudioIngestion from '../pages/AudioIngestion';
import MetadataPage from '../pages/MetadataPage';
import PatternsPage from '../pages/PatternsPage';
import AnalysisPage from '../pages/AnalysisPage';

const AppRouter = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<AudioIngestion />} />
          <Route path="metadata" element={<MetadataPage />} />
          <Route path="patterns" element={<PatternsPage />} />
          <Route path="analysis" element={<AnalysisPage />} />
          <Route path="*" element={<Navigate to="/" />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
};

export default AppRouter;