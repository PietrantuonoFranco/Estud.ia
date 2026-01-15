"use client"

import { useOptionContext } from "../contexts/OptionContext"

interface OptionButtonProps {
  optionName: string;
  icon: React.ComponentType<any>;
  label: string;
  colorClasses?: string;
  openPanel: boolean;
}

export default function OptionButton({ optionName, icon: Icon, label, colorClasses, openPanel }: OptionButtonProps) {
  const { setOption } = useOptionContext();


  return (
    <button
      onClick={() => setOption(optionName)}
      className={`cursor-pointer flex flex-col w-full gap-2 rounded-lg p-3 text-left transition-colors hover:bg-[var(--hover-bg)] ${colorClasses}`}
    >
      <Icon className="h-4 w-4" />
      <span className={`${ openPanel ? "text-sm font-medium" : "hidden"}`}>{label}</span>
    </button>
  )
}