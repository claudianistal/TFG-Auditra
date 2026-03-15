import React from "react";
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Layout from '../components/Layout';
import AudioIngestion from '../pages/AudioIngestion';
import MetadataPage from '../pages/MetadataPage';

const AppRouter = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<AudioIngestion />} />
          <Route path="metadata" element={<MetadataPage />} />
          <Route path="*" element={<Navigate to="/" />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
};

export default AppRouter;