import { Loader } from "lucide-react";

export function Spinner() {
  return (
    <div className="flex gap-2">
      Trwa przetwarzanie...
      <Loader className="animate-spin" />
    </div>
  );
}
