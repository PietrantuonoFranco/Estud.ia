"use client"

import OptionsBanner from "./components/home/OptionsBanner";
import NotebooksContainer from "./components/home/NotebooksContainer";
import { useState } from "react";


export default function Home() {
  const [orderBy, setOrderBy] = useState<"most-recently" | "title">("most-recently");
  const [viewMode, setViewMode] = useState<"grid" | "list">("grid");
  const [progress, setProgress] = useState(0);
  const [isLoading, setIsLoading] = useState(false);

  const handleStartUpload = () => {
    setIsLoading(true);
    setProgress(10);
  };

  const handleProgressUpdate = (newProgress: number) => {
    setProgress(Math.min(newProgress, 90));
  };

  const handleUploadComplete = () => {
    setProgress(100);
    setTimeout(() => {
      setIsLoading(false);
      setProgress(0);
    }, 300);
  };

  return (
      <div className="flex flex-col flex-1 bg-background">
        {/* Progress bar */}
        {isLoading && (
          <div className="h-2 bg-card w-full">
            <div
              className="h-full bg-gradient-to-r from-primary-accent to-primary shadow-md shadow-primary/20 transition-all rounded-r-full duration-300 ease-out"
              style={{ width: `${progress}%` }}
            />
          </div>
        )}
        
        <div className="flex flex-col flex-1 py-2 md:py-6 px-6 lg:px-42 space-y-6 overflow-y-auto">
          <OptionsBanner 
            orderBy={orderBy}
            setOrderBy={setOrderBy}
            viewMode={viewMode}
            setViewMode={setViewMode}
            onStartUpload={handleStartUpload}
            onProgressUpdate={handleProgressUpdate}
            onUploadComplete={handleUploadComplete}
          />

          <NotebooksContainer 
            orderBy={orderBy}
            viewMode={viewMode}
            onStartUpload={handleStartUpload}
            onProgressUpdate={handleProgressUpdate}
            onUploadComplete={handleUploadComplete}
          />
        </div>
      </div>
  )
}
