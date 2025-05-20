import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import './index.css';
import App from './epfrontend.jsx';
import TopMenu from './topmenu.jsx';
import AddTest from './addtest.jsx';
import TestList from './TestList.jsx';
import HistoryTab from './HistoryTab';
import Login from './Login.jsx';
import Register from './Register.jsx';
import LandingPage from './LandingPage.jsx';

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <Router>
      <Routes>
        <Route path="/" element={<TopMenu />}>
          <Route path="add-test" element={<AddTest />} />
          <Route path="history" element={<HistoryTab />} />
          <Route path="test-list" element={<TestList />} />
        </Route>
      </Routes>
    </Router>
  </StrictMode>
);
