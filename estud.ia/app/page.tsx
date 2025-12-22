"use client"

import Header from "./components/Header";
import OptionsBanner from "./components/OptionsBanner";
import NotebooksContainer from "./components/NotebooksContainer";
import { useState } from "react";


export default function Home() {
  const [orderBy, setOrderBy] = useState<"most-recently" | "title">("most-recently");
  const [viewMode, setViewMode] = useState<"grid" | "list">("grid");

  return (
      <div className="flex flex-col flex-1 py-6 px-42 space-y-6  bg-background  overflow-y-auto">
        <OptionsBanner 
          orderBy={orderBy}
          setOrderBy={setOrderBy}
          viewMode={viewMode}
          setViewMode={setViewMode}
        />

        <NotebooksContainer 
          orderBy={orderBy}
          viewMode={viewMode}
        />
      </div>
  )
}
