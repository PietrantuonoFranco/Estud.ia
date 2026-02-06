"use client";

import { useState } from "react";

import { ChatInformationProvider } from "./contexts/ChatInformationContext";
import { OptionContextProvider } from "./contexts/OptionContext";

import SourcesPanel from "./components/SourcesPanel";
import StudioPanel from "./components/FunctionPanel";
import OptionContainer from "./components/OptionContainer";
import OptionHeader from "./components/OptionHeader";

export default function Home() {
  const [isSourcesOpen, setIsSourcesOpen] = useState(false);
  const [isStudioOpen, setIsStudioOpen] = useState(false);

  const handleToggleSources = () => {
    setIsSourcesOpen((prev) => {
      const next = !prev;
      if (next) {
        setIsStudioOpen(false);
      }
      return next;
    });
  };

  const handleToggleStudio = () => {
    setIsStudioOpen((prev) => {
      const next = !prev;
      if (next) {
        setIsSourcesOpen(false);
      }
      return next;
    });
  };

  return (
    <div className="flex flex-col overflow-hidden bg-background">
      <ChatInformationProvider>
        <OptionContextProvider>
          <OptionHeader
            isSourcesOpen={isSourcesOpen}
            isStudioOpen={isStudioOpen}
            onToggleSources={handleToggleSources}
            onToggleStudio={handleToggleStudio}
          />

          <div className="relative flex flex-1 min-h-0 overflow-hidden">
            <OptionContainer />

            <div className="absolute inset-y-0 left-0 z-20">
              <SourcesPanel openPanel={isSourcesOpen} />
            </div>
            <div className="absolute inset-y-0 right-0 z-20">
              <StudioPanel openPanel={isStudioOpen} />
            </div>
          </div>
        </OptionContextProvider>
      </ChatInformationProvider>
    </div>
  );
}
