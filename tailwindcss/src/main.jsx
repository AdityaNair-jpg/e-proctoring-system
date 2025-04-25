import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import './index.css';
import App from './epfrontend.jsx';
import TopMenu from './topmenu.jsx';
import AddTest from './addtest.jsx';
import TestList from './TestList.jsx';
import HistoryTab from './HistoryTab';

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <Router>
      <TopMenu />
    </Router>
  </StrictMode>
);
