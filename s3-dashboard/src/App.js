import { useEffect, useState } from "react";
import Analysis from "./components/Analysis";
import Dropzone from "./components/Dropzone";

function App() {
  const [analysisData, setAnalysisData] = useState([]);
  const handleAnalData = (data) => {
    setAnalysisData(data);
  };
  useEffect(() => {
    document.title = "S3 Dashboard";
  });
  return (
    <div
      className={`bg-bg-dark h-screen w-screen text-white flex flex-col ${
        analysisData.length <= 0 && "justify-center text-center"
      }`}
    >
      {analysisData.length > 0 ? (
        <Analysis analyticData={analysisData} />
      ) : (
        <Dropzone setAnalData={handleAnalData} />
      )}
    </div>
  );
}

export default App;
