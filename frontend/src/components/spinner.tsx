import { Loader } from "lucide-react";

export function Spinner({ label }: { label: string }) {
  return (
    <div className="flex gap-2">
      {label}
      <Loader className="animate-spin" />
    </div>
  );
}
