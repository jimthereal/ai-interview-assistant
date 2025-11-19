import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import Home from './pages/Home';
import JobAnalysis from './pages/JobAnalysis';
import PracticeList from './pages/PracticeList';
import PracticeQuestion from './pages/PracticeQuestion';
import Progress from './pages/Progress';
import Explainer from './pages/Explainer';

function App() {
  return (
    <BrowserRouter>
      <Layout>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/job-analysis" element={<JobAnalysis />} />
          <Route path="/practice" element={<PracticeList />} />
          <Route path="/practice/question" element={<PracticeQuestion />} />
          <Route path="/progress" element={<Progress />} />
          <Route path="/explainer" element={<Explainer />} />
        </Routes>
      </Layout>
    </BrowserRouter>
  );
}

export default App;
