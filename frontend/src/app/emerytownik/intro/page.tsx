import IntroZUS from "@/components/intro-zus";
import { Navbar } from "@/components/navbar";

export default function Home() {
  return (
    <>
      <div className="px-90">
        <Navbar />
      </div>
      <div className="flex h-full w-full flex-col gap-4">
        <IntroZUS />
      </div>
    </>
  );
}
