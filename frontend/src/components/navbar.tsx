import Image from "next/image";
import Link from "next/link";

import zusLogo from "@/../public/logo_zus_darker_with_text.svg";

import { Button } from "./ui/button";

export function Navbar() {
  return (
    <div className="flex h-26.5 w-full flex-col pt-6">
      <div className="mx-3.5 flex">
        <Link href="/zus.html">
          <Image alt="zus logo" src={zusLogo} height={55} width={250} />
        </Link>
        <Button asChild variant="link">
          <Link
            href="/emerytownik/admin"
            className="ml-auto self-center text-sm font-medium"
          >
            Panel administracyjny
          </Link>
        </Button>
      </div>
      <div className="bg-gray/40 mt-5 h-full w-full"></div>
    </div>
  );
}
