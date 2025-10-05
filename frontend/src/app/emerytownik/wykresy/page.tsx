import { Navbar } from "@/components/navbar";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

export default function Graphs() {
  return (
    <>
      <div className="flex h-full w-full flex-col px-90">
        <Navbar />
        <Label className="flex w-fit flex-col items-start gap-2">
          Oczekiwana emerytura
          <Input />
        </Label>
        <iframe src="/pension_dashboard.html" className="h-full w-full" />
      </div>
    </>
  );
}
