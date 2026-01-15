"use client"

import React, { useState, useContext, useEffect } from "react"

enum OptionEnum {
  CHAT = "chat",
  FLASHCARD = "flashcard",
  SUMMARY = "summary",
  QUIZ = "quiz"
}

export default interface OptionContextType {
  option: OptionEnum | string;
  setOption: React.Dispatch<React.SetStateAction<OptionEnum | string>>;
}

const OptionContext = React.createContext<OptionContextType | null>(null);

export function useOptionContext() {
 const context = useContext(OptionContext);

  if (!context) {
    throw new Error("useOptionContext must be used within a OptionProvider");
  }

  return context;
}


export function OptionContextProvider({ children }: { children: React.ReactNode }) {
  const [option, setOption] = useState<OptionEnum | string>(OptionEnum.CHAT);
  
  //const API_URL = process.env.API_URL || 'http://localhost:5000';
  
  useEffect(() => {
    // You can add side effects here if needed when option changes
    console.log("Option changed to:", option);
  }, [option]);

  return (
    <OptionContext.Provider
      value={{
        option,
        setOption
      }}
    >
      {children}
    </OptionContext.Provider>
  );
}