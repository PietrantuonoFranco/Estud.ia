"use client";

import { useState } from "react";

import { ChatInformationProvider } from "./contexts/ChatInformationContext";
import { OptionContextProvider } from "./contexts/OptionContext";

import SourcesPanel from "./components/SourcesPanel";
import StudioPanel from "./components/FunctionPanel";
import OptionContainer from "./components/OptionContainer";
import OptionHeader from "./components/OptionHeader";

export default function Home() {
  const [isSourcesOpen, setIsSourcesOpen] = useState(true);
  const [isStudioOpen, setIsStudioOpen] = useState(true);

  return (
    <div className="flex flex-col overflow-hidden bg-background">
      <ChatInformationProvider>
        <OptionContextProvider>
          <OptionHeader
            isSourcesOpen={isSourcesOpen}
            isStudioOpen={isStudioOpen}
            onToggleSources={() => setIsSourcesOpen((prev) => !prev)}
            onToggleStudio={() => setIsStudioOpen((prev) => !prev)}
          />

          <div className="flex flex-1 overflow-hidden">
            <SourcesPanel openPanel={isSourcesOpen} />
            <OptionContainer />
            <StudioPanel openPanel={isStudioOpen} />
          </div>
        </OptionContextProvider>
      </ChatInformationProvider>
    </div>
  );
}
